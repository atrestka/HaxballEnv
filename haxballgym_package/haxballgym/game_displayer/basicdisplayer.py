import pygame
from pygame import gfxdraw
from haxballgym.config import config


class GameWindow:
    def __init__(self, winWidth, winHeight, fps=60, debug_surfs=[]):
        self.height = winHeight
        self.width = winWidth

        self.clock = pygame.time.Clock()
        self.fps = fps

        self.debug_surfs = debug_surfs

        self.rip = False

        pygame.init()

        self.win = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("TEST DISPLAY")

    def drawFrame(self, frame, hold=0.):
        self.win.fill((0, 0, 0))
        # draws background
        pygame.draw.rect(self.win, config.BORDER_COLOUR, (0, 0, config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
        # draws ball area
        pygame.draw.rect(self.win, config.PITCH_COLOUR, (config.PITCH_CORNER_X, config.PITCH_CORNER_Y,
                                                         config.PITCH_WIDTH, config.PITCH_HEIGHT))
        # draws area behind goal
        pygame.draw.rect(self.win, config.PITCH_COLOUR, (config.PITCH_CORNER_X - 30, config.GOAL_CORNER_Y, 30,
                                                         config.GOAL_SIZE))
        pygame.draw.rect(self.win, config.PITCH_COLOUR, (config.WINDOW_WIDTH - config.PITCH_CORNER_X,
                                                         config.GOAL_CORNER_Y, 30, config.GOAL_SIZE))

        # draws pitch borders
        pygame.draw.rect(
            self.win, config.GOAL_LINE_COLOUR, (
                config.PITCH_CORNER_X - config.GOAL_LINE_THICKNESS // 2,
                config.PITCH_CORNER_Y - config.GOAL_LINE_THICKNESS // 2,
                config.GOAL_LINE_THICKNESS,
                config.PITCH_HEIGHT + config.GOAL_LINE_THICKNESS
            )
        )
        pygame.draw.rect(
            self.win, config.GOAL_LINE_COLOUR, (
                config.WINDOW_WIDTH - config.PITCH_CORNER_X - config.GOAL_LINE_THICKNESS // 2,
                config.PITCH_CORNER_Y - config.GOAL_LINE_THICKNESS // 2, config.GOAL_LINE_THICKNESS,
                config.PITCH_HEIGHT + config.GOAL_LINE_THICKNESS
            )
        )
        pygame.draw.rect(
            self.win, config.GOAL_LINE_COLOUR, (
                config.PITCH_CORNER_X - config.GOAL_LINE_THICKNESS // 2,
                config.PITCH_CORNER_Y - config.GOAL_LINE_THICKNESS // 2,
                config.PITCH_WIDTH + config.GOAL_LINE_THICKNESS,
                config.GOAL_LINE_THICKNESS
            )
        )
        pygame.draw.rect(
            self.win, config.GOAL_LINE_COLOUR, (
                config.PITCH_CORNER_X - config.GOAL_LINE_THICKNESS // 2,
                config.WINDOW_HEIGHT - config.PITCH_CORNER_Y - config.GOAL_LINE_THICKNESS // 2,
                config.PITCH_WIDTH + config.GOAL_LINE_THICKNESS, config.GOAL_LINE_THICKNESS
            )
        )

        def drawGoalpost(goalpost, colour):
            gfxdraw.filled_circle(self.win, goalpost.x, goalpost.y, config.GOALPOST_RADIUS, (0, 0, 0))
            gfxdraw.aacircle(self.win, goalpost.x, goalpost.y, config.GOALPOST_RADIUS, (0, 0, 0))
            gfxdraw.filled_circle(self.win, goalpost.x, goalpost.y,
                                  config.GOALPOST_RADIUS - config.GOALPOST_BORDER_THICKNESS, colour)
            gfxdraw.aacircle(self.win, goalpost.x, goalpost.y,
                             config.GOALPOST_RADIUS - config.GOALPOST_BORDER_THICKNESS, colour)

        def drawPlayer(p, colour):
            if p.action.isKicking():
                gfxdraw.filled_circle(self.win, int(p.x), int(p.y),
                                      config.KICKING_CIRCLE_RADIUS, config.KICKING_CIRCLE_COLOUR)
                gfxdraw.aacircle(self.win, int(p.x), int(p.y),
                                 config.KICKING_CIRCLE_RADIUS, config.KICKING_CIRCLE_COLOUR)
            else:
                gfxdraw.filled_circle(self.win, int(p.x), int(p.y),
                                      config.KICKING_CIRCLE_RADIUS, (0, 0, 0))
                gfxdraw.aacircle(self.win, int(p.x), int(p.y),
                                 config.KICKING_CIRCLE_RADIUS, (0, 0, 0))

            gfxdraw.filled_circle(self.win, int(p.x), int(p.y),
                                  config.PLAYER_RADIUS - config.KICKING_CIRCLE_THICKNESS, colour)
            gfxdraw.aacircle(self.win, int(p.x), int(p.y),
                             config.PLAYER_RADIUS - config.KICKING_CIRCLE_THICKNESS, colour)

        def drawBox(b, colour, outer_colour=(0, 0, 0)):
            rect_outer = pygame.Rect(b.x,
                                     b.y,
                                     b.width,
                                     b.height)
            rect = pygame.Rect(b.x + config.GOALPOST_BORDER_THICKNESS,
                               b.y + config.GOALPOST_BORDER_THICKNESS,
                               b.width - 2 * config.GOALPOST_BORDER_THICKNESS,
                               b.height - 2 * config.GOALPOST_BORDER_THICKNESS)
            gfxdraw.box(self.win, rect_outer, outer_colour)
            gfxdraw.box(self.win, rect, colour)

        for b in frame.other_rectangles:
            if not b.active:
                drawBox(b, config.OTHER_RECT_COLOUR, config.GOAL_LINE_COLOUR)
            else:
                drawBox(b, config.OTHER_RECT_ACTIVE_COLOUR, config.GOAL_LINE_COLOUR)         
        for p in frame.players:
            drawPlayer(p, config.TEAM_COLOURS[p.team])
        for g in frame.goalposts:
            drawGoalpost(g, average_tuples(config.GOALPOST_COLOUR, config.TEAM_COLOURS[g.team]))
        for b in frame.rectangles:
            drawBox(b, config.WALL_COLOUR)

        for b in frame.balls:
            gfxdraw.filled_circle(self.win, int(b.x), int(b.y), config.BALL_RADIUS + 2, (0, 0, 0))
            gfxdraw.aacircle(self.win, int(b.x), int(b.y), config.BALL_RADIUS + 2, (0, 0, 0))
            gfxdraw.filled_circle(self.win, int(b.x), int(b.y), config.BALL_RADIUS, (255, 255, 255))
            gfxdraw.aacircle(self.win, int(b.x), int(b.y), config.BALL_RADIUS, (255, 255, 255))

        debug_pos = config.WINDOW_WIDTH
        for s in self.debug_surfs:
            # Add the debug thing
            self.win.blit(s, (debug_pos, 0))
            debug_pos += s.get_width()

        # Display
        self.clock.tick(self.fps)
        self.clock.tick(hold)
        pygame.display.update()

    def getInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.rip = True

    def isKeyPressed(self, key, is_int=False):
        # Checks whether a key is being pressed, input is a char or an int.
        pressed_keys = pygame.key.get_pressed()
        if not is_int:
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


def average_tuples(t1, t2):
    return ((t1[0] + t2[0]) // 2, (t1[1] + t2[1]) // 2, (t1[2] + t2[2]) // 2)