import pinecone
from numpy import ndarray
from config import PINECONE_API_KEY
import openai_helper
from typing import Union, List
import numpy as np



#   Initilize pinecone with the api key
def initialize_pinecone(): #   works
    try:
        pinecone.init(api_key=PINECONE_API_KEY, environment="us-west1-gcp-free")
        print("Pinecone initialized successfully")
    except Exception as e:
        print("Error initializing Pinecone:", e)


#   Create / Join the specified index, aka the vector database
def ensure_index_exists(index_name, dimension=1536): #   works
    try:
        if index_name in pinecone.list_indexes():
            print(f"Index '{index_name}' already exists. Connecting to it.")
        else:
            # Create the index with the specified dimension
            pinecone.create_index(index_name, dimension=dimension, metric="cosine")
            print(f"Index '{index_name}' created successfully")
    except Exception as e:
        print(f"Error creating or connecting to index '{index_name}':", e)



# Store vector in pinecone from string, handles single id & string or list of both.
def store_strings_in_pinecone(index_name: str, ids: Union[str, List[str]], texts: Union[str, List[str]]):  
    try:
        # Convert to list if single values are passed
        if isinstance(ids, str):
            ids = [ids]
        if isinstance(texts, str):
            texts = [texts]

        index = pinecone.Index(index_name)
        embeddings = openai_helper.generate_embeddings(texts)  # This now returns a list of embeddings

        if embeddings is None:
            print(f"Failed to generate embeddings for texts.")
            return

        vector_dicts = [{'id': id, 'values': vector} for id, vector in zip(ids, embeddings)]

        # Print debug info
        print(f"Storing with IDs: {ids}")
        truncated_embeddings = [[round(x, 4) for x in emb[:10]] for emb in embeddings]
        print(f"Storing with first 10 elements of Embeddings: {truncated_embeddings}")

        index.upsert(vector_dicts)
        
        print(f"Vectors stored successfully in index '{index_name}'")
    except Exception as e:
        print(f"Error storing vectors in index '{index_name}':", e)




#   Store vector in pinecone vector, handles single id & vector or list of both.
def store_vectors_in_pinecone(index_name: str, ids: Union[str, List[str]], vectors: Union[List[float], List[List[float]]]): #   Should work but untested
    try:
        index = pinecone.Index(index_name)
        
        if isinstance(ids, str):
            ids = [ids]
        if isinstance(vectors[0], float):
            vectors = [vectors]
        
        vector_dicts = [{'id': id, 'values': vector} for id, vector in zip(ids, vectors)]
        index.upsert(vector_dicts)
        
        print(f"Vectors stored successfully in index '{index_name}'")
    except Exception as e:
        print(f"Error storing vectors in index '{index_name}':", e)



#   Deletes vectors based on their id or a list of their ids
def delete_vectors_by_id(index_name, ids): #   works
    try:
        index = pinecone.Index(index_name)
        index.delete(ids)
        print("\nDeleting ids: ", ids, "\n")

        print(f"Vectors deleted successfully from index '{index_name}'")
    except Exception as e:
        print(f"Error deleting vectors from index '{index_name}':", e)



# Deletes ALL vectors in the index, be sure if you want to run this function!
def delete_all_vectors(index_name: str):    #   Works
    try:
        index = pinecone.Index(index_name)
        index.delete(ids=[], deleteAll=True)
        print(f"Deleted all vectors from index '{index_name}'")
    except Exception as e:
        print(f"Error deleting vectors from index '{index_name}':", e)



def delete_all_vectors_except(index_name: str, num_dimensions: int, exclude_ids):   #   Works
    try:
        # Initialize Pinecone Index
        index = pinecone.Index(index_name)
        
        # Ensure exclude_ids is a list, even if it's just one ID
        if not isinstance(exclude_ids, list):
            exclude_ids = [exclude_ids]
        
        # Fetch all IDs from Pinecone Index
        all_ids = get_all_ids_from_index(index, num_dimensions)
        
        # Create a list of IDs to delete, which excludes the IDs in exclude_ids
        ids_to_delete = [id for id in all_ids if id not in exclude_ids]
        
        if ids_to_delete:
            # Delete the vectors
            index.delete(ids_to_delete)
            print(f"Deleted all vectors from index '{index_name}' except {exclude_ids}")
        else:
            print(f"No vectors to delete from index '{index_name}' except {exclude_ids}")
    except Exception as e:
        print(f"Error deleting vectors from index '{index_name}':", e)



