import re
from lib.roulette.exceptions import *

class RouletteBet(object):
    def __init__(self, player, cookies):
        self.player = player
        self.cookies = cookies

    def has_won(self, res):
        raise NotImplementedError()

    def profit(self):
        raise NotImplementedError()

    @classmethod
    def split_nums(cls, cmd):
        return [int(n) for n in re.sub(r' +', ' ', cmd.replace(',', ' ')).split(' ')]

    @classmethod
    def parse(cls, p, c, cmd):
        raise NotImplementedError()

# ================================================================================================================================================ #

class StraightBet(RouletteBet):
    def __init__(self, player, cookies, num):
        super().__init__(player, cookies)
        self.num = num

    def has_won(self, res):
        return res.num==self.num

    def profit(self):
        return 36*self.cookies

    @classmethod
    def parse(cls, p, c, cmd):
        try:
            return cls(p, c, int(cmd))
        except Exception:
            #agli
            raise InvalidBetException()
              
class SplitBet(RouletteBet):
    def __init__(self, player, cookies, split):
        """
            split ... (n, m) --> tuple of both numbers
        """
        super().__init__(player, cookies)
        split = sorted(split)
        if any(map(lambda x: x < 0, split)) or not ((split[0]==split[1]-1 and (split[0]-1)//3==(split[1]-1)//3) or split[0]==split[1]-3):
            raise InvalidBetException()
        self.split = split

    def has_won(self, res):
        return res.num in self.split

    def profit(self):
        return 18*self.cookies

    @classmethod
    def parse(cls, p, c, cmd):
        nums = cls.split_nums(cmd)
        if len(nums) < 2:
            raise IncompleteCommandException()
        return cls(p, c, tuple(nums))

class StreetBet(RouletteBet):
    def __init__(self, player, cookies, street):
        super().__init__(player, cookies)
        self.street = street//3*3+1

    def has_won(self, res):
        return res.num in range(self.street, self.street+3)

    def profit(self):
        return 12*self.cookies

    @classmethod
    def parse(cls, p, c, cmd):
        try:
            return cls(p, c, int(cmd))
        except Exception as e:
            #agli
            raise InvalidBetException()

class CornerBet(RouletteBet):
    def __init__(self, player, cookies, corner):
        """
            vierer Tupel
        """
        super().__init__(player, cookies)
        corner = sorted(corner)
        if not all((corner[0]==corner[1]-1,corner[2]==corner[3]-1)) or corner[0] != corner[2]-3:
            raise InvalidBetException()
        self.corner = corner

    def has_won(self, res):
        return res.num in self.corner

    def profit(self):
        return 9*self.cookies

    @classmethod
    def parse(cls, p, c, cmd):
        nums = cls.split_nums(cmd)
        if len(nums) < 4:
            raise IncompleteCommandException()
        return cls(p, c, tuple(nums))

class DoubleStreetBet(RouletteBet):
    def __init__(self, player, cookies, street):
        super().__init__(player, cookies)
        self.street = street//3*3+1

    def has_won(self, res):
        return res.num in range(self.street, self.street+6)

    def profit(self):
        return 12*self.cookies

    @classmethod
    def parse(cls, p, c, cmd):
        try:
            return cls(p, c, int(cmd))
        except Exception:
            #agli
            raise InvalidBetException()
    
class TrioBet(RouletteBet): 
    def __init__(self, player, cookies, nums):
        """
        012 || 023
        """
        super().__init__(player, cookies)
        self.nums = nums
        #Ich bin nochmal dumm... xD
        if (nums[0]==0 and nums[1]==1 and nums[2]==2) or (nums[0]==0 and nums[1]==2 and nums[2]==3):
            raise InvalidBetException()

    def has_won(self, res):
        return res.num in nums

    def profit(self):
        return 12*self.cookies

    @classmethod
    def parse(cls, p, c, cmd):
        nums = cls.split_nums(cmd)
        if len(nums) < 3:
            raise IncompleteCommandException()
        return cls(p, c, tuple(nums))

class FirstFourBet(RouletteBet):
    def __init__(self, player, cookies):
        """
        0123
        """
        super().__init__(player, cookies)

    def has_won(self, res):
        return res.num in range(4)

    def profit(self):
        return 9*self.cookies

    @classmethod
    def parse(cls, p, c, cmd):
        nums = cls.split_nums(cmd)
        if len(nums) < 4:
            raise IncompleteCommandException()
        return cls(p, c, tuple(nums))

class LowHighBet(RouletteBet):
    def __init__(self, player, cookies, lowhigh):
        super().__init__(player, cookies)
        if not lowhigh.lower() in ('low','high'):
            raise InvalidBetException()
        self.lowhigh = {'low':range(1,18),'high':range(19,36)}[lowhigh.lower()]
    
    def has_won(self, res):
        return res.num in self.lowhigh
    
    def profit(self):
        return 2*self.cookies

    @classmethod
    def parse(cls, p, c, cmd):
        if not cmd.strip():
            raise InvalidBetException()
        return cls(p, c, cmd)

class RougeOuNoirBet(RouletteBet):
    def __init__(self, player, cookies, color):
        super().__init__(player, cookies)
        if not color.lower() in ('red','black',):
            raise InvalidBetException('Unknown color "{}"!'.format(color))
        self.color = color
    
    def has_won(self, res):
        return res.color==self.color

    def profit(self):
        return 2*self.cookies

    @classmethod
    def parse(cls, p, c, cmd):
        if not cmd.strip():
            raise IncompleteCommandException()
        return RougeOuNoirBet(p, c, cmd)
        
class PairOuImpair(RouletteBet):
    def __init__(self, player, cookies, even_odd):
        super().__init__(player, cookies)
        if even_odd.lower() not in ('odd','even'):
            raise InvalidBetException()
        self.even_odd = {'even':0,'odd':1}[even_odd.lower()]
    
    def has_won(self, res):
        return res.num%2 == self.even_odd

    def profit(self):
        return 2*self.cookies

    @classmethod
    def parse(cls, p, c, cmd):
        even_odd = cls.split_nums(cmd)
        if not cmd.strip():
            raise IncompleteCommandException()
        return cls(p, c, even_odd)

class DozenBet(RouletteBet):
    def __init__(self, player, cookies, dozen):
        """
    	    dozen ... (n, m) --> tuplay of range numbers
        """
        super().__init__(player, cookies)
        self.dozen = dozen
        if not (dozen[0]%12==1 and dozen[1]%12==0 and dozen[1]-dozen[0]==11):
            raise InvalidBetException()
    
    def has_won(self, res):
        return res.num in range(self.dozen[0], self.dozen[1]+1)
    
    def profit(self):
        return 3*self.cookies

    @classmethod
    def parse(cls, p, c, cmd):
        nums = cls.split_nums(cmd)
        if len(nums) < 2:
            raise IncompleteCommandException()
        return cls(p, c, tuple(nums))   

class ColumnBet(RouletteBet):
    def __init__(self, player, cookies, column):
        """
            keine Idee ...
        """
        super().__init__(player, cookies)
        if column not in range(1,4):
            raise InvalidBetException()
        self.column = column-1

    def has_won(self, res):
        return (res.num-1)%3 == self.column

    def profit(self):
        return 3*self.cookies

    @classmethod
    def parse(cls, p, c, cmd):
        try:
            return cls(p, c, int(cmd))
        except Exception:
            #sägli
            raise InvalidBetException()