import pygame
from math import *
from datetime import datetime

pygame.init()


def drawLineBetween(screen, index, start, end, width, color_mode):
    if color_mode == '1':
        color = (179, 11, 16)
    elif color_mode == '2':
        color = (17, 110, 42)
    elif color_mode == '3':
        color = (31, 100, 206)
    elif color_mode == '4':
        color = (255, 255, 255)
    elif color_mode == '5':
        color = (244, 255, 37)
    elif color_mode == '6':
        color = (240, 146, 21)
    elif color_mode == '7':
        color = (213, 81, 227)
    elif color_mode == '8':
        color = (98, 187, 219)
    elif color_mode == '9':
        color = (131, 153, 88)
    elif color_mode == 'black':
        color = (0, 0, 0)

    dx = start[0] - end[0]
    dy = start[1] - end[1]
    iterations = max(abs(dx), abs(dy))

    if iterations == 0:
        pygame.draw.circle(screen, color, start, width)
        return

    for i in range(iterations):
        progress = i / iterations
        aprogress = 1 - progress

        x = int(aprogress * start[0] + progress * end[0])
        y = int(aprogress * start[1] + progress * end[1])

        pygame.draw.circle(screen, color, (x, y), width)


def main():
    screen = pygame.display.set_mode((1400, 670))
    clock = pygame.time.Clock()

    base_layer = pygame.Surface((1400, 670))
    base_layer.fill((0, 0, 0))

    colorRED = (179, 11, 16)
    colorBLUE = (31, 100, 206)
    colorGREEN = (17, 110, 42)
    colorWHITE = (255, 255, 255)
    colorMOSS = (131, 153, 88)
    colorORNG = (240, 146, 21)
    colorYELL = (244, 255, 37)
    colorPINK = (213, 81, 227)
    colorBBL = (98, 187, 219)
    colorBLACK = (0, 0, 0)

    def get_color(mode):
        if mode == '1':
            return colorRED
        elif mode == '2':
            return colorGREEN
        elif mode == '3':
            return colorBLUE
        elif mode == '4':
            return colorWHITE
        elif mode == '5':
            return colorYELL
        elif mode == '6':
            return colorORNG
        elif mode == '7':
            return colorPINK
        elif mode == '8':
            return colorBBL
        elif mode == '9':
            return colorMOSS

    def draw_text(screen, text, font, color, x, y):
        image = font.render(text, True, color)
        screen.blit(image, (x, y))

    def calculate_rect(x1, y1, x2, y2):
        return pygame.Rect( min(x1, x2), min(y1, y2), abs(x1 - x2), abs(y1 - y2))

    def calculate_circ_radi(x1, y1, x2, y2):
        return int(sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) // 2)

    def calculate_circ_cent(x1, y1, x2, y2):
        return ((x1 + x2) // 2, (y1 + y2) // 2)

    def calculate_square(x1, y1, x2, y2):
        side = min(abs(x2 - x1), abs(y2 - y1))
        if x2 < x1:
            x = x1 - side
        else:
            x = x1
        if y2 < y1:
            y = y1 - side
        else:
            y = y1
        return pygame.Rect(x, y, side, side)

    def calculate_right_triangle(x1, y1, x2, y2):
        return [ (x1, y2), (x1, y1), (x2, y2)]

    def calculate_equilateral_triangle(x1, y1, x2, y2):
        base_center_x = (x1 + x2) // 2
        top_y = min(y1, y2)
        bottom_y = max(y1, y2)
        return [(base_center_x, top_y), (x1, bottom_y), (x2, bottom_y) ]

    def calculate_rhombus(x1, y1, x2, y2):
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2

        return [(center_x, y1), (x2, center_y), (center_x, y2), (x1, center_y)]

    def flood_fill(surface, x, y, fill_color):
        target_color = surface.get_at((x, y))

        if target_color == fill_color:
            return

        stack = [(x, y)]

        while stack:
            x, y = stack.pop()

            if x < 0 or x >= surface.get_width():
                continue
            if y < 0 or y >= surface.get_height():
                continue

            if surface.get_at((x, y)) != target_color:
                continue

            surface.set_at((x, y), fill_color)

            stack.append((x + 1, y))
            stack.append((x - 1, y))
            stack.append((x, y + 1))
            stack.append((x, y - 1))

    LMBpressed = False

    THICKNESS = 5
    radius = 5

    prevX = 0
    prevY = 0
    currX = 0
    currY = 0

    mode = '1'
    paint_mode = 'pencil'

    text_active = False
    text_input = ""
    text_pos = (0, 0)
    font = pygame.font.SysFont("Verdana", 24)

    running = True

    while running:
        pressed = pygame.key.get_pressed()
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:

                if text_active:
                    if event.key == pygame.K_RETURN:
                        text_surface = font.render(
                            text_input,
                            True,
                            get_color(mode)
                        )
                        base_layer.blit(text_surface, text_pos)

                        text_active = False
                        text_input = ""

                    elif event.key == pygame.K_ESCAPE:
                        text_active = False
                        text_input = ""

                    elif event.key == pygame.K_BACKSPACE:
                        text_input = text_input[:-1]

                    else:
                        if event.unicode.isprintable():
                            text_input += event.unicode

                    continue

                
                if event.key == pygame.K_ESCAPE:
                    running = False

                if event.key == pygame.K_q and ctrl_held:
                    running = False

                if event.key == pygame.K_s and ctrl_held:
                    filename = datetime.now().strftime(
                        "paint_%Y%m%d_%H%M%S.png"
                    )
                    pygame.image.save(base_layer, filename)
                    print(f"Saved as {filename}")

                if event.key == pygame.K_1:
                    mode = '1'
                elif event.key == pygame.K_2:
                    mode = '2'
                elif event.key == pygame.K_3:
                    mode = '3'
                elif event.key == pygame.K_4:
                    mode = '4'
                elif event.key == pygame.K_5:
                    mode = '5'
                elif event.key == pygame.K_6:
                    mode = '6'
                elif event.key == pygame.K_7:
                    mode = '7'
                elif event.key == pygame.K_8:
                    mode = '8'
                elif event.key == pygame.K_9:
                    mode = '9'

                if event.key == pygame.K_p:
                    paint_mode = 'pencil'
                elif event.key == pygame.K_e:
                    paint_mode = 'eraser'
                elif event.key == pygame.K_r:
                    paint_mode = 'rect'
                elif event.key == pygame.K_c:
                    paint_mode = 'circle'
                elif event.key == pygame.K_l:
                    paint_mode = 'line'
                elif event.key == pygame.K_k:
                    paint_mode = 'square'
                elif event.key == pygame.K_i:
                    paint_mode = 'right tr'
                elif event.key == pygame.K_q:
                    paint_mode = 'eq tr'
                elif event.key == pygame.K_m:
                    paint_mode = 'rhombus'
                elif event.key == pygame.K_f:
                    paint_mode = 'fill'
                elif event.key == pygame.K_t:
                    paint_mode = 'text'
                elif event.key == pygame.K_a:
                    base_layer.fill((0, 0, 0))

                if event.key == pygame.K_LEFT:
                    THICKNESS = 2
                    radius = 2

                elif event.key == pygame.K_DOWN:
                    THICKNESS = 5
                    radius = 5

                elif event.key == pygame.K_RIGHT:
                    THICKNESS = 10
                    radius = 10

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                LMBpressed = True
                prevX, prevY = event.pos

                if paint_mode == 'fill':
                    flood_fill( base_layer, prevX,prevY,get_color(mode))

                if paint_mode == 'text':
                    text_active = True
                    text_input = ""
                    text_pos = event.pos

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                LMBpressed = False
                currX, currY = event.pos

                if paint_mode == 'rect':
                    pygame.draw.rect(base_layer, get_color(mode), calculate_rect(prevX, prevY, currX, currY), THICKNESS)

                elif paint_mode == 'circle':
                    pygame.draw.circle( base_layer, get_color(mode), calculate_circ_cent(prevX, prevY, currX, currY), calculate_circ_radi(prevX, prevY, currX, currY), THICKNESS)

                elif paint_mode == 'line':
                    pygame.draw.line( base_layer, get_color(mode), (prevX, prevY), (currX, currY), THICKNESS)

                elif paint_mode == 'square':
                    pygame.draw.rect(base_layer, get_color(mode), calculate_square(prevX, prevY, currX, currY), THICKNESS)

                elif paint_mode == 'right tr':
                    pygame.draw.polygon(base_layer, get_color(mode), calculate_right_triangle(prevX, prevY, currX, currY), THICKNESS)

                elif paint_mode == 'eq tr':
                    pygame.draw.polygon(base_layer, get_color(mode), calculate_equilateral_triangle(prevX, prevY, currX, currY), THICKNESS)

                elif paint_mode == 'rhombus':
                    pygame.draw.polygon(base_layer, get_color(mode), calculate_rhombus(prevX, prevY, currX, currY), THICKNESS)

            if event.type == pygame.MOUSEMOTION:

                if paint_mode == 'pencil' and LMBpressed:
                    pygame.draw.line(base_layer, get_color(mode), (prevX, prevY), event.pos, THICKNESS)
                    prevX, prevY = event.pos

                elif paint_mode == 'eraser' and LMBpressed:
                    drawLineBetween(base_layer, 0, (prevX, prevY), event.pos, radius, 'black')
                    prevX, prevY = event.pos

        screen.blit(base_layer, (0, 0))

        if LMBpressed:
            currX, currY = pygame.mouse.get_pos()

            if paint_mode == 'rect':
                pygame.draw.rect(screen, get_color(mode), calculate_rect(prevX, prevY, currX, currY), THICKNESS)

            elif paint_mode == 'circle':
                pygame.draw.circle(screen, get_color(mode), calculate_circ_cent(prevX, prevY, currX, currY), calculate_circ_radi(prevX, prevY, currX, currY), THICKNESS)

            elif paint_mode == 'line':
                pygame.draw.line(screen, get_color(mode), (prevX, prevY), (currX, currY), THICKNESS)

            elif paint_mode == 'square':
                pygame.draw.rect(screen, get_color(mode), calculate_square(prevX, prevY, currX, currY), THICKNESS)

            elif paint_mode == 'right tr':
                pygame.draw.polygon(screen, get_color(mode), calculate_right_triangle(prevX, prevY, currX, currY), THICKNESS)

            elif paint_mode == 'eq tr':
                pygame.draw.polygon(screen, get_color(mode), calculate_equilateral_triangle(prevX, prevY, currX, currY), THICKNESS)

            elif paint_mode == 'rhombus':
                pygame.draw.polygon(screen, get_color(mode), calculate_rhombus(prevX, prevY, currX, currY), THICKNESS)

        if text_active:
            preview = font.render(text_input, True, get_color(mode))
            screen.blit(preview, text_pos)

        pygame.draw.rect(screen, colorBLACK, (0, 580, 1400, 90))

        ui_color = (252, 229, 155)
        ui_font = pygame.font.SysFont("Verdana", 16)

        draw_text(screen, f"MODE: {paint_mode}", ui_font, ui_color, 20, 590)
        draw_text(screen, f"COLOR: {mode}", ui_font, ui_color, 20, 615)
        draw_text(screen, f"SIZE: {THICKNESS}", ui_font, ui_color, 20, 640)

        draw_text(screen, "pencil - P", ui_font, ui_color, 250, 590)
        draw_text(screen, "eraser - E", ui_font, ui_color, 250, 615)
        draw_text(screen, "line - L", ui_font, ui_color, 250, 640)

        draw_text(screen, "rect - R", ui_font, ui_color, 430, 590)
        draw_text(screen, "circle - C", ui_font, ui_color, 430, 615)
        draw_text(screen, "square - K", ui_font, ui_color, 430, 640)

        draw_text(screen, "eq.tr - Q", ui_font, ui_color, 610, 590)
        draw_text(screen, "right tr - I", ui_font, ui_color, 610, 615)
        draw_text(screen, "rhombus - M", ui_font, ui_color, 610, 640)

        draw_text(screen, "fill - F", ui_font, ui_color, 800, 590)
        draw_text(screen, "text - T", ui_font, ui_color, 800, 615)
        draw_text(screen, "clear - A", ui_font, ui_color, 800, 640)

        draw_text(screen, "size: Left/Down/Right", ui_font, ui_color, 920, 590)
        draw_text(screen, "save: Ctrl+S", ui_font, ui_color, 920, 625)

        pygame.draw.rect(screen, get_color('1'), (1120, 590, 20, 20))
        pygame.draw.rect(screen, get_color('2'), (1120, 615, 20, 20))
        pygame.draw.rect(screen, get_color('3'), (1120, 640, 20, 20))
        pygame.draw.rect(screen, get_color('4'), (1225, 590, 20, 20))
        pygame.draw.rect(screen, get_color('5'), (1225, 615, 20, 20))
        pygame.draw.rect(screen, get_color('6'), (1225, 640, 20, 20))
        pygame.draw.rect(screen, get_color('7'), (1330, 590, 20, 20))
        pygame.draw.rect(screen, get_color('8'), (1330, 615, 20, 20))
        pygame.draw.rect(screen, get_color('9'), (1330, 640, 20, 20))

        draw_text(screen, f"- 1", pygame.font.SysFont("Verdana", 17), (252, 229, 155), 1145, 590)
        draw_text(screen, f"- 2", pygame.font.SysFont("Verdana", 17), (252, 229, 155), 1145, 615)
        draw_text(screen, f"- 3", pygame.font.SysFont("Verdana", 17), (252, 229, 155), 1145, 640)
        draw_text(screen, f"- 4", pygame.font.SysFont("Verdana", 17), (252, 229, 155), 1250, 590)
        draw_text(screen, f"- 5", pygame.font.SysFont("Verdana", 17), (252, 229, 155), 1250, 615)
        draw_text(screen, f"- 6", pygame.font.SysFont("Verdana", 17), (252, 229, 155), 1250, 640)
        draw_text(screen, f"- 7", pygame.font.SysFont("Verdana", 17), (252, 229, 155), 1355, 590)
        draw_text(screen, f"- 8", pygame.font.SysFont("Verdana", 17), (252, 229, 155), 1355, 615)
        draw_text(screen, f"- 9", pygame.font.SysFont("Verdana", 17), (252, 229, 155), 1355, 640)

        pygame.display.flip()
        clock.tick(120)


main()