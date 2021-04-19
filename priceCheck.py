import sys
import os.path
from os import path
import requests
from bs4 import BeautifulSoup
import re

supportedBrands = ['adidas']

def clean_tag_html(raw_html):
	cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
	cleantext = re.sub(cleanr, '', raw_html)
	return int(cleantext.replace('$', ''))

def adidas_get_price(url, product):
	hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'}
	htmlPage = requests.get(url, headers=hdr, timeout=15)
	if htmlPage.status_code != 200:
		return -1
	try:
		soup = BeautifulSoup(htmlPage.content, 'html.parser')
		htmlPrice = soup.find_all('div', class_='gl-price-item')
		raw_html = str(htmlPrice[0])
		return clean_tag_html(raw_html)
	except:
		print('[ERROR]: Unable to webscrape for ', product)
		return -1

def separate_brands(brand, url, price, product):
	priceOnPage = 0
	if brand == 'adidas':
		priceOnPage = adidas_get_price(url, product)

	if priceOnPage != -1:
		if int(priceOnPage) < price:
			print('[SUCCESS]: ', product, ' price dropped from ', price, ' -> ', priceOnPage)
		else:
			print('[CHECKED]: ', product)

def check_text_file_input(textFileInput):
	if len(textFileInput) == 1:
		return False
	if len(textFileInput) != 4:
		print('[ERROR]: Invalid syntax on line. Should be \'brand\' \'url\' \'price\' \'product name\'')
		return False
	elif textFileInput[0] not in supportedBrands:
		print('[ERROR]: \'',textFileInput[0], '\' not supported brand')
		return False
	try:
		int(textFileInput[2])
	except ValueError:
		print('[ERROR]: ', textFileInput[3], ' price couldn\'t be converted to int')
	return True

def parse_text_file(textFile):
	# I can make this the multithreaded part
	f = open(textFile, 'r')
	for item in f:
		items = item.split(' ')
		if check_text_file_input(items):
			separate_brands(items[0], items[1], int(items[2]), items[3].replace('\n', ''))

def main():
	if len(sys.argv) != 2:
		print('[ERROR]: expecting textfile')
		print('usage: python3 priceCheck.py [\'example.txt\']')
		quit()

	textFile = sys.argv[1]

	if path.exists(textFile) == False:
		print('[ERROR]: ', textFile, 'does not exist')
		quit()
	elif path.isfile(textFile) == False:
		print('[ERROR]: ', textFile, ' is not a file.')
		quit()
	elif textFile.endswith('.txt') == False:
		print('[ERROR]: ', textFile, ' is not a text file')
		quit()

	parse_text_file(textFile)

if __name__ == "__main__":
	main()

