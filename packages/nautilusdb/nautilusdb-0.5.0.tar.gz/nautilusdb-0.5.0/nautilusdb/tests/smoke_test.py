import unittest
import uuid

import nautilusdb as ndb


class SmokeTest(unittest.TestCase):
    """
    Verifies basic functionality of client. Not a hermetic test, it invokes real
    nautilusdb APIs
    """
    apikey1:str
    apikey2: str

    def setUp(self):
        # TODO: Replace hard-coded API key with dynamically created keys when
        # TODO: we have the ability to delete API keys
        self.apikey1 = ndb.create_api_key()
        self.apikey2 = ndb.create_api_key()
        #self.apikey1 = 'MS1hOTJmZDE1Ni1lNTg1LTcyM2ItMzZiNy0yYjEyYzdjZDQ3ZWE='
        #self.apikey2 = 'MS1iMjA0ZDc1Yi03MTc5LTZlMTgtMjBmMC02OWQzODZiOTExZDM='

    def test_invalid_api_key(self):
        ndb.init(api_key='invalid')

        # Invalid api_key triggers exception
        self.assertRaises(ndb.UnAuthorized, ndb.list_collections)

    def test_collection_apis(self):
        # Clear API key from config
        ndb.init(api_key=None)

        apikey1 = self.apikey1
        apikey2 = self.apikey2

        # Create a public collection
        public_col = self.create_collection()

        # Create private collections, one for each created key
        ndb.init(api_key=apikey1)
        private_col_key1 = self.create_collection()

        ndb.init(api_key=apikey2)
        private_col_key2 = self.create_collection()

        try:
            # List collections without API key
            ndb.init(api_key=None)
            collections_visible_to_public = \
                {col.name for col in ndb.list_collections()}
            assert private_col_key1.name not in collections_visible_to_public
            assert private_col_key2.name not in collections_visible_to_public
            assert public_col.name in collections_visible_to_public

            # List collections using API key1
            ndb.init(api_key=apikey1)
            collections_visible_to_key1 = \
                {col.name for col in ndb.list_collections()}
            assert private_col_key2.name not in collections_visible_to_key1
            assert private_col_key1.name in collections_visible_to_key1
            assert public_col.name in collections_visible_to_key1
            # Key1 is not authorized to delete a collection created by key2
            self.assertRaises(ndb.UnAuthorized, ndb.delete_collection, private_col_key2.name)

            # List collections using API key2
            ndb.init(api_key=apikey2)
            collections_visible_to_key2 = \
                {col.name for col in ndb.list_collections()}
            assert private_col_key1.name not in collections_visible_to_key2
            assert private_col_key2.name in collections_visible_to_key2
            assert public_col.name in collections_visible_to_key2
            # Key2 is not authorized to delete a collection created by key1
            self.assertRaises(ndb.UnAuthorized, ndb.delete_collection, private_col_key1.name)

        finally:
            # key1 is authorized to delete its own collections as well as public
            # collections
            ndb.init(api_key=apikey1)
            ndb.delete_collection(public_col.name)
            ndb.delete_collection(private_col_key1.name)

            ndb.init(api_key=apikey2)
            ndb.delete_collection(private_col_key2.name)

    def create_collection(self) -> ndb.Collection:
        unique_col = uuid.uuid4().hex
        col = (
            ndb.CollectionBuilder.question_answer(unique_col).build())
        return ndb.create_collection(col)

    def test_vector_apis(self):
        owner = self.apikey1
        ndb.init(owner)
        unique_col = uuid.uuid4().hex
        col = ndb.CollectionBuilder().set_name(unique_col).set_dimension(2).build()
        ndb.create_collection(col)

        try:
            # insert a collection with bad vector id should fail
            #col.upsert_vector([ndb.vector(vid="?!@#$%^&*", embedding=[1.1, 2.2])])

            # insert a collection with bad vector dimension should fail
            #col.upsert_vector([ndb.Vector(vid="\'a\'", embedding=[1.1, 2.2, 3.3])])

            col.upsert_vector([ndb.Vector(vid="abc123", embedding=[1.1, 2.2])])
            col.upsert_vector([ndb.Vector(vid="abc", embedding=[1.1, 2.2])])
            col.upsert_vector([
                ndb.Vector(vid="123", embedding=[1.1, 2.2]),
                ndb.Vector(vid="124", embedding=[1.1, 2.2]),
                ndb.Vector(vid="125", embedding=[1.1, 2.2]),
            ])

            # Upsert is idempotent
            col.upsert_vector([
                ndb.Vector(vid="123", embedding=[1.1, 2.2]),
                ndb.Vector(vid="124", embedding=[1.1, 2.2]),
                ndb.Vector(vid="125", embedding=[1.1, 2.2]),
            ])

            # Reject upsert calls if the correct api key is not provided
            ndb.init(self.apikey2)
            #self.assertRaises(ndb.UnAuthorized, col.upsert_vector, [ndb.Vector(vid="123",
            # embedding=[1.1, 2.2])])
            # self.assertRaises(ndb.UnAuthorized, col.delete_vector, ["123", "124", "125"])
        finally:
            ndb.init(owner)
            # Delete is idempotent
            #col.delete_vector(["123", "124", "125"])
            #col.delete_vector(["123", "124", "125"])
            ndb.delete_collection(col.name)

