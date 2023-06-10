import pinecone
import numpy as np
# Initialize Pinecone client
pinecone.init(api_key="110e3d1b-3d40-4f3c-b5e4-8d82d21b51ae", environment="asia-southeast1-gcp-free")

# Define Pinecone index name
index_name = "history"

    # Retrieve form data
field1 = "hello"
field2 = "test"
    # ...

# connect to index
index = pinecone.Index(index_name)
vector_dim = 100

# Create or retrieve the index
index = pinecone.Index(index_name=index_name)

# Define an example vector
vector_list = [1.0, 2.0, 3.0]
# Convert the list to a numpy array
vector_np = np.array(vector_list)
# Normalize the vector
vector_np /= np.linalg.norm(vector_np)
# Define an example ID
id_val = "example_id"


vector=[
    {
      "id": "id",
      "metadata": {"message":["hello","how are you"],"response":["hello","how are you"]},
      "values":np.random.rand(5)
    }
  ]
# Upsert the vector in Pinecone
index.upsert(ids=[id_val], vectors=vector)
index.upsert([
    ("A", [0.1, 0.1, 0.1, 0.1, 0.1], {"genre": "comedy", "year": 2020}),
    ("B", [0.2, 0.2, 0.2, 0.2, 0.2], {"genre": "documentary", "year": 2019}),
    ("C", [ 0.3, 0.3, 0.3, 0.3, 0.3], {"genre": "comedy", "year": 2019}),
    ("D", [0.4, 0.4, 0.4, 0.4, 0.4], {"genre": "drama"}),
    ("E", [0.5, 0.5, 0.5, 0.5, 0.5], {"genre": "drama"})
])
re=index.query(
    vector=[0.1, 0.1, 0.1, 0.1, 0.1],
    filter={
        "genre": {"$eq": "documentary"},
        "year": 2019
    },
    top_k=1,
    include_metadata=True
)

print(re)
# Returns:
# {'matches': [{'id': 'B',
#               'metadata': {'genre': 'documentary', 'year': 2019.0},
#               'score': 0.0800000429,
#               'values': []}],
#  'namespace': ''}
# Retrieve the vector by ID

# Close the Pinecone client
#pinecone.deinit()
# view index stats
#rint(index.describe_index_stats())

#vectors=list(map(vector, vector))
    # Convert vector to numpy array
#vector = np.array(vector)
#index = pinecone.Index(index_name=index_name)

    # Index vector in Pinecone
#index.upsert(vectors=[vectors])

