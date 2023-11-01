from producer import Producer
from consumer import Consumer
from threading import Condition
import numpy as np
import pandas as pd


class ProducerConsumer:
    """
    This class starts both the producer and consumer threads.
    """

    def __init__(self, MAX_LEN: int, N: int):
        self.buffer = (
            []
        )  # The shared buffer where the data is dumped and from which data is consumed
        self.condition = Condition()  # Conditional lock
        self.producer = Producer(self.buffer, self.condition, MAX_LEN, N)
        self.consumer = Consumer(self.buffer, self.condition)

    def run(self):
        self.producer.start()
        self.consumer.start()
        self.producer.join()
        self.consumer.join()
        self.consumer.consumed_data = np.vstack(self.consumer.consumed_data)
        self.consumer.consumed_data = pd.DataFrame(
            self.consumer.consumed_data,
            columns=[
                "product_id",
                "ask_quantity",
                "ask_price",
                "sell_quantity",
                "sell_price",
            ],
        )
