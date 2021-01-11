from PIL import Image, ImageDraw
from functools import cmp_to_key
import math


# Class that represents a convex polygon made of a set of points.
# Set of points is a list with tuples (x,y) to represent points.
# A convex polygon is a convex hull of a set of points.
# This class has also static methods to operate with convex polygons.
class ConvexPolygon:
    
    # ------------------ AUXILIAR FUNCTIONS ------------------

    # Find orientation of ordered triplet of points
    # == 0 --> Colinear
    # > 0 --> Clockwise
    # < 0 --> CounterClockwise
    def __leftop(p1, p2, p3):
        return (p2[1]-p1[1]) * (p3[0]-p1[0]) - \
               (p2[0]-p1[0]) * (p3[1]-p1[1])
    
    # Square distance of two points
    def __distSq(p0,p1):
            return (p0[0] - p1[0]) * (p0[0] - p1[0]) + \
                (p0[1] - p1[1]) * (p0[1] - p1[1])
    
    # Euclidean distance between 2 points
    def __diagonal(p0,p1):
            return math.sqrt(ConvexPolygon.__distSq(p0,p1))

    # Sort points by polar angle in counterclockwise order around leftmost point (p0)
    def __sort_points(points):
        
        # Compare polar angle of 2 points respect p0
        def compare(p1, p2):
            p0 = points[0]
            o = ConvexPolygon.__leftop(p0, p1, p2)
            if o == 0:
                # If same polar angle --> order by farthest
                return 1 if (ConvexPolygon.__distSq(p0,p1) > ConvexPolygon.__distSq(p0,p2)) else -1
            return 1 if o > 0 else -1
        
        # First point is p0, then sort by polar angle
        points.sort(key=lambda p: (p[0], p[1]))
        points = points[:1] + sorted(points[1:], key=cmp_to_key(compare))
        
        # If same polar angle --> take farthest point anf delete rest
        def delete_same_slot(points):
            p0 = points[0]
            new_p = []
            i = 0
            while i < len(points):
                while i < (len(points)-1) and ConvexPolygon.__leftop(p0, points[i], points[i+1]) == 0:
                    i += 1
                new_p.append(points[i])
                i += 1
            return points[:1] + new_p
        
        new_points = delete_same_slot(points)
        return new_points
    
    # Convex hull using Graham Scan (sort by polar angle and take it counterclockwise)
    # Temporal cost: O(n*log(n))
    def convex_hull(points):
        sorted_points = ConvexPolygon.__sort_points(points)
        convex_hull = []
        for p in sorted_points:
            while len(convex_hull) > 1 and ConvexPolygon.__leftop(convex_hull[-2], convex_hull[-1], p) >= 0:
                convex_hull.pop()
            convex_hull.append(p)
        return convex_hull


    # ------------------ INIT CLASS FUNCTIONS ------------------

    # Init instance given a set of points
    def __init__(self, points):
        self.color = (0,0,0)
        if len(points) < 3:
            self.vertices = points
        else: 
            self.vertices = ConvexPolygon.convex_hull(points)
    
    def __str__(self):
        s = ''
        for p in self.vertices:
            s += ("%.3f %.3f " % (p[0], p[1]))
        return s
    
    
    # ------------------ GETTERS FUNCTIONS ------------------

    # Get color
    def get_color(self):
        return self.color
    
    # Get all vertices
    def get_vertices(self):
        return self.vertices
    
    # Get vertex i
    def get_vertex(self, i):
        return self.vertices[i]
    
    # Get component x of vertex i
    def get_vertex_x(self, i):
        return self.vertices[i][0]
    
    # Get component y of vertex i
    def get_vertex_y(self, i):
        return self.vertices[i][1]

    # Get number of vertices (and edges)
    def get_n_vertices(self):
        return len(self.vertices)
    
    # Get perimeter of polygon
    def get_perimeter(self):
        p = 0.0
        n = self.get_n_vertices()
        if n < 2: return 0
        for i in range(n-1):
            p += ConvexPolygon.__diagonal(self.vertices[i], self.vertices[i+1])
        p += ConvexPolygon.__diagonal(self.vertices[-1], self.vertices[0])
        return p

    # Get area of polygon
    def get_area(self):
        a = 0.0
        n = self.get_n_vertices()
        if n < 3: return 0
        for i in range (n-1):
            a += (self.get_vertex_x(i) * self.get_vertex_y(i+1)) - \
                 (self.get_vertex_y(i) * self.get_vertex_x(i+1))
        a += (self.get_vertex_x(-1) * self.get_vertex_y(0)) - \
             (self.get_vertex_y(-1) * self.get_vertex_x(0))
        return abs(0.5*a)
    
    # Get centroid of polygon
    def get_centroid(self):
        cx = cy = 0.0
        det = tempDet = 0.0
        j = 0
        n = self.get_n_vertices()
        if n < 3: return 0
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


    # ------------------ SETTERS FUNCTIONS ------------------

    def set_color(self, color):
        self.color = color


    # ------------------ QUERY FUNCTIONS ------------------

    # True if polygon is regular (otherwise false)
    def is_regular(self):
        n = self.get_n_vertices()
        dist = ConvexPolygon.__diagonal(self.vertices[-1], self.vertices[0])
        for i in range(n-1):
            if dist != ConvexPolygon.__diagonal(self.vertices[i], self.vertices[i+1]):
                return False
        return True

    # True if point is inside polygon
    # Looks if point is at left of each continuous pair of vertices
    def is_point_inside(self, p):
        n = self.get_n_vertices()
        if n < 2: 
            if self.get_vertex(0) == p: return True
            return False
        for i in range(n-1):
            if ConvexPolygon.__leftop(self.get_vertex(i), self.get_vertex(i+1), p) > 0:
                return False
        if ConvexPolygon.__leftop(self.get_vertex(-1), self.get_vertex(0), p) > 0:
                return False
        return True
    
    # True if polygon Poly is inside it
    # Looks if each vertex of Poly is inside it
    def is_polygon_inside (self, Poly):
        points = Poly.get_vertices()
        for p in points:
            if not self.is_point_inside(p):
                return False
        return True

    # True if polygon Poly and instance polygon are equal
    # As all polygons are sorted, if equal -> must have same points at same position
    def is_equal (self, Poly):
        if self.get_n_vertices() != Poly.get_n_vertices(): return False
        for i in range(self.get_n_vertices()):
            if self.get_vertex(i) != Poly.get_vertex(i):
                return False
        return True
    
    # ------------------ OPERATE FUNCTIONS ------------------
    
    # Convex union of a list of polygons
    # Creates a new polygon (union) wich is the result of doing a convex hull of
    # all points of all polygons
    def convex_union (list_P):
        points = []
        for P in list_P:
            points += P.get_vertices()
        return ConvexPolygon(points)

    # Creates a bounding box paralel to x and y axis
    # Returns a bounding box polygon
    def bounding_box(list_P):
        points = []
        for P in list_P:
            points += P.get_vertices()
        x_min = min(points, key=lambda p: p[0])[0]
        x_max = max(points, key=lambda p: p[0])[0]
        y_min = min(points, key=lambda p: p[1])[1]
        y_max = max(points, key=lambda p: p[1])[1]
        new_p = [(x_min, y_min), (x_max, y_min), (x_max, y_max), (x_min, y_max)]
        return ConvexPolygon(new_p)
    
    def intersect(P, Q):

        subjectPolygon = P.get_vertices()
        clipPolygon = Q.get_vertices()

        def inside(p):
            return(cp2[0]-cp1[0])*(p[1]-cp1[1]) > (cp2[1]-cp1[1])*(p[0]-cp1[0])
 
        def computeIntersection():
            dc = [ cp1[0] - cp2[0], cp1[1] - cp2[1] ]
            dp = [ s[0] - e[0], s[1] - e[1] ]
            n1 = cp1[0] * cp2[1] - cp1[1] * cp2[0]
            n2 = s[0] * e[1] - s[1] * e[0] 
            n3 = 1.0 / (dc[0] * dp[1] - dc[1] * dp[0])
            return [(n1*dp[0] - n2*dc[0]) * n3, (n1*dp[1] - n2*dc[1]) * n3]
 
        outputList = subjectPolygon
        cp1 = clipPolygon[-1]
 
        for clipVertex in clipPolygon:
            cp2 = clipVertex
            inputList = outputList
            outputList = []
            s = inputList[-1]
 
            for subjectVertex in inputList:
                e = subjectVertex
                if inside(e):
                    if not inside(s):
                        outputList.append(computeIntersection())
                    outputList.append(e)
                elif inside(s):
                    outputList.append(computeIntersection())
                s = e
            cp1 = cp2
        return ConvexPolygon(outputList)


    # ------------------ DRAW FUNCTIONS ------------------

    # Draw polygon with its color
    # Re-escale polygon to git a 400x400px image
    # Save imatge with name output.png
    # FALTA REESCALAR AMB XMAX I YMAX!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    def draw(list_P, output):
        points = []
        for P in list_P:
            points += P.get_vertices()
        x_min = min(points, key=lambda p: p[0])[0]
        x_max = max(points, key=lambda p: p[0])[0]
        y_min = min(points, key=lambda p: p[1])[1]
        y_max = max(points, key=lambda p: p[1])[1]
        
        img = Image.new('RGB', (400, 400), 'White')
        dib = ImageDraw.Draw(img)

        def reescale(points):
            new_p = []
            for p in points:
                new_p.append(((399*(p[0]-x_min)/(x_max-x_min)),(399*(p[1]-y_min)/(y_max-y_min))))
            return new_p

        for P in list_P:
            rgb = tuple(int(255*x) for x in P.get_color())
            dib.polygon(reescale(P.get_vertices()), 'White', rgb)

        img.save(output)


        
if __name__ == "__main__":
    P = ConvexPolygon([(0, 0), (1, 1), (1,0), (0,1)])
    Q = ConvexPolygon([(0,1), (3,0), (2,2)])

    print("Perimeter: " + str(P.get_perimeter()))
    print("Area: " + str(P.get_area()))
    print("Centroid: " + str(P.get_centroid()))
    print("Is regular?: " + str(P.is_regular()))
    print("Is Q inside P: " + str(P.is_polygon_inside(Q)))
    print("Is P inside Q: " + str(Q.is_polygon_inside(P)))
    U = ConvexPolygon.convex_union([P,Q])
    print(U)
    B = ConvexPolygon.bounding_box([P,Q])
    print(B)
    I = ConvexPolygon.intersect(P,Q) 
    print(I)
    Q.set_color((0,1,0))
    ConvexPolygon.draw([Q,P], "hola")