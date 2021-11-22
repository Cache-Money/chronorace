class HTTPRequest:
    def __init__(self, file, replacements=[], secure=True):
        protocol = 'http'
        if secure:
            protocol += 's'
        self.raw_request = open(file, "r").read()
        self.perform_replacements(replacements)
        self.method = None
        self.path = None
        self.headers = {}
        self.cookies = None
        self.body = None
        self.parse_request()
        self.protocol = protocol

    def parse_request(self):
        lines = self.raw_request.split('\n')

        line_number = 1
        pre_body = 0
        for line in lines:
            line = line.strip()
            if line_number == 1:
                space = line.index(' ')
                self.method = line[0:space]
                self.path = line[space + 1: line.rindex(' ')]
            elif line == '' and pre_body == 0:
                pre_body += 1
            elif pre_body == 0:
                if 'Cookie:' in line and line.index('Cookie:') == 0:
                    self.cookies = line[7:].strip()
                key, val = line.split(':', 1)
                if key != 'Content-Length':
                    self.headers[key.strip()] = val.strip()

            if (pre_body > 0 and line != '') or pre_body > 1:  # in body
                pre_body += 1
                if self.body is None:
                    self.body = line
                else:
                    self.body += '\n' + line
            line_number += 1

    def get_method(self):
        return self.method

    def get_headers(self, with_cookies=True):
        if not with_cookies:
            new_arr = self.headers.copy()
            new_arr.pop('Cookie')
            return new_arr

        return self.headers

    def get_cookies(self, split=False):
        if split:
            return self.cookies.split(';')

        return self.cookies

    def get_path(self):
        return self.path

    def get_protocol(self):
        return self.protocol

    def get_body(self):
        return self.body

    def get_full_url(self):
        return '{}://{}{}'.format(self.get_protocol(), self.get_headers().get('Host'), self.get_path())

    def perform_replacements(self, replacements):
        if len(replacements) > 0 and not isinstance(replacements[0], list):
            replacements = [replacements]

        for replacement in replacements:
            self.raw_request = self.raw_request.replace(replacement[0], replacement[1])
