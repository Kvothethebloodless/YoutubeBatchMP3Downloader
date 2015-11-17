import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup

class youtubemp3():
	
	def __init__(self,filename):
		self.filename = filename;
		self.driver = webdriver.Firefox();
		self.driver.get("http://www.youtube-mp3.org/")
		self.youtubeurlbox = self.driver.find_element_by_id('youtube-url');
		self.youtubeurlbox.clear()
		self.convertbutton = self.driver.find_element_by_id('submit');
		self.list_links = self.parse_textfile()
		self.no_links = len(self.list_links)
		self.download_link_final = 'empty'
		self.htmlsource = None
		self.soup = None
		
	def parse_textfile(self):
		f = open(self.filename,'r');
		links = f.readlines();
		cleanlinks =[];
		for link in links:
			cleanlinks.append(link[0:-1]);
		return cleanlinks
	def fill_link(self,i):
		link = self.list_links[i];
		self.youtubeurlbox.clear()
		self.youtubeurlbox.send_keys(str(link));
		
	def press_enter(self):
		self.convertbutton.send_keys(Keys.RETURN);
	def wait_to_convert(self):
		time.sleep(2);
	def get_download_link(self):
		self.htmlsource = self.driver.page_source
		self.soup = BeautifulSoup(self.htmlsource);
		hreflist = self.soup.find_all('a',href=True)
		lengtharray = []
		for ele in hreflist:
			lengtharray.append(len(ele['href']))
		download_link_end = hreflist[lengtharray.index(max(lengtharray))]['href']
				
		
		print download_link_end
		download_link_end = download_link_end
		download_link_beginning = 'http://www.youtube-mp3.org'
		download_link = download_link_beginning+download_link_end
		self.download_link_final = download_link
		
	def final_download(self):
		self.driver.get(self.download_link_final)
		time.sleep(1)
		
		

batchdownloader = youtubemp3('list.txt');
no_links = batchdownloader.no_links;

if no_links ==0:
	print('No link to download from!')
	
else:
	for i in range(no_links):
		batchdownloader.fill_link(i);
		batchdownloader.press_enter();
		batchdownloader.wait_to_convert();
		batchdownloader.get_download_link();
		batchdownloader.final_download();

	print('Job completed!')

		
		