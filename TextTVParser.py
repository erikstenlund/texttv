from html.parser import HTMLParser


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
