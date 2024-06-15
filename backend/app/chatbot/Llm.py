from langchain_openai import ChatOpenAI


class Llm:
    def __init__(self, vendor, model):
        self.llm = self.initialize_llm(vendor, model)

    def initialize_llm(self, vendor, model):
        if vendor == 'openai':
            return ChatOpenAI(model=model)
