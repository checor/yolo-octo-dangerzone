#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2, ftplib
from bs4 import BeautifulSoup

def ftp_init():
    print "Entrando FTP . . ."
    try:
        ftp = ftplib.FTP('ftp.ponyshop.mx')
        passwd = raw_input("Password: ")
        ftp.login("ponyshop", passwd)
        ftp.cwd('public_html/imagenes')
        return ftp
    except:
        print "No se puede acceder al FTP"
        
def upload_ftp(archivo):
    pass    

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
    
def precio_venta_amzn(usd, mxn, taxas=1.16, envio=1.25):
    price = usd*taxas*mxn*envio
    return round(price, -1)
    

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
            sug_price = elem.find(class_="grey").string   
            price = elem.find(class_="bld lrg red").string
            img_file = elem.find(class_="productImage cfMarker")['src']
            raw_price = convert_amzn_price(price)
            print name, sug_price, price
            print "Venta: MXN", precio_venta_amzn(raw_price, mxn)
            print img_file
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

