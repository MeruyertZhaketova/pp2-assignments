import pygame


def main():
    pygame.init()
    screen = pygame.display.set_mode((1200, 600))
    clock = pygame.time.Clock()

    radius = 15
    mode = 'blue'
    points = []
    strokes = []

    figures = []
    figures_perm = []

    drawing = True
    drawing_mode = 1
    fig_start = (0, 0)

    text = """
P = Stop/Draw
L = Line
Z = Rectangle
X = Circle
Q = Square
T = Right Triangle
E = Equilateral Triangle
R = Rhombus
C = Eraser
A = Clear
"""

    r = pygame.Rect(30, 150, 30, 30)
    g = pygame.Rect(30, 200, 30, 30)
    b = pygame.Rect(30, 250, 30, 30)

    while True:
        pressed = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    return

                if event.key == pygame.K_p:
                    drawing = not drawing

                elif event.key == pygame.K_l:
                    drawing_mode = 1  # line

                elif event.key == pygame.K_z:
                    drawing_mode = 2  # rectangle

                elif event.key == pygame.K_x:
                    drawing_mode = 3  # circle

                elif event.key == pygame.K_q:
                    drawing_mode = 4  # square

                elif event.key == pygame.K_t:
                    drawing_mode = 5  # right triangle

                elif event.key == pygame.K_e:
                    drawing_mode = 6  # equilateral triangle

                elif event.key == pygame.K_r:
                    drawing_mode = 7  # rhombus

                elif event.key == pygame.K_c:
                    mode = 'erase'
                    if points:
                        strokes.append((points.copy(), mode, radius))
                    points = []

                elif event.key == pygame.K_a:
                    strokes = []
                    figures_perm = []
                    points = []

            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:
                    fig_start = mouse_pos

                    if drawing_mode == 1:
                        if points:
                            strokes.append((points.copy(), mode, radius))
                        points = []

                if r.collidepoint(mouse_pos):
                    mode = 'red'
                elif g.collidepoint(mouse_pos):
                    mode = 'green'
                elif b.collidepoint(mouse_pos):
                    mode = 'blue'

            if event.type == pygame.MOUSEBUTTONUP:

                if event.button == 1:
                    if drawing_mode in (2, 3, 4, 5, 6, 7):
                        figures_perm.append((fig_start, mouse_pos, mode, radius, drawing_mode))

            if event.type == pygame.MOUSEMOTION:
                if event.buttons[0]:
                    if drawing_mode == 1:
                        points.append(event.pos)

        screen.fill((0, 0, 0))

        # draw strokes
        for pts, col_mode, rad in strokes:
            for i in range(len(pts) - 1):
                drawLineBetween(screen, i, pts[i], pts[i+1], rad, col_mode)

        # draw saved figures
        for start, end, col_mode, rad, d_mode in figures_perm:
            drawfig(screen, start, end, rad, col_mode, d_mode)

        # draw current line
        if drawing and drawing_mode == 1:
            for i in range(len(points) - 1):
                drawLineBetween(screen, i, points[i], points[i+1], radius, mode)

        # UI
        font = pygame.font.SysFont(None, 26)
        screen.blit(font.render(text, True, (255, 255, 255)), (10, 10))

        pygame.draw.rect(screen, (0, 0, 255), b)
        pygame.draw.rect(screen, (255, 0, 0), r)
        pygame.draw.rect(screen, (0, 255, 0), g)

        pygame.display.flip()
        clock.tick(60)


# ---------------- FIGURES ----------------

def drawfig(screen, start, end, width, color_mode, draw_mode):

    x1, y1 = start
    x2, y2 = end

    if color_mode == 'blue':
        color = (0, 0, 255)
    elif color_mode == 'red':
        color = (255, 0, 0)
    elif color_mode == 'green':
        color = (0, 255, 0)
    else:
        color = (255, 255, 255)

    # rectangle
    if draw_mode == 2:
        rect = pygame.Rect(min(x1, x2), min(y1, y2),
                           abs(x2 - x1), abs(y2 - y1))
        pygame.draw.rect(screen, color, rect, width)

    # circle
    elif draw_mode == 3:
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        r = int(((x2-x1)**2 + (y2-y1)**2) ** 0.5 / 2)
        pygame.draw.circle(screen, color, (cx, cy), r, width)

    # square
    elif draw_mode == 4:
        side = max(abs(x2-x1), abs(y2-y1))
        rect = pygame.Rect(x1, y1, side, side)
        pygame.draw.rect(screen, color, rect, width)

    # right triangle
    elif draw_mode == 5:
        pygame.draw.polygon(screen, color, [
            (x1, y1),
            (x1, y2),
            (x2, y2)
        ], width)

    # equilateral triangle
    elif draw_mode == 6:
        pygame.draw.polygon(screen, color, [
            (x1, y2),
            ((x1 + x2)//2, y1),
            (x2, y2)
        ], width)

    # rhombus
    elif draw_mode == 7:
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        pygame.draw.polygon(screen, color, [
            (cx, y1),
            (x2, cy),
            (cx, y2),
            (x1, cy)
        ], width)


# ---------------- LINE ----------------

def drawLineBetween(screen, index, start, end, width, color_mode):
    color = (0, 0, 255)

    dx = start[0] - end[0]
    dy = start[1] - end[1]
    iterations = max(abs(dx), abs(dy))

    for i in range(iterations):
        progress = i / iterations if iterations != 0 else 0
        x = int(start[0] + (end[0] - start[0]) * progress)
        y = int(start[1] + (end[1] - start[1]) * progress)
        pygame.draw.circle(screen, color, (x, y), width)


main()