from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from chatmof.agents.agent import ChatMOF
from langchain.callbacks import StdOutCallbackHandler

import io
import re
from contextlib import redirect_stdout
import pandas as pd
import random
from pathlib import Path

df = pd.read_excel('./database/tables/coremof.xlsx')
names = df['name']


df = pd.read_excel('test/search_csv.xlsx')
questions = list(df[1])

verbose = True
search_internet = False


#llms = []
#for model in ['text-davinci-003', 'text-davinci-002', 'davinci', 'curie', 'babbage', 'ada']:
##    llm = OpenAI(temperature=0, model=model)
#    llms.append([model, llm])

#for model, llm in llms:
llm = ChatOpenAI(temperature=0.1, model_name='gpt-4')
model='gpt-4'

callback_manager = [StdOutCallbackHandler()]

chatmof = ChatMOF.from_llm(
    llm=llm, 
    verbose=verbose, 
)
qna = []

save_path = Path(f'./test/searcher_{model}')
save_path.mkdir(exist_ok=True, parents=True)

for i, question in enumerate(questions):
    question = question.strip()

    with io.StringIO() as buf, redirect_stdout(buf):
        try:
            output = chatmof.run(question, callbacks=callback_manager)
        except Exception as e:
            print (type(e), e)
            output = None
        log = buf.getvalue()

    qna.append([i, question, output])

    with (save_path/f'{i}_.output').open('w') as f:
        f.write(log)

df = pd.DataFrame(qna)
df.to_csv(f'test/search_csv_{model}.csv')