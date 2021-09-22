"""
The common GUI application base for the imager application.

The GUI part of the imager application is split into two parts: one for the Instagram
style filters, and another for the message encoding.  Because of how Kivy works, each
of these requires a distinct module and .kv file.

However, there is alot of shared functionality.  Therefore, this module defines the 
base classes with common code for the two applications.
The primary GUI interface for the imager application

The application corresponds to the class ImagerApp.  This class if is the root controller
for each of the View components defined in imager.kv.  The View (imager.kv) and this 
Controller module (imager.py) have the same name because they are so tightly
interconnected.

In addition, this file contains several class for pop-up gui elements like drop-down
menus and dialogs.

Based on an original file by Dexter Kozen (dck10) and Walker White (wmw2)

Author: Walker M. White (wmw2)
Date:   October 20, 2017 (Python 3 Version)
"""
from kivy.properties import *
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.graphics.texture import Texture

from dialogs import *

import traceback


class ImagePanel(Widget):
    """
    A controller for an ImagePanel, an widget to display an image on screen.
    
    An image panel displays an Image object for the user to see.  This GUI requires
    that the student have completed the Image class.  However, it does not require
    that the student have completed anything else.
    
    The view for this application is defined the appropriate .kv file. This class simply 
    contains the hooks for the view properties.  In addition, it has several helpful 
    methods for image processing.
    """
    # These fields are 'hooks' to connect to the imager.kv file
    # The image, represented as an Image object
    picture = ObjectProperty(None,allownone=True)
    # The image, represented as a Texture object
    texture = ObjectProperty(None)
    # The "interior" dimensions of this panel (ignoring the border)
    inside   = ListProperty((0,0))
    # The display size of the current image
    imagesize = ListProperty((0,0))
    # The position offset of the current image
    imageoff  = ListProperty((0,0))
    
    @classmethod
    def getResource(self,filename):
        """
        Returns: The absolute pathname for a file stored in the imager package folder.
        
        This is a class method that allows all objects of this class to load any
        image file stored in the imager folder.  Without it, we have to specify the
        full path to the file (which may vary depending on your installation).
        
        Parameter filename: The relative name of the file
        Precondition: filename is a string
        """
        import os.path
        dir = os.path.split(__file__)[0]
        return os.path.join(dir,filename)
    
    def setImage(self,picture):
        """
        Returns: True if the image panel successfully displayed picture
        
        This method sets the given picture to be the image of this panel, and returns
        True if it is successful.  If it fails, the texture is erased and the method
        returns false.
        
        Parameter picture: The image to display
        Precondition: picture is an Image object or None
        """
        import a6image
        try:
            self.picture = picture
            self.texture = Texture.create(size=(picture.getWidth(), picture.getHeight()), colorfmt='rgb', bufferfmt='ubyte')
            self.texture.blit_buffer(picture.getPixels().buffer, colorfmt='rgb', bufferfmt='ubyte')
            self.texture.flip_vertical()
            
            if self.texture.width < self.texture.height:
                self.imagesize[0] = int(self.inside[0]*(self.texture.width/self.texture.height))
                self.imagesize[1] = self.inside[1]
            elif self.texture.width > self.texture.height:
                self.imagesize[0] = self.inside[0]
                self.imagesize[1] = int(self.inside[1]*(self.texture.height/self.texture.width))
            else:
                self.imagesize = self.inside
        
            self.imageoff[0] = (self.size[0]-self.imagesize[0])//2
            self.imageoff[1] = (self.size[1]-self.imagesize[1])//2
            return True
        except:
            pass
        
        self.picture = None
        self.texture = None
        self.imagesize = self.inside
        self.imageoff[0] = (self.size[0]-self.imagesize[0])//2
        self.imageoff[1] = (self.size[1]-self.imagesize[1])//2
        return False
        
    def update(self,picture):
        """
        Returns: True if the image panel successfully displayed picture
        
        This method is slightly faster than setImage in the case where the picture
        is a (dimension-preserving) modification of the current one.  Otherwise it calls
        setImage.
        
        Parameter picture: The image to display
        Precondition: picture is an Image object or None
        """
        try:
            assert picture.getWidth() == self.texture.width
            self.picture = picture
            self.texture.blit_buffer(self.picture.getPixels().buffer, colorfmt='rgb', bufferfmt='ubyte')
            return True
        except:
            pass
        
        return self.setImage(picture)


