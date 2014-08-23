#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
from bs4 import BeautifulSoup

def get_banamex_dollar():
    ban_url = "http://www.dolar.mx/precio-del-dolar-hoy/"
    response = urllib2.urlopen(ban_url)
    html = response.read()
    soup = BeautifulSoup(html)
    precios = soup.findAll("h2")
    #Esto puede ser altamente variable, no confiable
    valores = str(precios[3])
    precio = valores[42:47]
    return float(precio)
    
def convert_amzn_price(precio_str):
    init = precio_str.find('$')
    init += 1
    precio = float(precio_str[init:])
    return precio
    
def precio_venta_amzn(usd):
    pass

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
    mxn = get_banamex_dollar()
    print "Precio del dolar:", mxn
    for elem in products:
        if elem.find(class_="srSprite sprPrime") != None:
            name = elem.find(class_="lrg bold").string
            del_price = elem.find(class_="grey").string   
            price = elem.find(class_="bld lrg red").string
            print name, del_price, price
            print "Precio de venta: ", convert_amzn_price(price)*mxn*1.1+100
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

