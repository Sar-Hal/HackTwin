"""
Gemini API Key Manager
Handles round-robin distribution of API keys to avoid rate limits
"""
import os
import threading
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class GeminiAPIManager:
    """Manages multiple Gemini API keys with round-robin distribution"""
    
    def __init__(self):
        self.api_keys = []
        self.current_key_index = 0
        self.lock = threading.Lock()  # Thread-safe key rotation
        
        # Load all available API keys
        key1 = os.getenv("GEMINI_API_KEY1")
        key2 = os.getenv("GEMINI_API_KEY2") 
        
        if key1:
            self.api_keys.append(key1)
        if key2:
            self.api_keys.append(key2)
            
        # Fallback to original key if new ones aren't available
        original_key = os.getenv("GEMINI_API_KEY")
        if original_key and original_key not in self.api_keys:
            self.api_keys.append(original_key)
            
        if not self.api_keys:
            raise ValueError("No Gemini API keys found! Please set GEMINI_API_KEY1 and GEMINI_API_KEY2 in .env")
            
        print(f"🔑 Initialized Gemini API Manager with {len(self.api_keys)} API keys")
    
    def get_next_api_key(self):
        """Get the next API key in round-robin fashion"""
        with self.lock:
            key = self.api_keys[self.current_key_index]
            self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
            print(f"🔄 Using API key #{self.current_key_index} (of {len(self.api_keys)})")
            return key
    
    def configure_genai(self):
        """Configure genai with the next available API key"""
        api_key = self.get_next_api_key()
        genai.configure(api_key=api_key)
        return api_key
    
    def get_configured_model(self, model_name="gemini-2.0-flash-exp"):
        """Get a configured Gemini model with rotated API key"""
        self.configure_genai()
        return genai.GenerativeModel(model_name)

# Global instance
api_manager = GeminiAPIManager()
