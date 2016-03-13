# pygame!

import pygame, sys
from pygame.locals import * 

c_black  = pygame.Color(  0,   0,   0)
c_white  = pygame.Color(255, 255, 255)
c_grey   = pygame.Color(196, 196, 196)
c_orange = pygame.Color(  0, 196, 196)
c_green  = pygame.Color( 64, 255,  64)
c_teal   = pygame.Color(255, 128,   0)

c_background = c_white        
c_binBorder  = c_grey

c_currentPt  = c_orange
c_point      = c_teal

c_inactive   = c_grey
c_rectangle  = c_teal
c_currentRect= c_orange
c_text       = c_black         

class LMAO_Window(object):
    def __init__(self, (W,H)):
        self.windowx = 1280
        self.windowy = 800
        self.size = 675
        self.border = 5
        self.offsetx = 25
        self.offsety = 25
        self.w = W
        self.h = H
        self.divider = 50
        
        pygame.init()  
        self.scale = self.size/max(W,H)      
        self.font = pygame.font.SysFont("segoeui", 24)
        self.window = pygame.display.set_mode((self.windowx, self.windowy))
        
    def quit(self):
        pygame.quit()        

    def draw_point(self, pt, colour = c_currentPt):                                  
            pygame.draw.rect(self.window, colour, ( self.offsetx+self.border + (pt.x*self.scale), 
                                                    self.windowy-(self.offsety+self.border) + (pt.y*self.scale), 5,-5))   
        
    def draw_rect(self, rect, colour = c_rectangle):
        pygame.draw.rect(self.window, colour, (  self.offsetx+2*self.border + (rect.x * self.scale), 
                                                 self.windowy-(self.offsety+2*self.border + (rect.y * self.scale)), 
                                                 (rect.w * self.scale) - self.border, 
                                                 -((rect.h * self.scale) - self.border)))
                                                 
    def draw_unpacked(self, (w,h), x, y, num, colour = c_inactive):
        pygame.draw.rect(self.window, colour, ( self.offsetx + self.scale*self.w + self.divider + x,
                                                self.border + y,
                                                w * self.scale,
                                                h * self.scale))
        label = self.font.render(str(num)+ "x "+str((w,h)), 1, c_background)
        self.window.blit(label, (self.offsetx + self.scale*self.w + self.divider +x +5, 
                                self.border + y))
    
    
    def draw_bin(self):
        pygame.draw.rect(self.window, c_binBorder,  (self.offsetx,                     self.windowy-self.offsety, 
                                                     self.w*self.scale+3*self.border,  -self.h*self.scale-3*self.border) )
        
        pygame.draw.rect(self.window, c_background, (self.offsetx+self.border,         self.windowy-(self.offsety+self.border), 
                                                     self.w*self.scale+self.border,    -self.h*self.scale-self.border) )
    
    def update(self, active, packed, lmao, rect, unpacked, message = ""):
        # Clear screen, draw new bin.
        self.window.fill(c_background)
        self.draw_bin()
        
        # render text
        label = self.font.render(message, 1, c_text)
        self.window.blit(label, (10, 10))
        
        # Draw active points
        for pt in active:
            self.draw_point(pt, c_point)
        
        if lmao != None:    
            self.draw_point(lmao ,c_currentPt)

        # Draw rectangles
        for r in packed:
            if r.is_real:
                self.draw_rect(r, c_rectangle)
            else:    
                self.draw_rect(r, c_inactive)
                
        if rect == None: 
            pass
        elif rect.is_real:        
            self.draw_rect(rect, c_currentRect)
        else:
            self.draw_rect(rect, c_inactive)
        
        x,y,nextx = 0,0,0 
        stable_order = unpacked.keys()
        stable_order.sort()    
        for r in stable_order:
            if y + r[1] * self.scale > self.size+self.offsety:
                y = 0
                x = nextx *self.scale + self.border
            
            self.draw_unpacked(r, x, y, unpacked[r], c_currentRect if rect is not None and r == rect.size() else c_inactive)
            
            y += r[1] * self.scale + self.border
            nextx = max(nextx, x+r[0])
        
        pygame.display.update()
        return


    def update_on_next_click(self, active, packed, lmao, rect, unpacked, message):
        while True: 
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.quit()
                elif event.type == MOUSEBUTTONDOWN:    
                    self.update(active, packed, lmao, rect, unpacked, message)
                    return
                    
                    
