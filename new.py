from pyray import *
from math import sin, cos, pi

init_window(800, 600, "2D Raytracer")
set_target_fps(60)

rects = []
walls = [
    ((100, 100), (700, 100)),
    ((700, 100), (700, 500)),
    ((700, 500), (100, 500)),
    ((100, 500), (100, 100)),
    # ((300, 300), (500, 400)),
    # ((500, 400), (300, 400)),
]
rays = []
ray_count = 200
max_length = 1000

def cast_ray(origin, angle, rects):
    end_x = origin[0] + max_length * cos(angle)
    end_y = origin[1] + max_length * sin(angle)

    closest = (end_x, end_y)

    for rect in rects:
        hit = get_Intersection_rect(origin, (end_x, end_y), rect)
        if hit:
            closest = hit
            break

    return closest

def get_rect_edges(rect):
    x, y, w, h = rect[0], rect[1], rect[2], rect[3]
    top_left = Vector2(x, y)
    top_right = Vector2(x + w, y)
    bottom_left = Vector2(x, y + h)
    bottom_right = Vector2(x + w, y + h)

    return [(top_left, top_right), (top_right, bottom_right), (bottom_right, bottom_left), (bottom_left, top_left)]

def ray_hits_rect(ray_start, ray_end, rect):
    for edge_start, edge_end in get_rect_edges(rect):
        hit = check_collision_lines(ray_start, ray_end, edge_start, edge_end, None)
        if hit:
            return True
    return False

def ray_hits_wall(ray_start, ray_end, walls):
    for wall_start, wall_end in walls:
        start = wall_start
        end = wall_end
        hit = check_collision_lines(ray_start, ray_end, start, end, None)
        if hit:
            return True
    return False

def get_Intersection_rect(p1, p2, rect):
    x, y, w, h = rect
    if ray_hits_rect(p1, p2, rect):
        return (x + w / 2, y+h /2)
    return None

def get_Intersection_walls(p1, p2, walls):
    x, y, w, h = walls[0][0], walls[0][1], walls[1][0], walls[1][1]
    if ray_hits_wall(p1, p2, walls):
        return (x + w / 2, y+h /2)
    return None

while not window_should_close():
    if is_mouse_button_pressed(MOUSE_LEFT_BUTTON):
        mx, my = get_mouse_x(), get_mouse_y()
        rects.append((mx - 10, my - 10, 20, 20))

    if is_key_pressed(KEY_R):
        rects.clear()

    mx, my = get_mouse_x(), get_mouse_y()
    rays = []

    for i in range(ray_count):
        angle = (2*pi) * (i/ray_count)
        end = cast_ray((mx, my), angle, rects)
        rays.append((mx, my, *end))

    begin_drawing()
    clear_background(DARKGRAY)

    for rect in rects:
        draw_rectangle_rec(Rectangle(*rect), BLACK)


    draw_rectangle_rec(Rectangle(100, 100, 600, 100), BLACK)

    for start_wall in walls:
        draw_line_ex(Vector2(start_wall[0][0], start_wall[0][1]), Vector2(start_wall[1][0], start_wall[1][1]), 2, BLACK)

    for ray in rays:
        draw_line(int(ray[0]), int(ray[1]), int(ray[2]), int(ray[3]), YELLOW)

    draw_text("Click to place walls. Press R to reset walls.", 10, 10, 20, RAYWHITE)

    end_drawing()

close_window()