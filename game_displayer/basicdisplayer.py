import pygame
from pygame import gfxdraw
from game_simulator import gameparams as gp

class GameWindow:
    def __init__(self, winWidth, winHeight, fps = 60, debug_surfs = []):
        self.height = winHeight
        self.width = winWidth

        self.clock = pygame.time.Clock()
        self.fps = fps

        self.debug_surfs = debug_surfs

        self.rip = False

        pygame.init()

        self.win = pygame.display.set_mode( (self.width, self.height ) )
        pygame.display.set_caption( "TEST DISPLAY" )

    def drawFrame(self, frame):
        self.win.fill( (0, 0, 0 ) )
        # draws background
        pygame.draw.rect(self.win, gp.bordercolour, (0, 0, gp.windowwidth, gp.windowheight))
        # draws ball area
        pygame.draw.rect(self.win, gp.pitchcolour, (gp.pitchcornerx, gp.pitchcornery, gp.pitchwidth, gp.pitchheight))
        #draws area behind goal
        pygame.draw.rect(self.win, gp.pitchcolour, (gp.pitchcornerx - 30, gp.goalcornery, 30, gp.goalsize))
        pygame.draw.rect(self.win, gp.pitchcolour, (gp.windowwidth - gp.pitchcornerx, gp.goalcornery, 30, gp.goalsize))

        # draws pitch borders
        pygame.draw.rect(self.win, gp.goallinecolour, (
        gp.pitchcornerx - gp.goallinethickness // 2, gp.pitchcornery - gp.goallinethickness // 2, gp.goallinethickness,
        gp.pitchheight + gp.goallinethickness))
        pygame.draw.rect(self.win, gp.goallinecolour, (
        gp.windowwidth - gp.pitchcornerx - gp.goallinethickness // 2, gp.pitchcornery - gp.goallinethickness // 2, gp.goallinethickness,
        gp.pitchheight + gp.goallinethickness))
        pygame.draw.rect(self.win, gp.goallinecolour, (
        gp.pitchcornerx - gp.goallinethickness // 2, gp.pitchcornery - gp.goallinethickness // 2, gp.pitchwidth + gp.goallinethickness,
        gp.goallinethickness))
        pygame.draw.rect(self.win, gp.goallinecolour, (
        gp.pitchcornerx - gp.goallinethickness // 2, gp.windowheight - gp.pitchcornery - gp.goallinethickness // 2,
        gp.pitchwidth + gp.goallinethickness, gp.goallinethickness))

        cnt = 0
        # draws goalposts
        for goalpost in gp.goalposts:
            cnt += 1
            pygame.gfxdraw.filled_circle(self.win, goalpost[0], goalpost[1], gp.goalpostradius, (0, 0, 0))
            pygame.gfxdraw.aacircle(self.win, goalpost[0], goalpost[1], gp.goalpostradius, (0, 0, 0))
            goalpostcol = (0, 0, 0)
            if cnt <= 2:
                goalpostcol = (200, 150, 150)
            else:
                goalpostcol = (150, 150, 200)
            pygame.gfxdraw.filled_circle(self.win, goalpost[0], goalpost[1], gp.goalpostradius-gp.goalpostborderthickness, goalpostcol)
            pygame.gfxdraw.aacircle(self.win, goalpost[0], goalpost[1], gp.goalpostradius-gp.goalpostborderthickness, goalpostcol)

        def drawPlayer(p, colour):
            if p.action.isKicking():
                pygame.gfxdraw.filled_circle(self.win, int(p.x), int(p.y),
                    gp.kickingcircleradius, gp.kickingcirclecolour)
                pygame.gfxdraw.aacircle(self.win, int(p.x), int(p.y),
                    gp.kickingcircleradius, gp.kickingcirclecolour)
            else:
                pygame.gfxdraw.filled_circle(self.win, int(p.x), int(p.y),
                    gp.kickingcircleradius, (0,0,0))
                pygame.gfxdraw.aacircle(self.win, int(p.x), int(p.y),
                    gp.kickingcircleradius, (0,0,0))

            pygame.gfxdraw.filled_circle(self.win, int(p.x), int(p.y),
                gp.playerradius-gp.kickingcirclethickness, colour)
            pygame.gfxdraw.aacircle(self.win, int(p.x), int(p.y),
                gp.playerradius-gp.kickingcirclethickness, colour)

        for p in frame.reds:
            drawPlayer(p, gp.redcolour)
        for p in frame.blues:
            drawPlayer(p, gp.bluecolour)

        for b in frame.balls:
            pygame.gfxdraw.filled_circle(self.win, int(b.x), int(b.y), gp.ballradius+2, (0, 0, 0))
            pygame.gfxdraw.aacircle(self.win, int(b.x), int(b.y), gp.ballradius+2, (0, 0, 0))
            pygame.gfxdraw.filled_circle(self.win, int(b.x), int(b.y), gp.ballradius, (255, 255, 255))
            pygame.gfxdraw.aacircle(self.win, int(b.x), int(b.y), gp.ballradius, (255, 255, 255))

        debug_pos = gp.windowwidth
        for s in self.debug_surfs:
            # Add the debug thing
            self.win.blit(s, (debug_pos, 0))
            debug_pos += s.get_width()

        # Display
        self.clock.tick(self.fps)
        pygame.display.update()


    def getInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.rip = True

    def isKeyPressed(self, key, is_int = False):
        # Checks whether a key is being pressed, input is a char or an int.
        pressed_keys = pygame.key.get_pressed()
        if is_int == False:
            if key == 'UP':
                return pressed_keys[273]
            elif key == 'RIGHT':
                return pressed_keys[275]
            elif key == 'DOWN':
                return pressed_keys[274]
            elif key == 'LEFT':
                return pressed_keys[276]
            elif key == 'LALT':
                return pressed_keys[308]
            elif key == 'RALT':
                return pressed_keys[307]
            elif key == 'LCTRL':
                return pressed_keys[306]
            elif key == 'RCTRL':
                return pressed_keys[305]
            elif key == 'LSHIFT':
                return pressed_keys[304]
            elif key == 'RSHIFT':
                return pressed_keys[303]
            else:
                return pressed_keys[ord(key)]
        else:
            return pressed_keys[key]

    def shutdown(self):
        pygame.quit()
