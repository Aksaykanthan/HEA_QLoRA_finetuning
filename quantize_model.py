import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


model_name = "huggingface/llama-3b"  
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)


quantized_model = torch.quantization.quantize_dynamic(
    model, {torch.nn.Linear}, dtype=torch.qint8
)


quantized_model_path = "quantized_llama3_model.pth"
torch.save(quantized_model.state_dict(), quantized_model_path)

print(f"Quantized model saved to {quantized_model_path}")


def generate_response(prompt, model, tokenizer):
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(inputs.input_ids, max_length=100, num_return_sequences=1)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response


# Testing
prompt = "What are some techniques suggested to develop a barrier against biocorrosion?"
response = generate_response(prompt, quantized_model, tokenizer)
print(f"Response: {response}")