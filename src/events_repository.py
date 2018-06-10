class EventsRepository:

    def __init__(self):
        self.storage = []

    def store(self, event):
        self.storage.append(event)

    def get_by_basket_id(self, basket_id):
        return [event for event in self.storage if (
            'basket_id' in event['payload'] and
            basket_id == event['payload']['basket_id'])]
