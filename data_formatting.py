import json
import os 


QUESTION_PATH = 'data/questions/'

files = [i for i in os.listdir(QUESTION_PATH)]

final_data = []
x
for file in files: 
    with open(f"{QUESTION_PATH}{file}",encoding="utf-8") as f:
        data = json.load(f)
        for i in range(len(data)):
            data[i]['inputs'] = ''
        final_data.extend(data)

#print(*final_data,sep='\n')

with open('data/dataset.json','w', encoding="utf-8") as f:
    temp = json.dumps(final_data)
    f.write(temp)