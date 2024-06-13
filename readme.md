

GitHub Link
https://github.com/Aksaykanthan/HEA_QLoRA_finetuning


Pre-trained Model can be downloaded from 
https://huggingface.co/AksayKanthan/model

summary_gen.py 
- Used to generate summary from data/pdf and store them in data/summarize

question_gen.py
- Used to generate question and answers from previously summarized txt file and store them in a json file

data_formatting.py
- Used to fetch all the generated QnA and format them for training

quantize_model.py
- Used to quantize a model from hugging face

model.py
- Locally installed Llama 3 can be accessed.

QLoRA_finetuning.ipynb
- Used to Train the quantized model using custom dataset created from data_formatting.py

data
- All pdf, questions, summaries are stored in this file

app.py
- contains Streamlit UI to access the model

lora_model
- Contains llama3 adapters