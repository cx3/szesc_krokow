import re, xlwt, json, os
from urllib.parse import urlparse
from urllib.request import urlopen
from bs4 import BeautifulSoup, NavigableString  # pip install beautifulsoup4
import requests


try:
    folder_gmin = 'folder-gmin'
    os.mkdir(folder_gmin)
except FileExistsError:
    pass


def read_cities():
    '''
    Reads line to line a cities to iterate over them in defs below
    :return:
    '''
    cities_file = open('miasta_dolnoslaskie.txt', 'r')
    lines = cities_file.readlines()
    cities_file.close()

    for line in lines:
        print('> ' + line[:-1])  # do not use '\n' so trim it


def lower_silesia():  # deprecated by now but now unusable in near future - DO NOT DEL THIS CODE!
    domain = 'https://6krokow.pl'
    base_href = 'https://6krokow.pl/urzedy-panstwowe/lista/02/'

    html = requests.get(base_href).content
    soup = BeautifulSoup(html, 'html.parser')

    divs = soup.find_all('div')

    links_to_parse = []

    os.mkdir(folder_gmin)

    for div in divs:
        if 'class' in div.attrs:
            if 'powiat' in div.get('class'):
                children = div.findChildren()
                for child in children:
                    if 'href' in child.attrs:
                        links_to_parse.append(domain + child.get('href'))

    links_file = open('linki-urzedow.txt', 'w')
    for i in range(len(links_to_parse)):
        links_file.write(links_to_parse[i]+'\n')
    links_file.close()


def extract_contact_to_screwed_html(url):

    if not url.endswith('/'):
        url += '/'
    city_name = str(url.split('/')[-2:-1]).replace('[\'', '').replace('\']', '')
    # upper line: gets last word from link but it still is a list so we del odd chars
    # making it a one word that is city name

    html = requests.get(url).content
    soup = BeautifulSoup(html, 'html.parser')

    lines = soup.prettify().split('\n')  # make html code more readable

    output_file_path = './'+folder_gmin+'/'+city_name+'.txt'
    file = open(output_file_path, 'w')
    for line in lines:
        file.write(line+'\n')
    file.close()
    return output_file_path


def parse_screwed_to_xls(filepath):
    file = open(filepath)
    lines = file.readline()

    a = 0
    for line in lines:
        a += 1
        if a > 400:
            print(str(a)+' -> '+line)
        if a > 700:
            break

    return True


def folder_gmin_printable():
    from os import listdir
    from os.path import isfile, join

    files = [f for f in listdir(folder_gmin) if isfile(join(folder_gmin, f))]

    for next_path in files:
        file = open(join(folder_gmin, next_path), 'r')
        file_lines = file.readlines()

        loc = 406
        for next_line in file_lines:
            loc += 1
            if loc > 400:
                print(str(loc)+' -> '+next_line.lstrip())
            if loc > 700:
                return True





def from_links_to_xls():
    lines = open('linki-urzedow.txt', 'r').readlines()

    a = 0
    for line in lines:
        a += 1
        if a > 10:
            break
        extract_contact_to_screwed_html(line[:-1])



folder_gmin_printable()

#from_links_to_xls()

#lower_silesia()
