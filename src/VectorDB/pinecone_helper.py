import pinecone
import numpy as np
import openai_helper
from typing import Union, List, Dict
from config import PINECONE_API_KEY
from datetime import datetime, timedelta
from datetime import datetime




'''
pinecone_helper.py Summary:

1. initialize_pinecone: (Works) Initializes Pinecone with specified API key.
2. ensure_index_exists: (Works) Checks if index exists, creates it if not.
3. store_strings_in_pinecone: (Works) Stores text strings as vectors with optional metadata.
4. store_vectors_in_pinecone: (Works) Stores pre-computed vectors with optional metadata.
5. delete_vectors_by_id: (Works) Deletes vectors by ID from Pinecone.
6. delete_all_vectors: (Works) Deletes all vectors from a Pinecone index.
7. delete_all_vectors_except: (Works) Deletes all vectors except those with specified IDs.
8. update_vector: (Works) Updates vector in Pinecone by ID.
9. query_index: (Works) Queries Pinecone for similar vectors to a given query vector, applies threshold.
10. get_ids_from_query: (Works) Fetches IDs matching a given query vector.
11. get_all_ids_from_index: (Works) Fetches all IDs in a Pinecone index.
12. ensure_context_vector_exists: (Works) Ensures context vector exists or creates it.
13. filter_by_metadata: (Works) Filters query results by metadata key-value pairs.
14. update_metadata: (Works) Updates metadata for a specific vector by ID.
15. advanced_search: (Works) Executes a query, filters by metadata and applies threshold.
16. add_metadata_pair: (Works) Adds / Updates existing, a single metadata key-value pair for one or many IDs.
17. remove_metadata_pair: (Works) Removes a single metadata key-value pair for one or many IDs.
'''




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



# Store vector in pinecone from string, handles single id & string or list of both.  #   works
def store_strings_in_pinecone(index_name: str, ids: Union[str, List[str]], texts: Union[str, List[str]], metadata: Union[None, dict, List[dict]] = None):  
    try:
        if isinstance(ids, str):
            ids = [ids]
        if isinstance(texts, str):
            texts = [texts]
        
        default_metadata = {'input_string': texts, 'timestamp': datetime.utcnow().isoformat()}
        
        if metadata is None:
            metadata = [default_metadata for _ in range(len(ids))]
        elif isinstance(metadata, dict):
            metadata = [metadata]
        
        for meta in metadata:
            meta.update(default_metadata)

        index = pinecone.Index(index_name)
        embeddings = openai_helper.generate_embeddings(texts)

        if embeddings is None:
            print(f"Failed to generate embeddings for texts.")
            return False

        vector_dicts = [{'id': id, 'values': vector, 'metadata': meta} for id, vector, meta in zip(ids, embeddings, metadata)]
        index.upsert(vector_dicts)
        
        print(f"Vectors stored successfully in index '{index_name}'")
        return True
    except Exception as e:
        print(f"Error storing vectors in index '{index_name}':", e)
        return False





#   Store vector in pinecone vector, handles single id & vector or list of both.    #   Works
def store_vectors_in_pinecone(index_name: str, ids: Union[str, List[str]], vectors: Union[List[float], List[List[float]]], input_string: Union[None, str, List[str]] = None, metadata: Union[None, dict, List[dict]] = None):
    try:
        if isinstance(ids, str):
            ids = [ids]
        if isinstance(vectors[0], float):
            vectors = [vectors]

        # Initialize default metadata
        default_metadata = {'timestamp': datetime.utcnow().isoformat()}

        # Handle input_string
        if input_string is None:
            input_string_list = [None for _ in range(len(ids))]
        elif isinstance(input_string, str):
            input_string_list = [input_string]
            print("input string list: ", input_string_list)
        else:
            input_string_list = input_string
            print("input string: ", input_string)

        if metadata is None:
            metadata = [default_metadata for _ in range(len(ids))]
        elif isinstance(metadata, dict):
            metadata = [metadata]

        # Append default metadata and input_string to each item in the metadata list
        for meta, inp_str in zip(metadata, input_string_list):
            meta.update(default_metadata)
            meta['input_string'] = inp_str

        index = pinecone.Index(index_name)
        vector_dicts = [{'id': id, 'values': vector, 'metadata': meta} for id, vector, meta in zip(ids, vectors, metadata)]

        index.upsert(vector_dicts)

        print(f"Vectors stored successfully in index '{index_name}'")
    except Exception as e:
        print(f"Error storing vectors in index '{index_name}':", e)



