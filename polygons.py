from PIL import Image, ImageDraw
from functools import cmp_to_key
import math

class Polygon:
    
    # Find orientation of ordered triplet of points
    # == 0 --> Colinear
    # > 0 --> Clockwise
    # < 0 --> CounterClockwise
    def __leftop(p1, p2, p3):
        return (p2[1]-p1[1]) * (p3[0]-p1[0]) - \
               (p2[0]-p1[0]) * (p3[1]-p1[1])
    
    def distSq(p0,p1):
            return (p0[0] - p1[0]) * (p0[0] - p1[0]) + \
                (p0[1] - p1[1]) * (p0[1] - p1[1])


    def __sort_points(points):
        
        def compare(p1, p2):
            p0 = points[0]
            o = Polygon.__leftop(p0, p1, p2)
            if o == 0:
                return 1 if (Polygon.distSq(p0,p1) > Polygon.distSq(p0,p2)) else -1
            return 1 if o > 0 else -1

        points.sort(key=lambda p: (p[0], p[1]))
        points = points[:1] + sorted(points[1:], key=cmp_to_key(compare))
        
        def delete_same_slot(points):
            p0 = points[0]
            new_p = []
            i = 0
            while i < len(points):
                while i < (len(points)-1) and Polygon.__leftop(p0, points[i], points[i+1]) == 0:
                    i += 1
                new_p.append(points[i])
                i += 1
            return points[:1] + new_p
        new_points = delete_same_slot(points)
        return new_points

    def convex_hull(points):
        sorted_points = Polygon.__sort_points(points)
        convex_hull = []
        for p in sorted_points:
            while len(convex_hull) > 1 and Polygon.__leftop(convex_hull[-2], convex_hull[-1], p) >= 0:
                convex_hull.pop()
            convex_hull.append(p)
        return convex_hull

    def __init__(self, points):
        self.vertices = Polygon.convex_hull(points)
    
    def __str__(self):
        s = ''
        for p in self.vertices:
            s += "("+str(p[0]) + " " + str(p[1])+")  "
        return s
    
    def get_vertices(self):
        return self.vertices
    
    def get_vertex(self, i):
        return self.vertices[i]
    
    def get_vertex_x(self, i):
        return self.vertices[i][0]
    
    def get_vertex_y(self, i):
        return self.vertices[i][1]

    def get_n_vertices(self):
        return len(self.vertices)
    
    def __diagonal(p0,p1):
            return math.sqrt(Polygon.distSq(p0,p1))

    def get_perimeter(self):
        p = 0.0
        n = self.get_n_vertices()
        for i in range(n-1):
            p += Polygon.__diagonal(self.vertices[i], self.vertices[i+1])
        p += Polygon.__diagonal(self.vertices[-1], self.vertices[0])
        return p

    def get_area(self):
        a = 0.0
        n = self.get_n_vertices()
        for i in range (n-1):
            a += (self.get_vertex_x(i) * self.get_vertex_y(i+1)) - \
                 (self.get_vertex_y(i) * self.get_vertex_x(i+1))
        a += (self.get_vertex_x(-1) * self.get_vertex_y(0)) - \
             (self.get_vertex_y(-1) * self.get_vertex_x(0))
        return abs(0.5*a)

    def get_centroid(self):
        cx = cy = 0.0
        det = tempDet = 0.0
        j = 0
        n = self.get_n_vertices()
        for i in range (n-1):
            tempDet = (self.get_vertex_x(i) * self.get_vertex_y(i+1)) - \
                      (self.get_vertex_y(i) * self.get_vertex_x(i+1))
            det += tempDet
            cx += (self.get_vertex_x(i) + self.get_vertex_x(i+1))*tempDet
            cy += (self.get_vertex_y(i) + self.get_vertex_y(i+1))*tempDet

        tempDet = (self.get_vertex_x(-1) * self.get_vertex_y(0)) - \
                      (self.get_vertex_y(-1) * self.get_vertex_x(0))
        det += tempDet
        cx += (self.get_vertex_x(-1) + self.get_vertex_x(0))*tempDet
        cy += (self.get_vertex_y(-1) + self.get_vertex_y(0))*tempDet
        cx = cx / (3.0*det)
        cy = cy / (3.0*det)
        return (cx,cy)

    def is_regular(self):
        n = self.get_n_vertices()
        dist = Polygon.__diagonal(self.vertices[-1], self.vertices[0])
        for i in range(n-1):
            if dist != Polygon.__diagonal(self.vertices[i], self.vertices[i+1]):
                return False
        return True

    def draw(self, output):
        img = Image.new('RGB', (400, 400), 'White')
        dib = ImageDraw.Draw(img)
        n = 40
        dib.polygon([(399, 4*n - 1), (200, 4*n - 1), (399, 3*n)], 'Orange')
        img.save(output + '.png')

    def is_point_inside(self, p):
        n = self.get_n_vertices()
        for i in range(n-1):
            if Polygon.__leftop(self.get_vertex(i), self.get_vertex(i+1), p) > 0:
                return False
        if Polygon.__leftop(self.get_vertex(-1), self.get_vertex(0), p) > 0:
                return False
        return True
    
    def is_polygon_inside (self, Poly):
        points = Poly.get_vertices()
        for p in points:
            if not self.is_point_inside(p):
                return False
        return True
    
    def convex_union (list_P):
        points = []
        for P in list_P:
            points += P.get_vertices()
        return Polygon(points)

    def bounding_box(list_P):
        points = []
        for P in list_P:
            points += P.get_vertices()
        x_min = min(points, key=lambda p: p[0])[0]
        x_max = max(points, key=lambda p: p[0])[0]
        y_min = min(points, key=lambda p: p[1])[1]
        y_max = max(points, key=lambda p: p[1])[1]
        new_p = [(x_min, y_min), (x_max, y_min), (x_max, y_max), (x_min, y_max)]
        return Polygon(new_p)
    
    
    


        
if __name__ == "__main__":
    P = Polygon([(0, 1), (1, 1), (1,0), (0,0)])
    Q = Polygon([(1,0), (3,0), (2,2)])

    print("Perimeter: " + str(P.get_perimeter()))
    print("Area: " + str(P.get_area()))
    print("Centroid: " + str(P.get_centroid()))
    print("Is regular?: " + str(P.is_regular()))
    print("Is Q inside P: " + str(P.is_polygon_inside(Q)))
    print("Is P inside Q: " + str(Q.is_polygon_inside(P)))
    print("Perimeter: " + str(P.get_perimeter()))
    U = Polygon.convex_union([P,Q])
    print(U)
    B = Polygon.bounding_box([P,Q])
    print(B)