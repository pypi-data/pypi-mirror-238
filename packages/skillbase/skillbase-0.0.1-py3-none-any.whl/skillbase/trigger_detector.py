import os

from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader
from langchain.indexes import VectorstoreIndexCreator

from skillbase.util import get_openai_api_key

class TriggerDetector:
    PRE_PROMPT = "What is the trigger type in this rule? Please answer in one word."
    
    MODEL_NAME = "gpt-3.5-turbo"

    def __init__(self):
        os.environ["OPENAI_API_KEY"] = get_openai_api_key()
        # Load KnowledgeBase from data files
        loader = DirectoryLoader("routinebase/knowledgeBase/")
        # Internal source
        self.index = VectorstoreIndexCreator().from_loaders([loader])
        # choose llm model use
        self.openai = ChatOpenAI(model_name=self.MODEL_NAME)

    def get_trigger_type(self, rule):
        # generate complete prompt
        prompt = self.PRE_PROMPT + rule
        response = self.index.query(prompt, llm=self.openai, retriever_kwargs={"k": 1})
        return response
