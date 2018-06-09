from expects import be_empty, expect
from doublex import Stub

from basket_consumer import BasketConsumer

with description('Consumer'):

    with it('disregards non related events'):

        event = {
            'sequence': 1,
            'ts': 'a_timestamp',
            'kind': 'irrelevant_event',
        }

        consumer = BasketConsumer(
            events_repository=Stub())

        next_events = consumer.process(event)

        expect(next_events).to(be_empty)
