import re 
import urllib.parse 
import urllib.request 
import datetime 
import time 
from downloader_p3 import Downloader
from mogon_cache import MongoCache
from scrape_callback2_p3 import ScrapeCallback
import lxml.html 



def link_crawler(seed_url,root_regx=None,node_regx=None,delay=5,max_depth=-1,max_urls=-1,user_agent='wswp',proxies=None,num_retries=1,scrape_callback=None,cache=None):
	crawl_queue = [seed_url]
	seen = {seed_url:0}
	D= Downloader(delay=delay,user_agent=user_agent,proxies=proxies,num_tries=num_retries,cache=cache)
	num_urls=0
	run_num=0
	while crawl_queue:
		url = crawl_queue.pop()
		depth = seen[url]
		html = D(url).decode('utf-8')#转化为正则表达式能够识别的格式
		run_num +=1
		print('run_num=',run_num)
		root_page_links = []
		node_page_links = []
		links=[]
		if depth != max_depth:
			if scrape_callback:
				scrape_callback.__call__(url,html)

			print('url_1=',url)
			if re.match('https://www.hao123.com/manhua/list/',url):
				print('url_2=',url)
				root_page_links = get_root_links(root_regx,html)
				node_page_links = get_node_links(node_regx,html)
				links.extend(root_page_links)
				links.extend(node_page_links)
			#print('links =')
			for link in links:
				link = normalize(seed_url,link)
				if link not in seen:
					seen[link] = depth + 1
					#if same_domain(seed_url,link):
					crawl_queue.append(link)
		num_urls +=1
		if num_urls == max_urls:
			break

def get_links(html):
	webpage_regx = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
	#print('links=',webpage_regx.findall(html))
	return webpage_regx.findall(html)

def get_root_links(root_regx,html):
	#print('html=',html)
	root_links= []
	tree = lxml.html.fromstring(html)
	results = tree.cssselect('div.pagination>div.pagelist>ul>li>a')
	root_links.extend(result.get('href') for result in results if re.match(root_regx,result.get('href')))
	#print('root_links=',root_links)
	return root_links

def get_node_links(node_regx,html):
	node_links = []
	tree = lxml.html.fromstring(html)
	results = tree.cssselect('div.list-wrap>div.list-page.clearfix>div.item-1>a.title')
	node_links.extend(result.get('href') for result in results if re.match(node_regx,result.get('href')))
	#print('node_links=',node_links)
	return node_links


def normalize(seed_url,link):
	link,_=urllib.parse.urldefrag(link)
	return urllib.parse.urljoin(seed_url,link)

def same_domain(url_1,url_2):
	return urllib.parse.urlparse(url_1).netloc == urllib.parse.urlparse(url_2).netloc

#link_regx='http://www.hao123.com/manhua/detail/'
seed_url ='https://www.hao123.com/manhua/list/?finish=&audience=&area=日本&cate=&order=&pn=1'
root_regx ='\?finish=&audience=&area=日本'
node_regx ='http://www.hao123.com/manhua/detail/'

link_crawler(seed_url=seed_url,root_regx = root_regx,node_regx=node_regx,scrape_callback=ScrapeCallback(),cache = MongoCache())