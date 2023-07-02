from array import array
from math import *
from tkinter import *
import numpy as np


class Engine(Tk):
    def __init__(self, height, width, back_color):
        super().__init__()
        self.geometry(str(height) + 'x' + str(width))
        self.canvas = Canvas(self, bg=back_color)
        self.canvas.pack(anchor='nw', fill='both', expand=1)
        self.img = PhotoImage(width=width, height=height)
        self.canvas.create_image(
            (height//2, width//2), image=self.img, state="normal")

    def Rectangle(self, x, y, height, width):
        return self.Rectangle_class(self, x, y, height, width)

    class Rectangle_class:
        def __init__(self, outer, x, y, height, width):
            self.outer = outer
            self.x = x
            self.y = y
            self.height = height
            self.width = width
            self.Points = np.array([[x, y], [x + width, y], [
                                   x + width, y + height], [x, y + height], [x, y]], int)
            self.DrawRectangle = self.DrawRectangle()

        def DrawRectangle(self):
            self.outer.verticies(self.Points)

        def Scale(self, Sx, Sy):
            self.Points = self.outer.Scale(Sx, Sy, self.Points)
            self.Points = np.array(
                [np.add(self.Points[0], np.array([-(Sx-1)*self.x, -(Sy-1)*self.y])), np.add(self.Points[1], np.array([-(Sx-1)*self.x, -(Sy-1)*self.y])), np.add(self.Points[2], np.array([-(Sx-1)*self.x, -(Sy-1)*self.y])), np.add(self.Points[3], np.array([-(Sx-1)*self.x, -(Sy-1)*self.y])), np.add(self.Points[0], np.array([-(Sx-1)*self.x, -(Sy-1)*self.y]))], int)
            self.outer.img.blank()
            self.outer.verticies(self.Points)
            return self

            # [np.add(ImageArray[0], np.array([-(Sx-1)*self.x, -(Sy-1)*self.y])), np.add(ImageArray[1], np.array([-(Sx-1)*self.x, -(Sy-1)*self.y])),
            # np.add(ImageArray[2], np.array([-(Sx-1)*self.x, -(Sy-1)*self.y])), np.add(ImageArray[3], np.array([-(Sx-1)*self.x, -(Sy-1)*self.y]))], np.add(ImageArray[0], np.array([-(Sx-1)*self.x, -(Sy-1)*self.y]))))
            #print(ImageArray[0], ImageArray[1], ImageArray[2], ImageArray[3])
            # print(np.add(ImageArray[0], np.array([-(Sx-1)*self.x, -(Sy-1)*self.y])), np.add(ImageArray[1], np.array([-(Sx-1)*self.x, -(Sy-1)*self.y])),
            # np.add(ImageArray[2], np.array([-(Sx-1)*self.x, -(Sy-1)*self.y])), np.add(ImageArray[3], np.array([-(Sx-1)*self.x, -(Sy-1)*self.y])))

        def Translate(self, Tx, Ty):
            self.x = self.x + Tx
            self.y = self.y + Ty
            self.Points = self.outer.Translate(Tx, Ty, self.Points)
            self.Points = np.array([
                self.Points[0], self.Points[1], self.Points[2], self.Points[3], self.Points[0]], int)
            self.outer.img.blank()
            self.outer.verticies(self.Points)
            return self

        def Rotate(self, teta):
            self.Points = self.outer.Rotate(teta, self.Points)
            self.Points = np.array([
                [self.x, self.y], self.Points[0], self.Points[1], self.Points[2], [self.x, self.y]], int)
            # print(ImageArray)
            self.outer.img.blank()
            self.outer.verticies(self.Points)
            return self

    def Draw_Line(self, x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1
        i = 1
        steps = 0
        xInc = 0
        yInc = 0
        if (abs(dx) >= abs(dy)):
            steps = abs(dx)
        else:
            steps = abs(dy)

        xInc = dx/steps
        yInc = dy/steps
        while (i <= steps):
            self.img.put('red', (floor(x1), floor(y1)))
            i += 1
            x1 += xInc
            y1 += yInc

    def lerp(a, b, percentage):
        point = a + (b - a)*percentage
        return (point)

    def BezierCurve(self, x1, y1, x2, y2, x3, y3, x4, y4, smothness):
        points = np.array([], int)
        for t in np.arange(0, 1, smothness):
            a = Engine.lerp(x1, x2, t)
            b = Engine.lerp(x2, x3, t)
            c = Engine.lerp(x3, x4, t)
            d = Engine.lerp(y1, y2, t)
            e = Engine.lerp(y2, y3, t)
            f = Engine.lerp(y3, y4, t)
            g = Engine.lerp(a, b, t)
            h = Engine.lerp(b, c, t)
            i = Engine.lerp(d, e, t)
            j = Engine.lerp(e, f, t)
            x = Engine.lerp(g, h, t)
            y = Engine.lerp(i, j, t)
            #print(int(x), int(y))
            points = np.append(points, np.array([int(x), int(y)], int))
            # print(len(points))
            self.img.put('red', (int(x), int(y)))
        # print(points)
        points = points.reshape(len(points)//2, 2)
        # print(points)
        Engine.verticies(self, points)

    def DrawEllipse(self, x0, y0, a, b):
        x = 0
        y = b
        p1 = (b**2) + (1/4 - b)*(a**2)
        p2 = 0
        while (y > 0):
            d = -((b**2)*x)/((a**2)*y)
            if (abs(d) <= 1):
                if (p1 >= 0):
                    p1 = p1 + (2*x + 3)*(b**2) + (-2*y + 2)*(a**2)
                    y -= 1
                else:
                    p1 = p1 + (2*x + 3)*(b**2)

                x += 1
                p2 = ((x + 0.5)**2)*(b**2)+((y - 1)**2)*(a**2) - (a*b)**2
            else:
                if (p2 >= 0):
                    p2 = p2 + (-2*y + 3)*(a**2)
                else:
                    p2 = p2 + (2*x + 2)*(b**2) + (-2*y + 3)*(a**2)
                    x += 1
                y -= 1
            self.img.put('red', (x0 + x, y0 + y))
            self.img.put('red', (x0 + x, y0 - y))
            self.img.put('red', (x0 - x, y0 - y))
            self.img.put('red', (x0 - x, y0 + y))

    def verticies(self, a: array):
        if (len(a) < 2):
            self.img.put('red', (a[0][0], a[0][1]))
        else:
            for i in range(len(a) - 1):
                Engine.Draw_Line(self, a[i][0], a[i][1], a[i+1][0], a[i+1][1])

    def DrawRectangle(self, x, y, width, height):
        Engine.verticies(self, np.array(
            [[x, y], [x + width, y], [x + width, y + height], [x, y + height], [x, y]]))

    def Scale(self, Sx, Sy, object: array):
        ImageArray = np.array([], int)
        for i in range(len(object)):
            ImageArray = np.append(ImageArray, np.array(
                [Sx*object[i][0], Sy*object[i][1]], int))
        ImageArray = np.reshape(ImageArray, (len(ImageArray)//2, 2))
        return ImageArray
        # print(ImageArray)

    def Translate(self, Tx, Ty, object: array):
        ImageArray = np.array([], int)
        for i in range(len(object)):
            ImageArray = np.append(ImageArray, np.add(
                object[i], np.array([Tx, Ty], int)))
        ImageArray = np.reshape(ImageArray, (len(ImageArray)//2, 2))
        return ImageArray

    def Rotate(self, teta, object: array):
        ImageArray = np.array([], int)
        for i in range(len(object) - 1):
            ImageArray = np.append(ImageArray, np.array(
                [(cos(teta)*(object[i+1][0] - object[0][0]) - sin(teta)*(object[i+1][1] - object[0][1]) + object[0][0]), (sin(teta)*(object[i+1][0] - object[0][0]) + cos(teta)*(object[i+1][1] - object[0][1]) + object[0][1])], int))
        ImageArray = np.reshape(ImageArray, (len(ImageArray)//2, 2))
        return ImageArray


if __name__ == "__main__":
    engine = Engine(500, 500, 'black')
    #engine.Draw_Line(100, 100, 200, 100)
    #engine.BezierCurve(200, 200, 250, 150, 300, 150, 400, 200, 0.1)
    #engine.DrawEllipse(300, 300, 50, 100)
    #engine.verticies(np.array([[200, 200], [215, 186], [230, 176]]))
    # engine.verticies(
    # np.array([[100, 100], [143, 125], [93, 211], [50, 186], [100, 100]]))
    #rectangle = engine.DrawRectangle(100, 100, 100, 50)
    # engine.Scale(2, 2, np.array(
    # [[100, 100], [200, 100], [200, 200], [100, 200], [100, 100]]))
    #rectangle = engine.Rectangle(250, 250, 100, 50)
    #rectangle.Scale(3, 3)
    # engine.Translate(50, 50, np.array(
    # [[100, 100], [200, 100], [200, 300], [100, 300]], int))
    #rectangle.Translate(-70, 150)
    # engine.__init__()

    # rectangle.Rotate(radians(60))
    engine.mainloop()
