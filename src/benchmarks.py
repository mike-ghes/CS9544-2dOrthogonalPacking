import util
from random import *
    
def quilt(i):
    if i == 14:
        return (i,i), util.counter({(6,6):1, (4,4):3, (3,3):4, (5,5):3})
    if i == 15:
        return (i,i), util.counter({(8,8):1, (7,7):1, (5,5):1, (4,4):3, (3,3):3})
    if i == 16:
        return (i,i), util.counter({(7,7):1, (6,6):2, (5,5):3, (4,4):2, (3,3):3})
    if i == 17:
        return (i,i), util.counter({(9,9):1, (8,8):2, (5,5):1, (4,4):2, (3,3):1, (2,2):3})
    if i == 18:
        return (i,i), util.counter({(7,7):3, (6,6):1, (5,5):3, (4,4):4})
    if i == 19:
        return (i,i), util.counter({(7,7):3, (6,6):3, (5,5):3, (3,3):3})
    if i == 20:
        return (i,i), util.counter({(8,8):1, (7,7):3, (6,6):3, (5,5):2, (3,3):3})
    if i == 21:
        return (i,i), util.counter({(9,9):1, (8,8):2, (7,7):1, (6,6):3, (5,5):1, (4,4):3})
    if i == 22:
        return (i,i), util.counter({(12,12):1, (10,10):2, (7,7):1, (5,5):2, (4,4):1, (3,3):2, (2,2):1})
    if i == 23:
        return (i,i), util.counter({(12,12):1, (11,11):2, (7,7):1, (5,5):2, (4,4):1, (3,3):2, (2,2):2})
    if i == 24:
        return (i,i), util.counter({(10,10):2, (9,9):1, (7,7):3, (5,5):3, (4,4):4})
    if i == 25:
        return (i,i), util.counter({(9,9):3, (8,8):3, (7,7):2, (5,5):3, (3,3):1})
    if i == 26:
        return (i,i), util.counter({(10,10):1, (9,9):3, (8,8):3, (7,7):1, (5,5):3, (3,3):1})
    if i == 27:
        return (i,i), util.counter({(11,11):2, (9,9):1, (8,8):3, (7,7):3, (5,5):2, (3,3):1})
    if i == 28:
        return (i,i), util.counter({(12,12):1, (11,11):1, (9,9):2, (8,8):3, (7,7):3, (5,5):2, (3,3):1})
    if i == 29:
        return (i,i), util.counter({(15,15):1, (14,14):2, (8,8):1, (7,7):2, (5,5):1, (3,3):3})
    if i == 30:
        return (i,i), util.counter({(11,11):3, (10,10):1, (9,9):3, (8,8):2, (4,4):4})
    if i == 31:
        return (i,i), util.counter({(16,16):1, (12,12):1, (10,10):2, (9,9):2, (6,6):2, (5,5):4})
    if i == 32:
        return (i,i), util.counter({(20,20):1, (12,12):3, (8,8):1, (7,7):1, (5,5):2, (3,3):2})
    if i == 33:
        return (i,i), util.counter({(20,20):1, (13,13):2, (9,9):1, (7,7):2, (6,6):2, (5,5):2, (4,4):3})
    if i == 34:
        return (i,i), util.counter({(17,17):3, (9,9):1, (8,8):2, (5,5):1, (4,4):2, (3,3):1, (2,2):3})
    if i == 35:
        return (i,i), util.counter({(15,15):1, (13,13):1, (12,12):2, (10,10):3, (8,8):2, (7,7):1, (4,4):3})
    if i == 36:
        return (i,i), util.counter({(13,13):2, (15,15):1, (8,8):4, (9,9):1, (11,11):2, (12,12):1})
    raise Exception("I don't know how to build that quilt.")
  
def random(e,n, (W,H)=(20,20)):
    a = {}

    for i in range(int((1. - e)*W*H)):
        r = randint(0,n-1)
        if r in a:
            a[r] += 1
        else:
            a[r] = 1
    
    c = util.counter({})       
    for area in a.values():
        r = [1,1]
        d = 2
        while d*d <= area:
            while (area % d) == 0:
                area /= d
                r[randint(0,1)] *= d
            d+= 1
        if area > 1:
            r[randint(0,1)] *= area
        c = c.incr((r[0],r[1]))
        
    return (W,H), c
    
def random2(e,n, (W,H)=(20,20)):
    while True:
        x = random(e,n)
        if all(a[1]<H and a[0]<W for a in x[1].keys()):
            return x   
        
def fromfile(filename):
    counter = util.counter()
    with open(filename) as f:
        for r in csv.reader(f):
            counter =  counter.incr((r[0], r[1]))
    return counter

def timer(f, args):
    t0 = time.clock()
    ret = f(*args)
    t1 = time.clock()
    return t1-t0, ret