class MessagePanel(Widget):
    """
    A controller for a MessagePanel, an widget to display scrollable text.
    
    An message panel displays the hidden message for the stenography part of the 
    assignment. It does not require any student code to function.
    
    The view for this application is defined the appropriate .kv file. This class simply 
    contains the hooks for the view properties.
    """
    # These fields are 'hooks' to connect to the imager.kv file
    # The text input field
    hidden = ObjectProperty(None)
    # The background color
    textclr = ListProperty([1, 1, .9, 1])
    
    @classmethod
    def getResource(self,filename):
        """
        Returns: The absolute pathname for a file stored in the imager package folder.
        
        This is a class method that allows all objects of this class to load any
        image file stored in the imager folder.  Without it, we have to specify the
        full path to the file (which may vary depending on your installation).
        
        Parameter filename: The relative name of the file
        Precondition: filename is a string
        """
        import os.path
        dir = os.path.split(__file__)[0]
        return os.path.join(dir,filename)
    
    def select(self,flag):
        """
        Changes the background color to notify of uncommitted changes
        
        Parameter flag: True if there are uncommitted changes
        Precondition: flag is a boolean
        """
        if flag:
            self.textclr = [.9, .9,  1,  1]
        else:
            self.textclr = [  1, 1, .9,  1]


