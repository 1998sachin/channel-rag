import chromadb
from chromadb.utils import embedding_functions
default_ef = embedding_functions.DefaultEmbeddingFunction()
        

class ChromaDBUtil:
    def __init__(self, collection_name="default_collection", model_name="all-MiniLM-L6-v2"):
        """
        Initializes the ChromaDB utility class.

        Args:
            collection_name (str): Name of the collection in ChromaDB.
            model_name (str): Name of the sentence-transformers model to use for embedding.
        """
        self.client = chromadb.PersistentClient(path="./chroma_db")  # Data will be stored in ./chroma_db directory
        self.collection_name = collection_name
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=default_ef
        )

    def embed_text(self, text):
        """
        Generate embeddings for a given text using the sentence-transformers model.

        Args:
            text (str): The input text to embed.

        Returns:
            list: Embedding vector.
        """
        if default_ef:
            return default_ef.model.encode(text).tolist()
        else:
            raise ValueError("No embedding function found in collection metadata.")


    def add_to_collection(self, id, text, metadata=None):
        """
        Adds text and its embedding to the ChromaDB collection.

        Args:
            id (str): Unique ID for the text.
            text (str): The input text to embed and store.
            metadata (dict, optional): Additional metadata to associate with the text.
        """
        if metadata is None:
            metadata = {}
        self.collection.add(ids=[id], documents=[text], metadatas=[metadata])

    def query_similar(self, query_text, top_k=5):
        """
        Queries the collection for texts similar to the given input text.

        Args:
            query_text (str): The input text to find similar texts for.
            top_k (int): Number of similar items to retrieve.

        Returns:
            dict: A dictionary containing matched IDs, documents, metadatas and distances.
        """
        results = self.collection.query(query_texts=[query_text], n_results=top_k)
        return results['documents']
    

    def delete_from_collection(self, id):
        """
        Deletes an item from the collection using its ID.

        Args:
            id (str): Unique ID of the item to delete.
        """
        self.collection.delete(ids=[id])

    def list_collection_items(self):
        """
        Lists all items in the collection.

        Returns:
            list: A list of item IDs.
        """
        return self.collection.get()['ids']

    def clear_collection(self):
        """
        Clears all items in the collection.
        """
        # Get all IDs in collection
        all_ids = self.collection.get()['ids']
        if all_ids:
            # Delete all items by passing list of all IDs
            self.collection.delete(ids=all_ids)

# Example usage
if __name__ == "__main__":
    pass
    # db_util = ChromaDBUtil(collection_name="tweet_collection")

#     # Add texts to the collection
#     db_util.add_to_collection(id="1", text="This is a sample text.", metadata={"category": "example"})
#     db_util.add_to_collection(id="2", text="Another example of text storage.", metadata={"category": "example"})

    # Query similar texts
    # query_results = db_util.query_similar(query_text="passio", top_k=2)
    # print("Query Results:", query_results)

#     # List items in the collection
    # print("Collection Items:", db_util.list_collection_items())
    # db_util.clear_collection()