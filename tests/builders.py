from kinds import ADD_ITEM, CHECKOUT


_sequence_number = 0


def generate_sequence_number():
    global _sequence_number
    _sequence_number += 1
    return _sequence_number


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


def create_checkout_command(basket_id):
    return {
        'sequence_number': generate_sequence_number(),
        'timestamp': 'irrelevant_timestamp',
        'kind': CHECKOUT,
        'payload': {
            'basket_id': basket_id,
        }
    }
