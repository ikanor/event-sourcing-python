class Receiver:

    def __init__(self, consumers, message_publisher):
        self.consumers = consumers
        self.message_publisher = message_publisher

    def process(self, message):
        next_messages = []

        for consumer in self.consumers:
            resulting_messages = consumer.process(message)
            if resulting_messages:
                next_messages += resulting_messages

        for message in next_messages:
            self.message_publisher.publish(message)
