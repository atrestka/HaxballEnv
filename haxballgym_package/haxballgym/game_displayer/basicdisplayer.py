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

    def drawFrame(self, frame):
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

        cnt = 0
        # draws GOALPOSTS
        for goalpost in config.GOALPOSTS:
            cnt += 1
            gfxdraw.filled_circle(self.win, goalpost[0], goalpost[1], config.GOALPOST_RADIUS, (0, 0, 0))
            gfxdraw.aacircle(self.win, goalpost[0], goalpost[1], config.GOALPOST_RADIUS, (0, 0, 0))
            goalpostcol = (0, 0, 0)
            if cnt <= 2:
                goalpostcol = (200, 150, 150)
            else:
                goalpostcol = (150, 150, 200)
            gfxdraw.filled_circle(self.win, goalpost[0], goalpost[1],
                                  config.GOALPOST_RADIUS - config.GOALPOST_BORDER_THICKNESS, goalpostcol)
            gfxdraw.aacircle(self.win, goalpost[0], goalpost[1],
                             config.GOALPOST_RADIUS - config.GOALPOST_BORDER_THICKNESS, goalpostcol)

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

        for p in frame.reds:
            drawPlayer(p, config.RED_COLOUR)
        for p in frame.blues:
            drawPlayer(p, config.BLUE_COLOUR)

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
