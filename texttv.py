#!/usr/bin/env python3
import readchar
import sys
import urllib.request
from TextTVParser import TextTVParser
from os import system, name

class colors:
    CYAN = '\033[36m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    BGBLUE = '\033[44m'
    set_color = {
        'C': lambda x: colors.CYAN + x + colors.ENDC,
        'Y': lambda x: colors.YELLOW + x + colors.ENDC,
        'W': lambda x: x,
        'G': lambda x: colors.GREEN + x + colors.ENDC,
        'DH': lambda x: colors.BOLD + x + colors.ENDC,
        'bgB': lambda x: colors.BGBLUE + x + colors.ENDC,
    }

class TextTV():
    def __init__(self):
        self.pages = {}
        self.input_buffer = ''
        self.current_page = 100

    def display(self, page=100):
        self.current_page = int(page)
        if self.current_page not in self.pages:
            html = self.get_html(page)
            parser = TextTVParser()
            lines = parser.parse(html)
            output = self.colorize(lines)
            self.pages[self.current_page] = output

        self.clear()
        print(self.pages[self.current_page])
        print(self.input_buffer)

    def read_input(self):
        while True:
            key = readchar.readkey()
            page = self.current_page
            if key == readchar.key.CTRL_C:
                break
            elif key == readchar.key.LEFT and self.current_page > 100:
                page = self.current_page - 1
                self.input_buffer = ''
            elif key == readchar.key.RIGHT and self.current_page < 999:
                page = self.current_page + 1
                self.input_buffer = ''
            elif key.isdigit():
                if len(self.input_buffer) == 0 and key != '0' or \
                   len(self.input_buffer) > 0:
                    self.input_buffer += key
                if len(self.input_buffer) == 3:
                    page = self.input_buffer
                    self.input_buffer = ''
            self.display(page)

    def get_html(self, page):
        url = 'http://www.svt.se/svttext/web/pages/%s.html' % self.current_page
        response = urllib.request.urlopen(url)
        html = response.read()
        html = html.decode('utf-8')
        return html

    @staticmethod
    def colorize(lines):
        output = ''
        for line in lines:
            text = line[0]
            for color in line[1].split():
                if color in colors.set_color:
                    text = colors.set_color[color](text)
            output += text
        return output

    @staticmethod
    def clear():
        if name == 'nt':
            _ = system('cls')
        else:
            _ = system('clear')

def print_usage():
    print('usage: texttv.py [page-index]')

if __name__ == '__main__':
    argc = len(sys.argv)
    texttv = TextTV()
    if (argc > 1):
        page = sys.argv[1]
        if page.isdigit() is False or int(page) not in range(100,999):
            print_usage()
            exit()
        texttv.display(page)
    else:
        texttv.display(100)
        texttv.read_input()
