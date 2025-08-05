#version 330

uniform vec2 light_pos;
uniform float max_radius;
uniform int num_points;
uniform vec2 points[128]; // Pass your ray hits here

out vec4 fragColor;

// Point-in-polygon test
bool inside(vec2 p) {
    int crossings = 0;
    for (int i = 0; i < num_points; i++) {
        vec2 a = points[i];
        vec2 b = points[(i + 1) % num_points];
        if (((a.y > p.y) != (b.y > p.y)) &&
            (p.x < (b.x - a.x) * (p.y - a.y) / (b.y - a.y + 0.0001) + a.x))
            crossings++;
    }
    return (crossings % 2 == 1);
}

void main() {
    vec2 fragCoord = gl_FragCoord.xy;
    float dist = distance(fragCoord, light_pos);
    float intensity = 1.0 - dist / max_radius;
    intensity = clamp(intensity, 0.0, 1.0);

    if (inside(fragCoord) && intensity > 0.0)
        fragColor = vec4(1.0, 1.0, 0.8, intensity); // Light color
    else
        fragColor = vec4(0.0, 0.0, 0.0, 1.0); // Shadow
}