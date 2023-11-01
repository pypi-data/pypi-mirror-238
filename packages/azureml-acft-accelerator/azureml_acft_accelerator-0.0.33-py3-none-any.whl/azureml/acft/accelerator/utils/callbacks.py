# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import os
import torch
from math import isnan
from pathlib import Path

from typing import Union, Optional

from safetensors.torch import save_file as safe_save_file

from transformers.trainer_callback import TrainerCallback, TrainerControl, TrainerState
from transformers.trainer_utils import IntervalStrategy
from transformers.training_args import TrainingArguments
from transformers.tokenization_utils_base import PreTrainedTokenizerBase
from transformers.modeling_utils import PreTrainedModel
from transformers.trainer import Trainer, TRAINING_ARGS_NAME
from transformers.trainer_seq2seq import Seq2SeqTrainer
from transformers.deepspeed import is_deepspeed_zero3_enabled

from peft import PeftModel

from azureml.acft.common_components import get_logger_app
from azureml.automl.core.inference.inference import AutoMLInferenceArtifactIDs, _get_model_name

from ..constants import (
    AzuremlRunType,
    RunPropertyConstants,
    AzuremlConstants,
    LoraAlgo,
    PeftLoRAConstants,
    LoraSaveFormat,
    _AzuremlOptimizationArgs,
)
from ..lora_wrapper.lora_wrapper import LoraWrapper
from ..lora_wrapper.peft_lora_wrapper import PeftLoraWrapper
from ..utils.model_utils import print_model_summary
from .code_utils import update_json_file_and_overwrite


logger = get_logger_app(__name__)


# Trainer call back to log metrics
# TODO move to mlflow logging
class FinetuneCallback(TrainerCallback):
    """
    A [`TrainerCallback`] that sends the logs to [AzureML](https://pypi.org/project/azureml-sdk/).
    """

    def __init__(self, azureml_run=None, log_metrics_at_root=True, set_log_prefix=True, model_name=None):
        """
        init azureml_run which is azureml Run object
        """
        self.azureml_run = azureml_run
        self.log_metrics_at_root = log_metrics_at_root
        self.set_log_prefix = set_log_prefix
        self.model_name = model_name

    def _should_log_to_parent(self):
        """
        Check if we should log to parent pipeline run.

        :return: Parent run if we should log else None.
        :rtype: azureml.core.run
        """
        parent_run = self.azureml_run.parent
        child_run = None
        while parent_run is not None and (parent_run.type == AzuremlRunType.PIPELINE_RUN or parent_run.type == AzuremlRunType.STEP_RUN):
            child_run = parent_run
            parent_run = parent_run.parent
        return child_run

    def _is_automl_child(self):
        root_pipeline_run = self._should_log_to_parent()
        if (
            root_pipeline_run is not None and
            root_pipeline_run.parent is not None and root_pipeline_run.parent.type == AzuremlRunType.HYPERDRIVE_RUN and
            root_pipeline_run.parent.parent is not None and root_pipeline_run.parent.parent.type == AzuremlRunType.AUTOML_RUN
        ):
            return root_pipeline_run
        else:
            return None

    def on_train_begin(self, args: TrainingArguments, state: TrainerState, control: TrainerControl, **kwargs):

        # Print the model summary at the beginning of the training loop
        print_model_summary(kwargs["model"], print_params=True)

    def on_init_end(self, args, state, control, **kwargs):
        """
        executes after init and sets azureml_run
        """
        from azureml.core.run import Run

        if self.azureml_run is None and state.is_world_process_zero:
            self.azureml_run = Run.get_context()
            logger.info("Initialized azureml run")

        if self.azureml_run is not None and "OfflineRun" in self.azureml_run.id:
            logger.info("Failed to get context, run as Local run")
            self.azureml_run = None

    def on_log(self, args, state, control, logs=None, **kwargs):
        """
        logs metrics to azureml
        """
        if self.azureml_run and state.is_world_process_zero:
            steps = None
            if args.logging_strategy == IntervalStrategy.STEPS:
                steps = state.global_step
            for k, v in logs.items():
                if isinstance(v, (int, float)) and not isnan(v):

                    if not self.set_log_prefix:
                        eval_prefix = 'eval_'
                        train_prefix = 'train_'
                        if k.startswith(eval_prefix):
                            k = k[len(eval_prefix):]
                        if k.startswith(train_prefix):
                            k = k[len(train_prefix):]
                            k = k + '_train'

                    self.azureml_run.log(k, v, description=k, step=steps)

                    if self.log_metrics_at_root:
                        # Check if parent is a pipeline run.
                        # If pipeline run, log all metrics to parent pipeline as well.
                        parent_run = self._should_log_to_parent()
                        if parent_run:
                            logger.info(f"Logging metrics to {parent_run}")
                            parent_run.log(k, v, description=k, step=steps)
        else:
            logger.info(f"Logging metrics for local run with step {state.global_step} - {logs}")

    def on_train_end(self, args, state, control, **kwargs):
        """
        executes at the end of training and add best metric, algorithm name to run properties
        """
        if self.azureml_run is None:
            logger.info("Local run. Not setting best metric properties")
            return

        best_metric = state.best_metric
        model_id = _get_model_name(self.azureml_run.id)
        metric_properties = {
            RunPropertyConstants.SCORE: best_metric,
            AutoMLInferenceArtifactIDs.ModelName: model_id,
            RunPropertyConstants.RUN_ALGORITHM: self.model_name,
        }

        self.azureml_run.add_properties(metric_properties)
        logger.info("Best metric properties set on run")
        parent_run = self._should_log_to_parent()
        if parent_run:
            parent_run.add_properties(metric_properties)
            logger.info("Best metric properties set on root pipeline run")

        parent_run = self._is_automl_child()
        if parent_run:
            automl_properties = {
                RunPropertyConstants.RUN_TEMPLATE: RunPropertyConstants.AUTOML_CHILD,
            }
            self.azureml_run.add_properties(automl_properties)
            logger.info("automl_child run template set on run")
            parent_run.add_properties(automl_properties)
            logger.info("automl_child run template set on root pipeline run")


