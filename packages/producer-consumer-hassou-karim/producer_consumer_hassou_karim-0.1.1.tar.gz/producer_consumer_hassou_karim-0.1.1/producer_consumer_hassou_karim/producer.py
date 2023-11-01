from threading import Thread, Condition
import numpy as np
from typing import List


class Producer(Thread):
    """
    Defines the producer thread class. This class should generate n_data data points
    and dump them in a buffer of a fixed size max_len (To avoid indefinite growing of the buffer
    if the producer is faster than the consumer).
    """

    def __init__(
        self, buffer: List[np.array], condition: Condition, max_len: int, n_data: int
    ):
        super().__init__()
        self.condition = condition  # The condition (conditional lock) ensures that the data in the buffer doesn't surpass max_len
        self.buffer = buffer
        self.MAX_LEN = max_len
        self.n_data = n_data
        self.pid_c = 0

    def _generate_bid(self):
        """
        Generates dummy bid data.
        """
        product_id = self.pid_c
        self.pid_c += 1
        qty_ask = 0
        ask_price = 0
        qty_sell = 0
        sell_price = 0
        return np.array([product_id, qty_ask, ask_price, qty_sell, sell_price])

    def run(self):
        """
        Overridern run method called upon using the start method. This method
        pushes dummy data into the buffer.
        """
        for i in range(self.n_data + 1):
            with self.condition:
                while len(self.buffer) >= self.MAX_LEN:
                    self.condition.wait()  # Wait if the buffer is full

                if i != self.n_data:
                    data = self._generate_bid()
                    self.buffer.append(data)
                else:
                    self.buffer.append(
                        None
                    )  # Add a dummy None token to signal that the consumer's stream of data finished

                self.condition.notify()  # Notifies the consumer in the case it was waiting because the buffer was empty
