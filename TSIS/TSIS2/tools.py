import pygame
import math
from collections import deque


def get_color(mode):
    if mode == "red":
        return (255, 0, 0)
    if mode == "green":
        return (0, 255, 0)
    if mode == "blue":
        return (0, 0, 255)
    if mode == "erase":
        return (0, 0, 0)
    return (255, 255, 255)


def flood_fill(surface, x, y, fill_color):
    width, height = surface.get_size()

    if not (0 <= x < width and 0 <= y < height):
        return

    target_color = surface.get_at((x, y))[:3]
    fill_color = tuple(fill_color[:3])

    if target_color == fill_color:
        return

    queue = deque([(x, y)])
    visited = {(x, y)}

    while queue:
        cx, cy = queue.popleft()
        surface.set_at((cx, cy), fill_color)

        neighbours = [
            (cx - 1, cy),
            (cx + 1, cy),
            (cx, cy - 1),
            (cx, cy + 1)
        ]

        for nx, ny in neighbours:
            if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in visited:
                if surface.get_at((nx, ny))[:3] == target_color:
                    visited.add((nx, ny))
                    queue.append((nx, ny))


def draw_line_between(surface, start, end, width, mode):
    color = get_color(mode)

    dx = start[0] - end[0]
    dy = start[1] - end[1]
    steps = max(abs(dx), abs(dy))

    if steps == 0:
        pygame.draw.circle(surface, color, start, width)
        return

    for i in range(steps + 1):
        progress = i / steps
        x = int(start[0] + (end[0] - start[0]) * progress)
        y = int(start[1] + (end[1] - start[1]) * progress)
        pygame.draw.circle(surface, color, (x, y), width)


def draw_shape(surface, start, end, width, mode, tool):
    color = get_color(mode)

    x1, y1 = start
    x2, y2 = end

    if tool == "rectangle":
        rect = pygame.Rect(
            min(x1, x2),
            min(y1, y2),
            abs(x2 - x1),
            abs(y2 - y1)
        )
        pygame.draw.rect(surface, color, rect, width)

    elif tool == "circle":
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        radius = int(math.hypot(x2 - x1, y2 - y1) / 2)
        pygame.draw.circle(surface, color, (cx, cy), radius, width)

    elif tool == "square":
        side = min(abs(x2 - x1), abs(y2 - y1))
        sx = x1 + side if x2 >= x1 else x1 - side
        sy = y1 + side if y2 >= y1 else y1 - side

        rect = pygame.Rect(
            min(x1, sx),
            min(y1, sy),
            side,
            side
        )
        pygame.draw.rect(surface, color, rect, width)

    elif tool == "right_triangle":
        points = [
            (x1, y1),
            (x1, y2),
            (x2, y2)
        ]
        pygame.draw.polygon(surface, color, points, width)

    elif tool == "equilateral_triangle":
        base = abs(x2 - x1)
        height = math.sqrt(3) / 2 * base
        apex_x = (x1 + x2) / 2

        if y2 >= y1:
            apex_y = y2 - height
        else:
            apex_y = y2 + height

        points = [
            (x1, y2),
            (x2, y2),
            (apex_x, apex_y)
        ]
        pygame.draw.polygon(surface, color, points, width)

    elif tool == "rhombus":
        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2

        points = [
            (cx, y1),
            (x2, cy),
            (cx, y2),
            (x1, cy)
        ]
        pygame.draw.polygon(surface, color, points, width)

    elif tool == "straight_line":
        pygame.draw.line(surface, color, start, end, width)
