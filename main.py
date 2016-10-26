import threading
from queue import Queue 
from spider import Spider
from domain import *
from general import *

PROJECT_NAME = 'find a PhD'
HOME_PAGE = 'https://www.findaphd.com'
DOMAIN_NAME = get_domain_name(HOME_PAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
NUMBER_OF_THREADS = 4
queue = Queue()
Spider(PROJECT_NAME, HOME_PAGE, DOMAIN_NAME)

def create_workers():
	for _ in  range(NUMBER_OF_THREADS):
		t = threading.Thread(target=work)
		t.daemon = True # die when the main exit
		t.start()

def work():
	while True:
		url = queue.get()
		Spider.crawl_page(threading.current_thread().name, url)
		queue.task_done()


def create_jobs():
	for link in file_to_set(QUEUE_FILE):
		queue.put(link)
	queue.join() #for avoiding multi-thread problem
	crawl()


def crawl():
	queued_links = file_to_set(QUEUE_FILE)
	if len(queued_links) > 0:
		print(str(len(queued_links)) + ' links left')
		create_jobs()


create_workers()
crawl()
