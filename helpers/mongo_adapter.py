from pymongo import MongoClient
from helpers.jsonbuilder import JsonBuilder

class MongoConnect:

    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.shopdata
        self.products = self.db.products
        self.orders = self.db.orders
        self.jb = JsonBuilder()


    def collection_check(self, collection):
        if collection == 'products':
            collection = self.products
        elif collection == 'orders':
            collection == self.orders
        else:
            print('Collection does not exist!')
            return self.jb.build(False, 'Collection does not exist')
        return collection


    def object_check(self, collection, pk):
        coll = self.collection_check(collection)
        query = coll.find_one({'id': int(pk)})
        if query:
            return True
        else:
            return False


    def get(self, collection, params):
        coll = self.collection_check(collection)
        job = coll.find_one(params, {'_id':0})

        if job == None:
            print('Product/order does not exist')
            return self.jb.build(False, 'Product/order does not exist')
        return job


    def insert(self, collection, params):
        coll = self.collection_check(collection)
        pk = int(params['id'])

        check = self.object_check(collection=collection, pk=pk)
        if check:
            print('Product/order already exists')
            return self.jb.build(False, 'Product/order already exists')

        try:
            coll.insert_one(params)
        except Exception as e:
            print('Error inserting new object on MongoDB', e)
            return self.jb.build(False, 'Error inserting new object on MongoDB - See console for error reference')
        
        return self.jb.build(True, 'Product/order created with success!')


    def delete(self, collection, params):
        coll = self.collection_check(collection)

        try:
            coll.delete_one(params)
        except Exception as e:
            print('Error deleting product', e)
            return self.jb.build(False, 'Error deleting object on MongoDB - See console for error reference')

        return self.jb.build(True, 'Product/order deleted with success!')

  
    def update(self, collection, pk, params):
        pass

        coll = self.collection_check(collection)




