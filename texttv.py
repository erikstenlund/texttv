#!/usr/bin/env python3

import sys
import os
import json

if sys.version_info.major >= 3:
    import urllib.request
else:
    from datetime import datetime
    now = datetime.now()
    print('It is %d! Use python 3' % now.year)
    exit()

from html.parser import HTMLParser

class colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

class TextTVParser(HTMLParser):
    def __init__(self):
        super(TextTVParser, self).__init__()
        self.save_data = False
        self.data = [] 
        self.current_color = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'pre':
            self.save_data = True
            self.data.append(('=' * 41 + '\n', 'W'))
        elif self.save_data is True and tag == 'span':
            self.current_color = attrs[0][1]

    def handle_endtag(self, tag):
        if tag == 'pre':
            self.save_data = False
            self.data.append(('=' * 41 + '\n','W'))

    def handle_data(self, data):
        if self.save_data is True:
            self.data.append((data, self.current_color))

    def get_data(self):
        return self.data

def print_usage():
    print('usage: texttv.py [page-index]')
    exit()

def private_page(page):
    conf = {}
    if os.path.isfile('.texttvconf'):
        with open('.texttvconf') as conffile:
            conf = json.loads(conffile.read())
    else:
        print_usage()

    if int(page) not in range(conf['min_index'], conf['max_index']):
        print_usage()
                
    url = 'http://' + conf['url'] + '/' + page
    headers = { }
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req)
    html = response.read()
    #ToDo parsing printing etc
    print(html)


def main(page):
    url = 'http://www.svt.se/svttext/web/pages/%s.html' % page
    response = urllib.request.urlopen(url)

    html = response.read()
    lines = scrape_html(html)
    print_lines(lines)

def scrape_html(html):
    html = html.decode('utf-8')
    parser = TextTVParser()
    parser.feed(html)
    return parser.get_data()
 
def print_lines(lines):
    set_color = {
        'C': lambda x: colors.BOLD + x + colors.ENDC,
        'Y': lambda x: colors.YELLOW + x + colors.ENDC,
        'W': lambda x: x,
        'G': lambda x: colors.GREEN + x + colors.ENDC,
    }
    output = ''
    for line in lines:
        if line[1] in set_color:
            output += set_color[line[1]](line[0])
        else:
            output += line[0]

    print(output)

if __name__ == '__main__':
    page = '100'
    argc = len(sys.argv)
    if (argc > 1):
        page = sys.argv[1]
    if page.isdigit() is False:
        print_usage()
    elif int(page) in range(100,900):
        main(page)
    else:
        private_page(page)

