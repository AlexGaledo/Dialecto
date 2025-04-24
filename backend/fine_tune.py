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

# Ensure correct column names
train_df.columns = ["source", "target"]
test_df.columns = ["source", "target"]

# Convert CSV to Hugging Face Dataset
train_dataset = Dataset.from_pandas(train_df)
test_dataset = Dataset.from_pandas(test_df)

# Load Tokenizer
tokenizer = AutoTokenizer.from_pretrained(base_model)

def tokenize_data(example):
    inputs = tokenizer(example["source"], padding="max_length", truncation=True, max_length=32)
    targets = tokenizer(example["target"], padding="max_length", truncation=True, max_length=32)
    return {
        "input_ids": inputs["input_ids"],
        "attention_mask": inputs["attention_mask"],
        "labels": targets["input_ids"],
    }




# Tokenize Dataset
train_dataset = train_dataset.map(tokenize_data, batched=True)
test_dataset = test_dataset.map(tokenize_data, batched=True)

# Define Training Arguments
training_args = Seq2SeqTrainingArguments(
    output_dir=repo_id,
    evaluation_strategy="epoch",
    learning_rate=5e-5,  # Lower LR for stability
    per_device_train_batch_size=4,  
    per_device_eval_batch_size=4,
    gradient_accumulation_steps=8,  
    weight_decay=0.01,
    save_total_limit=3,  # Keep more checkpoints
    num_train_epochs=10,  
    predict_with_generate=True,
    fp16=torch.cuda.is_available(),  
    save_strategy="epoch",  
    logging_dir="./logs",
    logging_steps=10,
    load_best_model_at_end=True,  # Restore best model
    metric_for_best_model="eval_loss",
    greater_is_better=False,  
    lr_scheduler_type="linear",  # Use a scheduler
    warmup_steps=500,  # Stabilize training
)



# Trainer
trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
    data_collator=DataCollatorForSeq2Seq(tokenizer, model=model), 
)


# Train the Model
trainer.train()

#Save and Push Model to Hugging Face
model.save_pretrained(repo_id)
tokenizer.save_pretrained(repo_id)
model.push_to_hub(repo_id)
tokenizer.push_to_hub(repo_id)
print(train_dataset)
print(test_dataset)


print("Fine-tuning completed and model pushed to Hugging Face!")

