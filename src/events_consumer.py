class EventsConsumer:

    def __init__(self, events_repository):
        self.events_repository = events_repository

    def process(self, message):
        self.events_repository.store(message)
