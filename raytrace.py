#AndresQ 18288 RT2
# Dependencies
from library import *
from sphere import *
from math import pi, tan
# Standard colors
Darks = color(0, 0, 0)
White = color(255, 255, 255)

class Raytracer(object):
  def __init__(self, width, height):
    self.width = width
    self.height = height
    self.background_color = White
    self.scene = []
    self.clear()
    self.light = None

  def clear(self):
    self.pixels = [
      [self.background_color for x in range(self.width)]
      for y in range(self.height)
    ]

  def write(self, filename):
    writebmp(filename, self.width, self.height, self.pixels)


  def point(self, x, y, c = None):
    try:
      self.pixels[y][x] = c or self.current_color
    except:
      pass

  def cast_ray(self, orig, direction):
    material, intersect = self.scene_intersect(orig, direction)

    if material is None:
      return self.background_color
    
    light_dir = norm(sub(self.light.position, intersect.point))
    light_distance = length(sub(self.light.position, intersect.point))

    offset_normal = mul(intersect.normal, 1.1) #Evita que se intercepte con el mismo
    shadow_orig = sub(intersect.point, offset_normal) if dot(light_dir, intersect.normal) < 0 else sum(intersect.point, offset_normal)
    shadow_material, shadow_intersect = self.scene_intersect(shadow_orig, light_dir)
    shadow_intensity = 0

    if shadow_material and length(sub(shadow_intersect.point, shadow_orig)) < light_distance:
      shadow_intensity = 0.9

    intensity = self.light.intensity * max(0, dot(light_dir, intersect.normal)) * (1 - shadow_intensity)

    reflection = reflect(light_dir, intersect.normal)
    specular_intensity = self.light.intensity * (
      max(0, -dot(reflection, direction))**material.spec
    )

    diffuse = material.diffuse * intensity * material.albedo[0]
    specular = color(255, 255, 255) * specular_intensity * material.albedo[1]
    return diffuse + specular

  def scene_intersect(self, orig, direction):
      zbuffer = float('inf')

      material = None
      intersect = None

      for obj in self.scene:
        hit = obj.ray_intersect(orig, direction)
        if hit is not None:
          if hit.distance < zbuffer:
            zbuffer = hit.distance
            material = obj.material
            intersect = hit

      return material, intersect

  def render(self):
    fov = int(pi/2)
    for y in range(self.height):
      for x in range(self.width):
        i =  (2*(x + 0.5)/self.width - 1) * tan(fov/2) * self.width/self.height
        j =  (2*(y + 0.5)/self.height - 1) * tan(fov/2)
        direction = norm(V3(i, j, -1))
        self.pixels[y][x] = self.cast_ray(V3(0,0,0), direction)



#oso izq
cuerpoizq = Material(diffuse = color(218, 223, 231), albedo = (1, 1, 1), spec = 30)


#oso der
cuerpoder = Material(diffuse = color(255, 203, 163), albedo = (1, 1, 1), spec = 30)
cuerpoder1 = Material(diffuse = color(255, 63, 52), albedo = (1, 1, 1), spec = 30) 
cuerpoder2 = Material(diffuse = color(210, 125, 70), albedo = (1, 1, 1), spec = 15)

#Plano
eye = Material(diffuse = Darks, albedo = (0.7,  0.4), spec = 35)

#init
r = Raytracer(1000, 1000)

#luz
r.light = Light(
  position=V3(0,0,20),
  intensity=1
)

r.background_color = White

r.scene = [
    
    #orejas
    Sphere(V3(3.4, 2.9, -9), 0.4, cuerpoder2),
    Sphere(V3(-3.4, 2.9, -9), 0.4, cuerpoizq),

    Sphere(V3(1.4, 2.9, -9), 0.4, cuerpoder2),
    Sphere(V3(-1.4, 2.9, -9), 0.4, cuerpoizq),
    
    #rostro
    Sphere(V3(2.5, 2, -10), 1.5, cuerpoder),
    Sphere(V3(-2.5, 2, -10), 1.5, cuerpoizq),
    #ojos
    Sphere(V3(-2.4, 2.1, -8), 0.1, eye),
    Sphere(V3(2.4, 2.1, -8), 0.1, eye),

    Sphere(V3(-1.7, 2.1, -8), 0.1, eye),
    Sphere(V3(1.7, 2.1, -8), 0.1, eye),
    #nariz
    Sphere(V3(2.4, 1.5, -9), 0.65, cuerpoder2),
    Sphere(V3(-2.4, 1.5, -9), 0.65, cuerpoizq),
    #punto de nariz
    Sphere(V3(-2.1, 1.7, -8), 0.1, eye),
    Sphere(V3(2.1, 1.7, -8), 0.1, eye),

    #panza
    Sphere(V3(2.5, -1, -10), 1.75, cuerpoder1),
    Sphere(V3(-2.5, -1, -10), 1.75, cuerpoizq),

    #brazos

    Sphere(V3(4, 0, -9), 0.6, cuerpoder),
    Sphere(V3(-4, 0, -9), 0.6, cuerpoizq),

    Sphere(V3(1, 0, -9), 0.6, cuerpoder),
    Sphere(V3(-1, 0, -9), 0.6, cuerpoizq),

    #piernas

    Sphere(V3(4, -2.5, -9), 0.70, cuerpoder),
    Sphere(V3(-4, -2.5, -9), 0.70, cuerpoizq),

    Sphere(V3(1, -2.5, -9), 0.70, cuerpoder),
    Sphere(V3(-1, -2.5, -9), 0.70, cuerpoizq),    
]
r.render()
r.write('out.bmp')