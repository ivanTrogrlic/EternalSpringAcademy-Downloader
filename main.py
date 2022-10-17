import threading
from downloader import Downloader
from link_finder import *

NUMBER_OF_THREADS = 1
URL = "https://akademijavjecnogproljeca.org/dudde_poruke_0_3.html"

Downloader(URL)

# Create worker threads (will die when main exits)
def main():
    # for _ in range(NUMBER_OF_THREADS):
        # t = threading.Thread(target=work)
        # t.daemon = True
        # t.start()
        # t.run()
    print("Work started")
    Downloader.crawl_page(threading.current_thread().name, URL)
    print("Work ended")

# Do the next job in the queue
def work():
    print("Work started")
    Downloader.crawl_page(threading.current_thread().name, URL)
    print("Work ended")
        
main()