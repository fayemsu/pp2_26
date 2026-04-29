import pygame
from math import *

def main():
    pygame.init()

    screen = pygame.display.set_mode((1200, 670))
    base_layer = pygame.Surface((1200, 670))
    
    base_layer.fill((0, 0, 0))  # persistent canvas
    clock = pygame.time.Clock()
    
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

    LMBpressed = False
    THICKNESS = 5

    currX = 0
    currY = 0

    prevX = 0
    prevY = 0

    radius = 5
    

    def calculate_rect(x1, y1, x2, y2):
        return pygame.Rect(min(x1, x2), min(y1, y2), abs(x1 - x2), abs(y1 - y2))

    def calculate_circ_radi(x1, y1, x2, y2):
        return int(sqrt((x2-x1)**2 + (y2-y1)**2) // 2)

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
        return [ (x1, y2), (x1, y1), (x2, y2) ]
    
    def calculate_equilateral_triangle(x1, y1, x2, y2):
        base_center_x = (x1 + x2) // 2
        top_y = min(y1, y2)
        bottom_y = max(y1, y2)

        return [
            (base_center_x, top_y),
            (x1, bottom_y),
            (x2, bottom_y)
        ]
    

    def calculate_rhombus(x1, y1, x2, y2):
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2

        return [
            (center_x, y1),   # top
            (x2, center_y),   # right
            (center_x, y2),   # bottom
            (x1, center_y)    # left
        ]
   
    
    def draw_text(screen, text, font, color, x, y):
        image = font.render(text, True, color)
        screen.blit(image, (x, y))

    mode = '1'
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

                # switch drawing mode
                if event.key == pygame.K_r:
                    paint_mode = 'rect'
                elif event.key == pygame.K_c:
                    paint_mode = 'circle'
                elif event.key == pygame.K_b:
                    paint_mode = 'brush'
                elif event.key == pygame.K_m:
                    paint_mode = 'rhombus'
                elif event.key == pygame.K_q:
                    paint_mode = 'eq tr'
                elif event.key == pygame.K_i:
                    paint_mode = 'right tr'
                elif event.key == pygame.K_e:
                    paint_mode = 'eraser'
                elif event.key == pygame.K_s:
                    paint_mode = 'square'
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
                
                elif paint_mode == 'square':
                    pygame.draw.rect( base_layer, get_color(mode), calculate_square(prevX, prevY, currX, currY), THICKNESS )

                elif paint_mode == 'right tr':
                    pygame.draw.polygon( base_layer, get_color(mode), calculate_right_triangle(prevX, prevY, currX, currY), THICKNESS)

                elif paint_mode == 'eq tr':
                    pygame.draw.polygon(base_layer, get_color(mode), calculate_equilateral_triangle(prevX, prevY, currX, currY), THICKNESS)

                elif paint_mode == 'rhombus':
                    pygame.draw.polygon(base_layer, get_color(mode), calculate_rhombus(prevX, prevY, currX, currY), THICKNESS)

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
        if LMBpressed:
            currX, currY = pygame.mouse.get_pos()

            if paint_mode == 'rect':
                pygame.draw.rect(screen, get_color(mode), calculate_rect(prevX, prevY, currX, currY), THICKNESS)

            elif paint_mode == 'circle':
                pygame.draw.circle(screen, get_color(mode), calculate_circ_cent(prevX, prevY, currX, currY), calculate_circ_radi(prevX, prevY, currX, currY), THICKNESS)
            
            elif paint_mode == 'square':
                pygame.draw.rect( screen, get_color(mode), calculate_square(prevX, prevY, currX, currY), THICKNESS )

            elif paint_mode == 'right tr':
                pygame.draw.polygon( screen, get_color(mode), calculate_right_triangle(prevX, prevY, currX, currY), THICKNESS)

            elif paint_mode == 'eq tr':
                pygame.draw.polygon(screen, get_color(mode), calculate_equilateral_triangle(prevX, prevY, currX, currY), THICKNESS)

            elif paint_mode == 'rhombus':
                pygame.draw.polygon(screen, get_color(mode), calculate_rhombus(prevX, prevY, currX, currY), THICKNESS)

        pygame.draw.rect(screen, colorBLACK, (0, 580, 1200, 90))
        draw_text(screen, f"MODE: {paint_mode}", pygame.font.SysFont("Verdana", 17), (252, 229, 155), 30, 590)
        draw_text(screen, f"COLOR: {mode}", pygame.font.SysFont("Verdana", 17), (252, 229, 155), 30, 615)
        draw_text(screen, f"THICKNESS: {THICKNESS}", pygame.font.SysFont("Verdana", 17), (252, 229, 155), 30, 640)

        draw_text(screen, f"brush - B", pygame.font.SysFont("Verdana", 17), (252, 229, 155), 285, 590)
        draw_text(screen, f"eraser - E", pygame.font.SysFont("Verdana", 17), (252, 229, 155), 285, 615)
        draw_text(screen, f"clean all - A", pygame.font.SysFont("Verdana", 17), (252, 229, 155), 285, 640)

        draw_text(screen, f"rectangle - R", pygame.font.SysFont("Verdana", 17), (252, 229, 155), 465, 590)
        draw_text(screen, f"circle - C", pygame.font.SysFont("Verdana", 17), (252, 229, 155), 465, 615)
        draw_text(screen, f"rhombus - M", pygame.font.SysFont("Verdana", 17), (252, 229, 155), 465, 640)

        draw_text(screen, f"eq. triangle - Q", pygame.font.SysFont("Verdana", 17), (252, 229, 155), 670, 590)
        draw_text(screen, f"right triangle - I", pygame.font.SysFont("Verdana", 17), (252, 229, 155), 670, 615)
        draw_text(screen, f"square - S", pygame.font.SysFont("Verdana", 17), (252, 229, 155), 670, 640)
    

        pygame.draw.rect(screen, get_color('1'), (870, 590, 20, 20))
        pygame.draw.rect(screen, get_color('2'), (870, 615, 20, 20))
        pygame.draw.rect(screen, get_color('3'), (870, 640, 20, 20))
        pygame.draw.rect(screen, get_color('4'), (975, 590, 20, 20))
        pygame.draw.rect(screen, get_color('5'), (975, 615, 20, 20))
        pygame.draw.rect(screen, get_color('6'), (975, 640, 20, 20))
        pygame.draw.rect(screen, get_color('7'), (1080, 590, 20, 20))
        pygame.draw.rect(screen, get_color('8'), (1080, 615, 20, 20))
        pygame.draw.rect(screen, get_color('9'), (1080, 640, 20, 20))

        draw_text(screen, f"- 1", pygame.font.SysFont("Verdana", 17), (252, 229, 155), 895, 590)
        draw_text(screen, f"- 2", pygame.font.SysFont("Verdana", 17), (252, 229, 155), 895, 615)
        draw_text(screen, f"- 3", pygame.font.SysFont("Verdana", 17), (252, 229, 155), 895, 640)
        draw_text(screen, f"- 4", pygame.font.SysFont("Verdana", 17), (252, 229, 155), 1000, 590)
        draw_text(screen, f"- 5", pygame.font.SysFont("Verdana", 17), (252, 229, 155), 1000, 615)
        draw_text(screen, f"- 6", pygame.font.SysFont("Verdana", 17), (252, 229, 155), 1000, 640)
        draw_text(screen, f"- 7", pygame.font.SysFont("Verdana", 17), (252, 229, 155), 1105, 590)
        draw_text(screen, f"- 8", pygame.font.SysFont("Verdana", 17), (252, 229, 155), 1105, 615)
        draw_text(screen, f"- 9", pygame.font.SysFont("Verdana", 17), (252, 229, 155), 1105, 640)


        pygame.display.flip()
        clock.tick(120)



def drawLineBetween(screen, index, start, end, width, color_mode):
    c1 = max(0, min(255, 2 * index - 256))
    c2 = max(0, min(255, 2 * index))

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
    
    for i in range(iterations):
        progress = i / iterations
        aprogress = 1 - progress
        x = int(aprogress * start[0] + progress * end[0])
        y = int(aprogress * start[1] + progress * end[1])
        pygame.draw.circle(screen, color, (x, y), width)


main()