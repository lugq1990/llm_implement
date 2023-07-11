from transformers import AutoModel, AutoTokenizer
from langchain.embeddings import HuggingFaceEmbeddings
import torch

model_id = "THUDM/chatglm-6b-int4"
embedding_id = ""


class LLMModel:
    def __init__(self, model_id, embedding_id, embedding_device=None) -> None:
        self.model_id = model_id
        self.embedding_id = embedding_id
        if not embedding_device:
            if torch.cuda.is_available():
                embedding_device = 'gpu'
        self.embedding_device = embedding_device if not embedding_id else 'cpu'
        
    def load_llm_model(self):
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_id, trust_remote_code=True)
            self.model = AutoModel.from_pretrained(self.model_id, trust_remote_code=True).half().cuda()        
            print("Model have been loaded!")  
        except:
            self.tokenizer = None
            self.model = None
            print("Couldn't get models and tokenizer for model: {}".format(model_id))
    
    def _load_embeddings(self):
        self.embedding = HuggingFaceEmbeddings(self.embedding_id, 
                                               model_kwargs={'device':self.embedding_device})
        

llm = LLMModel()