from expects import be_empty, contain_exactly, expect, have_keys, have_len
from doublex import ANY_ARG, Stub

from basket_consumer import BasketConsumer
from kinds import ITEM_ADDED, CHECKOUT_STARTED, PAY_ORDER

from tests.builders import (
    create_basket_created_event, create_add_item_command,
    create_item_added_event, create_checkout_command)


with description('BasketConsumer'):

    with it('disregards non related events'):

        event = {
            'sequence': 1,
            'ts': 'a_timestamp',
            'kind': 'irrelevant_event',
        }

        consumer = BasketConsumer(
            events_repository=Stub(),
            items_repository={})

        next_events = consumer.process(event)

        expect(next_events).to(be_empty)

    with context('When processing an add_item command'):

        with it('generates an item_added event'):
            basket_id = 'a_basket_id'
            item_id = 'an_item_id'
            add_item_command = create_add_item_command(basket_id, item_id)
            items_repository = {
                item_id: {
                    'price': 9.99,
                    'name': 'An Item',
                }
            }

            with Stub() as events_repository:
                events_repository.get_by_basket_id(ANY_ARG).returns([
                    create_basket_created_event(basket_id),
                ])

            consumer = BasketConsumer(
                events_repository=events_repository,
                items_repository=items_repository)

            next_events = consumer.process(add_item_command)

            expect(next_events).to(have_len(1))
            expect(next_events[0]).to(have_keys({
                'kind': ITEM_ADDED,
                'payload': {
                    'basket_id': basket_id,
                    'item_id': item_id,
                    'item_name': 'An Item',
                    'item_price': 9.99,
                }
            }))

    with context('When processing a checkout command'):

        with it('generates a pay_order command and a checkout_started event'):
            basket_id = 'a_basket_id'
            item_id = 'an_item_id'
            item_name = 'Irrelevant Item Name'
            item_price = 9.99
            checkout_command = create_checkout_command(basket_id)

            with Stub() as events_repository:
                events_repository.get_by_basket_id(ANY_ARG).returns([
                    create_basket_created_event(basket_id),
                    create_item_added_event(basket_id, item_id, item_price),
                    create_item_added_event(basket_id, item_id, item_price),
                ])

            consumer = BasketConsumer(
                events_repository=events_repository,
                items_repository=Stub())

            next_events = consumer.process(checkout_command)

            expect(next_events).to(have_len(2))
            expect(next_events).to(contain_exactly(
                have_keys({
                    'kind': CHECKOUT_STARTED,
                    'payload': {
                        'basket_id': basket_id,
                        'total_price': 2*item_price,
                        'num_unique_items': 1,
                        'num_items': 2,
                    }
                }),
                have_keys({
                    'kind': PAY_ORDER,
                    'payload': {
                        'basket_id': basket_id,
                        'total_price': 2*item_price,
                    }
                }),
            ))
