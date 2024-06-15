from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

from backend.app.chatbot.Llm import Llm
from backend.app.services.search import SearchService


class ChatBot:
    def __init__(self, tenant_id, collection_name, model_vendor, model_name):
        self.tenant_id = tenant_id
        self.collection_name = collection_name
        self.model_vendor = model_vendor
        self.model_name = model_name
        self.retriever = self.initialize_retrevier()
        self.llm = self.initialize_llm()
        self.chatbot = self.initialize_chatbot()

    def initialize_retrevier(self):
        search_service = SearchService()
        return search_service.get_tenant_retriever(collection_name=self.collection_name, tenant_id=self.tenant_id)

    def initialize_llm(self):
        return Llm(self.model_vendor, self.model_name).llm

    def initialize_chatbot(self):
        template = """

        You are an assistant for question-answering tasks. \
        Use the following pieces of retrieved context to answer the question. \
        If you don't know the answer , just say that you don't know. \


        Question: {input}
        Context: {context}

        Answer:

        """

        prompt = ChatPromptTemplate.from_template(template)
        llm = self.llm
        retriever = self.retriever
        combine_docs_chain = create_stuff_documents_chain(
            llm, prompt
        )
        chatbot = create_retrieval_chain(retriever, combine_docs_chain)
        return chatbot

    def chat(self, question):
        return self.chatbot.invoke({"input": question})