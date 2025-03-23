from pygame.ftfont import Font
import pygame.ftfont
import pygame


pygame.ftfont.init()
FONT = Font("JetBrainsMonoNerdFont-Regular.ttf", size=30)
__A_RECT = FONT.get_rect("A")
GRID_WIDTH = __A_RECT.width
GRID_HEIGHT = __A_RECT.height
GRID_SIZE = (GRID_WIDTH, GRID_HEIGHT)


def draw_text(
    surface: pygame.Surface, txt: str, rect: pygame.Rect, color=(255, 255, 255)
):
    txt_surf = FONT.render(txt, True, color)
    txt_rect = txt_surf.get_rect()
    txt_rect.center = rect.center
    surface.blit(txt_surf, txt_rect)
