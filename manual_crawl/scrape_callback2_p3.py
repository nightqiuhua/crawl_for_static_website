import csv 
import re 
import lxml.html 
import urllib.parse

class ScrapeCallback:
	def __init__(self):
		self.writer = csv.writer(open('manhua','w'),lineterminator='\n')
		self.fields =('title','author','area','stored_number','type','content','popular')
		self.writer.writerow(self.fields)

	def __call__(self,url,html):
		if re.search('http://www.hao123.com/manhua/detail/',url):
			tree = lxml.html.fromstring(html)
			row=[]
			title_item = tree.xpath('//div[@class="title-wrap"]/text()')[0]
			row.append(str(title_item))
			node_list = tree.xpath('//ul[@class="info-list clearfix"]/li[@class="item"]')
			area = node_list[1].xpath('string(./span[@class="value"])')
			if re.match('日本',str(area)):
				for node in node_list:
					value = node.xpath('./span[@class="value"]')[0]
					item = value.xpath('string(.)')
					row.append(str(item).replace('\xa0',''))
				print('row=',row)
				try:
					self.writer.writerow(row)
				except UnicodeEncodeError:
					row = []
					self.writer.writerow('')
			else:
				print('not produced by Japan')