class AppPanel(BoxLayout):
    """
    A base controller for all imager applications.

    This controller manages all of the buttons and text fields of the application. Since
    both application (Filter and Encode) need drop-down menu support, file saving and
    loading, and image display support, it provides this functionaly.
    
    The view for this application is defined the appropriate .kv file.
    """
    # These fields are 'hooks' to connect to the .kv file
    # The source file for the initial image
    source = StringProperty(ImagePanel.getResource('im_walker.png'))
    # The Image object for the loaded file
    picture   = ObjectProperty(None,allownone=True)
    # The editor object for working on the file
    workspace = ObjectProperty(None,allownone=True)
    # The most recent file edit
    workimage = ObjectProperty(None,allownone=True)
    
    def config(self):
        """
        Configures the application at start-up.
    
        Controllers are responsible for initializing the application and creating all of 
        the other objects. This method does just that. It loads the currently selected 
        image file, and creates an editor for that file (if possible).
        """
        # For working with pop-ups (Hidden since not .kv aware)
        self._popup = None
        self.place_image('',self.source)
    
    def undo(self):
        """
        Undos the last edit to the image.
        
        This method will undo the last edit to the image.  If the ImageHistory class
        is not implemented correctly, this will display an error message onscreen as
        well as in the command line.
        """
        try:
            self.workspace.undo()
            self.workimage.update(self.workspace.getCurrent())
            self.canvas.ask_update()
        except:
            traceback.print_exc()
            self.error('An error occurred when trying to undo')
        
    def clear(self):
        """
        Clears all edits to the image.
        
        This method will remove all edits to the image.  If the ImageHistory class
        is not implemented correctly, this will display an error message onscreen as
        well as in the command line.
        """
        try:
            self.workspace.clear()
            self.workimage.update(self.workspace.getCurrent())
            self.canvas.ask_update()
        except:
            traceback.print_exc()
            self.error('An error occurred when trying to clear edits')
    
    def read_image(self, file):
        """
        Returns: An Image object for the give file.
        
        If it cannot read the image (either Image is not defined or the file is not
        an image file), this method returns None.
        
        Parameter file: An absolute path to an image file
        Precondition: file is a string
        """
        import pixels
        import array
        import a6image
        from PIL import Image as CoreImage

        try:
            image = CoreImage.open(file)
            image = image.convert("RGB")
            flatten = []
            for pixel in image.getdata():
                flatten.append(pixel[0])
                flatten.append(pixel[1])
                flatten.append(pixel[2])
            buffer = array.array('B',flatten)
            size  = image.size[0]*image.size[1]
            width = image.size[0]
        except:
            traceback.print_exc()
            self.error('Could not load the image file')
            buffer = None
        
        result = None
        if not buffer is None:
            data = pixels.Pixels(0)
            data._size   = size
            data._buffer = buffer
            try:
                result = a6image.Image(data,width)
            except:
                traceback.print_exc()
                result = None
        return result
    
    def place_image(self, path, filename):
        """
        Loads the image from file and stores the result in the image panel(s)
        
        If it cannot read the image (either Image is not defined or the file is not
        an image file), this method does nothing.
        
        Parameter path: The base path to the file
        Precondition: path is a string
        
        Parameter filename: An absolute or relative filename
        Precondition: filename is a string
        """
        import os.path
        self.dismiss_popup()
        
        if os.path.isabs(filename):
            file = filename
        else:
            file = os.path.join(path,filename)
        
        import a6editor
        self.picture = self.read_image(file)
        try:
            self.workspace = a6editor.Editor(self.picture)
            self.workimage.setImage(self.workspace.getCurrent())
        except:
            self.workspace = None
            self.workimage.setImage(self.picture)
        self.canvas.ask_update()
    
    # Dialog options
    def load(self,title,callback, filters=None):
        """
        Opens a dialog to load a file.
        
        The dialog will take up most of the Window, and last until the user dismisses it.
        
        Parameter title: The title to display
        Precondition: title is a string
        
        Parameter callback: The callback to invoke on load
        Precondition: callback is callable
        """
        content = LoadDialog(loadchoice=callback, exitchoice=self.dismiss_popup)
        if filters:
            content.filechooser.filters = filters
        self._popup = Popup(title=title, content=content,size_hint=(0.8,0.9))
        self._popup.open()

    def save(self,title,callback,filters=None):
        """
        Opens a dialog to save a file.
        
        The dialog will take up most of the Window, and last until the user dismisses it.
        
        Parameter title: The title to display
        Precondition: title is a string
        
        Parameter callback: The callback to invoke on save
        Precondition: callback is callable
        """
        content = SaveDialog(savechoice=callback, exitchoice=self.dismiss_popup)
        if filters:
            content.filechooser.filters = filters
        self._popup = Popup(title=title, content=content,size_hint=(0.8,0.9))
        self._popup.open()

    def error(self, msg):
        """
        Opens a dialog to report an error to the user
        
        The dialog will take up most of the Window, and last until the user dismisses it.
        
        Parameter msg: the error message
        Precondition: msg is a string
        """
        assert type(msg) == str, repr(msg)+' is not a string'
        content = ErrorDialog(message=msg, okchoice=self.dismiss_popup)
        self._popup = Popup(title='Error', content=content, size_hint=(0.4, 0.4))
        self._popup.open()
    
    def warn(self, msg, data, callback):
        """
        Alerts the user of an issue when trying to load or save a file
        
        The dialog will take up most of the Window, and last until the user dismisses it.
        
        Parameter msg: the error message
        Precondition: msg is a string
        
        Parameter data: the problematic file
        Precondition: data is a string
        
        Parameter callback: The callback to invoke on ok
        Precondition: callback is callable
        """
        content = WarningDialog(message=msg, payload=data, okchoice=callback, exitchoice=self.dismiss_popup)
        self._popup = Popup(title='Warning', content=content, size_hint=(0.4, 0.4))
        self._popup.open()

    def dismiss_popup(self):
        """
        Dismisses the currently active pop-up
        """
        if self._popup:
            self._popup.dismiss()
            self._popup = None
    
    # Image saving helpers
    def check_save_png(self, path, filename):
        """
        Saves the current image to a file, checking first that the format is PNG
        
        If user uses another extension, or no extension at all, this method forces
        the file to be a .png
        
        Parameter path: The base path to the file
        Precondition: path is a string
        
        Parameter filename: An absolute or relative filename
        Precondition: filename is a string
        """
        import os.path
        self.dismiss_popup()
        
        if os.path.isabs(filename):
            file = filename
        else:
            file = os.path.join(path,filename)
        
        if file.lower().endswith('.png'):
            self.save_png(file)
        else:
            file = os.path.splitext(file)[0]+'.png'
            msg = 'File will be saved as {} in .png format.\nProceed?'
            self.warn(msg.format(os.path.split(file)[1]), file, self.save_png)

    def save_png(self, filename):
        """
        Saves the current image to a file, checking first if the file exists.
        
        If the file exist, this will display a warning.
        
        Parameter filename: An absolute filename
        Precondition: filename is a string
        """
        import os.path
        assert filename.lower().endswith('.png')
        self.dismiss_popup()
        if os.path.isfile(filename):
            msg = 'File {} exists.\nOverwrite?'
            self.warn(msg.format(os.path.split(filename)[1]), filename, self.force_png)
        else:
            self.force_png(filename)

    def force_png(self, filename):
        """
        Saves the current image, without user confirmation.
        
        Parameter filename: An absolute filename
        Precondition: filename is a string
        """
        import os.path
        import traceback
        self.dismiss_popup()
        
        # prepare image for saving
        from PIL import Image as CoreImage

        # This worked (Unlike Kivy)!  But is slow.
        current = self.workspace.getCurrent()
        try:
            im = CoreImage.new('RGBA',(current.getWidth(),current.getHeight()))
            im.putdata(tuple(current.getPixels()))
            im.save(filename,'PNG')
        except:
            traceback.print_exc()
            self.error('Cannot save image file ' + os.path.split(filename)[1])