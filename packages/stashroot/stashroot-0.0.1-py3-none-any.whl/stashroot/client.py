# stashroot/client.py
import requests
import json

class Client:
    def __init__(self, access_key):
        self.access_key = access_key
        self.base_url = "https://api.stashroot.com/"  # Replace with your actual API URL

    def from_documents(self, documents, embeddings_model, vdb_type, collection_name):
        payload = {
            "documents": documents,
            "embeddings_model": embeddings_model,
            "vdb_type": vdb_type,
            "collection_name": collection_name
        }
        headers = {'Authorization': f'Bearer {self.access_key}'}

        response = requests.post(f"{self.base_url}/from_documents", json=payload, headers=headers)

        if response.status_code == 200:
            return json.loads(response.text)
        else:
            raise Exception(f"Failed to create documents: {response.text}")

    def similarity_search(self, query):
        payload = {"query": query}
        headers = {'Authorization': f'Bearer {self.access_key}'}

        response = requests.post(f"{self.base_url}/similarity_search", json=payload, headers=headers)

        if response.status_code == 200:
            return json.loads(response.text)
        else:
            raise Exception(f"Failed to perform similarity search: {response.text}")
