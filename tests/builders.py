from kinds import BASKET_CREATED, ADD_ITEM, ITEM_ADDED, CHECKOUT


_sequence_number = 0


def generate_sequence_number():
    global _sequence_number
    _sequence_number += 1
    return _sequence_number


def create_basket_created_event(basket_id):
    return {
        'sequence_number': generate_sequence_number(),
        'timestamp': 'irrelevant_timestamp',
        'kind': BASKET_CREATED,
        'payload': {
            'basket_id': basket_id,
        }
    }


def create_add_item_command(basket_id, item_id):
    return {
        'sequence_number': generate_sequence_number(),
        'timestamp': 'irrelevant_timestamp',
        'kind': ADD_ITEM,
        'payload': {
            'basket_id': basket_id,
            'item_id': item_id,
        }
    }


def create_item_added_event(basket_id, item_id, item_price):
    return {
        'sequence_number': generate_sequence_number(),
        'timestamp': 'irrelevant_timestamp',
        'kind': ITEM_ADDED,
        'payload': {
            'basket_id': basket_id,
            'item_id': item_id,
            'item_name': 'Item #{} Name'.format(item_id),
            'item_price': item_price,
        }
    }


def create_checkout_command(basket_id):
    return {
        'sequence_number': generate_sequence_number(),
        'timestamp': 'irrelevant_timestamp',
        'kind': CHECKOUT,
        'payload': {
            'basket_id': basket_id,
        }
    }
