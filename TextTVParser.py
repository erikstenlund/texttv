from html.parser import HTMLParser

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
        elif self.save_data is True and tag == 'span':
            self.current_color = attrs[0][1]
            self.color_tag = tag

    def handle_endtag(self, tag):
        if self.color_tag == tag:
            self.current_color = ''
        if tag == 'pre':
            self.save_data = False

    def handle_data(self, data):
        if self.save_data is True:
            self.data.append((data, self.current_color))

    def parse(self, html):
        self.feed(html)
        return self.data