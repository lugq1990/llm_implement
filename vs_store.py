from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma, Redis


class VectorStore:
    def __init__(self, em_model_id=None) -> None:
        em_model_id = em_model_id if em_model_id else "all-MiniLM-L6-v2"
        self.embedding = HuggingFaceEmbeddings(model_name=em_model_id)
        self.rds_url = "redis://localhost:6379"
        self.index_name = "vs_link"
    
    def init_vs(self, docs):
        self.vs = Redis.from_texts(docs, 
                                   embedding=self.embedding, 
                                   redis_url=self.rds_url, 
                                   index_name=self.index_name)
        return self
        # self.vs = Chroma.from_texts(docs, embedding=self.embedding)
        
    def _check_vs_exist(self):
        if not self.vs:
            raise RuntimeError('please init vs first')
    
    def add_one_doc_str(self, doc):
        self._check_vs_exist()
        if not isinstance(doc, str):
            raise ValueError("doc should be string")
        self.vs.add_texts([doc])
    
    def similarity_search(self, query, k=3):
        self._check_vs_exist()
        return self.vs.similarity_search(query=query, k=k)
        


if __name__ == '__main__':
    texts = ['this is test']
    vs = VectorStore().init_vs(texts)
    query = 'this'
    print(vs.similarity_search(query))