import numpy as np
from sentence_transformers import SentenceTransformer
from config import Config

class EmbeddingGenerator:
    def __init__(self, config):
        self.model = SentenceTransformer(config.EMBEDDING_MODEL)
        
    def generate_embeddings(self, texts):
        return self.model.encode(texts)
    
    def save_embeddings(self, embeddings, file_path):
        np.save(file_path, embeddings)
        
    def load_embeddings(self, file_path):
        return np.load(file_path)