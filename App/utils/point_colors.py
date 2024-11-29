import random

# Generate a list of random colors with higher opacity, avoiding white
def generate_point_colors(num_colors):
    colors = []
    for _ in range(num_colors):
        while True:
            r, g, b = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
            # Evita colores cercanos al blanco
            if not (r > 240 and g > 240 and b > 240):  
                break
        color = f'rgba({r}, {g}, {b}, 0.8)'  # Cambiado a 0.8 para mayor intensidad
        colors.append(color)
    return colors
