#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

"""
Aplicacion web simple para acortar URLs
Rosa Cristina Ruiz Rivas
Alumna de SAT
"""

import webapp
import urlparse


class p1(webapp.webApp):

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
        formulario += '<INPUT type="text" id="url"><BR>'
        formulario += '<INPUT type="submit" value="Send"></p></FORM>'

        if (peticion == "GET"):
            if recurso == "/":
                codigoHTTP = "200 OK"
                cuerpoHtml = str(dic) + formulario + str(cuerpo)
            else:
                recursoNum = int(recurso[1:])
                if recursoNum in dicNum:
                    url = dicNum[recursoNum]
                    codigoHTTP = "303 SEE OTHER\r\nLocation: " + url
                    cuerpoHtml = str(cuerpo)
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
                # if dicURLreal.has_key(url):
                if url in dicURLreal:
                    numSec = dicURLreal[url]
                    URLcorta = "http://localhost:1234/" + str(numSec)
                    URLlarga = '<a href="' + url + '">' + url + '</a>'
                    codigoHTTP = "200 OK"
                    cuerpoHtml = '<p>' + URLlarga + '<a href="' + url + '">'
                    cuerpoHtml += dic[url] + '</a></p>'
                else:  # Determina URL acortada
                    numSec = len(dicURLreal)
                    dicURLreal[url] = numSec
                    dicNum[numSec] = url
                    print dicURLreal
                    URLcorta = "http://localhost:1234/" + str(numSec)
                    dic[url] = URLcorta
                    codigoHTTP = "200 OK"
                    cuerpoHtml = '<p><a href="' + dicNum[numSec] + '">'
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
    # Diccionario cuya clave es la urlCompleta y el valor es el num asignado
    dicURLreal = {}
    # La clave es el numero asignado y el valor es la url completa
    dicNum = {}
    # La clave es la url completa y el valor la url corta. Para el GET
    dic = {}
    testWebApp = p1("localhost", 1234)
