import threading
import logging
import time

class FakeDatabase:
    def __init__(self):
        self.value = 0
        self._lock = threading.Lock()

    def locked_update(self, name):
        logging.info("Thread %s: starting update", name)
        logging.debug("Thread %s about to lock", name)
        with self._lock:
            logging.debug("Thread %s has lock", name)
            local_copy = self.value
            local_copy += 1
            time.sleep(0.1)  # Simula una operación lenta
            self.value = local_copy
            logging.debug("Thread %s about to release lock", name)
        logging.debug("Thread %s after release", name)
        logging.info("Thread %s: finishing update", name)

def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S"
    )

    database = FakeDatabase()
    threads = []
    for i in range(5):
        thread = threading.Thread(target=database.locked_update, args=(f"Thread-{i+1}",))
        threads.append(thread)
        thread.start()


    for thread in threads:
        thread.join()

    logging.info("Valor final en base de datos: %d", database.value)

if __name__ == "__main__":
    main()