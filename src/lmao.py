import util

def pack((W,H), unpacked, packed, active, area, on_update):
    
    # Base Cases:
    if not unpacked:
        on_update(active, packed, None, None, unpacked, "Nothing left to pack. Success.")
        return True, packed
    if area > W*H:
        on_update(active, packed, None, None, unpacked, "... no room left in the bin (" + str(area) + " / " + str(W*H) + ")" )
        return False, []
    if not active:
        on_update(active, packed, None, None, unpacked, "No active points remaining. Backtracking." )
        return False, []
                
    # LMAO will be consumed. 
    lmao = active.pop().project(packed)
    
    if W == lmao.x or H == lmao.y or any( r.covers(lmao.pos()) for r in packed ):
        return pack((W,H), unpacked, packed, active, area, on_update)

    # Try every rectangle in this spot (or leave it unused).
    for rectangle in unpacked.keys():

        rect = util.Rectangle(rectangle, lmao.pos()) 

        on_update(active, packed, lmao, rect, unpacked, "Trying rectangle " + str(rect) + " at position " + str(lmao))
       
        if(rect.right() > W or rect.top() > H):
            on_update(active, packed, lmao, rect, unpacked, "... but it's out of bounds")
        elif any([rect.intersect(x) for x in packed if x.is_real]):
            on_update(active, packed, lmao, rect, unpacked, "... but it intersects with another rectangle")
        else:
            on_update(active, packed, lmao, rect, unpacked, "... it fits")

            newactive = active.copy()
            newactive.push(util.ActivePoint(rect.left(), rect.top(), axis=0))
            newactive.push(util.ActivePoint(rect.right(), rect.bottom(), axis=1))
            
            allfit, packed2 = pack((W,H), unpacked.decr(rectangle), packed + [ rect ], newactive, area, on_update)
            
            if allfit:
                return True, packed2
    
    nextsmallest = active.peek().x if active else W
    dummy_h = 1
    dummy_w = max(1, nextsmallest - lmao.x)
    rect = util.Rectangle((dummy_w, dummy_h), lmao.pos(), is_real=False)

    allfit, packed2 = pack((W,H), unpacked, packed + [ rect ], active.copy(), area + rect.area(), on_update)
            
    if allfit:
        return True, packed2
    else:
        on_update(active, packed, lmao, rect, unpacked, "... Backtracking.")
        return False, []