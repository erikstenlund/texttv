#!/usr/bin/env python3
import readchar
import sys
if sys.version_info.major >= 3:
    import urllib.request
else:
    from datetime import datetime
    now = datetime.now()
    print('It is %d! Use python 3' % now.year)
    exit()

from html.parser import HTMLParser
from os import system, name

class colors:
    CYAN = '\033[36m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    BGBLUE = '\033[44m'


class TextTVParser(HTMLParser):
    def __init__(self):
        super(TextTVParser, self).__init__()
        self.save_data = False
        self.color_tag = ''
        self.data = []
        self.current_color = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'pre':
            self.save_data = True
            #self.data.append(('=' * 41 + '\n', 'W'))
        elif self.save_data is True and tag == 'span':
            self.current_color = attrs[0][1]
            self.color_tag = tag

    def handle_endtag(self, tag):
        if self.color_tag == tag:
            self.current_color = ''
        if tag == 'pre':
            self.save_data = False
            #self.data.append(('=' * 41 + '\n','W'))

    def handle_data(self, data):
        if self.save_data is True:
            self.data.append((data, self.current_color))

    def get_data(self):
        return self.data

def print_usage():
    print('usage: texttv.py [page-index]')

def main(page):
    url = 'http://www.svt.se/svttext/web/pages/%s.html' % page
    response = urllib.request.urlopen(url)

    html = response.read()
    html = html.decode('utf-8')

    parser = TextTVParser()
    parser.feed(html)
    lines = parser.get_data()


    set_color = {
        'C': lambda x: colors.CYAN + x + colors.ENDC,
        'Y': lambda x: colors.YELLOW + x + colors.ENDC,
        'W': lambda x: x,
        'G': lambda x: colors.GREEN + x + colors.ENDC,
        'DH': lambda x: colors.BOLD + x + colors.ENDC,
        'bgB': lambda x: colors.BGBLUE + x + colors.ENDC,
    }
    output = ''
    for line in lines:
        text = line[0]
        for color in line[1].split():
            if color in set_color:
                text = set_color[color](text)
        output += text

    clear()
    print(output)

def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

def read_input(page):
    while True:
        key = readchar.readkey()
        if key == readchar.key.CTRL_C:
            break
        elif key == readchar.key.LEFT and int(page) > 100:
            page = str(int(page) - 1)
            main(page)
        elif key == readchar.key.RIGHT and int(page) < 999:
            page = str(int(page) + 1)
            main(page)
        elif key.isdigit():
            if len(page) > 2:
                page = ''
            page += key
            print(key, end='', flush=True)
            if len(page) == 3 and int(page) > 100:
                main(page)

if __name__ == '__main__':
    argc = len(sys.argv)
    if (argc > 1):
        page = sys.argv[1]
        if page.isdigit() is False or int(page) not in range(100,999):
            print_usage()
            exit()
        main(page)
    else:
        page = '100'
        main(page)
        read_input(page)
