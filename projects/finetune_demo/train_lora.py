from __future__ import annotations

import argparse
from dataclasses import dataclass

from datasets import load_dataset
from peft import LoraConfig
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, TrainingArguments
from trl import SFTTrainer


@dataclass
class ScriptArgs:
    base_model: str
    train_file: str
    val_file: str
    output_dir: str
    max_seq_len: int
    lr: float
    batch_size: int
    epochs: int
    use_4bit: bool


def parse_args() -> ScriptArgs:
    parser = argparse.ArgumentParser(description="LoRA SFT training script")
    parser.add_argument("--base_model", default="Qwen/Qwen2.5-1.5B-Instruct")
    parser.add_argument("--train_file", required=True)
    parser.add_argument("--val_file", required=True)
    parser.add_argument("--output_dir", required=True)
    parser.add_argument("--max_seq_len", type=int, default=1024)
    parser.add_argument("--lr", type=float, default=2e-4)
    parser.add_argument("--batch_size", type=int, default=2)
    parser.add_argument("--epochs", type=int, default=2)
    parser.add_argument("--use_4bit", action="store_true")
    ns = parser.parse_args()
    return ScriptArgs(
        base_model=ns.base_model,
        train_file=ns.train_file,
        val_file=ns.val_file,
        output_dir=ns.output_dir,
        max_seq_len=ns.max_seq_len,
        lr=ns.lr,
        batch_size=ns.batch_size,
        epochs=ns.epochs,
        use_4bit=ns.use_4bit,
    )


def build_prompt(example: dict) -> dict:
    text = (
        "<|im_start|>system\n你是金融客服助手，请先给意图，再给简短回复。<|im_end|>\n"
        f"<|im_start|>user\n{example['instruction']}\n{example['input']}<|im_end|>\n"
        f"<|im_start|>assistant\n{example['output']}<|im_end|>"
    )
    return {"text": text}


def main() -> None:
    args = parse_args()

    dataset = load_dataset(
        "json",
        data_files={"train": args.train_file, "validation": args.val_file},
    )
    dataset = dataset.map(build_prompt, remove_columns=dataset["train"].column_names)

    tokenizer = AutoTokenizer.from_pretrained(args.base_model, use_fast=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    quant_config = None
    if args.use_4bit:
        quant_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype="float16",
        )

    model = AutoModelForCausalLM.from_pretrained(
        args.base_model,
        quantization_config=quant_config,
        device_map="auto",
    )

    peft_config = LoraConfig(
        r=16,
        lora_alpha=32,
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    )

    training_args = TrainingArguments(
        output_dir=args.output_dir,
        per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=args.batch_size,
        gradient_accumulation_steps=4,
        learning_rate=args.lr,
        num_train_epochs=args.epochs,
        logging_steps=10,
        eval_strategy="steps",
        eval_steps=50,
        save_steps=50,
        save_total_limit=2,
        bf16=False,
        fp16=True,
        report_to="none",
    )

    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=dataset["train"],
        eval_dataset=dataset["validation"],
        peft_config=peft_config,
        dataset_text_field="text",
        max_seq_length=args.max_seq_len,
        args=training_args,
    )

    trainer.train()
    trainer.model.save_pretrained(args.output_dir)
    tokenizer.save_pretrained(args.output_dir)


if __name__ == "__main__":
    main()
