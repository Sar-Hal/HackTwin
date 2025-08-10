from sentence_transformers import SentenceTransformer
import numpy as np
from transformers import pipeline
from config import Config
import torch

class RAGSystem:
    def __init__(self, config):
        self.config = config
        self.embedder = SentenceTransformer(config.EMBEDDING_MODEL)
        self.llm = pipeline(
            'text-generation',
            model=config.LLM_MODEL,
            device='cuda' if torch.cuda.is_available() else 'cpu'
        )
        self.qa_pairs = self._load_faqs()
        self.embeddings = self._generate_embeddings()
    
    def _load_faqs(self):
        with open(self.config.FAQ_FILE, 'r') as f:
            return [line.strip().split('|') for line in f if '|' in line]
    
    def _generate_embeddings(self):
        return np.array([self.embedder.encode(q) for q, _ in self.qa_pairs])
    
    async def generate_answer(self, question):
        query_embed = self.embedder.encode(question)
        scores = np.dot(self.embeddings, query_embed)
        best_idx = np.argmax(scores)
        
        if scores[best_idx] < 0.5:  # confidence threshold
            return "I'm not sure about that. Please ask an organizer."
            
        context = f"Q: {self.qa_pairs[best_idx][0]}\nA: {self.qa_pairs[best_idx][1]}"
        
        response = self.llm(
            f"Based on this context: {context}\n\nQuestion: {question}\nAnswer:",
            max_new_tokens=150,
            temperature=0.7
        )
        
        return response[0]['generated_text'].split('Answer:')[-1].strip()