#   Deletes vectors based on their id or a list of their ids
def delete_vectors_by_id(index_name, ids): #   Works
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
        index = pinecone.Index(index_name)
        if not isinstance(exclude_ids, list):
            exclude_ids = [exclude_ids]

        all_ids = get_all_ids_from_index(index, num_dimensions)

        print(f"All IDs from Pinecone: {all_ids}")  # Debug line

        non_existent_ids = [id for id in exclude_ids if id not in all_ids]
        if non_existent_ids:
            print(f"Warning: These IDs in exclude_ids do not exist in Pinecone DB: {non_existent_ids}")

        ids_to_delete = [id for id in all_ids if id not in exclude_ids]
        
        print(f"IDs to delete: {ids_to_delete}")  # Debug line

        if ids_to_delete:
            index.delete(ids_to_delete)
            print(f"Deleted all vectors from index '{index_name}' except {exclude_ids}")
        else:
            print(f"No vectors to delete from index '{index_name}' except {exclude_ids}")

    except KeyError as ke:
        print(f"KeyError encountered: {ke}")
    except Exception as e:
        print(f"Error deleting vectors from index '{index_name}':", e)




#   Updated only the embedding portion of the vector specified by it's ID
def update_vector(index_name, id, new_vector):  #   Works
    print("\nEntered update_vector function \n")
    try:
        store_vectors_in_pinecone(index_name, [id], [new_vector])
        print(f"Vector updated successfully in index '{index_name}'")
    except Exception as e:
        print(f"Error updating vector in index '{index_name}':", e)



def update_metadata(index_name, id, new_metadata):  #   works
    index = pinecone.Index(index_name)
    try:
        print(f"Updating metadata for ID: {id}")

        # Fetch the existing metadata
        existing_metadata = index.fetch(ids=[id])['vectors'][id]['metadata']
        print(f"Existing metadata: {existing_metadata}")

        # Preserve 'timestamp' and 'input_string' from existing metadata
        for key in ['timestamp', 'input_string']:
            if key in existing_metadata:
                new_metadata[key] = existing_metadata[key]
        
        # Add or update the 'update_timestamp'
        new_metadata['update_timestamp'] = datetime.utcnow().isoformat()
        
        print(f"New metadata: {new_metadata}")

        # Fetch the vector for the given ID
        fetched_vector = index.fetch(ids=[id])
        if 'vectors' in fetched_vector and id in fetched_vector['vectors']:
            vector = fetched_vector['vectors'][id]['values']
        else:
            print(f"No vector found for ID {id}")
            return False

        print(f"Existing vector for ID {id}: {vector}")

        # Update metadata
        upsert_data = [{"id": id, "values": vector, "metadata": new_metadata}]
        upsert_result = index.upsert(upsert_data)
        
        print(f"Upsert result: {upsert_result}")

        print(f"Metadata updated successfully.")
        return True

    except Exception as e:
        print(f"Error updating metadata: {e}")
        return False



def update_vector_and_metadata(index_name, id, new_vector, new_metadata):   #   Works
    """
    Updates both the vector and metadata for a given ID in the specified Pinecone index.
    
    Args:
        index_name (str): The name of the Pinecone index.
        id (str): The ID of the vector to update.
        new_vector (List[float]): The new vector.
        new_metadata (dict): The new metadata.
        
    Returns:
        bool: True if both updates were successful, False otherwise.
    """
    try:
        vector_status = update_vector(index_name, id, new_vector)
        metadata_status = update_metadata(index_name, id, new_metadata)

        if vector_status and metadata_status:
            print(f"Successfully updated both vector and metadata for ID {id} in index {index_name}.")
            return True
        else:
            print(f"Failed to update both vector and metadata for ID {id} in index {index_name}.")
            return False
    except Exception as e:
        print(f"Error updating vector and metadata in index {index_name} for ID {id}: {e}")
        return False


