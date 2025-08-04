from dataclasses import dataclass
from typing import override
import pyray

@dataclass
class Shape:
    position: tuple[float, float]
    color: tuple[int, int, int, int] = (255, 255, 255, 255)
    
    def draw(self) -> None:
        pass  # Base drawing method

class Rectangle(Shape):
    def __init__(self, x: float, y: float, width: float, height: float, color: tuple[int, int, int, int] = (255, 255, 255, 255), rotation: float = 0.0):
        super().__init__((x, y), color)
        self.rotation: float = rotation
        self.width: float = width
        self.height: float = height
        self.segments: list[tuple[tuple[float, float], tuple[float, float]]] = self._create_segments()
    
    def _create_segments(self) -> list[tuple[tuple[float, float], tuple[float, float]]]:
        x, y = self.position
        w, h = self.width, self.height
        return [
            ((x, y), (x + w, y)),          # top
            ((x + w, y), (x + w, y + h)),  # right
            ((x + w, y + h), (x, y + h)),  # bottom
            ((x, y + h), (x, y))           # left
        ]
    
    def get_segments(self) -> list[tuple[tuple[float, float], tuple[float, float]]]:
        return self.segments
    
    def draw(self) -> None:
        # Draw filled rectangle
        x, y = self.position
        pyray.draw_rectangle(
            int(x),
            int(y),
            int(self.width),
            int(self.height),
            pyray.Color(*self.color)
        )
        
        # Draw outline
        for segment in self.segments:
            pyray.draw_line_ex(
                pyray.Vector2(*segment[0]),
                pyray.Vector2(*segment[1]),
                2,
                pyray.WHITE
            )

class unregularPoly(Shape):
    def __init__(self, points: list[tuple[float, float]], color: tuple[int, int, int, int] = (255, 255, 255, 255)):
        super().__init__((0, 0), color)
        self.points = points
        self.segments = self._create_segments()

    def _create_segments(self) -> list[tuple[tuple[float, float], tuple[float, float]]]:
        segments = []
        for i in range(len(self.points)):
            start = self.points[i]
            end = self.points[(i + 1) % len(self.points)]
            segments.append((start, end))
        return segments

    def get_segments(self) -> list[tuple[tuple[float, float], tuple[float, float]]]:
        return self.segments

    def draw(self) -> None:
        if len(self.points) < 3:
            vertices = [pyray.Vector2(*point) for point in self.points]
            pyray.draw_triangle_fan(
                vertices,
                len(self.points),
                pyray.Color(*self.color)
            )

        for segment in self.segments:
            pyray.draw_line_ex(
                pyray.Vector2(*segment[0]),
                pyray.Vector2(*segment[1]),
                2,
                pyray.Color(*self.color)
            )