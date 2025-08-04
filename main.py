from math import cos, sin, radians
import pyray

pyray.init_window(800, 600, "2D Raytracer")
pyray.set_target_fps(60)

walls = [
    ((100, 100), (700, 100)),
    ((700, 100), (700, 500)),
    ((700, 500), (100, 500)),
    ((100, 500), (100, 100)),
    ((300, 300), (500, 400)),
    ((500, 400), (300, 400)),
]

ray_origin = (400, 300)


def ray_segment_intersect(ro, rd, p1, p2):
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
    for angle in range(0, 360, 360 // num_rays):
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
        if closest:
            hits.append(closest)
    return hits


while not pyray.window_should_close():
    ray_origin = pyray.get_mouse_position()

    pyray.begin_drawing()
    pyray.clear_background(pyray.BLACK)

    # Draw walls
    for wall in walls:
        pyray.draw_line_ex(
            pyray.Vector2(*wall[0]), pyray.Vector2(*wall[1]), 2, pyray.WHITE
        )

    # Draw rays
    hits = cast_rays((ray_origin.x, ray_origin.y), walls, 360)
    for hit in hits:
        pyray.draw_line_ex(
            pyray.Vector2(int(ray_origin.x), int(ray_origin.y)),
            pyray.Vector2(int(hit[0]), int(hit[1])),
            1.0,
            pyray.YELLOW,
        )
        pyray.draw_circle(int(hit[0]), int(hit[1]), 2, pyray.RED)

    pyray.end_drawing()

pyray.close_window()
