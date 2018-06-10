from basket import Basket
from kinds import ADD_ITEM, ITEM_ADDED, CHECKOUT, CHECKOUT_STARTED, PAY_ORDER


class BasketConsumer:

    def __init__(self, events_repository, items_repository):
        self.events_repository = events_repository
        self.items_repository = items_repository
        self.message_processors = {
            ADD_ITEM: self.process_add_item_command,
            CHECKOUT: self.process_checkout_command,
        }

    def process(self, message):

        if message['kind'] not in self.message_processors:
            return []

        basket_id = message['payload']['basket_id']
        events = self.events_repository.get_by_basket_id(basket_id)
        basket = Basket(events)
        process = self.message_processors[message['kind']]

        return process(message['payload'])

    def process_add_item_command(self, payload):
        basket_id = payload['basket_id']
        item_id = payload['item_id']
        item = self.items_repository.get(item_id)

        return [{
            'kind': ITEM_ADDED,
            'payload': {
                'basket_id': basket_id,
                'item_id': item_id,
                'item_name': item['name'],
                'item_price': item['price'],
            }
        }]

    def process_checkout_command(self, payload):
        basket_id = payload['basket_id']

        checkout_started_event = {
            'kind': CHECKOUT_STARTED,
            'payload': {
                'basket_id': basket_id,
            }
        }
        pay_order_command = {
            'kind': PAY_ORDER,
            'payload': {
                'basket_id': basket_id,
                'total_price': 9.99,
            }
        }
        return [checkout_started_event, pay_order_command]
