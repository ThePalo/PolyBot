from PIL import Image, ImageDraw

class Polygon:
    def __init__(self, points):
        self.vertexs = convex_hull(points)

    @staticmethod
    def convex_hull(points):
        n = len(points)
        left = min(points, key = lambda p: p[0])
        
