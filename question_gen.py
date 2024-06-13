
from model import llama3
import os
import json

SUMMARIZED_PATH = 'data/summarize/'
QUESTION_PATH = 'data/questions/'

pre_question = [i.rstrip('.json') for i in os.listdir(QUESTION_PATH) if i.endswith('.json')]
filenames = [i.rstrip('.txt') for i in os.listdir(SUMMARIZED_PATH) if (i.endswith(".txt") and i.rstrip('.txt') not in pre_question)]

def read_summary(filename):
    
    with open(f"{SUMMARIZED_PATH}{filename}.txt", encoding="utf-8") as f:
        data = f.read()
    print(f'Reading {filename}.txt')
    return data


def generate_questions(content):
    chunk_size = 1000
    chunks = [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]
    text = "[\n"
    iteration = 0

    for chunk in chunks:
        prompt = f"""{chunk} \n\n\n create 6 questions with detail answer based on the above paper,
        focus on Corrosion properties of high entropy alloys. 
        questions regarding the publisher and publication details are not required. 
        don't add any extra text. in list of all the question and answer in json format, 
        give the answers in a little detailed manner,
        and exclude 'Here are the questions and answers:' so that i can write directly to JSON file """

        res = llama3(prompt)
        json_data = res.split('[')[1].split(']')[0]
        text += json_data

        iteration += 1
        print(f"{iteration = } |  {(iteration/len(chunks))*100}%")

        if iteration < len(chunks):
            text += ','
        else:
            text += '\n'
        
    text += ']\n'

    return text


def save_questions(content, filename):
    with open(f"{QUESTION_PATH}{filename}.json", 'w', encoding="utf-8") as f:
        f.write(content)
    
    print(f"Saved {filename}.json")


def generate_questions_dataset():
    for filename in filenames:
        summary = read_summary(filename)
        questions = generate_questions(summary)
        save_questions(questions,filename)


if __name__ == "__main__":
    generate_questions_dataset()
