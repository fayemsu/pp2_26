import pygame
from math import *

def main():
    pygame.init()

    screen = pygame.display.set_mode((1000, 670))
    base_layer = pygame.Surface((1000, 670))
    
    base_layer.fill((0, 0, 0))  # persistent canvas
    clock = pygame.time.Clock()
    
    colorRED = (255, 0, 0)
    colorBLUE = (0, 0, 255)
    colorGREEN = (0, 255, 0)
    colorWHITE = (255, 255, 255)
    colorBLACK = (0, 0, 0)

    LMBpressed = False
    THICKNESS = 5

    currX = 0
    currY = 0

    prevX = 0
    prevY = 0

    radius = 15
    

    def calculate_rect(x1, y1, x2, y2):
        return pygame.Rect(min(x1, x2), min(y1, y2), abs(x1 - x2), abs(y1 - y2))

    def calculate_circ_radi(x1, y1, x2, y2):
        return int(sqrt((x2-x1)**2 + (y2-y1)**2) // 2)

    def calculate_circ_cent(x1, y1, x2, y2):
        return ((x1 + x2) // 2, (y1 + y2) // 2)
    
    def get_color(mode):
        if mode == 'red':
            return colorRED
        elif mode == 'green':
            return colorGREEN
        return colorBLUE
    
    def draw_text(screen, text, font, color, x, y):
        image = font.render(text, True, color)
        screen.blit(image, (x, y))

    mode = 'blue'
    paint_mode = 'brush'
    
    running = True 

    while running:
        
        pressed = pygame.key.get_pressed()
        
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]
        
        for event in pygame.event.get():
            
            # determine if X was clicked, or Ctrl+Q or ESC was used
            if event.type == pygame.QUIT:
                running = False 

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q and ctrl_held:
                    running = False
                if event.key == pygame.K_ESCAPE:
                    running = False
            
                # determine if a letter key was pressed
                if event.key == pygame.K_r:
                    mode = 'red'
                elif event.key == pygame.K_g:
                    mode = 'green'
                elif event.key == pygame.K_b:
                    mode = 'blue'

                # switch drawing mode
                if event.key == pygame.K_s:
                    paint_mode = 'rect'
                elif event.key == pygame.K_c:
                    paint_mode = 'circle'
                elif event.key == pygame.K_k:
                    paint_mode = 'brush'
                elif event.key == pygame.K_e:
                    paint_mode = 'eraser'
                elif event.key == pygame.K_a:
                    base_layer.fill((0, 0, 0))

                # thickness / radius control
                if event.key == pygame.K_EQUALS:
                    THICKNESS += 1
                    radius += 1
                if event.key == pygame.K_MINUS:
                    THICKNESS = max(1, THICKNESS - 1)
                    radius = max(1, radius - 1)

            # detect mouse press
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                print("LMB pressed!")
                LMBpressed = True
                prevX, prevY = event.pos

            # detect mouse release
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                print("LMB released!")
                LMBpressed = False
                currX, currY = event.pos

                # finalize shapes on base_layer
                if paint_mode == 'rect':
                    pygame.draw.rect(base_layer, get_color(mode), calculate_rect(prevX, prevY, currX, currY), THICKNESS)

                elif paint_mode == 'circle':
                    pygame.draw.circle(base_layer, get_color(mode),calculate_circ_cent(prevX, prevY, currX, currY), calculate_circ_radi(prevX, prevY, currX, currY), THICKNESS)

            # mouse movement
            if event.type == pygame.MOUSEMOTION:
                
                # BRUSH DRAWING (permanent)
                if (paint_mode == 'brush') and LMBpressed:
                    drawLineBetween(base_layer, 0, (prevX, prevY), event.pos, radius, mode)
                    prevX, prevY = event.pos
                elif (paint_mode == 'eraser') and LMBpressed:
                    drawLineBetween(base_layer, 0, (prevX, prevY), event.pos, radius, 'black')
                    prevX, prevY = event.pos

        

        # always start by drawing the base layer
        screen.blit(base_layer, (0, 0))

        # SHAPE PREVIEW (temporary)
        if LMBpressed and (paint_mode == 'rect' or paint_mode == 'circle'):
            currX, currY = pygame.mouse.get_pos()

            if paint_mode == 'rect':
                pygame.draw.rect(screen, get_color(mode), calculate_rect(prevX, prevY, currX, currY), THICKNESS)

            elif paint_mode == 'circle':
                pygame.draw.circle(screen, get_color(mode), calculate_circ_cent(prevX, prevY, currX, currY), calculate_circ_radi(prevX, prevY, currX, currY), THICKNESS)

        pygame.draw.rect(screen, colorBLACK, (0, 580, 1000, 90))
        draw_text(screen, f"CURRENT MODE: {paint_mode}", pygame.font.SysFont("Verdana", 17), (252, 229, 155), 30, 590)
        draw_text(screen, f"CURRENT COLOR: {mode}", pygame.font.SysFont("Verdana", 17), (252, 229, 155), 30, 615)
        draw_text(screen, f"CURRENT THICKNESS: {THICKNESS}", pygame.font.SysFont("Verdana", 17), (252, 229, 155), 30, 640)

        draw_text(screen, f"rectangle - S", pygame.font.SysFont("Verdana", 17), (252, 229, 155), 335, 600)
        draw_text(screen, f"circle - C", pygame.font.SysFont("Verdana", 17), (252, 229, 155), 335, 635)

        draw_text(screen, f"brush - K", pygame.font.SysFont("Verdana", 17), (252, 229, 155), 540, 590)
        draw_text(screen, f"eraser - E", pygame.font.SysFont("Verdana", 17), (252, 229, 155), 540, 615)
        draw_text(screen, f"clean all - A", pygame.font.SysFont("Verdana", 17), (252, 229, 155), 540, 640)

        draw_text(screen, f"blue - B", pygame.font.SysFont("Verdana", 17), (252, 229, 155), 790, 590)
        draw_text(screen, f"red - R", pygame.font.SysFont("Verdana", 17), (252, 229, 155), 790, 615)
        draw_text(screen, f"green - G", pygame.font.SysFont("Verdana", 17), (252, 229, 155), 790, 640)


        pygame.display.flip()
        clock.tick(120)



def drawLineBetween(screen, index, start, end, width, color_mode):
    c1 = max(0, min(255, 2 * index - 256))
    c2 = max(0, min(255, 2 * index))
    
    if color_mode == 'blue':
        color = (0, 0, 255)
    elif color_mode == 'red':
        color = (255, 0, 0)
    elif color_mode == 'green':
        color = (0, 255, 0)
    elif color_mode == 'black':
        color = (0, 0, 0)
    
    dx = start[0] - end[0]
    dy = start[1] - end[1]
    iterations = max(abs(dx), abs(dy))
    
    for i in range(iterations):
        progress = i / iterations
        aprogress = 1 - progress
        x = int(aprogress * start[0] + progress * end[0])
        y = int(aprogress * start[1] + progress * end[1])
        pygame.draw.circle(screen, color, (x, y), width)


main()