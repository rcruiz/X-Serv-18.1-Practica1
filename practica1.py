#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

"""
Aplicacion web simple para acortar URLs
Rosa Cristina Ruiz Rivas
"""

import webapp
import urlparse
import csv


class p1(webapp.webApp):
    # Diccionario cuya clave es la urlCompleta y el valor es el num asignado
    dicURLreal = {}
    # La clave es el numero asignado y el valor es la url completa
    dicNum = {}
    # La clave es la url completa y el valor la url corta. Para el GET
    dic = {}

    def leerCSV(self):
        try:
            with open("URLcortas.csv", "r") as csvfile:
                lurlCortas_csv = csv.reader(csvfile, delimiter=" ")
                for row in lurlCortas_csv:  # Puntaje = numero de URLcorta
                    self.dicURLreal[row[0]] = int(row[1])
                    self.dicNum[int(row[1])] = row[0]
                    self.dic[row[0]] = "http://localhost:1234/" + row[1]
                    print " ".join(row)
        except IOError:  # Para crear el fichero CSV la primera vez 
            URLcortas = open("URLcortas.csv","w")
            URLcortas.close()

    def parse(self, request):
        peticion = request.split(' ')[0]
        print "Recibido: " + peticion
        recurso = request.split(' ')[1]  # Cojo '/recurso'
        print "Recurso solicitado: " + recurso

        if (peticion == "GET"):
            cuerpo = None

        elif (peticion == "POST"):
            cuerpo = request.split('\r\n\r\n')[1]
            print cuerpo
        else:
            recurso = None
            cuerpo = None

        return (peticion, recurso, cuerpo)

    def process(self, parsedRequest):
        peticion = parsedRequest[0]
        recurso = parsedRequest[1]
        cuerpo = parsedRequest[2]
        formulario = '<FORM action="" method="post"><p>'
        formulario += '<LABEL for="URL">URL: </LABEL>'
        formulario += '<INPUT type="text" name="url"><BR>'
        formulario += '<INPUT type="submit" value="Send"></p></FORM>'

        if self.dicNum == {} or self.dicURLreal == {}:
            self.leerCSV()

        if (peticion == "GET"):
            if recurso == "/":
                codigoHTTP = "200 OK"
                cuerpoHtml = formulario + str(cuerpo) + str(self.dic)
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
                    cuerpoHtml = "Recurso no disponible"

        elif (peticion == "POST"):
            params = urlparse.parse_qs(cuerpo)
            print params
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
                        elementoCSV = csv.writer(csvfile, delimiter=" ")
                        elementoCSV.writerow([url, numSec])           
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

        return (codigoHTTP, "<HTML> <HEAD></HEAD> <BODY>" +
                cuerpoHtml + "</BODY></HTML>")


if __name__ == "__main__":

    testWebApp = p1("localhost", 1234)
