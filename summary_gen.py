
from pypdf import PdfReader 
import os
from transformers import BartTokenizer, BartForConditionalGeneration, BartConfig
import pdfplumber
import torch

# from numba import jit, cuda
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(device)

PDF_PATH = 'data/pdf/'
SUMMARY_PATH = "data/summarize/"

model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')
model = model.to(device)  

tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')

# @jit(target_backend='cuda')                          
def summarize(content):
    text = ""

    chunk_size = 2000
    chunks = [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]

    iteration = 0
    for chunk in chunks:
        try : 
            inputs = tokenizer([chunk],return_tensors='pt')
            inputs = {name: tensor.to(device) for name, tensor in inputs.items()}  # Move the inputs to the GPU
            summary_ids = model.generate(inputs['input_ids'], max_length=700, early_stopping=False)
            text += [tokenizer.decode(g, skip_special_tokens=True) for g in summary_ids][0]
        except Exception as e:
            print(e)
            
    
        iteration += 1
        print(f"{iteration = } |  {(iteration/len(chunks))*100}%")
    
    return text

# @jit(target_backend='cuda')                          
def save_summary(content,filename):
    if content == "":
        print(f"Empty File content {filename}")
        return 
    
    with open(f"{SUMMARY_PATH}{filename}.txt", "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Saved {filename}.txt")

# @jit(target_backend='cuda')                          
def read_pdf(filename):
    text = ""
    with pdfplumber.open(f"{PDF_PATH}{filename}.pdf") as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    if text == "":
        print(f"Can't read {filename} -")
    return text

def read_pdf2(filename):
    reader = PdfReader(f"{PDF_PATH}{filename}.pdf") 
    text = ''
    for i in reader.pages:
        text += i.extract_text()
    if text == "":
        print(f"Can't read {filename} -")
    return text


# def read_pdfnew(filename):
#     text = ""
#     reader = PdfReader('data/pdf/'+filename+'.pdf')
#     for i in range(0,(len(reader.pages)) ):
#         page=reader.pages[i]
#         text+=page.extract_text()
#     print(text)
#     return text

# @jit(target_backend='cuda')                          
def generate_summaries():
    pre_summaried = [i.rstrip('.txt') for i in os.listdir(SUMMARY_PATH) if i.endswith(".txt")]
    filenames = [i.rstrip('.pdf') for i in os.listdir(PDF_PATH) if i.endswith(".pdf") and i.rstrip('.pdf') not in pre_summaried]

    print("Files to summarize : ", *filenames )

    for filename in filenames:
        print(f"Generating summary for {filename}")
        content = read_pdf2(filename)
        summary = summarize(content)
        save_summary(summary,filename)
    print("Done")

if __name__ == "__main__":
    generate_summaries()

