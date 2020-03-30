class Player(object):
    def __init__(self, name, cookies):
        self.name = name
        self.cookies = cookies

    def __str__(self):
        return '{} ({}c)'.format(self.name, self.cookies)