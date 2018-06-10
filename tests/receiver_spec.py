from expects import be_empty, contain, expect, have_key, have_keys
from doublex import ANY_ARG, Spy
from doublex_expects import have_been_called, have_been_called_with

from events_repository import EventsRepository
from events_consumer import EventsConsumer
from basket_consumer import BasketConsumer
from receiver import Receiver

from kinds import ITEM_ADDED, CHECKOUT_STARTED

from tests.builders import (
    create_basket_created_event, create_add_item_command,
    create_checkout_command)

SHIRT_ID = 'SHIRT'
HAT_ID = 'HAT'
JACKET_ID = 'JACKET'

ITEMS = {
    SHIRT_ID: {'name': 'White Shirt', 'price': 8.95},
    HAT_ID: {'name': 'Black Fedora', 'price': 16.60},
    JACKET_ID: {'name': 'Leather Jacket', 'price': 105.75},
}

with description('Receiver'):

    with it('processes a checkout cycle'):

        basket_id = 'a_basket_id'
        item_id = 'an_item_id'
        item_name = 'Irrelevant Item Name'
        item_price = 9.99

        items_repository = ITEMS
        events_repository = EventsRepository()
        events_consumer = EventsConsumer(events_repository)
        basket_consumer = BasketConsumer(events_repository, items_repository)
        message_publisher = Spy()

        receiver = Receiver(
            consumers=[events_consumer, basket_consumer],
            message_publisher=message_publisher)

        with message_publisher:
            message_publisher.publish(ANY_ARG).delegates(receiver.process)

        total_price = 0
        num_items = 0
        receiver.process(create_basket_created_event(basket_id))
        expect(message_publisher.publish).not_to(have_been_called)

        receiver.process(create_add_item_command(basket_id, SHIRT_ID))
        expect(message_publisher.publish).to(have_been_called_with(
            have_key('kind', ITEM_ADDED)).once)
        total_price += ITEMS[SHIRT_ID]['price']
        num_items += 1

        receiver.process(create_add_item_command(basket_id, SHIRT_ID))
        expect(message_publisher.publish).to(have_been_called_with(
            have_key('kind', ITEM_ADDED)).twice)
        total_price += ITEMS[SHIRT_ID]['price']
        num_items += 1

        receiver.process(create_add_item_command(basket_id, HAT_ID))
        expect(message_publisher.publish).to(have_been_called_with(
            have_key('kind', ITEM_ADDED)).exactly(3))
        total_price += ITEMS[HAT_ID]['price']
        num_items += 1

        receiver.process(create_checkout_command(basket_id))
        expect(message_publisher.publish).to(have_been_called_with(
            have_keys({
                'kind': CHECKOUT_STARTED,
                'payload': have_keys({
                    'total_price': total_price,
                    'num_items': num_items,
                })
            })).once)
