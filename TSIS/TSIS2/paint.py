import pygame
import datetime

from tools import draw_line_between, draw_shape, flood_fill, get_color


WIDTH = 1200
HEIGHT = 600
BRUSH_SIZES = [2, 5, 10]


def save_canvas(canvas):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"canvas_{timestamp}.png"
    pygame.image.save(canvas, filename)
    print(f"Saved as {filename}")


def draw_instructions(screen, font, current_tool, brush_size):
    text = [
        "P = Stop/Draw",
        "L = Pencil",
        "N = Straight line",
        "Z = Rectangle",
        "X = Circle",
        "Q = Square",
        "W = Right triangle",
        "E = Equilateral triangle",
        "R = Rhombus",
        "F = Flood fill",
        "T = Text tool",
        "C = Eraser",
        "A = Clear",
        "1/2/3 = Brush size",
        "Ctrl+S = Save PNG",
        f"Tool: {current_tool}",
        f"Brush: {brush_size}px"
    ]

    y = 10
    for line in text:
        rendered = font.render(line, True, (255, 255, 255))
        screen.blit(rendered, (10, y))
        y += 22


def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("TSIS2 Paint")
    clock = pygame.time.Clock()

    canvas = pygame.Surface((WIDTH, HEIGHT))
    canvas.fill((0, 0, 0))

    font = pygame.font.SysFont(None, 24)
    text_font = pygame.font.SysFont(None, 36)

    current_tool = "pencil"
    current_color = "blue"
    brush_index = 1
    drawing_enabled = True

    start_pos = None
    current_pos = None
    previous_pos = None

    text_active = False
    text_position = (0, 0)
    text_value = ""

    red_button = pygame.Rect(30, 360, 30, 30)
    green_button = pygame.Rect(30, 410, 30, 30)
    blue_button = pygame.Rect(30, 460, 30, 30)

    shape_tools = {
        "rectangle",
        "circle",
        "square",
        "right_triangle",
        "equilateral_triangle",
        "rhombus",
        "straight_line"
    }

    running = True

    while running:
        ctrl_pressed = pygame.key.get_pressed()[pygame.K_LCTRL] or pygame.key.get_pressed()[pygame.K_RCTRL]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if text_active:
                    if event.key == pygame.K_RETURN:
                        canvas.blit(
                            text_font.render(text_value, True, get_color(current_color)),
                            text_position
                        )
                        text_active = False
                        text_value = ""

                    elif event.key == pygame.K_ESCAPE:
                        text_active = False
                        text_value = ""

                    elif event.key == pygame.K_BACKSPACE:
                        text_value = text_value[:-1]

                    elif event.unicode and event.unicode.isprintable():
                        text_value += event.unicode

                    continue

                if event.key == pygame.K_ESCAPE:
                    running = False

                elif event.key == pygame.K_s and ctrl_pressed:
                    save_canvas(canvas)

                elif event.key == pygame.K_p:
                    drawing_enabled = not drawing_enabled

                elif event.key == pygame.K_1:
                    brush_index = 0

                elif event.key == pygame.K_2:
                    brush_index = 1

                elif event.key == pygame.K_3:
                    brush_index = 2

                elif event.key == pygame.K_l:
                    current_tool = "pencil"

                elif event.key == pygame.K_n:
                    current_tool = "straight_line"

                elif event.key == pygame.K_z:
                    current_tool = "rectangle"

                elif event.key == pygame.K_x:
                    current_tool = "circle"

                elif event.key == pygame.K_q:
                    current_tool = "square"

                elif event.key == pygame.K_w:
                    current_tool = "right_triangle"

                elif event.key == pygame.K_e:
                    current_tool = "equilateral_triangle"

                elif event.key == pygame.K_r:
                    current_tool = "rhombus"

                elif event.key == pygame.K_f:
                    current_tool = "fill"

                elif event.key == pygame.K_t:
                    current_tool = "text"

                elif event.key == pygame.K_c:
                    current_color = "erase"

                elif event.key == pygame.K_a:
                    canvas.fill((0, 0, 0))

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                if red_button.collidepoint(mouse_pos):
                    current_color = "red"
                    continue

                elif green_button.collidepoint(mouse_pos):
                    current_color = "green"
                    continue

                elif blue_button.collidepoint(mouse_pos):
                    current_color = "blue"
                    continue

                if event.button == 1 and drawing_enabled:
                    if current_tool == "pencil":
                        previous_pos = mouse_pos

                    elif current_tool in shape_tools:
                        start_pos = mouse_pos
                        current_pos = mouse_pos

                    elif current_tool == "fill":
                        flood_fill(canvas, mouse_pos[0], mouse_pos[1], get_color(current_color))

                    elif current_tool == "text":
                        text_active = True
                        text_position = mouse_pos
                        text_value = ""

            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos

                if event.buttons[0] and drawing_enabled:
                    if current_tool == "pencil" and previous_pos is not None:
                        draw_line_between(
                            canvas,
                            previous_pos,
                            mouse_pos,
                            BRUSH_SIZES[brush_index],
                            current_color
                        )
                        previous_pos = mouse_pos

                    elif current_tool in shape_tools and start_pos is not None:
                        current_pos = mouse_pos

            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = event.pos

                if event.button == 1 and drawing_enabled:
                    if current_tool == "pencil":
                        previous_pos = None

                    elif current_tool in shape_tools and start_pos is not None:
                        draw_shape(
                            canvas,
                            start_pos,
                            mouse_pos,
                            BRUSH_SIZES[brush_index],
                            current_color,
                            current_tool
                        )
                        start_pos = None
                        current_pos = None

        screen.blit(canvas, (0, 0))

        if drawing_enabled and current_tool in shape_tools and start_pos is not None and current_pos is not None:
            draw_shape(
                screen,
                start_pos,
                current_pos,
                BRUSH_SIZES[brush_index],
                current_color,
                current_tool
            )

        if text_active:
            preview = text_font.render(text_value + "|", True, get_color(current_color))
            screen.blit(preview, text_position)

        draw_instructions(screen, font, current_tool, BRUSH_SIZES[brush_index])

        pygame.draw.rect(screen, (255, 0, 0), red_button)
        pygame.draw.rect(screen, (0, 255, 0), green_button)
        pygame.draw.rect(screen, (0, 0, 255), blue_button)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