#   untested if working     this doesnt rlly update it deletes then stores a new one idk if its intended this way
def update_vector(index_name, id, new_vector):  #   Should work now untested 
    try:
        #delete_vectors_by_id(index_name, [id]) #   this should not be needed based on pinecone docs upsert will update if already in index and wont make duplicates.
        store_vectors_in_pinecone(index_name, [id], [new_vector])
        print(f"Vector updated successfully in index '{index_name}'")
    except Exception as e:
        print(f"Error updating vector in index '{index_name}':", e)



#   Search the vectordb for a similiar match to the embedding you want to look up
def query_index(index_name, query_vector, top_k=10, threshold=0.7):  #  Works
    try:
        index = pinecone.Index(index_name)
        results = index.query(queries=[query_vector], top_k=top_k)
        print("Complete query results:")
        print(results)

        filtered_results = []  # List to store filtered results

        if results and 'results' in results and len(results['results']) > 0 and 'matches' in results['results'][0]:
            matches = results['results'][0]['matches']
            print("Query results:")
            for result in matches:
                if result['score'] >= threshold:  # Filter based on threshold
                    print(result['id'], result['score'])
                    filtered_results.append(result)
        else:
            print("No query results found.")

        print("Filtered query results:")
        print(filtered_results)

    except Exception as e:
        print(f"Error querying index '{index_name}':", e)



#   Return list of ids from index unsure amount of them
def get_ids_from_query(index, input_vector):   #   Works
    """
    Fetches IDs from Pinecone using a query vector.

    Args:
        index (pinecone.Index): The Pinecone index object.
        input_vector (list): The query vector.

    Returns:
        set: A set of IDs that match the query.
    """
    print("Searching Pinecone...")
    # Query Pinecone with the input vector, and get up to 10000 IDs.
    results = index.query(queries=[input_vector], top_k=10000, include_values=False)
    ids = set()
    
    # Iterate through the query results and add IDs to the set.
    for result in results['results'][0]['matches']:
        ids.add(result['id'])
    return ids



#   Return all the ids in the vector index
def get_all_ids_from_index(index, num_dimensions, namespace=""):   #   Works
    """
    Fetches all IDs from a Pinecone index by continuously querying it with random vectors.

    Args:
        index (pinecone.Index): The Pinecone index object.
        num_dimensions (int): The dimensionality of vectors in the index.
        namespace (str, optional): The namespace to query. Defaults to an empty string.

    Returns:
        set: A set of all IDs in the index.
    """
    # Get the total number of vectors in the index.
    num_vectors = index.describe_index_stats()["namespaces"][namespace]['vector_count']
    all_ids = set()
    
    # Keep querying until we have fetched all IDs.
    while len(all_ids) < num_vectors:
        print("Length of IDs list is shorter than the number of total vectors...")
        
        # Generate a random query vector.
        input_vector = np.random.rand(num_dimensions).tolist()
        print("Creating random vector...")
        
        # Fetch IDs that are close to the random vector.
        ids = get_ids_from_query(index, input_vector)
        print("Getting IDs from a vector query...")
        
        # Update the master list of IDs.
        all_ids.update(ids)
        print(f"Collected {len(all_ids)} IDs out of {num_vectors}.")

    return all_ids




    #   Pinecone Helpful Information 
    """
    Pinecone will perform an upsert operation, which means that it will insert the new vector if the ID
    is not already present, and update the existing vector if the ID is already there. The duplication 
    check is not based on the vector values but on the IDs. If the ID is the same, the vector will be 
    updated regardless of whether the vector values are the same or different.
    """



def ensure_context_vector_exists(index_name: str, dimension: int,   context_vector_id: str, context_text: str): #   works
    index = pinecone.Index(index_name)
    existing_ids = get_all_ids_from_index(index, dimension)  # Assumes you have a function to get all IDs

    if context_vector_id in existing_ids:
        print(f"Context vector '{context_vector_id}' already exists in index '{index_name}'.")
        return "exists"
    else:
        store_strings_in_pinecone(index_name, [context_vector_id], [context_text])
        print(f"Created context vector '{context_vector_id}' in index '{index_name}'.")
        return "created"


