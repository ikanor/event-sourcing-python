from kinds import ADD_ITEM, ITEM_ADDED


class BasketConsumer:

    def __init__(self, events_repository, items_repository):
        self.items_repository = items_repository

    def process(self, event):

        if event['kind'] == ADD_ITEM:
            return self.process_add_item_command(event['payload'])
        else:
            return []

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
