import os
import sys
import tkinter
import urllib
from urllib.request import urlopen
import dropbox


import requests
from bs4 import BeautifulSoup
import weasyprint
import Dropbox
import OptionWindows
import zeregina4


def check_validity(my_url):
    if my_url=='':
        return False
    try:
        urlopen(my_url)
        print("Valid URL")
        return True
    except IOError:
        print ("Invalid URL")
        return False

def html2pdf(url,gorde,opcion):
    if check_validity(url):
        pdfname=url.replace('http:://','D')
        pdfname = pdfname.replace('https://', 'D')
        pdfname = pdfname.replace('/', '-')
        if opcion=='Local':
            if gorde=='' or not os.path.exists(gorde):
                gorde='./'
            if not gorde.endswith('/'):
                gorde=gorde+'/'
            doc_pdf = weasyprint.HTML(url).write_pdf(gorde+pdfname)
        else:
            lista=[]
            lista.append(url)
            doc_pdf = weasyprint.HTML(url).write_pdf(gorde + pdfname)
            filePath = './' + pdfname

            OptionWindows.DropBox(filePath,url)
            # Handle errors while calling os.remove()
            try:
                os.remove(filePath)
            except:
                print("Error while deleting file ", filePath)

    else:
        OptionWindows.error()


def is_downloadable(url):
    """
    Does the url contain a downloadable resource
    """
    print(url)
    try:
        h = requests.head(url, allow_redirects=True)
        print('lo hace')
        header = h.headers
        content_type = header.get('content-type')
        if 'text' in content_type.lower():
            return False
        if 'html' in content_type.lower():
            return False
        if url.contains('.pdf') or url.contains('.docx') or url.contains('.txt') or url.contains('.zip') or url.contains('.pdf'):
            return True
        else:
            return True
    except:
        return False

def getAllLinks(url):
    lista=[]
    datos = urllib.request.urlopen(url).read().decode()
    soup = BeautifulSoup(datos)
    tags = soup('a')
    for tag in tags:
            if is_downloadable(tag.get('href')):
                if check_validity(url):
                    print(tag.get('href'))
                    lista.append(tag.get('href'))
                    print(lista)

    return lista

def get_url_paths(url, ext='', params={}):
    parent=[]
    try:
         response = requests.get(url, params=params)
         if response.ok:
             response_text = response.text
         else:
             return response.raise_for_status()
         soup = BeautifulSoup(response_text, 'html.parser')
         parent = [url + node.get('href') for node in soup.find_all('a') if node.get('href').endswith(ext)]
         return parent
    except:
        return parent



def download(url):
    pdfname = url.replace('http:://', '')
    pdfname = pdfname.replace('https://', '')
    pdfname = pdfname.replace('/', '-')
    r = requests.get(url, allow_redirects=True)
    open(pdfname, 'wb').write(r.content)

def dropbox(lista):

 #   r = requests.get(url, allow_redirects=True)
  #  open(pdfname, 'wb').write(r.content)
    OptionWindows.DropBoxLista(lista)