from pymongo import MongoClient
from helpers.jsonbuilder import JsonBuilder
from helpers.mongo_adapter import MongoConnect

class OrderManager:

    def __init__(self):
        self.jb = JsonBuilder()
        self.mc = MongoConnect()

    def item_check(self, item_id, item_qty):
        item_exist = self.mc.id_check(collection='products', pk=int(item_id))
        if not item_exist:
            print('Invalid order: Item id {} does not exist'.format(item_id))
            return False
        
        item_doc = self.mc.get(collection='products', params={'id':int(item_id)})
        stock = 0
        if 'stock' in item_doc.keys():
            stock = int(item_doc['stock'])
        if int(item_qty) > stock:
            print('Invalid order: There is not enough item id {} on stock'.format(item_id))
            return False

        return True

    def price_setter(self, item_id, qty):
        item = self.mc.get(collection='products', params={'id':int(item_id)})
        item_price = item['price']
        total_price = item_price * int(qty)
        return item_price, total_price


    def validate_new_order(self, order):
        id = order['id']
        order_check = self.mc.id_check(collection='orders', pk=int(id))
        if order_check:
            print('There is already a order with this id')
            return self.jb.build(False, 'There is already a order with this id')

        items = order['items']
        for item in items:
            item_check = self.item_check(item_id=int(item['id']), item_qty=int(item['qty']))
            if not item_check:
                return self.jb.build(False, 'Invalid Order - Check console for details')
        
        for item in items:
            item_id = item['id']
            item_qty = int(item['qty'])
            self.mc.update(collection='products', pk=int(item_id), params={'$inc': {'stock': -item_qty}})
            price, total_price = self.price_setter(item_id=int(item_id), qty=item_qty)
            item['unit_price'] = price
            item['total_price'] = total_price + int(order['shipping'])
            order['total_price'] += item['total_price']

        try:
            save_order = self.mc.insert(collection='orders', params=order)
        except Exception as e:
            print('Error creating order no. {1} - Error: {2}'.format(id, e))
            return self.jb.build(False, 'Error creating order: {}'.format(e))
        
        return save_order

    def calculate_ticket(self):
        orders = self.mc.get_all_orders()
        count = 0
        total_value = 0
        for order in orders:
            count += 1
            total_value += int(order['total_price'])

        ticket = total_value / count
        print('Average ticket is $', ticket)
        return self.jb.build(True, 'Average ticket is ${}'.format(ticket))