#   Search the vectordb for a similiar match to the embedding you want to look up
def query_index(index_name, query_vector, top_k=10, threshold=0.7, include_metadata=True, include_values=False):    #   Works
    try:
        index = pinecone.Index(index_name)
        results = index.query(queries=[query_vector], top_k=top_k, include_metadata=include_metadata, include_values=include_values)
        filtered_results = []
        
        if 'results' in results and len(results['results']) > 0 and 'matches' in results['results'][0]:
            for result in results['results'][0]['matches']:
                if result['score'] >= threshold:
                    filtered_results.append(result)
        
        return filtered_results  # Return the filtered results

    except Exception as e:
        print(f"Error querying index '{index_name}':", e)
        return None  # Return None if an exception occurs




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
def get_all_ids_from_index(index, num_dimensions, namespace=""):    #   Works
    try:
        stats = index.describe_index_stats()
        num_vectors = stats.get("namespaces", {}).get(namespace, {}).get('vector_count', 0)
        print(f"Total number of vectors in index: {num_vectors}")  # Debug line

        all_ids = set()
        
        while len(all_ids) < num_vectors:
            print("Length of IDs list is shorter than the number of total vectors...")
            
            input_vector = np.random.rand(num_dimensions).tolist()
            print("Creating random vector...")
            
            try:
                ids = get_ids_from_query(index, input_vector)
            except Exception as inner_e:
                print(f"Error in get_ids_from_query: {inner_e}")
                raise  # Propagate the exception to the outer try-except block

            print("Getting IDs from a vector query...")
            
            all_ids.update(ids)
            print(f"Collected {len(all_ids)} IDs out of {num_vectors}.")

        return all_ids

    except KeyError as ke:
        print(f"KeyError encountered: {ke}")
        raise  # Propagate the exception to let the calling function know that an error occurred
    except Exception as e:
        print(f"General error in get_all_ids_from_index: {e}")
        raise  # Propagate the exception



def ensure_context_vector_exists(index_name: str, dimension: int, context_vector_id: str, context_text: str): #   works
    print("entered ensure_context_vector_exists function")
    index = pinecone.Index(index_name)

    existing_ids = get_all_ids_from_index(index, dimension)  # Assumes you have a function to get all IDs

    if context_vector_id in existing_ids:
        print(f"Context vector '{context_vector_id}' already exists in index '{index_name}'.")
        return "exists"
    else:
        context_metadata = {'type': 'context', 'description': 'This is the context vector for story-telling.'}
        store_strings_in_pinecone(index_name, [context_vector_id], [context_text], metadata=context_metadata)
        print(f"Created context vector '{context_vector_id}' with metadata in index '{index_name}'.")
        return "created"




# Filters query results based on metadata key-value pairs
def filter_by_metadata(results, key, value):    #   Works
    try:
        print("Filtering by metadata...")
        return [res for res in results if res['metadata'].get(key) == value]
    except Exception as e:
        print(f"Error filtering by metadata: {e}")


# Executes a query, returns results filtered by metadata key-value pairs
def advanced_search(index_name, query_vector, key, value, top_k=10, threshold=0.7): #   Works
    try:
        print("Performing advanced search...")
        index = pinecone.Index(index_name)
        results = index.query(queries=[query_vector], top_k=top_k, include_metadata=True)['results'][0]['matches']
        
        # Filter results by threshold and metadata
        filtered_results = [res for res in results if res['score'] >= threshold]
        filtered_results = filter_by_metadata(filtered_results, key, value)
        
        return filtered_results
    except Exception as e:
        print(f"Error in advanced search: {e}")



