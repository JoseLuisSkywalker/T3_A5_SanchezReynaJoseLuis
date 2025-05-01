import random
import logging
import threading
import concurrent.futures

SENTINEL = object()

class Pipeline:
    """
    Clase para permitir una comunicación tipo pipeline entre productor y consumidor.
    """
    def __init__(self):
        self.message = 0
        self.producer_lock = threading.Lock()
        self.consumer_lock = threading.Lock()
        self.consumer_lock.acquire()  # Consumidor espera al inicio

    def get_message(self, name):
        logging.debug("%s: esperando para recibir mensaje", name)
        self.consumer_lock.acquire()
        logging.debug("%s: recibió mensaje", name)
        message = self.message
        self.producer_lock.release()
        return message

    def set_message(self, message, name):
        logging.debug("%s: esperando para enviar mensaje", name)
        self.producer_lock.acquire()
        logging.debug("%s: envió mensaje", name)
        self.message = message
        self.consumer_lock.release()

def producer(pipeline):
    """Simulamos recibir mensajes de la red."""
    for _ in range(10):
        message = random.randint(1, 101)
        logging.info("Producer got message: %s", message)
        pipeline.set_message(message, "Producer")

    pipeline.set_message(SENTINEL, "Producer")

def consumer(pipeline):
    """Simulamos guardar mensajes en una base de datos."""
    message = None
    while message is not SENTINEL:
        message = pipeline.get_message("Consumer")
        if message is not SENTINEL:
            logging.info("Consumer storing message: %s", message)

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    # logging.getLogger().setLevel(logging.DEBUG)

    pipeline = Pipeline()
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(producer, pipeline)
        executor.submit(consumer, pipeline)