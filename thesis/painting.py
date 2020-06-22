from individual import Individual

from PIL import Image, ImageDraw
from imgcompare import image_diff
from random import *

class DrawImage:
    def __init__(self, numPolygons, targetImage, background_color=(0, 0, 0)):
        self.width, self.height = targetImage.size
        self.targetImage = targetImage
        self.polygons = [Individual(self.width, self.height) for _ in range(numPolygons)]
        self.background_color = (*background_color, 255)

    @property
    def getImageWidth(self):
        return self.width

    @property
    def getImageHeight(self):
        return self.height
    
    @property
    def get_background_color(self):
        return self.background_color[:3]

    @property
    def numPolygons(self):
        return len(self.polygons)

    def mutatePolygons(self, rate=0.04, sigma=1.0):

        rand = random()
        if rand < rate:
            random_indices = list(range(self.numPolygons))
            shuffle(random_indices)
            # mutate random triangles
            for i in range(self.numPolygons):
                index = random_indices[i]
                self.polygons[index].mutate(sigma=sigma)


    def draw(self) -> Image:
        image = Image.new('RGBA', (self.width, self.height))
        draw = ImageDraw.Draw(image)
        draw.polygon([(0, 0), (0, self.height), (self.width, self.height), (self.width, 0)],
                     fill=self.background_color)

        for p in self.polygons:
            new_polygon = Image.new('RGBA', (self.width, self.height))
            pdraw = ImageDraw.Draw(new_polygon)
            pdraw.polygon([(x, y) for x, y in p.points], fill=p.color)
            
            image = Image.alpha_composite(image, new_polygon)
            
        return image


    @staticmethod
    def mate(a, b):
        aback = a.get_background_color
        bback = b.get_background_color
        new_background = (int((aback[i] + bback[i]) / 2) for i in range(3))
        
        child_a = DrawImage(0, a.targetImage, background_color=new_background)
        child_b = DrawImage(0, a.targetImage, background_color=new_background)

        for ap, bp in zip(a.polygons, b.polygons):
            if randint(0, 1) == 0:
                child_a.polygons.append(ap)
                child_b.polygons.append(bp)
            else:
                child_a.polygons.append(bp)
                child_b.polygons.append(ap)

        return child_a, child_b
    
    def image_diff(self, target: Image) -> float:
        source = self.draw()
        return image_diff(source, target)

