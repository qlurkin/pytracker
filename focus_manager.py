import pygame
from typing import Optional
from util import add

FOCUS_CORNER_SIZE = 7
FOCUS_CORNER_WIDTH = 2
FOCUS_CORNER_COLOR = (255, 255, 0)
FOCUS_PADDING = 2


def draw_focus(screen: pygame.Surface, rect: pygame.Rect):
    topleft = add(rect.topleft, (-FOCUS_PADDING, -FOCUS_PADDING))
    topright = add(rect.topright, (FOCUS_PADDING, -FOCUS_PADDING))
    bottomleft = add(rect.bottomleft, (-FOCUS_PADDING, FOCUS_PADDING))
    bottomright = add(rect.bottomright, (FOCUS_PADDING, FOCUS_PADDING))
    pygame.draw.line(
        screen,
        FOCUS_CORNER_COLOR,
        topleft,
        add(topleft, (FOCUS_CORNER_SIZE, 0)),
        FOCUS_CORNER_WIDTH,
    )

    pygame.draw.line(
        screen,
        FOCUS_CORNER_COLOR,
        topleft,
        add(topleft, (0, FOCUS_CORNER_SIZE)),
        FOCUS_CORNER_WIDTH,
    )

    pygame.draw.line(
        screen,
        FOCUS_CORNER_COLOR,
        topright,
        add(topright, (-FOCUS_CORNER_SIZE, 0)),
        FOCUS_CORNER_WIDTH,
    )

    pygame.draw.line(
        screen,
        FOCUS_CORNER_COLOR,
        topright,
        add(topright, (0, FOCUS_CORNER_SIZE)),
        FOCUS_CORNER_WIDTH,
    )

    pygame.draw.line(
        screen,
        FOCUS_CORNER_COLOR,
        bottomleft,
        add(bottomleft, (FOCUS_CORNER_SIZE, 0)),
        FOCUS_CORNER_WIDTH,
    )

    pygame.draw.line(
        screen,
        FOCUS_CORNER_COLOR,
        bottomleft,
        add(bottomleft, (0, -FOCUS_CORNER_SIZE)),
        FOCUS_CORNER_WIDTH,
    )

    pygame.draw.line(
        screen,
        FOCUS_CORNER_COLOR,
        bottomright,
        add(bottomright, (-FOCUS_CORNER_SIZE, 0)),
        FOCUS_CORNER_WIDTH,
    )

    pygame.draw.line(
        screen,
        FOCUS_CORNER_COLOR,
        bottomright,
        add(bottomright, (0, -FOCUS_CORNER_SIZE)),
        FOCUS_CORNER_WIDTH,
    )


class FocusManager:
    def __init__(self):
        self.__index = 0
        self.__focused = 0
        self.__rects: list[pygame.Rect] = []

    def begin_frame(self):
        self.__index = 0

    def __call__(self, rect: pygame.Rect):
        if self.__index >= len(self.__rects):
            self.__rects.append(rect)
        self.__rects[self.__index] = rect
        res = self.__index == self.__focused
        self.__index += 1
        return res

    def search(self, dist_fn) -> bool:
        next = self.__focused
        best = float("inf")
        cur = self.get_focused_rect()
        if cur is None:
            return False
        for i, rect in enumerate(self.__rects):
            dist = dist_fn(cur, rect)
            if dist < best:
                best = dist
                next = i
        if next == self.__focused:
            return False
        self.__focused = next
        return True

    def up(self) -> bool:
        def dist(f: pygame.Rect, t: pygame.Rect):
            xt, yt = t.center
            xf, yf = f.center
            if yt < yf:
                return 2 * abs(xt - xf) + abs(yt - yf)
            return float("inf")

        return self.search(dist)

    def down(self) -> bool:
        def dist(f: pygame.Rect, t: pygame.Rect):
            xt, yt = t.center
            xf, yf = f.center
            if yt > yf:
                return 2 * abs(xt - xf) + abs(yt - yf)
            return float("inf")

        return self.search(dist)

    def right(self) -> bool:
        def dist(f: pygame.Rect, t: pygame.Rect):
            xt, yt = t.center
            xf, yf = f.center
            if xt > xf:
                return abs(xt - xf) + 2 * abs(yt - yf)
            return float("inf")

        return self.search(dist)

    def left(self) -> bool:
        def dist(f: pygame.Rect, t: pygame.Rect):
            xt, yt = t.center
            xf, yf = f.center
            if xt < xf:
                return abs(xt - xf) + 2 * abs(yt - yf)
            return float("inf")

        return self.search(dist)

    def get_focused_rect(self) -> Optional[pygame.Rect]:
        if len(self.__rects) == 0:
            return None
        return self.__rects[self.__focused]
