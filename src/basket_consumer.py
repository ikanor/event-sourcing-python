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

        return process(basket, message['payload'])

    def process_add_item_command(self, basket, payload):
        item_id = payload['item_id']
        item = self.items_repository.get(item_id)

        return basket.add_item(item_id, item['name'], item['price'])

    def process_checkout_command(self, basket, payload):

        return basket.checkout()
