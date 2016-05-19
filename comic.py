#!/usr/bin/python

import requests
from bs4 import BeautifulSoup
import simplejson as json
import webbrowser
import sys

URL = "http://www.commitstrip.com/en/?"
JSONFILE = './commitStrip.json'

# Helper functions to read and write json files
def load_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def write_json_file(jsonObj, filename):
    with open(filename, 'w') as f:
        json.dump(jsonObj, f, indent=4)


def get_strip(section):
    title = section.find('strong').text
    url = section.find('a').get('href')

    return {'title': title, 'url': url}


def store_data(soup):
    data = [get_strip(section) for section in soup.find_all('section')]
    write_json_file(data, JSONFILE)


def check_new(soup):
    
    titles = [title.text for title in soup.find_all('strong')]
    
    data = load_json(JSONFILE)
    old_titles = [comic['title'] for comic in data]

    if sorted(titles) == sorted(old_titles):
        return False
    
    return titles


def main():
    
    try:
        command = sys.argv[1]
        
        if command == '-c':
            response = requests.get(URL)
            soup = BeautifulSoup(response.text, 'lxml')
            
            new = check_new(soup)
            if new:
                store_data(soup)
                print("\n\tNew Commic: {0}".format(new[0]))
            else:
                print("\n\tNo New Comics, Use comic -t to list available comics\n")

        elif command == '-t':
            data = load_json(JSONFILE)
            titles = [comic['title'] for comic in data]
            
            print('')
            for i in xrange(len(titles)):
                print('\t' + str(i) + '.\t' + titles[i])
            print('')
        
        elif command == '-o':
            try:
                option = int(sys.argv[2])
                data = load_json(JSONFILE)

                links = [comic['url'] for comic in data]
                
                webbrowser.open(links[option])

            except IndexError:
                print("Comic Number missing")

    except IndexError:
        print("\n\tSimple script to check out commitStrip new comics\n\n\tAvailable Commmands:\n\n\t\t-c\t\t check new commics\n\t\t-t \t\t to list comics titles\n\t\t-o [number] \t to open comic link in browser\n")


if __name__  == '__main__':
    main()
