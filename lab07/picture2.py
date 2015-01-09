#!/usr/bin/env python
import math
try:
    import Image
    import ImageDraw
    import ImageTk
except ImportError:
    from PIL import Image, ImageDraw, ImageTk
import Tkinter as tk

_IS_RUNNING = False

class Picture():
    
    def __init__(self, width, height=None):
        '''
        Takes either a single string for a filename, or width and
        height of an empty picture.
        '''
        if height:
            self.image = Image.new('RGB', (width, height))
            self.title = 'Picture'
            self.width = width
            self.height = height
        else:
            self.image = Image.open(width) # actually filename
            self.title = width
            self.width, self.height = self.image.size
        # Default values for pen
        self.pen_color = (0, 0, 0)
        self.pen_position = (0, 0)
        self.pen_width = 1
        self.pen_rotation = 0
        # Pixel data of the image
        self.pixel = self.image.load()
        # Draw object of the image
        self.draw = ImageDraw.Draw(self.image)
        # The main window, and associated widgets.
        self.root = None
        self.canvas = None
    
    def display(self):
        'Displays the picture.'
        if self.root is None:
            global _IS_RUNNING
            if not _IS_RUNNING:
                self.root = tk.Tk()
                _IS_RUNNING = True
            else:
                self.root = tk.Toplevel() ##### border is highlightthickness
            self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, highlightthickness = 0)
            self.root.title(self.title)
            self.img = tk.PhotoImage(width=self.width, height=self.height)
            self.canvas.pack()
        self.img.put(self.data_to_string())        
        self.canvas.create_image(0, 0, image=self.img, anchor=tk.NW)
        
    def getWidth(self):
        'Returns the width of the picture.'
        return self.image.size[0]
    
    def getHeight(self):
        'Returns the height of the picture.'
        return self.image.size[1]
    
    def close(self):
        'Closes the picture.'
        if self.root:
            self.root.destroy()
            self.root = None
    
    def getPixelColor(self, x, y):
        'Returns the color of the pixel at (x, y).'
        return self.pixel[x, y]
    
    def getPixelRed(self, x, y):
        'Returns the red value of the pixel at (x, y).'
        return self.pixel[x, y][0]
    
    def getPixelBlue(self, x, y):
        'Returns the blue value of the pixel at (x, y).'
        return self.pixel[x, y][2]
    
    def getPixelGreen(self, x, y):
        'Returns the green value of the pixel at (x, y).'
        return self.pixel[x, y][1]
    
    def setPixelColor(self, x, y, r, g, b):
        'Sets the RGB value of the pixel at (x, y).'
        self.pixel[x, y] = (r, g, b)
        
    def setPixelRed(self, x, y, val):
        'Sets the red value of the pixel at (x, y).'
        green = self.pixel[x, y][1]
        blue = self.pixel[x, y][2]
        self.pixel[x, y] = (val, green, blue)
    
    def setPixelBlue(self, x, y, val):
        'Sets the blue value of the pixel at (x, y).'
        red = self.pixel[x, y][0]
        green = self.pixel[x, y][1]
        self.pixel[x, y] = (red, green, val)
    
    def setPixelGreen(self, x, y, val):
        'Sets the green value of the pixel at (x, y).'
        red = self.pixel[x, y][0]
        blue = self.pixel[x, y][2]
        self.pixel[x, y] = (red, val, blue)
    
    def setPenColor(self, r, g, b):
        'Sets the pen color.'
        self.pen_color = (r, g, b)
    
    def setPosition(self, x, y):
        'Sets the pen position.'
        self.setPenX(x)
        self.setPenY(y)
    
    def setPenX(self, x):
        'Sets the x coordinate of the pen.'
        self.pen_position = (x, self.pen_position[1])

    def setPenY(self, y):
        'Sets the y coordinate of the pen.'
        self.pen_position = (self.pen_position[0], y)
    
    def getPenWidth(self):
        'Returns the width of the pen.'
        return self.pen_width
        
    def setPenWidth(self, width):
        'Sets the width of the pen.'
        self.pen_width = width
    
    def rotate(self, theta):
        """
        Rotates the pen's angle of drawing by theta, where theta is in
        degrees.
        """
        self.pen_rotation += theta
        self.pen_rotation %= 360
    
    def setDirection(self, theta):
        """Sets the pen's direction to theta, where theta is in degrees."""
        self.pen_rotation = theta
        self.pen_rotation %= 360

    def getDirection(self):
        "Returns the pen's direction, in degrees."
        return self.pen_rotation
    
    def drawForward(self, distance):
        'Draws forward by the given distance.'
        radian = math.radians(self.pen_rotation)
        endX = self.pen_position[0] + math.cos(radian)*distance
        endY = self.pen_position[1] + math.sin(radian)*distance
        end = (endX, endY)
        self.draw.line((self.pen_position, end), fill=self.pen_color, width = self.pen_width)
        self.pen_position = end

    def drawLine(self, startX, startY, endX, endY):
        'Draws a line from (startX, startY) to (endX, endY).'
        self.draw.line(((startX, startY),(endX, endY)), fill=self.pen_color, width = self.pen_width)

    def drawCircle(self, x, y, radius):
        'Draws an empty circle at (x, y) with the given radius.'
        if (self.pen_width == 1):
            self.draw.ellipse((x-radius/2, y-radius/2,
                               x+radius/2, y+radius/2),
                              outline=self.pen_color)
        elif (self.pen_width < radius):
            for r in xrange(0, self.pen_width):
                tempRadius=radius-r
                self.draw.ellipse((x-tempRadius/2, y-tempRadius/2, x+tempRadius/2, y+tempRadius/2), outline=self.pen_color)
        else:
            self.drawCircleFill(x, y, radius)

    def drawCircleFill(self, x, y, radius):
        'Draws a filled circle at (x, y) with the given radius.'
        self.draw.ellipse((x-radius/2, y-radius/2,
                           x+radius/2, y+radius/2),
                          fill=self.pen_color)
    
    def fillPoly(self, xs, ys):
        '''
        Draws a filled polygon with vertices at (x, y) for each
        element in the two lists xs and ys.
        '''
        self.draw.polygon(list(zip(xs, ys)), fill=self.pen_color)
        
    def drawPoly(self, xs, ys):
        '''
        Draws an empty polygon with vertices at (x, y) for each
        element in the two lists xs and ys.
        '''
        if (self.pen_width == 1):
            self.draw.polygon(list(zip(xs, ys)), outline=self.pen_color)
        else:
            numVertices = len(list(xs))
            for x in xrange(0, numVertices-1):
                self.drawLine(xs[x], ys[x],xs[x+1], ys[x+1])
            self.drawLine(xs[numVertices-1], ys[numVertices-1], xs[0], ys[0])
    
    def drawRectFill(self, x, y, w, h):
        '''
        Draws a filled rectangle with vertices at (x, y) for each
        element in the two lists xs and ys.
        '''
        self.draw.rectangle(((x, y), (x+w, y+h)), fill=self.pen_color)

    def drawRect(self, x, y, w, h):
        '''
        Draws an empty rectangle with vertices at (x, y) for each
        element in the two lists xs and ys.
        '''
        if (self.pen_width == 1):
            self.draw.rectangle(((x, y), (x+w, y+h)), outline=self.pen_color)
        elif (int((self.pen_width+1)/2)>=w or int((self.pen_width+1)/2)>=h):
            self.drawRectFill(x, y, w, h)
        else:
            for r in xrange(0, int((self.pen_width+1)/2)):
                self.draw.rectangle(((x+r, y+r), (x-r+w, y-r+h)), outline=self.pen_color)
    
    def drawString(self, x, y, string):
        'Draws a string at (x, y).'
        self.draw.text((x, y), string, fill=self.pen_color)

    def writeFile(self, filename):
        'Writes the image to the given filename.'
        def write_file_func():
            self.image.save(filename)
        self._submit_operation(write_file_func)
        
    def data_to_string(self):
        "Turns a PIL pixel array into tkinter's rubbish color format."
        s = ''
        for col in xrange(self.height):
            s += '{'
            for row in xrange(self.width):
                s += ' ' + color_to_hex(self.pixel[row, col])
            s += '} '
        return s


def color_to_hex(color):
    ''
    return '#%02x%02x%02x'.upper() % color

if __name__ == '__main__':
    pic = Picture('sunset.ppm')
    pic2 = Picture('sunset.ppm')

    for col in range(pic.getHeight()):
        for row in range(pic.getWidth()):
            r1,g1,b1 = pic.getPixelColor(row,col)
            r2,g2,b2 = pic.getPixelColor(row,pic.getHeight()-1-col)
            pic2.setPixelColor(row, col, (r1+r2)/2,(g1+g2)/2,(b1+b2)/2)
    pic.display()
    pic2.display()
    x = raw_input('enter:')
    
