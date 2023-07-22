import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
import math

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800*4, 600*4
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cubo con sombreado Phong usando PyOpenGL y GLSL")

# Código del vértice GLSL
vertex_shader = """
#version 120
void main() {
    gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
}
"""

# Código del fragmento GLSL
fragment_shader = """
#version 120
void main() {
    gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0);  // Color rojo sólido para cada fragmento
}
"""

# Crear los programas de sombreado
def create_shader(shader_type, source):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)
    return shader

vertex_program = create_shader(GL_VERTEX_SHADER, vertex_shader)
fragment_program = create_shader(GL_FRAGMENT_SHADER, fragment_shader)

# Crear el programa de sombreado completo
shader_program = glCreateProgram()
glAttachShader(shader_program, vertex_program)
glAttachShader(shader_program, fragment_program)
glLinkProgram(shader_program)

# Validar el programa de sombreado
glValidateProgram(shader_program)
glUseProgram(shader_program)

# Función para dibujar el cubo con colores y sombreado Phong
def draw_cube():
    vertices = [
        (-1, -1, -1),
        (1, -1, -1),
        (1, 1, -1),
        (-1, 1, -1),
        (-1, -1, 1),
        (1, -1, 1),
        (1, 1, 1),
        (-1, 1, 1)
    ]

    # Especificar las caras del cubo
    faces = [
        (0, 1, 2, 3),
        (3, 2, 6, 7),
        (7, 6, 5, 4),
        (4, 5, 1, 0),
        (1, 5, 6, 2),
        (4, 0, 3, 7)
    ]

    glBegin(GL_QUADS)
    for face in faces:
        for i in range(4):
            glVertex3fv(vertices[face[i]])
    glEnd()

# Bucle principal
angle = 0
while True:
    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Configuración de la vista 3D
    glViewport(0, 0, WIDTH, HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (WIDTH / HEIGHT), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Posición de la cámara
    camera_distance = 7.0
    camera_x = camera_distance * math.sin(math.radians(angle))
    camera_z = camera_distance * math.cos(math.radians(angle))
    gluLookAt(camera_x, 0, camera_z, 0, 0, 0, 0, 1, 0)

    # Limpiar la pantalla
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Dibujar el cubo con sombreado Phong
    draw_cube()

    # Actualizar el ángulo de la cámara para la siguiente iteración
    angle += 1
    if angle >= 360:
        angle = 0

    # Actualizar la pantalla
    pygame.display.flip()

