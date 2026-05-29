from pinecone import Pinecone

API_KEY = "pcsk_6XTJiF_Azamvb6rnwqtZQYaabxDvuaYj794YfSEG39LSvbb6ZkL5tcEf9itQNFp7t81QwM"

pc = Pinecone(api_key=API_KEY)

indexes = pc.list_indexes()

print(indexes)