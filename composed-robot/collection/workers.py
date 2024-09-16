from threading import Thread


class Worker(Thread):
    def __init__(self, subscriber, queue):
        super().__init__()
        self.subscriber = subscriber
        self.queue = queue

    def run(self):
        self.subscriber.start()
        for topic, node, message in self.subscriber.json_stream():
            self.queue.put((topic, node, message))


class LocalWorker(Thread):
    def __init__(self, event_generator, queue):
        super().__init__()
        self.event_generator = event_generator
        self.queue = queue

    def run(self):
        for topic, node, message in self.event_generator():
            self.queue.put((topic, node, message))
