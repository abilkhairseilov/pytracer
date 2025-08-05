from typing import Any
from math import cos, sin, radians
from src.shapes import Rectangle, unregularPoly
import pyray

WIDTH = 800
HEIGHT = 600

pyray.init_window(WIDTH, HEIGHT, "2D Raytracer")
pyray.set_target_fps(60)

light = pyray.load_shader("", "static/light_mask.fs")
light_pos_index = pyray.get_shader_location(light, "light_pos")
max_radius_index = pyray.get_shader_location(light, "max_radius")
num_points_index = pyray.get_shader_location(light, "num_points")
points_index = pyray.get_shader_location(light, "points")

walls: list[tuple[tuple[int, int], tuple[int, int]]] = [
    ((100, 100), (700, 100)),
    ((700, 100), (700, 500)),
    ((700, 500), (100, 500)),
    ((100, 500), (100, 100)),
    # ((300, 300), (500, 400)),
    # ((500, 400), (300, 400)),
]

shapes = [
    Rectangle(200, 200, 100, 50, (255, 255, 255, 0)),
    unregularPoly(
        [(400, 300), (450, 350), (400, 400), (350, 350)], (255, 255, 255, 255)
    ),
]

ray_origin = pyray.Vector2(400, 300)


def ray_segment_intersect(ro, rd, p1, p2) -> tuple[float, float] | None:
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = ro
    x4, y4 = ro[0] + rd[0], ro[1] + rd[1]

    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if den == 0:
        return None  # Parallel

    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
    u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den

    if 0 <= t <= 1 and u >= 0:
        px = x1 + t * (x2 - x1)
        py = y1 + t * (y2 - y1)
        return (px, py)
    return None


def cast_rays(origin, walls, num_rays=360):
    hits = []
    for i in range(num_rays):
        angle = i * (360 / num_rays)
        rd = (cos(radians(angle)), sin(radians(angle)))
        closest = None
        min_dist = float("inf")
        for wall in walls:
            hit = ray_segment_intersect(origin, rd, *wall)
            if hit:
                dist = (hit[0] - origin[0]) ** 2 + (hit[1] - origin[1]) ** 2
                if dist < min_dist:
                    min_dist = dist
                    closest = hit
        for shape in shapes:
            for wall in shape.get_segments():
                hit = ray_segment_intersect(origin, rd, *wall)
                if hit:
                    dist = (hit[0] - origin[0]) ** 2 + (hit[1] - origin[1]) ** 2
                    if dist < min_dist:
                        min_dist = dist
                        closest = hit
        if closest:
            hits.append(closest)
    return hits


max_radius = 200
steps = 50


while not pyray.window_should_close():
    ray_origin = pyray.get_mouse_position()
    hits = cast_rays((ray_origin.x, ray_origin.y), walls, 360)

    pyray.set_shader_value(
        light,
        light_pos_index,
        pyray.Vector2(ray_origin.x, ray_origin.y),
        pyray.SHADER_UNIFORM_VEC2,
    )

    pyray.set_shader_value(
        light,
        max_radius_index,
        pyray.ffi.new("float *", max_radius),
        pyray.SHADER_UNIFORM_FLOAT,
    )
    pyray.set_shader_value(
        light,
        num_points_index,
        pyray.ffi.new("int *", len(hits)),
        pyray.SHADER_UNIFORM_INT,
    )
    if hits:
        flat_hits = [coord for hit in hits for coord in hit]
        arr = pyray.ffi.new("float[]", flat_hits)
        pyray.set_shader_value(
            light,
            points_index,
            arr,
            pyray.SHADER_UNIFORM_VEC2,
        )

    pyray.begin_shader_mode(light)
    pyray.draw_rectangle(0, 0, WIDTH, HEIGHT, pyray.WHITE)
    pyray.end_shader_mode()

    pyray.begin_drawing()
    pyray.clear_background(pyray.BLACK)

    for wall in walls:
        pyray.draw_line_ex(
            pyray.Vector2(*wall[0]), pyray.Vector2(*wall[1]), 2, pyray.WHITE
        )

    for hit in hits:
        pyray.draw_line_ex(
            pyray.Vector2(int(ray_origin.x), int(ray_origin.y)),
            pyray.Vector2(int(hit[0]), int(hit[1])),
            1.5,
            pyray.YELLOW,
        )
        pyray.draw_circle(int(hit[0]), int(hit[1]), 2, pyray.RED)

    for i in range(steps, 0, -1):
        radius = int(max_radius * i / steps)
        alpha = int(255 * (i / steps) * 0.2)  # Adjust 0.2 for overall intensity
        pyray.draw_circle(
            int(ray_origin.x),
            int(ray_origin.y),
            radius,
            pyray.Color(255, 255, 200, alpha),
        )
    for shape in shapes:
        shape.draw()

    pyray.end_drawing()

pyray.close_window()
