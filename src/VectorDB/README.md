# LLGM DB

## Overview

This GitHub repository hosts the VectorDB component of my capstone project, which involves building an AI Gamemaster. The aim of this project is to create an intelligent game master capable of understanding context within a game. The VectorDB, powered by Pinecone and OpenAI, plays a crucial role in storing and retrieving the data necessary for the AI Gamemaster's operation.

## Features
-   openai_helper.py
    generate_embedding(text: str, model: str = "text-embedding-ada-002") pass a string returns embeddings as list of vectors from openai's api

-   pinecone_helper.py
    initialize_pinecone() Initilize pinecone with the api key
    ensure_index_exists(index_name, dimension=1536) check if the index exists so it connects instead of trying to create one 
    store_vectors(index_name, ids, vectors) Store 1 or more vectors by passing the ids and vector data 
    delete_vectors(index_name, ids) Deletes vectors based on a list of ids of vectors
    update_vector(index_name, id, new_vector) Update a certain vector based on id
    query_index(index_name, query_vector, top_k=10) Search the vectordb for a similiar match to the embedding you want to look up
    get_all_vectors(index_name, batch_size=1000) Retreieve entire vectordb to print out and see

-   main.py
    #add functions to main and document them here 

## Getting Started

Install everything in the requirments file and run the main.py file

## Installation



## Usage

Show examples of how to use your project.

## Contributing

Explain how others can contribute to your project.

## License

Specify the project's license.

## Acknowledgments

Mention any acknowledgments or credits.

## Notes

Add notes, known issues, or anything else relevant.
