from langchain.chains import LLMChain
from langchain import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.memory.chat_message_histories import RedisChatMessageHistory
from langchain.agents import ZeroShotAgent, Tool, AgentExecutor
import os
from util import load_keys
from prompts import SUMMARY_PROMPT


# based on OpenAI models
keys = load_keys()

os.environ["OPENAI_API_KEY"] = keys['openai_key']

llm = OpenAI(temperature=.9)

inputs = "hi"

chain = ConversationChain(llm=llm, verbose=True)

prefix = """Have a conversation with a human, answering the following questions as best you can. """
suffix = """Begin!"

{chat_history}
Question: {input}"""



i =0
while True:
    if i == 0:
        hist = []
    inputs = input("please text: ")
    res = chain.run(inputs)
    print(res)
    hist.append(res)
    print('get hist', hist)
    i += 1