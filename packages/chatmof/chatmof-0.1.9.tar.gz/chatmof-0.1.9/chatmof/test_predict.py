from langchain.chat_models import ChatOpenAI
from chatmof.agents.agent import ChatMOF
from langchain.callbacks import StdOutCallbackHandler

import io
from contextlib import redirect_stdout
import pandas as pd
import random
from pathlib import Path

files = Path('/storage/dudgns1675/data/moftransformer/coremof/4_descriptor/total')
names = [cif.stem for cif in files.glob('*.grid')]


with open('test/predictor2.txt') as f:
    questions = f.readlines()

verbose = True
search_internet = False


model = 'gpt-4'
llm = ChatOpenAI(temperature=0.1, model=model)
callback_manager = [StdOutCallbackHandler()]

chatmof = ChatMOF.from_llm(
    llm=llm, 
    verbose=verbose, 
)

qna = []

save_path = Path(f'./test/predictor_{model}')
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

    with (save_path/f'{i}.output').open('w') as f:
        f.write(log)

df = pd.DataFrame(qna)
df.to_csv(f'test/predictor_{model}.csv')