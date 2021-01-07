from PIL import Image, ImageDraw

class Polygon:
    
    def __leftop(p1, p2, p3):
        return (p2[1]-p1[1]) * (p3[0]-p1[0]) - \
               (p2[0]-p1[0]) * (p3[1]-p1[1])
    
    def __sort_points(points):
        
        def slope(p):
            p0 = points[0]
            try:
                z = (p0[1] - p[1]) / (p0[0] - p[0])
            except ZeroDivisionError:
               z = 0
            return z

        points.sort(key=lambda p: (p[0], p[1]))
        points = points[:1] + sorted(points[1:], key=slope)
        print(points)        
        return points

    def convex_hull(points):
        sorted_points = Polygon.__sort_points(points)
        convex_hull = []
        for p in sorted_points:
            while len(convex_hull) > 1 and Polygon.__leftop(convex_hull[-2], convex_hull[-1], p) >= 0:
                convex_hull.pop()
            convex_hull.append(p)
        return convex_hull

    def __init__(self, points):
        self.vertexs = Polygon.convex_hull(points)
    
    def print(self):
        for p in self.vertexs:
            print(p[0], p[1])



        
if __name__ == "__main__":
    points = [(0, 1), (0, 0), (1, 1), (0.2, 0.8)]
    P = Polygon(points)
    P.print()


