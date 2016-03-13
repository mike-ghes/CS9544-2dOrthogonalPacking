import heapq


"""
Active point class. Contains a point and axis.
"""
class ActivePoint(object):
    # ctor
    def __init__(self, x, y, axis):
        self.x = x
        self.y = y
        self.axis = axis
    
    # representative
    def __repr__(self):
        return ("vert" if self.axis == 1 else "horz" if self.axis == 0 else "none") + str((self.x,self.y))    
    
    # comparator            
    def __cmp__(self, other):
        if type(self) != type(other):
            return cmp(type(self), type(other))
        return cmp((self.axis, self.x, self.y), (other.axis, other.x, other.y))
    
    # just the position    
    def pos(self):
        return self.x, self.y
        
    #If the active point is followed, from it's position, along it's axis, returns the location which intersects with a rectangle.
    def hits(self, rectangle):        
        if self.axis == 0 and rectangle.y <= self.y and self.y < rectangle.y + rectangle.h and rectangle.x+rectangle.w <= self.x:
            return rectangle.x + rectangle.w
        elif self.axis == 1 and rectangle.x <= self.x and self.x < rectangle.x + rectangle.w and rectangle.y+rectangle.h <= self.y:
            return rectangle.y + rectangle.h
        else:
            return 0
    
    # project a point along it's axis onto a set of rectangles. Used for finding LMAO.    
    def project(self, packed):

        if self.axis == None:
            return self
            
        z = 0 
        for rect in packed:
            z = max(z, self.hits(rect))   
            
        if self.axis == 0:
            return ActivePoint(min(z, self.x), self.y, self.axis)
        elif self.axis == 1:
            return ActivePoint(self.x, min(z, self.y), self.axis)
            
        
            
        
"""
Class representing a placed item with position: (X,Y), size: (W,H) and a flag for whether it's a dummy.
"""
class Rectangle(object):
    #ctor
    def __init__(self, (W,H), (X,Y), is_real=True):
        self.w = W
        self.h = H
        self.x = X
        self.y = Y
        self.is_real = is_real
    
    #to String        
    def __str__(self):
        return ("real" if self.is_real else "dummy") + str(self.size()) +"@" + str(self.pos())    
    def __repr__(self):
        return str(self)
            
    # do two rectangles intersect?        
    def intersect(self, rect):
        return (self.is_real and
                 rect.is_real and
                (self.x < rect.x + rect.w) and
                (rect.x < self.x + self.w) and
                (self.y + self.h > rect.y) and
                (rect.y + rect.h > self.y))

    # y coordinate of top edge
    def top(self):
        return self.y + self.h
        
    # y coordinate of bottom edge
    def bottom(self):
        return self.y
        
    # x coordinate of right edge
    def right(self):
        return self.x + self.w
        
    # x coordinate of right edge
    def left(self):
        return self.x

    # (x,y) coordinates of specified corner (deprecated)
    def corner(self, s = "topright"):
        return self.x + (self.w if "right" in s else 0) , self.y + (self.h if "top" in s else 0)
    
    # does a rectangle cover a point?
    def covers(self, (x, y)):
        return self.x <= x and x < self.x + self.w and self.y <= y and y < self.y + self.h
        
    # size of the rectangle
    def size(self):
        return self.w, self.h
        
    # position of the rectangle
    def pos(self):
        return self.x, self.y
        
    # area of the rectangle
    def area(self):
        return self.w * self.h


"""
Heap data structure which only allows one of each item.
"""
class heapset(list):
    # ctor
    def __init__(self, q=None):
        if q == None:
            q = []
        self.q = q
        
    # to string
    def __repr__(self):
        return repr(self.q)
        
    # to boolean
    def __nonzero__(self):
        return bool(self.q) 
        
    # "in"
    def __contains__(self, item):
        return item in self.q
    
    # iterator over items
    def __iter__(self):
        return iter(self.q)
            
    # deep copy of heap
    def copy(self):
        return heapset(self.q[:])
        
    # add item to heap
    def push(self, x):
        if x not in self.q:
           heapq.heappush(self.q, x)
           return True
        return False
           
    # remove smallest item from heap
    def pop(self):
        return heapq.heappop(self.q)
        
    # peek at smallest item in heap
    def peek(self):
        return self.q[0]
            
"""
Used for unpacked points
"""
class counter(dict):
    # increment a key
    def incr(self, x):
        c = counter(self.copy())
        if x in c:
            c[x] += 1
        else:
            c[x] = 1
        return c

    # decrement a key
    def decr(self, x):
        c = counter(self.copy())
        c[x] -= 1
        if c[x] <= 0:
            del c[x]
        return c

"""      
Used for TSBP outer tree.
"""
class histogram(object):
    # ctor
    def __init__(self, (w,h), a = None):
        if a == None:
            a = [(0,0)]
            
        self.w = w
        self.h = h
        self.a = a
    
    # to string
    def __repr__(self):
        return str((self.w,self.h)) + str(self.a)
    
    # to boolean
    def __nonzero__(self):
        return bool(self.a)  
    
    # will an item fit?
    def fits(self, (w,h)):
        return (self.a and self.a[0][1] + h <= self.h and self.a[0][0] + w <= self.w)
    
    def dummy_area(self):
        if not self.a:
            return 0
        elif len(self.a)==1:
            return (self.w -self.a[0][0])*(self.h-self.a[0][1])
        else:
            return (self.a[1][0] - self.a[0][0]) * (self.h-self.a[0][1])
            
       
    # add a filler item 
    def add_dummy(self):
        if self.a:
            return histogram((self.w, self.h), self.a[1:])
        else:
            raise Exception("already full")
        
    # add a real item
    def add(self, (w,h)):
        if self.fits((w,h)):
            a2 = list(self.a)
            i = 0
            while w != 0:
                a2[i]= ( a2[i][0], a2[i][1] + h)
                if len(a2) > i+1:
                    if w >= a2[i+1][0] - a2[i][0]:
                        w -= (a2[i+1][0] - a2[i][0])
                    else:
                        a2.insert(i+1,[a2[i][0]+w, a2[i][1]-h])
                        w = 0
                else:
                    a2 += [(a2[i][0]+w, 0)]
                    w = 0
                if a2[i][1] == self.h:
                    del a2[i]
                else:
                    i+=1
            return histogram((self.w, self.h), a2)
        else:
            raise Exception("Couldn't add. Make sure it fits")