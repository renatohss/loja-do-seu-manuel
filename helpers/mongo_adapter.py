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
        if collection == 'products' or collection == 'product':
            collection = self.products
        elif collection == 'orders' or collection == 'order':
            collection = self.orders
        else:
            print('Collection does not exist!')
            return self.jb.build(False, 'Collection does not exist')
        return collection


    def id_check(self, collection, pk):
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

        check = self.id_check(collection=collection, pk=pk)
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
        check = self.id_check(collection=collection, pk=int(params['id']))
        if not check:
            print('Object does not exist')
            return self.jb.build(False, 'Object does not exist')

        coll = self.collection_check(collection)

        try:
            coll.delete_one(params)
        except Exception as e:
            print('Error deleting product', e)
            return self.jb.build(False, 'Error deleting object on MongoDB - See console for error reference')

        return self.jb.build(True, 'Product/order deleted with success!')

  
    def update(self, collection, pk, params):
        check = self.id_check(collection=collection, pk=int(pk))
        if not check:
            print('Object does not exist')
            return self.jb.build(False, 'Object does not exist')

        coll = self.collection_check(collection)
        try:
            coll.update_one({'id': pk}, {'$set':params})
        except Exception as e:
            print('Error updating object on MongoDB', e)
            return self.jb.build(False, "Error updating object on MongoDB - See console for error reference")
        
        return self.jb.build(True, "Object updated with success!")


    def get_all_orders(self):
        response = self.orders.find({}, {'_id': 0, 'total_price': 1})
        return response



