import benchmarks
import animation
import animation2
import util
import lmao
import tsbp


def LMAO((W,H), unpacked, anim = True):
    active = util.heapset([util.ActivePoint(0,0,axis=None)])
    packed = []
    area = sum([w*h*unpacked[(w,h)] for w,h in unpacked])
    window = animation.LMAO_Window((W,H))
    
    if anim:
        on_update = lambda active, packed, lmao, rect, unpacked, msg: window.update_on_next_click(active, packed, lmao, rect, unpacked, msg)
    else:
        on_update = lambda active, packed, lmao, rect, unpacked, msg: 0
    
    ret = lmao.pack((W,H), unpacked, packed, active, area, on_update)
    window.quit()
    return ret

        
def TSBP((W,H), unpacked, anim1=True, anim2=True):
    hist = util.histogram((W,H))
    packed = []
    area =  sum([w*h*unpacked[(w,h)] for w,h in unpacked])
    window = animation.TSBP_Window((W,H))

    if anim1:
        on_update1 = lambda hist, item, unpacked, msg: window.update_on_next_click((hist, item), [], [], None, None, unpacked, msg)
    else:
        on_update1 = lambda hist, item, unpacked, msg: 0
    
    partialpack, state = tsbp.pack1((W,H), unpacked, packed, hist, area, on_update1)
    while partialpack:
        active = util.heapset([util.ActivePoint(0,0,axis=None)])
        packed = []
        #area = sum([w*h*unpacked[(w,h)] for w,h in unpacked])
        
        if anim2:
            on_update2 = lambda active, packed, lmao, rect, unpacked, msg: window.update_on_next_click((state[3],None), active, packed, lmao, rect, unpacked, msg)
        else:
            on_update2 = lambda active, packed, lmao, rect, unpacked, msg: 0
        
        branch = tsbp.pack2((W,H), partialpack, packed, active, on_update2)
        if branch:
            window.quit()
            return branch
        partialpack, state = tsbp.pack1(*state, skipFirst=True)
    window.quit()
    return False    


