import logging
logging.basicConfig(level=logging.INFO)
import unittest
import numpy as np
import pinecone_helper
import openai_helper

def run_function(cond, func, *args, **kwargs):
    if cond:
        func(*args, **kwargs)

if __name__ == "__main__":
    try:

        logging.info("Initializing Pinecone.")
        pinecone_helper.initialize_pinecone()
        index_name = "llgm"
        id = "eastridge_village_description"
        excalibur_string = "Excalibur is a legendary sword found in Arthurian legends."
        builder_string = "Builder's Shield is a magical shield."
        eastridge_string = "eastridge village by the waterfall"
        excalibur_metadata = {"schema_type": "item", "item_type": "weapon"}
        builder_metadata = {"schema_type": "item", "item_type": "shield"}
        eastridge_metadata = {"schema_type": "location", "location_type": "village"}
        dimension = 1536
        context_vector_id = "context_vector"

        logging.info(f"Initializing index '{index_name}'...")
        pinecone_helper.ensure_index_exists(index_name, dimension)

        print("Begin Testing\n")

        # Conditionally run delete_all_vectors
        run_function(False, pinecone_helper.delete_all_vectors, index_name)
      
        # Conditionally run delete_all_except_ids
        run_function(True, pinecone_helper.delete_all_vectors_except, index_name, dimension, [context_vector_id])




        # Store vectors with metadata
        print("Testing ensure_context_vector_exists...")
        context_vector_status = pinecone_helper.ensure_context_vector_exists(index_name, dimension, context_vector_id, "I am context vector for story telling history.")
        print(f"context_vector_status: {context_vector_status}\n")


        # Store vectors with metadata
        print("Testing store_strings_in_pinecone...")
        metadata_result = pinecone_helper.store_strings_in_pinecone(index_name, id, eastridge_string, eastridge_metadata)
        print(f"\nMetadata storage result: {metadata_result}\n")     

        print("Testing store_strings_in_pinecone...")
        metadata_result = pinecone_helper.store_strings_in_pinecone(index_name, "Excalibur", excalibur_string, excalibur_metadata)
        print(f"\nMetadata storage result: {metadata_result}\n")     

        # #   Check if None is returned in metadata_result may not be necesarry if returning true or false from the function
        # if metadata_result is None:
        #     logging.error("Metadata storage returned None. Something went wrong.")

        # # # Update metadata for an context vector
        # # print("Testing update_metadata...")
        # # new_metadata = {"schema_type": "location", "location_type": "updated_village"}      #   works I think
        # # update_metadata_result = pinecone_helper.update_metadata(index_name, context_vector_id, new_metadata)
        # # print(f"Metadata update result: {update_metadata_result}\n")


        # # Update metadata for an existing vector
        # print("Testing update_metadata...")
        # new_metadata = {"schema_type": "location", "location_type": "updated_village"}      #   works I think
        # update_metadata_result = pinecone_helper.update_metadata(index_name, id, new_metadata)
        # print(f"Metadata update result: {update_metadata_result}\n")

        # # Check if fetch_metadata exists in pinecone_helper
        # if hasattr(pinecone_helper, 'fetch_metadata'):
        #     print("Testing fetch_metadata...")
        #     fetched_metadata = pinecone_helper.fetch_metadata(index_name, [id])
        #     print(f"Fetched metadata: {fetched_metadata}\n")
        # else:
        #     print("fetch_metadata function not found in pinecone_helper.\n")



        #   Need to test Query Function
        query_string = "Village"
        embedding = openai_helper.generate_embeddings(query_string)

        query_results = pinecone_helper.query_index(index_name, embedding, top_k=10, threshold=0.5)
        print("Query Results: ", query_results)


        # # Filter the results based on 1 metadata pair
        # filtered_results = pinecone_helper.filter_by_metadata(query_results, 'item_type', 'weapon')
        
        # print(f"Filtered results: {filtered_results}")


        # Metadata key-value pair for filtering
        key = 'item_type'
        value = 'weapon'

        # Perform advanced search and get filtered results
        filtered_results = pinecone_helper.advanced_search(index_name, embedding, key, value, top_k=10, threshold=0.7)
        
        print(f"Filtered results from advanced search: {filtered_results}")



        # # Add or update a metadata pair for multiple IDs    Works
        # pinecone_helper.update_metadata_pair(index_name, ['eastridge_village_description', context_vector_id], 'location_type', 'Castle')

        # # Remove a metadata pair for a single ID    Works
        # pinecone_helper.remove_metadata_pair(index_name, 'eastridge_village_description', 'location_type')



         # Step 2: Create a test vector
        # test_id = "test_vector"
        # input_string = "Sample input string"
        # initial_vector = np.random.rand(1536).tolist()  # Assuming dimension is 1536
        # pinecone_helper.store_vectors_in_pinecone(index_name, [test_id], [initial_vector], input_string)  #   Works

        # # Step 3: Update vector
        # new_vector = np.random.rand(1536).tolist()
        # # pinecone_helper.update_vector(index_name, test_id, new_vector)    #   Works

        # # Step 4: Update vector and metadata
        # new_metadata = {"field1": "new_value", "field2": "another_value"}
        # pinecone_helper.update_vector_and_metadata(index_name, test_id, new_vector, new_metadata)   #   Works

        #   make sure the input string is working for these update and store vector functions 





        print("\nEnd Testing\n")

    except Exception as e:
        logging.error(f"An error occurred: {e}, Type: {type(e)}")
        exit(1)
