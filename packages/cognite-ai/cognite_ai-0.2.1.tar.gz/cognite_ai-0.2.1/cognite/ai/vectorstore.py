import numpy as np
from uuid import uuid4
from .embeddingmodel import EmbeddingModel
from .utils import chop_and_chunk, cos_sim
import datetime

class MemoryVectorStore:
    '''
    MemoryVectorStore is a simple vector database that stores vectors in a numpy array.
    It is based on Vlite.
    '''
    def __init__(self, client, collection=None, model_name=None):
		# Filename must be unique between runs. Saving to the same file will append vectors to previous run's vectors
        if collection is None:
            current_datetime = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            collection = f"vlite_{current_datetime}.npz"
        self.client = client
        self.collection = collection
        self.model = EmbeddingModel(client) if model_name is None else EmbeddingModel(client, model_name)
        try:
            with np.load(self.collection, allow_pickle=True) as data:
                self.texts = data['texts'].tolist()
                self.metadata = data['metadata'].tolist()
                self.vectors = data['vectors']
        except FileNotFoundError:
            self.texts = []
            self.metadata = {}
            self.vectors = np.empty((0, self.model.dimension))
    
    def add_vector(self, vector):
        self.vectors = np.vstack((self.vectors, vector))

    def get_similar_vectors(self, vector, top_k=5):
        sims = cos_sim(vector, self.vectors)
        sims = sims[0]
        # print("[get_similar_vectors] Sims:", sims.shape)
        top_k_idx = np.argsort(sims)[::-1][:top_k]
        # print("[get_similar_vectors] Top k idx:", top_k_idx)
        # print("[get_similar_vectors] Top k sims:", sims[top_k_idx])
        return top_k_idx, sims[top_k_idx]

    def query_text(self, text, top_k=5):
        sims = cos_sim(self.model.embed(texts=text) , self.vectors)
        # print("[get_similar_texts] Sims:", sims.shape)
        sims = sims[0]
        top_k_idx = np.argsort(sims)[::-1][:top_k]
        # print("[get_similar_texts] Top k idx:", top_k_idx)
        # print("[get_similar_texts] Top k sims:", sims[top_k_idx])
        return [self.texts[idx] for idx in top_k_idx], sims[top_k_idx]
    
    def store_text(self, texts, max_seq_length=None, id=None, metadata=None):
        if isinstance(texts, list):
            for text in texts:
                self.store_text(text, id, metadata)
            return
        id = id or str(uuid4())
        if max_seq_length is None:
            max_seq_length = self.model.max_seq_length
        chunks = chop_and_chunk(texts, max_seq_length=max_seq_length)
        encoded_data = self.model.embed(texts=chunks)
        self.vectors = np.vstack((self.vectors, encoded_data))
        for chunk in chunks:
            self.texts.append(chunk)
            idx = len(self.texts) - 1
            self.metadata[idx] = metadata or {}
            self.metadata[idx]['index'] = id or idx
        # self.save()

    def save(self):
        with open(self.collection, 'wb') as f:
            np.savez(f, texts=self.texts, metadata=self.metadata, vectors=self.vectors)
