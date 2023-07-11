from langchain.prompts import PromptTemplate


SUMMARY_TEMPLATE = """This is a conversation between a human and a bot:

{chat_history}

Write a summary of the conversation for {input}:
"""

SUMMARY_PROMPT = PromptTemplate(
    input_variables=["input", "chat_history"],
    template=SUMMARY_TEMPLATE
)