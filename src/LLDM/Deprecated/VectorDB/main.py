import logging
logging.basicConfig(level=logging.INFO)

import pinecone_helper
import openai_helper
# import json_schema_helper

if __name__ == "__main__":
    try:
        logging.info("Initializing Pinecone.")
        pinecone_helper.initialize_pinecone()
        index_name = "llgm"
        id = "eastridge_village_description"
        string = "Excalibur is a legendary sword found in Arthurian legends. It's a magical weapon."
        string2 = "Builder's Shield is a magical shield embowed with the power of creation and offers the ultimate utility."
        string3 = "eastridge village by the waterfall"
        dimension = 1536  # Update this to match the dimension of your embeddings
        context_vector_id = "context_vector"
        logging.info(f"\nInitializing index '{index_name}'...")
        pinecone_helper.ensure_index_exists(index_name, dimension=dimension)

        #   Begin tests code here    ------------
        print("\nBegin Testing\n")

        # print("Testing delete all vectors functions")
        # pinecone_helper.delete_all_vectors(index_name)  #   CAREFUL DELETES ALL VECTORS


        # # Sample D&D item based on the item.schema.json
        # sample_item = {
        #     "id": 1,
        #     "name": "Excalibur",
        #     "weight": 10,
        #     "description": "A legendary sword.",
        #     "magic": True,
        #     "source": {
        #         "text": "Arthurian Legends",
        #         "note": "From ancient mythology",
        #         "href": "https://example.com/arthurian-legends"
        #     }
        # }

        #   Test out delete_all_except_ids function
        pinecone_helper.delete_all_vectors_except(index_name, dimension, context_vector_id)


        # # Store the sample item in vectordb
        pinecone_helper.store_strings_in_pinecone(index_name, id, string3)
        pinecone_helper.store_strings_in_pinecone(index_name, ["item_2", "item_3"], [string, string2])
        # pinecone_helper.store_strings_in_pinecone(index_name, "item_3", string)

        # context_vector_status = pinecone_helper.ensure_context_vector_exists(index_name, dimension, context_vector_id, "I am context vector for story telling history.")
        # print("\ncontext_vector_status", context_vector_status, "\n")




        
        # # Retrieve the sample item from vectordb by its ID
        # retrieved_item = json_schema_helper.retrieve_json_from_vectordb(1, "item", "some_index_name")
        # print("Retrieved item:")
        # json_schema_helper.print_json(retrieved_item)





        #   End tests code here  ------------
        print("\End Json Testing\n")

        # ids_to_delete = [
        #      'id: 1, name: Excalibur, weight: 10, description: A legendary sword, '
            
        # ]

        # pinecone_helper.delete_vectors(index_name, ids_to_delete)
        # print("Deleted ")



        # sentence = "eastridge village by the waterfall"
        # # word = "eastridge village"
        word = "eastridge village"
        # # word = "Excalibur"
        # flattened_json = "id: 1, name: Excalibur, weight: 10, description: A legendary sword, magic: True, source_text: Arthurian Legends, source_note: From ancient mythology, source_href: https://example.com/arthurian-legends"


        # logging.info(f"\nGenerating embedding for sentence: {sentence}")
        # embedded_sentence = openai_helper.generate_embeddings(sentence)
        logging.info(f"\nGenerating embedding for word: {word}")
        embedded_word = openai_helper.generate_embeddings(word)

        # # After generating embeddings
        # if embedded_sentence is not None and embedded_word is not None:
        #     logging.info(f"\nSuccessfully generated embeddings.")
        #     logging.info(f"Type of embedded_sentence: {type(embedded_sentence)}, first few elements: {embedded_sentence[:10]}")
        #     logging.info(f"Type of embedded_word: {type(embedded_word)}, first few elements: {embedded_word[:10]}")

        #     #   Store a description of eastridge village in the vectordb
        #     print("\n\n")
        #     logging.info(f"\nStoring embeddings in vector database...")
        #     ids = [sentence]
        #     vectors = [embedded_sentence]
        #     pinecone_helper.store_vectors_in_pinecone(index_name, ids, vectors)

        #   Query the database for the words eastridge village
        print("\n\n")
        logging.info(f"\nQuerying database for: {word}...")
        pinecone_helper.query_index(index_name, embedded_word, top_k=5)

        #     #   Test the delete function on eastridge village description
        #     print("\n\n")
        #     # Test the delete_vectors function
        #     delete_ids = ["eastridge_village_by_the_waterfall_id"]
        #     pinecone_helper.delete_vectors(index_name, delete_ids)
        #     logging.info(f"\nDeleted vectors with IDs: {delete_ids}")


        #     # #   Test the update_vector function
        #     # print("\n\n")
        #     # update_id = "eastridge_village_id"
        #     # new_vector = [0.1] * dimension  # Replace with the new vector you want to use
        #     # pinecone_helper.update_vector(index_name, update_id, new_vector)
        #     # logging.info(f"\nUpdated vector with ID: {update_id}")


        #     #   Query Database again for the word after the delete function has been run.
        #     print("\n\n")
        #     logging.info(f"\nQuerying database for: {word}...")
        #     pinecone_helper.query_index(index_name, embedded_word, top_k=5)

        #     # print("\n\n")
        #     # # Display the entire vector database if it's not empty
        #     # all_vectors = pinecone_helper.get_all_vectors(index_name)
        #     # if all_vectors is not None:
        #     #     logging.info("\nDisplaying the entire vector database:")
        #     #     for id, vector in all_vectors.items():
        #     #         logging.info(f"ID: {id}, Vector: {vector[:10]}")
        #     # else:
        #     #     logging.error("Failed to retrieve vectors from the database.")


        # else:
        #     logging.error("One or both embeddings failed to generate.")
        #     exit(1)

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        exit(1)



        #   I need functions that will print out the entire vectordb
        #   I need functions that will print out all data in vectordb that match a string query
        #   I need functions that will print out all data in vectordb that has a id that contains a given string
        #   I need functions that will delete an entire docarray object scope based on its id from the vectordb
        #   I need functions that will delete all data in the vectordb
        #   I need functions that will delete all data in the vectordb that matches a given string for its vectors id
        #   I need functions that will query the vectordb for all matches of given string in vectors id
        #   I need functions that will query for an entire docarray object based on id matching for vector ids
        #   I need functions that will update an entire docarray object in the vectordb with new information
        #   I need functions that will update a vector embedding given its id and an updated embedding  (may not be needed or possible)

        #   I need functions for storing large amounts of data into the vectordb either as strings json or docarray




        #   I have functions that will store a docarray into a vectordb
        #   I have functions that create embeddings from strings 
        #   I have docarrays that deal with embeddings internally 
