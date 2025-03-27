from pygame.ftfont import Font
import pygame.ftfont
import pygame

from util import add


pygame.ftfont.init()
# FONT = Font("ProFontIIxNerdFont-Regular.ttf", size=20)
# FONT = Font("TerminusTTF-4.49.3.ttf", size=20)
FONT = Font("JetBrainsMonoNerdFont-Regular.ttf", size=20)

__A_RECT = FONT.get_rect("A")
GRID_WIDTH = __A_RECT.width
GRID_HEIGHT = __A_RECT.y - 1
GRID_SIZE = (GRID_WIDTH, GRID_HEIGHT)


def draw_text(
    surface: pygame.Surface, txt: str, rect: pygame.Rect, color=(255, 255, 255)
):
    txt_surf = FONT.render(txt, True, color)
    txt_rect = txt_surf.get_rect()
    txt_rect.topleft = add(rect.topleft, (2, -2))
    surface.blit(txt_surf, txt_rect)


if __name__ == "__main__":
    print(FONT.get_metrics("A"))
    print(FONT.get_rect("A"))
    print(FONT.size("A"))
