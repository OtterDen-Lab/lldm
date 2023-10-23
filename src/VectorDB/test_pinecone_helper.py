import unittest
import pinecone_helper

class TestPineconeHelper(unittest.TestCase):

    index_name = "llgm"
    dimension = 1536
    context_vector_id = "context_vector_for_dnd"

    @classmethod
    def setUpClass(cls):
        """Initialize Pinecone and ensure the index exists before running any tests."""
        print("Initializing Pinecone and setting up index...")
        pinecone_helper.initialize_pinecone()
        pinecone_helper.ensure_index_exists(cls.index_name, dimension=cls.dimension)
        pinecone_helper.delete_all_vectors(cls.index_name)  # Delete all vectors before running tests
        print("Setup complete.\n")

    def test_initialize_pinecone(self):
        """Test the initialization of Pinecone."""
        print("Testing Pinecone initialization...")
        self.assertIsNone(pinecone_helper.initialize_pinecone())
        print("Test passed.\n")
        
    def test_ensure_index_exists(self):
        """Test if the Pinecone index exists."""
        print("Testing index existence...")
        self.assertIsNone(pinecone_helper.ensure_index_exists(self.index_name, self.dimension))
        print("Test passed.\n")

    def test_store_strings_in_pinecone(self):
        """Test storing strings in Pinecone."""
        print("Testing storing strings...")
        metadata = {"schema_type": "weapon", "weapon_type": "sword"}
        self.assertIsNone(pinecone_helper.store_strings_in_pinecone(self.index_name, "sword_of_doom", "A magical sword", metadata))
        print("Test passed.\n")

    def test_store_vectors_in_pinecone(self):
        """Test storing vectors in Pinecone."""
        print("Testing storing vectors...")
        vectors = [0.1] * self.dimension
        metadata = {"schema_type": "shield", "shield_type": "magical"}
        self.assertIsNone(pinecone_helper.store_vectors_in_pinecone(self.index_name, "shield_of_honor", vectors, metadata))
        print("Test passed.\n")

    def test_delete_vectors_by_id(self):
        """Test deleting vectors by ID."""
        print("Testing deleting vectors by ID...")
        self.assertIsNone(pinecone_helper.delete_vectors_by_id(self.index_name, ["sword_of_doom"]))
        print("Test passed.\n")

    def test_delete_all_vectors(self):
        """Test deleting all vectors."""
        print("Testing deleting all vectors...")
        self.assertIsNone(pinecone_helper.delete_all_vectors(self.index_name))
        print("Test passed.\n")

    def test_delete_all_vectors_except(self):
        """Test deleting all vectors except specified IDs."""
        print("Testing deleting vectors except some...")
        self.assertIsNone(pinecone_helper.delete_all_vectors_except(self.index_name, self.dimension, [self.context_vector_id]))
        print("Test passed.\n")

    def test_update_vector(self):
        """Test updating a vector."""
        print("Testing updating a vector...")
        new_vector = [0.2] * self.dimension
        self.assertIsNone(pinecone_helper.update_vector(self.index_name, "sword_of_doom", new_vector))
        print("Test passed.\n")

    def test_update_metadata(self):
        """Test updating metadata."""
        print("Testing updating metadata...")
        new_metadata = {"schema_type": "weapon", "weapon_type": "axe"}
        self.assertIsNone(pinecone_helper.update_metadata(self.index_name, "sword_of_doom", new_metadata))
        print("Test passed.\n")

    def test_ensure_context_vector_exists(self):
        """Test ensuring a context vector exists."""
        print("Testing ensuring context vector exists...")
        self.assertIsNotNone(pinecone_helper.ensure_context_vector_exists(self.index_name, self.dimension, self.context_vector_id, "A context vector for DnD storytelling"))
        print("Test passed.\n")

    @classmethod
    def tearDownClass(cls):
        """Delete all vectors after tests are completed."""
        #print("Tearing down, deleting all vectors...")
        #pinecone_helper.delete_all_vectors(cls.index_name)
        print("Teardown complete.\n")
        # Optionally, you can add code to deinitialize Pinecone here.

if __name__ == "__main__":
    unittest.main()
