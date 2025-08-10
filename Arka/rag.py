import google.generativeai as genai
from config import Config
import os

class RAGSystem:
    def __init__(self):
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')  # Updated to Gemini 2.0 Flash Experimental
        self.faqs = self._load_faqs()

    def _load_faqs(self):
        try:
            faq_path = os.path.join(os.path.dirname(__file__), 'faqs.txt')
            with open(faq_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return "FAQ content not available."

    async def get_answer(self, question):
        prompt = f"""
        Based on the following FAQ document, please answer the question. 
        If the answer isn't directly in the FAQs, provide the most relevant information available.
        If the question is completely unrelated to the hackathon, respond with "I can only answer questions about the Global AI Hackathon."

        FAQ Document:
        {self.faqs}

        Question: {question}

        Please provide a clear and concise answer based on the FAQ content.
        """

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"I apologize, but I encountered an error: {str(e)}"
        
        if scores[best_idx] < 0.5:  # confidence threshold
            return "I'm not sure about that. Please ask an organizer."
            
        context = f"Q: {self.qa_pairs[best_idx][0]}\nA: {self.qa_pairs[best_idx][1]}"
        
        response = self.llm(
            f"Based on this context: {context}\n\nQuestion: {question}\nAnswer:",
            max_new_tokens=150,
            temperature=0.7
        )
        
        return response[0]['generated_text'].split('Answer:')[-1].strip()