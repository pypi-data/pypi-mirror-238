import numpy as np

class EmbeddingModel:
    '''
    EmbeddingModel gets vector embeddings from Cognite Data Fusion
    '''
    def __init__(self, client, model_name='sentence-transformers/all-MiniLM-L6-v2'):
        self.client = client
        self.model_name = model_name
        self.dimension = 384 # Depending on model
        self.max_seq_length = 1000 # Depending on model
        
    def embed(self, texts, max_seq_length=256):
        # Divide chunks of 10 texts
        chunks = [texts[i:i + 10] for i in range(0, len(texts), 10)]
        vectors = []
        for chunk in chunks:
            body = {
                "items": [{"text": text} for text in chunk],
            }
            
            embedding_response = self.client.post(f"/api/v1/projects/{self.client.config.project}/vectorstore/embedding", body)
            vectors.extend([v["values"] for v in embedding_response.json()["items"]])
            
        return np.asarray(vectors)
