import util
import animation

def pack1((W,H), unpacked, packed, hist, area, on_update, skipFirst=False):
    #base cases
    if area > W*H:
        on_update(hist, None, unpacked,"... no room left in the bin (" + str(area) + " / " + str(W*H) + ")" )
        return False
    if not unpacked and not skipFirst:
        return packed, ((W,H), unpacked, packed, hist, area, on_update)  
    if not hist:
        return False

    for rect in unpacked.keys() + [None]:
        on_update(hist, rect, unpacked, "Trying rectangle " + str(rect) + " at " + str(hist.a[0][0]) )
        if rect == None:
            on_update(hist, rect, unpacked, "Inserting dummy")
            branch = pack1((W,H), unpacked, packed + [(None, hist.a[0][0])] , hist.add_dummy(), area + hist.dummy_area(), on_update)
        elif hist.a[0][0] + rect[0] > hist.w:
            on_update(hist, rect, unpacked, "Item is too wide and will never fit.")
            return False  
        elif hist.fits(rect):
            on_update(hist, rect, unpacked, "Inserting item")
            branch = pack1((W,H), unpacked.decr(rect), packed + [(rect, hist.a[0][0])], hist.add(rect), area, on_update) 
        else:
            branch = False   
        
        if branch:
            return branch
    return False

def pack2( (W,H), partialpack, packed, active, on_update ):
    if not partialpack:
        on_update(active, packed, None, None, {}, "Nothing left to pack. Success.")
        return True, packed
        
    if not active:
        #print "No active points left"
        return False, []
    
    lmao = active.pop()
        
    activerects = [ item for item in partialpack if item[1] == lmao.x ]
    inactiverects = [ item for item in partialpack if item[1] != lmao.x ]
    
    c = util.counter()
    for item,x in activerects:
        if item != None:
            c = c.incr(item)
    
    if not activerects or W == lmao.x or H == lmao.y or any( r.covers(lmao.pos()) for r in packed ):
        return pack2((W,H), partialpack, packed, active, on_update)
    
    for i, (rectangle, _) in enumerate(activerects):
        if rectangle != None:
            rect = util.Rectangle(rectangle, lmao.pos())
        else:
            rect = util.Rectangle((1,1), lmao.pos(), is_real=False)
            
        on_update(active, packed, lmao, rect, c, "Trying rectangle " + str(rect) + " at position " + str(lmao))
        
        if(rect.right() > W or rect.top() > H):
            on_update(active, packed, lmao, rect, c, "... but it's out of bounds")
        elif any([rect.intersect(x) for x in packed if x.is_real]):
            on_update(active, packed, lmao, rect, c, "... but it intersects with another rectangle")
        else:
            on_update(active, packed, lmao, rect, c, "... it fits")

            newactive = active.copy()
            newactive.push(util.ActivePoint(rect.left(), rect.top(), axis=0))
            newactive.push(util.ActivePoint(rect.right(), rect.bottom(), axis=1))
            
            allfit, packed2 = pack2((W,H), activerects[:i]+activerects[i+1:]+inactiverects, packed + [ rect ], newactive, on_update)
            if allfit:
                return True, packed2
    nextsmallest = active.peek().x if active else W
    dummy_h = 1
    dummy_w = max(1, nextsmallest - lmao.x)
    rect = util.Rectangle((dummy_w, dummy_h), lmao.pos(), is_real=False)

    allfit, packed2 = pack2((W,H), partialpack, packed + [ rect ], active.copy(), on_update)
            
    if allfit:
        return True, packed2
    else:
        on_update(active, packed, lmao, rect, c, "... Backtracking.")
        return False, []
    #window.update_on_next_click(active, packed, lmao, rect, unpacked, "... Backtracking.")
    return False, []
