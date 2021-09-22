"""
The primary controller module for the Imager application

This module provides all of the image processing operations that are called whenever you 
press a button. Some of these are provided for you and others you are expected to write
on your own.

Based on an original file by Dexter Kozen (dck10) and Walker White (wmw2)

Author: Walker M. White (wmw2), Philip Cipollina(pjc272), Luke Marcinkiewicz(lam365)
Date:    October 20, 2017 (Python 3 Version), November 16, 2017 (Assignment)
"""
import a6history
import math #for math.ceil-need to think of a better way


class Editor(a6history.ImageHistory):
    """
    A class that contains a collection of image processing methods
    
    This class is a subclass of ImageHistory.  That means it inherits all of the methods
    and attributes of that class.  We do that (1) to put all of the image processing
    methods in one easy-to-read place and (2) because we might want to change how we 
    implement the undo functionality later.
    
    This class is broken up into three parts (1) implemented non-hidden methods, (2)
    non-implemented non-hidden methods and (3) hidden methods.  The non-hidden methods
    each correspond to a button press in the main application.  The hidden methods are
    all helper functions.
    
    Each one of the non-hidden functions should edit the most recent image in the
    edit history (which is inherited from ImageHistory).
    """
    
    # PROVIDED ACTIONS (STUDY THESE)
    def invert(self):
        """
        Inverts the current image, replacing each element with its color complement
        """
        current = self.getCurrent()
        for pos in range(current.getLength()):
            rgb = current.getFlatPixel(pos)
            red   = 255 - rgb[0]
            green = 255 - rgb[1]
            blue  = 255 - rgb[2]
            rgb = (red,green,blue) # New pixel value
            current.setFlatPixel(pos,rgb)
    
    def transpose(self):
        """
        Transposes the current image
        
        Transposing is tricky, as it is hard to remember which values have been changed 
        and which have not.  To simplify the process, we copy the current image and use
        that as a reference.  So we change the current image with setPixel, but read
        (with getPixel) from the copy.
        
        The transposed image will be drawn on the screen immediately afterwards.
        """
        current  = self.getCurrent()
        original = current.copy()
        current.setWidth(current.getHeight())
        
        for row in range(current.getHeight()):
            for col in range(current.getWidth()):
                current.setPixel(row,col,original.getPixel(col,row))
    
    def reflectHori(self):
        """
        Reflects the current image around the horizontal middle.
        """
        current = self.getCurrent()
        for h in range(current.getWidth()//2):
            for row in range(current.getHeight()):
                k = current.getWidth()-1-h
                current.swapPixels(row,h,row,k)
    
    def rotateRight(self):
        """
        Rotates the current image left by 90 degrees.
        
        Technically, we can implement this via a transpose followed by a vertical
        reflection. However, this is slow, so we use the faster strategy below.
        """
        current  = self.getCurrent()
        original = current.copy()
        current.setWidth(current.getHeight())
        
        for row in range(current.getHeight()):
            for col in range(current.getWidth()):
                current.setPixel(row,col,original.getPixel(original.getHeight()-col-1,row))
    
    def rotateLeft(self):
        """
        Rotates the current image left by 90 degrees.
        
        Technically, we can implement this via a transpose followed by a vertical
        reflection. However, this is slow, so we use the faster strategy below.
        """
        current  = self.getCurrent()
        original = current.copy()
        current.setWidth(current.getHeight())
        
        for row in range(current.getHeight()):
            for col in range(current.getWidth()):
                current.setPixel(row,col,original.getPixel(col,original.getWidth()-row-1))
    
    
    # ASSIGNMENT METHODS (IMPLEMENT THESE)
    def reflectVert(self):
        """ 
        Reflects the current image around the vertical middle.
        """
        current = self.getCurrent()
        for n in range(current.getHeight()//2):
            for col in range(current.getWidth()):
                x=current.getHeight()-1-n
                current.swapPixels(n,col,x,col)
    
    def monochromify(self, sepia):
        """
        Converts the current image to monochrome, using either greyscale or sepia tone.
        
        If `sepia` is False, then this function uses greyscale.  It removes all color 
        from the image by setting the three color components of each pixel to that pixel's 
        overall brightness, defined as 
            
            0.3 * red + 0.6 * green + 0.1 * blue.
        
        If sepia is True, it makes the same computations as before but sets green to
        0.6 * brightness and blue to 0.4 * brightness.
        
        Parameter sepia: Whether to use sepia tone instead of greyscale.
        Precondition: sepia is a bool
        """
        assert isinstance(sepia,bool)
        current=self.getCurrent()
        for pos in range(current.getLength()):
            rgb=current.getFlatPixel(pos)
            brightness=rgb[0]*0.3+0.6*rgb[1]+0.1*rgb[2]
            red=int(round(brightness))
            if sepia==False:
                green=red
                blue=red
            else:
                green=int(round(brightness*0.6))
                blue=int(round(brightness*0.4))
            rgb=(red,green,blue)
            current.setFlatPixel(pos,rgb)
            
    
    def jail(self):
        """
        Puts jail bars on the current image
         
        The jail should be built as follows:
        * Put 3-pixel-wide horizontal bars across top and bottom,
        * Put 4-pixel vertical bars down left and right, and
        * Put n 4-pixel vertical bars inside, where n is (number of columns - 8) // 50.
        
        The n+2 vertical bars should be as evenly spaced as possible.
        """
        current=self.getCurrent()
        color=(255,0,0)
        n=(current.getWidth()-8)//50
        self._drawHBar(0,color) #draw top bar
        self._drawHBar(current.getHeight()-3,color) #draw bottom bar
        d=(current.getWidth()-4)/(n+1) #1 more gap than bars-subtract 4 for last bar width
        for x in range(0,n+2): #+2 accounts for border bars
            pos=round(d*(x))
            self._drawVBar(pos,color)
            #print('Bar #' + str(x) + ' drawn at ' + str(pos))


    
    def vignette(self):
        """
        Modifies the current image to simulates vignetting (corner darkening).
        
        Vignetting is a characteristic of antique lenses. This plus sepia tone helps
        give a photo an antique feel.
        
        To vignette, darken each pixel in the image by the factor
        
            1 - (d / hfD)^2
        
        where d is the distance from the pixel to the center of the image and hfD 
        (for half diagonal) is the distance from the center of the image to any of 
        the corners.
        """
        current=self.getCurrent()
        hfD=((current.getWidth()/2)**2+ (current.getHeight()/2)**2)  #constant- don't put in loop
        for row in range(current.getHeight()):
            for col in range(current.getWidth()):
                #print('Starting row ' + str(row) +', column ' + str(col))
                d=((row-(current.getHeight()/2))**2+
                    (col-(current.getWidth()/2))**2) #get d
                value=1-(d)/(hfD)
                p=current.getPixel(row,col)
                np=(round(value*p[0]), round(value*p[1]), round(value*p[2]))
                #round at end for accuracy                   
                current.setPixel(row,col,np)
    
    def pixellate(self,step):
        """
        Pixellates the current image to give it a blocky feel.
        
        To pixellate an image, start with the top left corner (e.g. the first row and
        column).  Average the colors of the step x step block to the right and down
        from this corner (if there are less than step rows or step columns, go to the
        edge of the image). Then assign that average to ALL of the pixels in that block.
        
        When you are done, skip over step rows and step columns to go to the next 
        corner pixel.  Repeat this process again.  The result will be a pixellated image.
        
        Parameter step: The number of pixels in a pixellated block
        Precondition: step is an int > 0
        """
        assert isinstance(step,int) and step>0
        current=self.getCurrent()
        for row in range(math.ceil(current.getHeight()/step)): #number of times to iterate
            x=row*step                                         #is height and width divided
            x1=x+step                                          #by step- always rounds up to
            if x1>current.getHeight():                         #prevent cutoffs
                x1=current.getHeight()     #makes sure size of picture is never exceeded
            for col in range(math.ceil(current.getWidth()/step)):
                y=col*step
                y1=y+step
                if y1>current.getWidth():
                    y1=current.getWidth()
                pos1, pos2=(x,y), (x1,y1)
                p=self._avg_color(pos1,pos2)
                [current.setPixel(b,a,p) for a in range(pos1[1],pos2[1]) for b
                 in range(pos1[0], pos2[0])]  #learned from Python API while trying to make function run faster
    
    def encode(self, text):
        """
        Returns: True if it could hide the given text in the current image; False otherwise.
        
        This method attemps to hide the given message text in the current image.  It uses
        the ASCII representation of the text's characters.  If successful, it returns
        True.
        
        If the text has more than 999999 characters or the picture does not have enough
        pixels to store the text, this method returns False without storing the message.
        
        To show that there is a message hidden in the image, a 2-letter string is
        encoded before the hidden message.  This results in a 1 in 10^12 chance
        of a false positive (1 in 1000 that a single pixel has the right values
        for 4 different pixels).  To communicate the length of the string,
        the following two pixels directly encode the length, i.e a length of
        12345 encodes the following two pixels as 012 and 345.
        
        Parameter text: a message to hide
        Precondition: text is a string
        """
        assert isinstance(text,str) #makes sure input is valid
        current=self.getCurrent()
        if len(text)>999999 or len(text)>(current.getWidth()*
                                          current.getHeight())-6:
            return False
        key='@#%&'  
        for _ in range(0,4):  #encodes key in first 4 pixels
            self._encode_pixel(_,ord(key[_])) #very unlikely to result in false positives
        self._encode_pixel(4,len(text)//1000)  #encodes length of the string in
        self._encode_pixel(5,len(text)%1000)   #next two pixels
        for z in range(len(text)):
            #print('z is '+ str(z))
            self._encode_pixel(z+6,ord(text[z]))   #encodes pixels from 6 to end of text
        #print(current.getPixels()[:(8+len(text))])
        return True

    
    def decode(self):
        """
        Returns: The secret message stored in the current image. 
        
        If no message is detected, it returns None
        """
        key, text= '', '' #accumulators
        for _ in range(0,4):   #finds the key at the beginning
            key=key+chr(self._decode_pixel(_))
        if key!='@#%&': #stop if it doesn't find the key
            return None
        r=int(str(self._decode_pixel(4))+str(self._decode_pixel(5))) #gets length
        for x in range(r):
            text+=chr(self._decode_pixel(x+6)) #calls helper on pixel at position
        return text
        
    
    
    # HELPER FUNCTIONS
    def _drawHBar(self, row, pixel):
        """
        Draws a horizontal bar on the current image at the given row.
        
        This method draws a horizontal 3-pixel-wide bar at the given row of the current
        image. This means that the bar includes the pixels row, row+1, and row+2.
        The bar uses the color given by the pixel value.
        
        Parameter row: The start of the row to draw the bar
        Precondition: row is an int, with 0 <= row  &&  row+2 < image height
        
        Parameter pixel: The pixel color to use
        Precondition: pixel is a 3-element tuple (r,g,b) where each value is 0..255
        """
        current = self.getCurrent()
        for col in range(current.getWidth()):
            current.setPixel(row,   col, pixel)
            current.setPixel(row+1, col, pixel)
            current.setPixel(row+2, col, pixel)

    def _drawVBar(self, col, pixel):
        """
        Draws a vertical bar on the current image at the given column.
        
        This method draws a vertical 4-pixel-wide bar at the given column of the
        current image. This means that the bar includes the pixels col, col+1,
        col+2, and col+3. The bar uses the color given by the pixel value.
        
        Parameter col: The start of the col to draw the bar
        Precondition: col is an int, with 0 <= col  &&  col+2 < image width
        
        Parameter pixel: The pixel color to use
        Precondition: pixel is a 3-element tuple (r,g,b) where each value is 0..255
        """
        current = self.getCurrent()
        for row in range(current.getHeight()):
            current.setPixel(row,   col, pixel)
            current.setPixel(row, col+1, pixel)
            current.setPixel(row, col+2, pixel)
            current.setPixel(row, col+3, pixel)
            
    def _avg_color(self,pos1,pos2):
        """
        Returns: the average pixel color for pixels between posl 1 and pos 2.
        
        This function returns a tuple representing the average red, green, and blue
        values of the pixels in the rangeobtained by summing each individual
        value and dividing by the number of pixels.
        
        Parameter pos1: The upper-left corner of the range.
        Precondition: pos1 is a tuple representing the row and column of a pixel
        object.
        Parameter pos2: The lower-right corner of the range.
        Precondition: pos2 is a tuple representing the row and column of a pixel
        object with both row and column greater than or equal to the row and column
        of pos1, respectively.
        """
        reds,greens,blues=0,0,0 #accumulators
        dx, dy, current = pos2[0]-pos1[0], pos2[1]-pos1[1], self.getCurrent()
        if dx==0 and dy==0:  #make sure that there are no errors if we end up
            return(pos1[0],pos1[1])              #with exactly one pixel left   
        elif dx==0 or dy==0:
            n=dy+dx   #if one and only one is zero, set n equal to the other (one row or column overflow)
        else:
            n=dx*dy
        for x in range(pos1[0],pos2[0]):    #sums all RGB values
            for y in range(pos1[1],pos2[1]):
                p=current.getPixel(x,y)
                reds=reds+p[0]
                greens=greens+p[1]
                blues=blues+p[2]
        #taking care of edge cases
        if dx==0:
            for y in range(pos1[1],pos2[1]):
                p=current.getPixel(pos1[0],y)
                reds=reds+p[0]
                greens=greens+p[1]
                blues=blues+p[2]
        if dy==0:
            for x in range(pos1[0],pos2[0]):
                p=current.getPixel(x,pos2[1])
                reds=reds+p[0]
                greens=greens+p[1]
                blues=blues+p[2]
        return (round(reds/n),round(greens/n),round(blues/n))

    def _decode_pixel(self, pos):
        """
        Returns: the number n that is hidden in pixel pos of the current image.
        
        This function assumes that the value was a 3-digit number encoded as the
        last digit in each color channel (e.g. red, green and blue).
        
        Parameter pos: a pixel position
        Precondition: pos is an int with  0 <= p < image length (as a 1d list)
        """
        rgb = self.getCurrent().getFlatPixel(pos)
        red   = rgb[0]
        green = rgb[1]
        blue  = rgb[2]
        return  (red % 10) * 100  +  (green % 10) * 10  +  blue % 10

    def _encode_pixel(self,pos,n):
        """
        Encodes a 3-digit number in the RGB value of the pixel at position pos
        
        Alters the pixel at the given position so the last digit of each RGB
        color value is a digit from n, with the red value getting the hundreds
        value of n, the green getting the tens, and the blue getting the ones.
        
        If changing the value of the last digit causes the value to exceed 255,
        10 is subtracted from the value so it is once again lower than 255 but
        maintains the necessary last digit.
        
        Example: If pixel at position pos is (123,27,99) and n is 111, the pixel
        is changed to (121,21,91).  If the pixel is (255,20,7) and n is 780, the
        new pixel is (247,28,0).
        
        Parameter pos: a pixel position
        Precondition: pos is an int with  0 <= p < image length (as a 1d list)
        Parameter n: The value to be encoded.
        Precondition: n is an int of at most 3 digits(0<=n<=999)
        """
        #print('n is '+str(n))
        #print('pos is '+str(pos))
        pixel=self.getCurrent().getFlatPixel(pos)  #create pixel
        red,green,blue = str(pixel[0]),str(pixel[1]),str(pixel[2])  #get rgb values as strings
                                                                    #easier to operate on
        red=red[:-1]+str(n//100)   #replace last digit with proper place from n
        green=green[:-1]+str((n//10)%10)   
        blue=blue[:-1]+str(n%10)
        #print('red final is '+str(red))
        rgb=[int(red),int(green),int(blue)]  
        for x in [0,1,2]:              #takes care of 'greater than 255' error       
            if rgb[x]>255:
                rgb[x]-=10
        rgb=tuple(rgb)
        self.getCurrent().setFlatPixel(pos,rgb) #sets the pixel to the right value
        
        
        
        
        
       
        