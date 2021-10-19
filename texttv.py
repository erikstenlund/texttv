#!/usr/bin/env python3
import readchar
import sys
import urllib.request
import json
from TextTVParser import TextTVParser
from os import system, name


class Colors:
    CYAN = '\033[36m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    BGBLUE = '\033[44m'
    set_color = {
        'C': lambda x: Colors.CYAN + x + Colors.ENDC,
        'Y': lambda x: Colors.YELLOW + x + Colors.ENDC,
        'W': lambda x: x,
        'G': lambda x: Colors.GREEN + x + Colors.ENDC,
        'DH': lambda x: Colors.BOLD + x + Colors.ENDC,
        'bgB': lambda x: Colors.BGBLUE + x + Colors.ENDC,
    }


class TextTV:
    def __init__(self):
        self.pages = {}
        self.input_buffer = ''
        self.current_page = 100

    def display(self, tv_page=100):
        self.current_page = int(tv_page)
        if self.current_page not in self.pages:
            self.pages[self.current_page] = {}
            html = self.get_html()
            parser = TextTVParser()
            lines = parser.parse(html)
            output = self.colorize(lines)
            self.pages[self.current_page]['content'] = output

        self.clear()
        print(self.pages[self.current_page]['content'])
        print(self.input_buffer)

    def read_input(self):
        while True:
            key = readchar.readkey()
            tv_page = self.current_page
            if key == readchar.key.CTRL_C:
                break
            elif key == readchar.key.LEFT:
                tv_page = self.pages[self.current_page]['prev']
                self.input_buffer = ''
            elif key == readchar.key.RIGHT:
                tv_page = self.pages[self.current_page]['next']
                self.input_buffer = ''
            elif key == readchar.key.BACKSPACE:
                self.input_buffer = self.input_buffer[:-1]
            elif key.isdigit():
                if len(self.input_buffer) == 0 and key != '0' or \
                   len(self.input_buffer) > 0:
                    self.input_buffer += key
                if len(self.input_buffer) == 3:
                    tv_page = self.input_buffer
                    self.input_buffer = ''
            self.display(tv_page)

    def get_html(self,):
        url = 'http://api.texttv.nu/api/get/%s?app=Ejdamm/texttv' % self.current_page
        http_response = urllib.request.urlopen(url)
        api_response = http_response.read()
        json_data = json.loads(api_response)
        html = json_data[0]['content'][0]
        self.pages[self.current_page]['next'] = int(json_data[0]['next_page'])
        self.pages[self.current_page]['prev'] = int(json_data[0]['prev_page'])
        return html

    @staticmethod
    def colorize(lines):
        output = ''
        for line in lines:
            text = line[0]
            for color in line[1].split():
                if color in Colors.set_color:
                    text = Colors.set_color[color](text)
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
    if argc > 1:
        page = sys.argv[1]
        if page.isdigit() is False or int(page) not in range(100, 999):
            print_usage()
            exit()
        texttv.display(page)
    else:
        texttv.display(100)
        texttv.read_input()
