import random
from enum import Enum
from lib.roulette.bets import *
from lib.roulette.exceptions import *
from lib.roulette.player import RoulettePlayer

class RouletteField(object):
    def __init__(self, num, color):
        self.num = num
        self.color = color

    def __str__(self):
        return '{} - :{}_circle:'.format(self.num, self.color)

class Roulette(object):
    BETS = {
        'stra': StraightBet,
        'sp': SplitBet,
        'stre': StreetBet,
        'cor': CornerBet,
        'dou': DoubleStreetBet,
        't': TrioBet,
        'f': FirstFourBet,
        'l': LowHighBet,
        'r': RougeOuNoirBet,
        'p': PairOuImpair,
        'doz': DozenBet,
        'col': ColumnBet,
    }

    def __init__(self):
        self.bets = dict()
        self.__fields = [RouletteField(0, 'green')]
        for i in [*range(1,11), *range(19,29)]:
            self.__fields.append(RouletteField(i, 'red' if i%2 else 'black'))
        for i in [*range(11,19), *range(29,37)]:
            self.__fields.append(RouletteField(i, 'black' if i%2 else 'red'))
        self.__fields.sort(key=lambda f: f.num)

    def join(self, p):
        self.bets[p] = None

    def new_round(self):
        for p, b in self.bets.items():
            self.bets[p] = None

    def bet(self, p, cmd):
        ps = re.sub(r' +', ' ', cmd).split(' ')
        c = int(ps[0])
        if p.cookies - c < 0:
            raise InvalidBetException('Too little funds available!')
        if len(ps) < 3:
            raise IncompleteCommandException()
        b = list(filter(lambda x: ps[1].lower().startswith(x), Roulette.BETS))

        if not b:
            raise InvalidBetException()
        self._bet(p, Roulette.BETS[b[0]].parse(p, c, ' '.join(ps[2:])))

    def _bet(self, p, bet):
        if not p in self.bets.keys():
            raise InvalidPlayerException()
        if self.bets[p]:
            return
        self.bets[p] = bet
        p.cookies -= bet.cookies

    def start_round(self, debug=False):
        res = self.__fields[random.randint(0,len(self.__fields)-1)]
        diffs = []
        if debug:
            print('- Random field: ' + str(res))
        for p, b in self.bets.items():
            if not b:
                continue
            p.cookies += b.profit() if b.has_won(res) else 0
            diffs.append((p, (b.profit() if b.has_won(res) else 0) - b.cookies))
            if debug:
                print('  {} has {}won! (new balance: {} [+{}])'.format(p.name, '' if b.has_won(res) else 'not ', p.cookies, (b.profit() if b.has_won(res) else 0) - b.cookies))
        return (res, diffs)

if __name__ == '__main__':
    p = RoulettePlayer('David', 100)
    p2 = RoulettePlayer('Matthias', 100)

    r = Roulette()
    r.join(p)
    r.join(p2)
    
    try:
        while p.cookies > 0:
            r.new_round()
            r.bet(p, input('# '))
            r.start_round()
    except Exception as e:
        print(e)
        pass
    if p.cookies == 0:
        print('u suck! u lost! haha! ur m0m g4y!')

    # r.new_round()
    # r.bet(p, '100 straight 0')
    # r.bet(p2, '100 lowhigh low')
    # r.start_round()