class LoraPyTorchSaveCallback(TrainerCallback):
    """
    The callback handles saving the pytorch model when lora is enabled either through CUSTOM / PEFT algo
    """

    def __init__(
            self,
            trainer: Union[Trainer, Seq2SeqTrainer],
            lora_wrapper_obj: Union[LoraWrapper, PeftLoraWrapper],
            pytorch_save_folder: str,
            optimization_args: _AzuremlOptimizationArgs,
            lora_algo: Union[str, LoraAlgo] = LoraAlgo.CUSTOM,
    ):
        """
        init lora parameters
        """
        self.trainer = trainer
        self.lora_wrapper_obj = lora_wrapper_obj
        self.pytorch_save_folder = pytorch_save_folder
        self.optimization_args = optimization_args
        self.lora_algo = lora_algo

        logger.info(f"Lora call back initialized with lora algo: {self.lora_algo}")

    def save_model_tokenizer_and_trainer_args(
        self,
        model: PreTrainedModel,
        tokenizer: PreTrainedTokenizerBase,
        args: TrainingArguments,
        state_dict: Optional[dict] = None,
    ):

        model.save_pretrained(self.pytorch_save_folder, state_dict=state_dict)

        if tokenizer is not None:
            tokenizer.save_pretrained(self.pytorch_save_folder)

        # Good practice: save your training arguments together with the trained model
        torch.save(args, os.path.join(self.pytorch_save_folder, TRAINING_ARGS_NAME))
    
    def save_lora_model(
            self,
            model: Union[PreTrainedModel, PeftModel],
            state_dict: dict,
        ):
        """Save the lora layers as a model"""
        # save lora model seperately
        if self.optimization_args.lora_save_path:
            Path(self.optimization_args.lora_save_path).mkdir(exist_ok=True, parents=True)
            logger.info(f"Saving {self.lora_algo} LoRA layers in {self.optimization_args.lora_save_format} format.")
            if self.lora_algo == LoraAlgo.PEFT:
                # peft lora
                if self.optimization_args.lora_save_format == LoraSaveFormat.SAFETENSORS:
                    # save adapter weights in safetensors format
                    model.save_pretrained(
                        self.optimization_args.lora_save_path,
                        state_dict=state_dict,
                        safe_serialization=True,
                    )
                else:
                    # save adapter weights in pytorch format
                    model.save_pretrained(
                        self.optimization_args.lora_save_path,
                        state_dict=state_dict,
                        safe_serialization=False,
                    )
                # the `base_model_path` in peft adapter_config must be updated by respective 
                # components to point correct model location
                update_config = {
                    PeftLoRAConstants.PEFT_LORA_BASE_MODEL_PATH_KEY: self.optimization_args.model_name,
                }
                # modify `base_model_path` in peft adapter_config.json
                adapter_config_file = str(Path(
                    self.optimization_args.lora_save_path,
                    PeftLoRAConstants.PEFT_ADAPTER_CONFIG_FILE_NAME,
                ))
                update_json_file_and_overwrite(adapter_config_file, update_config)
            else:
                # custom lora
                if self.optimization_args.lora_save_format == LoraSaveFormat.SAFETENSORS:
                    # save adapter weights in safetensors format
                    lora_model_file_name = str(Path(
                        self.optimization_args.lora_save_path,
                        AzuremlConstants.LORA_SAFE_TENSORS_WEIGHTS_NAME
                    ))
                    safe_save_file(state_dict, lora_model_file_name, metadata={"format": "pt"})
                else:
                    # save adapter weights in pytorch format
                    lora_model_file_name = str(Path(
                        self.optimization_args.lora_save_path,
                        AzuremlConstants.LORA_WEIGHTS_NAME
                    ))
                    torch.save(state_dict, lora_model_file_name)

    def on_train_end_custom_lora(self, args: TrainingArguments, state: TrainerState, control: TrainerControl, **kwargs):
        """Save the lora model trained with custom lora implementation."""

        if state.is_world_process_zero:

            if not isinstance(self.lora_wrapper_obj, LoraWrapper):
                raise ValueError(f"Incorrect lora wrapper object found: {type(self.lora_wrapper_obj)}")

            model, tokenizer = kwargs["model"], kwargs["tokenizer"]

            lora_layer_search_strings = AzuremlConstants.LORA_LAYER_SEARCH_STRINGS
            logger.info(f"Merging the lora weights! Lora layer search strings: {lora_layer_search_strings}")

            model = self.lora_wrapper_obj.merge_lora_layers(model, lora_layer_search_strings=lora_layer_search_strings)

            # store the lora layers state dict separately
            lora_layers_state_dict = self.lora_wrapper_obj.get_lora_layers_state_dict(
                model,
                lora_layer_search_strings=lora_layer_search_strings
            )
            lora_weights_save_path = os.path.join(
                self.pytorch_save_folder, AzuremlConstants.LORA_BASE_FOLDER, AzuremlConstants.LORA_WEIGHTS_NAME)
            os.makedirs(os.path.dirname(lora_weights_save_path), exist_ok=True)
            logger.info(f"Saving the lora weights to {lora_weights_save_path}")
            torch.save(lora_layers_state_dict, lora_weights_save_path)  # save only lora weights

            # save LoRA model seperately
            self.save_lora_model(model, state_dict=lora_layers_state_dict)

            # set the ignore weights to lora layers so that only HF model weights will be saved
            # TODO see if there is a way to not set the private variable
            ignore_keys = list(lora_layers_state_dict.keys())
            # TODO keys_to_ignore_on_save is not valid for nn.Module
            model._keys_to_ignore_on_save = ignore_keys
            logger.info(f"Ignoring the following keys while saving the merged lora model: {ignore_keys}")

            self.save_model_tokenizer_and_trainer_args(model, tokenizer, args)

    def on_train_end_peft_kbit(self, args: TrainingArguments, state: TrainerState, control: TrainerControl, **kwargs):
        """
        Save the lora model trained with PEFT quantization.

        NOTE: LoRA weights cannot be merged for 4bit and 8bit quantized model
        Alternate solution (round about one)
        1. save the adapter weights
        2. load the model using auto peft model in fp32
        3. merge the weights
        4. save the merged weights
        """

        # wait for all processes
        self.trainer.accelerator.wait_for_everyone()

        # get state-dict of model in case of deepspeed stage-3
        # do not fetch state-dict only from process 0 as it gathers weigts from all processes
        state_dict = None
        if is_deepspeed_zero3_enabled():
            # in-case of deepspeed stage 3 unmerged model is only saved
            # get base model weights
            state_dict = self.trainer.accelerator.get_state_dict(self.trainer.deepspeed)
            logger.info("Gathered model weights from all processes.")

        if state.is_world_process_zero:

            if not isinstance(self.lora_wrapper_obj, PeftLoraWrapper):
                raise ValueError(f"Incorrect lora wrapper object found: {type(self.lora_wrapper_obj)}")

            model, tokenizer = kwargs["model"], kwargs["tokenizer"]

            # update the model in lora wrapper obj
            self.lora_wrapper_obj.model = model

            if is_deepspeed_zero3_enabled():
                unwrapped_model = self.trainer.accelerator.unwrap_model(self.trainer.deepspeed)
                # save adapter weights
                peft_model_path = str(Path(self.pytorch_save_folder, PeftLoRAConstants.PEFT_ADAPTER_WEIGHTS_FOLDER))
                Path(peft_model_path).mkdir(exist_ok=True, parents=True)
                unwrapped_model.save_pretrained(peft_model_path, state_dict=state_dict)

                # update state dict from peft layer names to base model layer names
                from collections import OrderedDict
                new_state_dict = OrderedDict()
                for layer_name in state_dict.keys():    #type: ignore
                    if PeftLoRAConstants.PEFT_LORA_LAYER_PREFIX in layer_name:
                        new_state_dict[layer_name] = state_dict[layer_name] #type: ignore
                    else:
                        new_layer_name = layer_name[len(PeftLoRAConstants.PEFT_MODEL_LAYER_PREFIX):] \
                            if layer_name.startswith(PeftLoRAConstants.PEFT_MODEL_LAYER_PREFIX) else layer_name
                        new_state_dict[new_layer_name] = state_dict[layer_name] #type: ignore

                # update base model path in peft config
                # modify `base_model_path` in peft adapter_config.json
                adapter_config_file = str(Path(
                    peft_model_path,
                    PeftLoRAConstants.PEFT_ADAPTER_CONFIG_FILE_NAME,
                ))
                # the `base_model_path` in peft adapter_config must be updated by respective 
                # components to point correct model location
                update_config = {
                    PeftLoRAConstants.PEFT_LORA_BASE_MODEL_PATH_KEY: self.pytorch_save_folder,
                }
                update_json_file_and_overwrite(adapter_config_file, update_config)

                # save LoRA model seperately
                self.save_lora_model(unwrapped_model, state_dict=state_dict)    # type: ignore

                # save unmerged model, tokenizer and trainer args
                self.save_model_tokenizer_and_trainer_args(
                    unwrapped_model.base_model, tokenizer, args, new_state_dict,
                )
            else:
                # merge the weights
                self.lora_wrapper_obj.peft_model_merge()

                # save model, tokenizer and trainer args
                self.save_model_tokenizer_and_trainer_args(self.lora_wrapper_obj.model, tokenizer, args)

        # wait for all processes
        self.trainer.accelerator.wait_for_everyone()

    def on_train_end(self, args: TrainingArguments, state: TrainerState, control: TrainerControl, **kwargs):

        if self.lora_algo == LoraAlgo.CUSTOM:
            logger.info("Calling on_train_end callback for custom lora")
            self.on_train_end_custom_lora(args=args, state=state, control=control, **kwargs)
        elif self.lora_algo == LoraAlgo.PEFT:
            logger.info("Calling on_train_end callback for PEFT based lora")
            self.on_train_end_peft_kbit(args=args, state=state, control=control, **kwargs)
