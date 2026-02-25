# from sentence_transformers import SentenceTransformer   #The model (SentenceTransformer) is the data.

from langchain_huggingface import HuggingFaceEndpointEmbeddings
import os
import numpy as np
from dotenv import load_dotenv

load_dotenv()
# Embeddings are used to convert text into vector representations that can be stored in a vector database and used for similarity search.
class EmbeddingModel:
    def __init__(self):
        
        # Use HuggingFace Inference API instead of loading model locally
        # This significantly reduces memory usage (no model loaded in RAM)
        self.model = HuggingFaceEndpointEmbeddings(
            model="sentence-transformers/all-MiniLM-L6-v2",
            huggingfacehub_api_token=os.getenv("HF_API_KEY")
        )
        # Loading "all-MiniLM-L6-v2" is expensive.
        # If you didn’t use a class, you might accidentally reload it many times. Downloads model (first time only). Loads it into memory. Ready to convert text → vector

        #We will use:

        # sentence-transformers/all-MiniLM-L6-v2
        # This is: 384 dimensional, Small, Fast, CPU friendly, Industry common


    def encode(self, text: str):
        # Convert text into embedding vector using HuggingFace API
        # Returns a numpy array for compatibility with existing code
        embedding = self.model.embed_query(text)
        return np.array(embedding)



# why we use raw embeddings instead of huggingface?

# Right now my  structure is: main.py -> uses -> EmbeddingModel
# main.py does NOT care: Which model is used, Local or API, HuggingFace or OpenAI, CPU or GPU. That’s called: Abstacrtion bounary. 

