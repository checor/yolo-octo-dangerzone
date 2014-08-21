#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
from bs4 import BeautifulSoup

def get_amazon_results(keywords):
	search_url = "http://www.amazon.com/s/field-keywords=" + keywords
	response = urllib2.urlopen(search_url)
	html = response.read()
	soup = BeautifulSoup(html)
	products = soup.find_all(class_ = "rslt prod celwidget")
	for elem in products:
		price = elem.find_all(class_="bld lrg red")
		print "Precio encontrado: ", price, type(price)
	return products

def main():
	get_amazon_results("funko mlp")
	return 0

if __name__ == '__main__':
	main()

