import os
import torch
from datasets import load_dataset, load_from_disk
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    # HfArgumentParser,
    TrainingArguments,
    # pipeline,
    # logging,
)
from peft import LoraConfig, PeftModel
from trl import SFTTrainer
import configparser


def main():
    # config
    training_file = os.environ["TRAINING"]
    print("Using training file:"+training_file)

    config = configparser.ConfigParser()
    config.read(training_file)

    training = config["training"]
    model_name = training["model"]
    dataset_name = training["dataset"]
    newmodel_finalname = training["finalname"]
    new_model_name = newmodel_finalname + "_training"
    os.environ['AWS_PROFILE'] = training["aws_profile"]

    # BitsAndBytesConfig
    use_4bit = True
    compute_dtype = getattr(torch, "float16")
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=compute_dtype,
        bnb_4bit_use_double_quant=False,
    )

    # Load the entire model on the GPU 0
    device_map = {"": 0}

    # base model
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        quantization_config=bnb_config,
        device_map=device_map
    )
    model.config.use_cache = False
    model.config.pretraining_tp = 1

    # tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    tokenizer.add_special_tokens({'pad_token': '[PAD]'})
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"

    # Load LoRA configuration
    lora_r = 64
    lora_alpha = 16
    lora_dropout = 0.1
    peft_config = LoraConfig(
        lora_alpha=lora_alpha,
        lora_dropout=lora_dropout,
        r=lora_r,
        bias="none",
        task_type="CAUSAL_LM",
    )

    # training arguments
    # Output directory where the model predictions and checkpoints will be stored
    # output_dir = "./results"
    output_dir = "./" + model_name + "_training"

    # Number of training epochs
    num_train_epochs = 1

    # Enable fp16/bf16 training (set bf16 to True with an A100)
    fp16 = False
    bf16 = False

    # Batch size per GPU for training
    per_device_train_batch_size = 2

    # Batch size per GPU for evaluation
    per_device_eval_batch_size = 2

    # Number of update steps to accumulate the gradients for
    gradient_accumulation_steps = 1

    # Enable gradient checkpointing
    gradient_checkpointing = True

    # Maximum gradient normal (gradient clipping)
    max_grad_norm = 0.3

    # Initial learning rate (AdamW optimizer)
    # learning_rate = 2e-4
    # learning_rate = 2e-3
    learning_rate = float(training["learning_rate"])

    # Weight decay to apply to all layers except bias/LayerNorm weights
    weight_decay = 0.001

    # Optimizer to use
    optim = "paged_adamw_32bit"

    # Learning rate schedule (constant a bit better than cosine)
    lr_scheduler_type = "constant"

    # Number of training steps (overrides num_train_epochs)
    # max_steps = -1
    # max_steps = 100
    max_steps = int(training["max_steps"])

    # Ratio of steps for a linear warmup (from 0 to learning rate)
    warmup_ratio = 0.03

    # Group sequences into batches with same length
    # Saves memory and speeds up training considerably
    group_by_length = True

    # Save checkpoint every X updates steps
    save_steps = 25

    # Log every X updates steps
    logging_steps = 10

    training_arguments = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=num_train_epochs,
        per_device_train_batch_size=per_device_train_batch_size,
        gradient_accumulation_steps=gradient_accumulation_steps,
        optim=optim,
        save_steps=save_steps,
        logging_steps=logging_steps,
        learning_rate=learning_rate,
        weight_decay=weight_decay,
        fp16=fp16,
        bf16=bf16,
        max_grad_norm=max_grad_norm,
        max_steps=max_steps,
        warmup_ratio=warmup_ratio,
        group_by_length=group_by_length,
        lr_scheduler_type=lr_scheduler_type,
        # report_to="tensorboard"
    )

    dataset = load_from_disk(dataset_name)
    print(dataset[:1])

    # SFT parameters
    # Maximum sequence length to use
    max_seq_length = None
    # Pack multiple short examples in the same input sequence to increase efficiency
    packing = False
    # Load the entire model on the GPU 0
    # device_map = {"": 0}

    # Set supervised fine-tuning parameters
    trainer = SFTTrainer(
        model=model,
        train_dataset=dataset,
        peft_config=peft_config,
        dataset_text_field="text",
        max_seq_length=max_seq_length,
        tokenizer=tokenizer,
        args=training_arguments,
        packing=packing,
    )

    trainer.train()

    trainer.model.save_pretrained(new_model_name)
    tokenizer.save_pretrained(new_model_name)

    # merge and save
    model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True)
    model = PeftModel.from_pretrained(model, new_model_name)
    model = model.merge_and_unload()

    # final save
    model.save_pretrained(newmodel_finalname)
    tokenizer.save_pretrained(newmodel_finalname)


if __name__ == '__main__':
    main()