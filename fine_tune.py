from datasets import Dataset
import pandas as pd
import torch
from transformers import (
    AutoModelForSeq2SeqLM, AutoTokenizer, Seq2SeqTrainer,
    Seq2SeqTrainingArguments, DataCollatorForSeq2Seq, BitsAndBytesConfig
)
from peft import LoraConfig, get_peft_model
from huggingface_hub import login

# Login to Hugging Face
login()

# Define model name & Hugging Face repo
base_model = "facebook/nllb-200-distilled-600M"
repo_id = "Splintir/Nllb_dialecto"

# Load quantized model (8-bit) with LoRA
quantization_config = BitsAndBytesConfig(load_in_8bit=True)
model = AutoModelForSeq2SeqLM.from_pretrained(base_model, quantization_config=quantization_config, device_map="auto")

# Apply LoRA Adapters
lora_config = LoraConfig(
    r=8, lora_alpha=16, lora_dropout=0.05, bias="none",
    task_type="SEQ_2_SEQ_LM",
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"]
)

model = get_peft_model(model, lora_config)
model.print_trainable_parameters()

# Move model to GPU if available
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")
model = model.to(device)

# Load dataset
train_df = pd.read_csv("train.csv")
test_df = pd.read_csv("test.csv")

# Convert CSV to Hugging Face Dataset
train_dataset = Dataset.from_pandas(train_df)
test_dataset = Dataset.from_pandas(test_df)

# Load Tokenizer
tokenizer = AutoTokenizer.from_pretrained(base_model)

# Tokenization Function
def tokenize_data(example):
    inputs = tokenizer(example["source"], padding="max_length", truncation=True, max_length=32)
    targets = tokenizer(example["target"], padding="max_length", truncation=True, max_length=32)
    inputs["labels"] = targets["input_ids"]
    return inputs

# Tokenize Dataset
train_dataset = train_dataset.map(tokenize_data, batched=True)
test_dataset = test_dataset.map(tokenize_data, batched=True)

# Define Training Arguments
training_args = Seq2SeqTrainingArguments(
    output_dir=repo_id,
    evaluation_strategy="epoch",
    learning_rate=1e-4,
    per_device_train_batch_size=1,
    per_device_eval_batch_size=1,
    gradient_accumulation_steps=8,
    weight_decay=0.01,
    save_total_limit=2,
    num_train_epochs=3,
    predict_with_generate=True,
    fp16=True,
    save_strategy="no",
    logging_dir="./logs",
    logging_steps=10,
)

# Trainer
trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
    tokenizer=tokenizer,
    data_collator=DataCollatorForSeq2Seq(tokenizer, model=model),
)

# Train the Model
trainer.train()

# Save and Push Model to Hugging Face
model.save_pretrained(repo_id)
tokenizer.save_pretrained(repo_id)
model.push_to_hub(repo_id)
tokenizer.push_to_hub(repo_id)

print("Fine-tuning completed and model pushed to Hugging Face!")