class TSBP_Window(object):
    def __init__(self, (W,H)):
        self.windowx = 1280
        self.windowy = 800
        self.size = 325
        self.border = 5
        self.offsetx = 25
        self.offsety = 25
        self.w = W
        self.h = H
        self.divider = 50
        
        pygame.init()
        
        self.scale = self.size/max(W,H)      
        self.offsety2 = self.offsety+ self.h*self.scale +self.divider

        self.font = pygame.font.SysFont("segoeui", 24)
        self.window = pygame.display.set_mode((self.windowx, self.windowy))
        
    def quit(self):
        pygame.quit()        

    def draw_point(self, pt, colour = c_currentPt):                                  
            pygame.draw.rect(self.window, colour, ( self.offsetx+self.border + (pt.x*self.scale), 
                                                    self.windowy-(self.offsety+self.border) + (pt.y*self.scale), 5,-5))   
        
    def draw_rect(self, rect, colour = c_rectangle):
        pygame.draw.rect(self.window, colour, (  self.offsetx+2*self.border + (rect.x * self.scale), 
                                                 self.windowy-(self.offsety+2*self.border + (rect.y * self.scale)), 
                                                 (rect.w * self.scale) - self.border, 
                                                 -((rect.h * self.scale) - self.border)))
                                                 
    def draw_unpacked(self, (w,h), x, y, num, colour = c_inactive):
        pygame.draw.rect(self.window, colour, ( self.offsetx + self.scale*self.w + self.divider + x,
                                                self.border + y,
                                                w * self.scale,
                                                h * self.scale))
        label = self.font.render(str(num)+ "x "+str((w,h)), 1, c_background)
        self.window.blit(label, (self.offsetx + self.scale*self.w + self.divider +x +5, 
                                self.border + y))
    
    
    def draw_bins(self):
        pygame.draw.rect(self.window, c_binBorder,  (self.offsetx,                     self.windowy-self.offsety, 
                                                     self.w*self.scale+3*self.border,  -self.h*self.scale-3*self.border) )
        
        pygame.draw.rect(self.window, c_background, (self.offsetx+self.border,         self.windowy-(self.offsety+self.border), 
                                                     self.w*self.scale+self.border,    -self.h*self.scale-self.border) )
    
        pygame.draw.rect(self.window, c_binBorder,  (self.offsetx,                     self.windowy-self.offsety2, 
                                                     self.w*self.scale+3*self.border,  -self.h*self.scale-3*self.border) )
        
        pygame.draw.rect(self.window, c_background, (self.offsetx+self.border,         self.windowy-(self.offsety2+self.border), 
                                                     self.w*self.scale+self.border,    -self.h*self.scale-self.border) )
    
    
    def draw_hist(self, hist, item):
        x1 = 0
        h = hist.h
        for x2,h1 in hist.a:
            if x2 == 0:
                h= h1
                continue
            pygame.draw.rect(self.window, c_inactive, ( self.offsetx + 2*self.border + (x1 * self.scale), 
                                                        self.windowy-(self.offsety2+2*self.border ), 
                                                        ((x2-x1) * self.scale) - self.border, 
                                                        -((h * self.scale) - self.border)))
            x1 = x2
            h = h1

    
    def update(self, (hist, item), active, packed, lmao, rect, unpacked, message = ""):
        # Clear screen, draw new bin.
        self.window.fill(c_background)
        self.draw_bins()
        
        # render text
        label = self.font.render(message, 1, c_text)
        self.window.blit(label, (10, 10))
        
        self.draw_hist(hist, item)
        
        # Draw active points
        for pt in active:
            self.draw_point(pt, c_point)
        
        if lmao != None:    
            self.draw_point(lmao ,c_currentPt)

        # Draw rectangles
        for r in packed:
            if r.is_real:
                self.draw_rect(r, c_rectangle)
            else:    
                self.draw_rect(r, c_inactive)
                
        if rect == None: 
            pass
        elif rect.is_real:        
            self.draw_rect(rect, c_currentRect)
        else:
            self.draw_rect(rect, c_inactive)
        
        x,y,nextx = 0,0,0 
        stable_order = unpacked.keys()
        stable_order.sort()   
        for r in stable_order:
            if y + r[1] * self.scale > self.size+self.offsety:
                y = 0
                x = nextx *self.scale + self.border
            
            self.draw_unpacked(r, x, y, unpacked[r], c_currentRect if r == item or rect is not None and r == rect.size() else c_inactive)
            
            y += r[1] * self.scale + self.border
            nextx = max(nextx, x+r[0])
        
        pygame.display.update()
        return


    def update_on_next_click(self, (hist, item), active, packed, lmao, rect, unpacked, message):
        while True: 
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.quit()
                elif event.type == MOUSEBUTTONDOWN:    
                    self.update((hist,item), active, packed, lmao, rect, unpacked, message)
                    return