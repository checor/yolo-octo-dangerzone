#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
from bs4 import BeautifulSoup

def get_banamex_dollar():
	ban_url = "http://www.banamex.com/economia_finanzas/es/divisas_metales/resumen.htm"
	response = urllib2.urlopen(ban_url)
	html = response.read()
	soup = BeautifulSoup(html)
	

def get_amazon_results(keywords):
    print "Buscando", keywords, ". . ."
    keywords = urllib2.quote(keywords)
    search_url = "http://www.amazon.com/s/field-keywords=" + keywords
    response = urllib2.urlopen(search_url)
    html = response.read()
    soup = BeautifulSoup(html)
    products = soup.findAll(class_ = "prod")
    names = []
    prices = []
    for elem in products:
        if elem.find(class_="srSprite sprPrime") != None:
            name = elem.find(class_="lrg bold").string
            del_price = elem.find(class_="grey").string   
            price = elem.find(class_="bld lrg red").string
            print name, del_price, price
            names.append(name)
            prices.append(price)
    print ""
    return products
    
def main():
    while True:
        item = raw_input("Buscar: ")
        if item == 'q' or item == '':
            break
        get_amazon_results(item)
    return 0

if __name__ == '__main__':
    main()