def add_metadata_pair(index_name, ids, key, value):  #   Works
    if not isinstance(ids, list):
        ids = [ids]
    
    index = pinecone.Index(index_name)
    vectors = index.fetch(ids=ids)['vectors']

    for id in ids:
        existing_metadata = vectors[id]['metadata']
        existing_metadata[key] = value
        upsert_data = {"id": id, "values": vectors[id]['values'], "metadata": existing_metadata}
        index.upsert([upsert_data])


def remove_metadata_pair(index_name, ids, key): #   Works
    if not isinstance(ids, list):
        ids = [ids]

    index = pinecone.Index(index_name)
    vectors = index.fetch(ids=ids)['vectors']

    for id in ids:
        existing_metadata = vectors[id]['metadata']
        if key in existing_metadata:
            del existing_metadata[key]
        upsert_data = {"id": id, "values": vectors[id]['values'], "metadata": existing_metadata}
        index.upsert([upsert_data])





def decay_function(timestamp, current_time, half_life=timedelta(days=7)):
    elapsed_time = (current_time - timestamp).total_seconds()
    decay_factor = np.exp(-elapsed_time / half_life.total_seconds())
    return decay_factor



def update_game_context(index_name, context_id, new_text):
    current_time = datetime.utcnow()
    print(f"Debug: Current time is {current_time}")

    # Generate embedding for the new text
    new_vector = openai_helper.generate_embeddings([new_text])[0]
    print(f"Debug: New vector type is {type(new_vector)}, first 10 values are {new_vector[:10]}")
    
    if new_vector is None:
        print("Failed to generate embeddings for the new text.")
        return "Failure"

    index = pinecone.Index(index_name)
    existing_vector_info = index.fetch(ids=[context_id])['vectors'][context_id]
    print(f"Debug: Existing vector info first 10 values are {list(existing_vector_info['values'][:10])}")

    existing_vector = existing_vector_info['values']
    print(f"Debug: Existing vector type is {type(existing_vector)}, first 10 values are {existing_vector[:10]}")

    existing_timestamp_str = existing_vector_info['metadata'].get('updated_timestamp', current_time.isoformat())
    print(f"Debug: Existing timestamp string type is {type(existing_timestamp_str)}, value is {existing_timestamp_str}")

    if isinstance(existing_timestamp_str, datetime):
        existing_timestamp = existing_timestamp_str
    else:
        existing_timestamp = datetime.fromisoformat(existing_timestamp_str)
    
    print(f"Debug: Existing timestamp type is {type(existing_timestamp)}, value is {existing_timestamp}")

    # Calculate decay factors
    existing_decay = decay_function(existing_timestamp, current_time)
    print(f"Debug: Existing decay type is {type(existing_decay)}, value is {existing_decay}")

    new_decay = decay_function(current_time, current_time)  # Will be 1.0, since the new vector is from "now"
    print(f"Debug: New decay type is {type(new_decay)}, value is {new_decay}")

    # Calculate updated vector
    updated_vector = (np.array(existing_vector) * existing_decay + np.array(new_vector) * new_decay) / (existing_decay + new_decay)
    print(f"Debug: Updated vector type is {type(updated_vector)}, first 10 values are {updated_vector[:10]}")

    # Update metadata timestamp
    existing_vector_info['metadata']['updated_timestamp'] = current_time.isoformat()
    print(f"Debug: Updated metadata is {existing_vector_info['metadata']}")

    # Upsert the updated vector
    vector_dict = {'id': context_id, 'values': updated_vector.tolist(), 'metadata': existing_vector_info['metadata']}
    try:
        index.upsert([vector_dict])
        print(f"Updated context vector '{context_id}' in index '{index_name}'.")
        return "Success"
    except Exception as e:
        print(f"Failed to update context vector: {e}")
        return "Failure"




# Query the game context
def query_game_context(index_name, query_vector, top_k=10, threshold=0.7):
    return query_index(index_name, query_vector, top_k=top_k, threshold=threshold, include_metadata=True)



# Perform a weighted average of vectors
def weighted_average(vectors, weights):
    return np.average(vectors, axis=0, weights=weights)



# Sort the vectors by their metadata timestamps
def sort_by_timestamp(vectors):
    return sorted(vectors, key=lambda x: x['metadata']['timestamp'])
