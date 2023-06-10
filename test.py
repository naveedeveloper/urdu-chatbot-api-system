import inspect

from getpass import getpass
from langchain import OpenAI
from langchain.chains import LLMChain, ConversationChain
from langchain.chains.conversation.memory import (ConversationBufferMemory, 
                                                  ConversationSummaryMemory, 
                                                  ConversationBufferWindowMemory,
                                                  ConversationKGMemory)
from langchain.callbacks import get_openai_callback
import tiktoken


llm = OpenAI(
    temperature=0, 
    openai_api_key='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',
    model_name='gpt-3.5-turbo'  # can be used with llms like 'gpt-3.5-turbo'
)
def count_tokens(chain, query):
    with get_openai_callback() as cb:
        result = chain.run(query)
       # print(f'Spent a total of {cb.total_tokens} tokens')

    return result

conversation = ConversationChain(
    llm=llm, 
)

conversation_buf = ConversationChain(
    llm=llm,
    memory=ConversationBufferMemory()
)

conversation_buf("Good morning AI!")

print(count_tokens(conversation_buf, "My interest here is to explore the potential of integrating Large Language Models with external knowledge"))

