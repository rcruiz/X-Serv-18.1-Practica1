#!/usr/bin/python3
# -*- coding: iso-8859-15 -*-

"""
Aplicacion web simple para acortar URLs
Rosa Cristina Ruiz Rivas
"""

import webapp
import urllib.parse
import csv


class p1(webapp.webApp):
    # Diccionario cuya clave es la urlCompleta y el valor es el num asignado
    dicURLreal = {}
    # La clave es el numero asignado y el valor es la url completa
    dicNum = {}
    # La clave es la url completa y el valor la url corta. Para el GET /
    dic = {}

    def leerCSV(self):
        try:
            with open("URLcortas.csv", "r") as csvfile:
                lurlCortas_csv = csv.reader(csvfile, delimiter=",")
                for row in lurlCortas_csv:
                    self.dicURLreal[row[1]] = int(row[0])
                    self.dicNum[int(row[0])] = row[1]
                    self.dic[row[1]] = "http://localhost:1234/" + row[0]
                    print(",".join(row))
        except IOError:  # Para crear el fichero CSV la primera vez
            URLcortas = open("URLcortas.csv", "w")
            URLcortas.close()

    def parse(self, request):
        metodo = request.split(' ')[0]
        recurso = request.split(' ')[1]  # Cojo '/recurso'
        if (metodo == "GET"):
            cuerpo = None
        elif (metodo == "POST"):
            cuerpo = request.split('\r\n\r\n')[1]
            print(cuerpo)
        else:
            recurso = None
            cuerpo = None

        return (metodo, recurso, cuerpo)

    def process(self, parsedRequest):
        metodo, recurso, cuerpo = parsedRequest
        formulario = "<form method = 'POST' action=''>URL: "
        formulario += "<input type='text' name='url'><br>"
        formulario += "<input type='submit' value='Enviar'></form>"

        if self.dicNum == {} or self.dicURLreal == {}:
            self.leerCSV()

        if (metodo == "GET"):
            if recurso == "/":
                codigoHTTP = "200 OK"
                # Visualiza dic como una tabla en html
                htmldic = '<table><tr><th>'
                htmldic += '</th><th>'.join(self.dic.values()) + '</th></tr>'
                htmldic += '<tr><td>' + '</td><td>'.join(self.dic.keys())
                htmldic += '</td></tr></table>'
                # cuerpoHtml = formulario + str(self.dic)
                cuerpoHtml = formulario + htmldic
            else:
                if recurso[1:].isdigit():
                    recursoNum = int(recurso[1:])
                    if recursoNum in self.dicNum:
                        url = self.dicNum[recursoNum]
                        codigoHTTP = "303 SEE OTHER\r\nLocation: " + url
                        cuerpoHtml = str(cuerpo)
                    else:
                        codigoHTTP = "404 Not Found"
                        cuerpoHtml = "Recurso no disponible"
                else:
                    codigoHTTP = "404 Not Found"
                    cuerpoHtml = "Recurso no valido.No es numero"

        elif (metodo == "POST"):
            params = urllib.parse.parse_qs(cuerpo)
            print(params)
            if "url" in params:
                valorURL = params['url']
                url = "".join(valorURL)
                if url[0:4] != "http":  # Incluye http:// si es necesario
                    url = "http://" + url
                # Gestion de diccionarios con URL reales y acortadas
                if url in self.dicURLreal:
                    numSec = self.dicURLreal[url]
                    URLcorta = "http://localhost:1234/" + str(numSec)
                    URLlarga = '<a href="' + url + '">' + url + '</a><br>'
                    codigoHTTP = "200 OK"
                    cuerpoHtml = '<p>' + URLlarga + '<a href="' + url + '">'
                    cuerpoHtml += str(self.dic[url]) + '</a></p>'
                else:  # Determina URL acortada
                    numSec = len(self.dicURLreal)
                    self.dicURLreal[url] = numSec
                    self.dicNum[numSec] = url
                    # LLamada a CSV para escribir
                    with open("URLcortas.csv", "a") as csvfile:
                        elementoCSV = csv.writer(csvfile, delimiter=",")
                        elementoCSV.writerow([numSec, url])
                    URLcorta = "http://localhost:1234/" + str(numSec)
                    self.dic[url] = URLcorta
                    codigoHTTP = "200 OK"
                    cuerpoHtml = '<p><a href="' + self.dicNum[numSec] + '">'
                    cuerpoHtml += URLcorta + '</a></p>'
            else:
                codigoHTTP = "404 Not Found"
                cuerpoHtml = cuerpo + formulario

        else:
            codigoHTTP = "400 request not available"
            cuerpoHtml = "Peticion no permitida"

        return (codigoHTTP, "<html><body>" + cuerpoHtml + "</body></html>")


if __name__ == "__main__":

    testWebApp = p1("localhost", 1234)
