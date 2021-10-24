#!/usr/bin/env python3

import argparse
import readchar
import urllib.request
import json
from os import system
from html.parser import HTMLParser

class TerminalUI:
    def __init__(self, handlers = {}):
        self.handlers = handlers
        self.input_buffer = ''

    def set_handlers(self, handlers):
        self.handlers = handlers

    def refresh(self, data, clear=True):
        if clear:
            self.clear()
        print(data)

    def read_input(self):
        key = readchar.readkey()
        if key == readchar.key.CTRL_C or key in 'qQ':
            self.handlers['exit']()
        elif key == readchar.key.LEFT:
            self.input_buffer = ''
            self.handlers['prev']()
        elif key == readchar.key.RIGHT:
            self.input_buffer = ''
            self.handlers['next']()
        elif key == readchar.key.BACKSPACE:
            self.input_buffer = self.input_buffer[:-1]
        elif key.isdigit():
            if len(self.input_buffer) == 0 and key != '0' or \
                len(self.input_buffer) > 0:
                self.input_buffer += key
            if len(self.input_buffer) == 3:
                self.handlers['new_page'](int(self.input_buffer))
                self.input_buffer = ''

    @staticmethod
    def clear():
        system('clear')


class TextTVParser(HTMLParser):
    def __init__(self):
        super(TextTVParser, self).__init__()
        self.save_data = False
        self.color_tag = ''
        self.data = []
        self.current_color = ''
        self.added_line = False

    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            self.save_data = True
        elif self.save_data is True and (tag == 'span' or tag == 'h1'):
            self.current_color = attrs[0][1]
            self.color_tag = tag

        if attrs[0][1] == 'added-line':
            self.save_data = False
            self.added_line = True
        elif self.added_line:
            self.save_data = True
            self.added_line = False

    def handle_endtag(self, tag):
        if self.color_tag == tag:
            self.current_color = ''
        if tag == 'div':
            self.save_data = False

    def handle_data(self, data):
        if self.save_data is True:
            self.data.append((data, self.current_color))

    def parse(self, html):
        self.feed(html)
        return self.data

    def error(self, message):
        print(message)


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
    def __init__(self, ui):
        self.ui = ui
        self.ui.set_handlers({
            'prev': self.prev,
            'next': self.next,
            'exit': self.exit,
            'new_page': self.show_page,
        })
        self.interactive = False
        self.pages = {}
        self.current_page = 100

    def prev(self):
        self.current_page = self.pages[self.current_page]['prev']
        self.ui.refresh(self.get_page(self.current_page))

    def next(self):
        self.current_page = self.pages[self.current_page]['next']
        self.ui.refresh(self.get_page(self.current_page))
        pass

    def exit(self):
        self.interactive = False

    def show_single_page(self, page):
        self.ui.refresh(self.get_page(page), clear=False)

    def show_page(self, page):
        self.current_page = page
        self.ui.refresh(self.get_page(self.current_page))

    def get_page(self, page):
        if page not in self.pages:
            self.pages[page] = {}
            html, prev, next = self.get_html_and_metadata(page)
            self.pages[page]['prev'] = prev
            self.pages[page]['next'] = next

            parser = TextTVParser()
            lines = parser.parse(html)
            output = self.colorize(lines)
            self.pages[page]['content'] = output

        return self.pages[page]['content']

    def run(self, page=100):
        self.interactive = True
        self.show_page(page)

        while self.interactive:
            self.ui.read_input()

    def get_html_and_metadata(self, page):
        url = 'http://api.texttv.nu/api/get/%s?app=texttv.py' % page
        http_response = urllib.request.urlopen(url)
        api_response = http_response.read()
        json_data = json.loads(api_response)
        html = json_data[0]['content'][0]
        next_page = int(json_data[0]['next_page'])
        prev_page = int(json_data[0]['prev_page'])
        return html, prev_page, next_page

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


def parse_args():
    parser = argparse.ArgumentParser()
    parser.description = """Terminal SVT Text TV viewer.\n
    The application may both show single pages or run in interactive mode where pages can be viewed
    using the directional keys or by entering new page numbers on the keyboard.
    Running the application without any arguments will start the application in interactive mode.
    """

    parser.add_argument("-i", "--interactive", help="run the application in interactive mode", action="store_true")
    parser.add_argument("page", type=int, help="the texttv page to show [100, 900]", nargs="?")
    args = parser.parse_args()

    # choices cant handle to many values so we check page manually
    if args.page is not None and args.page not in range(100, 901):
        parser.print_help()
        exit(1)

    return args

def cli():
    args = parse_args()
    ui = TerminalUI()
    texttv = TextTV(ui)

    if args.page is None:
        # Start with page 100 in interactive mode
        texttv.run(100)
    else:
        if args.interactive:
            texttv.run(args.page)
        else:
            texttv.show_single_page(args.page)


if __name__ == '__main__':
    cli()
