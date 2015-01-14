#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  tienda.py
#  
#  Copyright 2014 Sergio I. Urbina <checor@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import csv
import urllib
import datetime
from amazon.api import AmazonAPI
from bs4 import BeautifulSoup as BS

#Verbose
verbose = True

#Llaves de Amazon
KeyId="AKIAJXBNQWSG3IODNABA"
SecretKey="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"
asoc = "poshmx-20"

#Precio del dolar
dolar = 0.0

#Fecha
hoy = datetime.date.today()

#Para evitar deteccion por parte de bots
from fake_useragent import UserAgent
ua = UserAgent()

if verbose:
    def vprint(*args):
        for arg in args:
           print arg,
        print
else:   
    vprint = lambda *a: None      # do-nothing function

class MyOpener(urllib.FancyURLopener):
    version = ua.random
    vprint("Fake agent", version)

def get_price(id_, store):
    opener = MyOpener()
    if store.startswith('amazon'):
        api = AmazonAPI(KeyId, SecretKey,asoc)
        product = api.lookup(ItemId=id_)
        price = str(product.price_and_currency[0])
        price = float(price.translate(None, '$'))
        vprint("Precio de Amazon: ", price)
        return price
    elif store == 'hottopic':
        page = opener.open(id_).read()
        soup = BS(page)
        try:
            price = str(soup.find(class_ = "Now").text)
            price = float(price.translate(None, '$'))
            vprint("Precio de Hot Topic: ", price)
            return price
        except:
            print "Articulo no encontrado"
            return None
    elif store == 'toywiz':
        page = opener.open(id_).read()
        soup = BS(page)
        price = str(soup.find(class_ = "itemPriceBlock").text)
        price = float(price.translate(None, '$'))
        vprint("Precio de Toy Wiz: ", price)
        return price
    else:
        print "Tienda", store, "aun no implementada"
        return None

def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)

def get_dollar():
    ban_url = "http://www.dolar.mx/precio-del-dolar-hoy/"
    opener = MyOpener()
    page = BS(opener.open(ban_url).read())
    precios = page.findAll("h2")
    #Esto puede ser altamente variable, no confiable
    valores = str(precios[3])
    precio = valores[42:47]
    vprint("Precio del dolar: ", precio)
    return float(precio)

def check_csv(filename):
    dolar = get_dollar()
    
    rfile = open(filename)
    reader = csv.reader(rfile)

    lines = [l for l in reader]

    rownum = 0
    coldict = {}
    
    for row in lines:
        if rownum == 0:
            colnum = 0
            for col in row:
                coldict[col] = colnum
                colnum += 1
        else:  #¿Que hacemos para cada producto?
            vprint ("Item: ", row[coldict['post_title']], row[coldict['sku']])
            prices = {}
            stores = ('amazon', 'amazon2', 'toywiz', 'hottopic')
            for elem in stores:
                if row[coldict[elem]] != "":
                    price = get_price(row[coldict[elem]], elem)
                    if price is not None:
                        if elem.startswith('amazon'):
                            prices[elem] = price * 1.1
                        else:
                            prices[elem] = price + 3
            if prices == {}:
                row[coldict['stock_status']] = 'outofstock'
            else:
                row[coldict['stock_status']] = 'instock'
                min_price = min(prices.items(), key=lambda x: x[1]) 
                vprint("Mejor precio ", min_price)
                if min_price[0].startswith('amazon'):
                    next_tuesday = next_weekday(hoy, 1)
                    next_next = next_weekday(next_tuesday, 0)
                    row[coldict['post_excerpt']] = "Artículo bajo pedido. Ordena este prodcuto antes del Martes " + \
                    next_tuesday.strftime('%d/%m/%Y') + " y se te manda el Lunes " + next_next.strftime('%d/%m/%Y') + ". Visita el blog para corroborar esta fechas."
                else:
                    next_day = next_weekday(hoy, 0)
                    next_next = next_weekday(next_day, 0)
                    row[coldict['post_excerpt']] = "Artículo bajo pedido. Ordena este prodcuto antes del Lunes " + \
                    next_day.strftime('%d/%m/%Y') + " y se te manda el Lunes " + next_next.strftime('%d/%m/%Y') + ". Visita el blog para corroborar esta fechas."
                vprint("Costo en USD", min_price)
                mxn_buy = min_price[1] * dolar
                vprint("Costo en pesos", mxn_buy)
                costo = (float(row[coldict['porcentual']]) *  mxn_buy, \
                         float(row[coldict['fijo_min']]))
                vprint("Costos de traida: ", costo)
                mxn_total = mxn_buy + max(costo)
                vprint("Precio de venta MXN: ", mxn_total)
                if 'sale_price' in coldict:
                    row[coldict['sale_price']] = round(mxn_total, -1)
                else:
                    row[coldict['regular_price']] = round(mxn_total, -1)
        lines[rownum] = row
        rownum += 1

    writer = csv.writer(open(filename, 'w'))
    writer.writerows(lines)

def main():
    check_csv(
    return 0

if __name__ == '__main__':
    main()

