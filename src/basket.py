from kinds import (
    BASKET_CREATED, ITEM_ADDED, CHECKOUT_STARTED, PAY_ORDER)


class Basket:

    def __init__(self, events):
        self._id = None
        self._items = []
        self._status = 'empty'
        self._total_price = 0

        self._rebuild_processors = {
            BASKET_CREATED: self._rebuild_basket_created,
            ITEM_ADDED: self._rebuild_item_added,
            CHECKOUT_STARTED: self._rebuild_checkout_started,
        }
        self._rebuild(events)

    def _rebuild(self, events):
        for event in events:
            rebuilder = self._rebuild_processors[event['kind']]
            rebuilder(event['payload'])

    def _rebuild_basket_created(self, payload):
        self._id = payload['basket_id']

    def _rebuild_item_added(self, payload):
        item = (payload['item_id'], payload['item_name'],
                payload['item_price'])
        self._items.append(item)
        self._status = 'with_items'
        self._total_price += payload['item_price']

    def _rebuild_checkout_started(self, payload):
        self._status = 'checking_out'

    def add_item(self, item_id, name, price):
        item_added_event = {
            'kind': ITEM_ADDED,
            'payload': {
                'basket_id': self._id,
                'item_id': item_id,
                'item_name': name,
                'item_price': price,
            }
        }
        return [item_added_event]

    def checkout(self):
        checkout_started_event = {
            'kind': CHECKOUT_STARTED,
            'payload': {
                'basket_id': self._id,
            }
        }
        pay_order_command = {
            'kind': PAY_ORDER,
            'payload': {
                'basket_id': self._id,
                'total_price': self._total_price,
            }
        }
        return [checkout_started_event, pay_order_command]
