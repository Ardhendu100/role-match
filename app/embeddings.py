from sentence_transformers import SentenceTransformer   #The model (SentenceTransformer) is the data.


# Embeddings are used to convert text into vector representations that can be stored in a vector database and used for similarity search.
class EmbeddingModel:
    def __init__(self):
        
        # Load the pre-trained model
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        # Loading "all-MiniLM-L6-v2" is expensive.
        # If you didn’t use a class, you might accidentally reload it many times. Downloads model (first time only). Loads it into memory. Ready to convert text → vector

        #We will use:

        # sentence-transformers/all-MiniLM-L6-v2
        # This is: 384 dimensional, Small, Fast, CPU friendly, Industry common


    def encode(self, text: str):
        # Convert text into embedding vector
        embedding = self.model.encode(text)
        return embedding



# why we use raw embeddings instead of huggingface?

# Right now my  structure is: main.py -> uses -> EmbeddingModel
# main.py does NOT care: Which model is used, Local or API, HuggingFace or OpenAI, CPU or GPU. That’s called: Abstacrtion bounary. 

