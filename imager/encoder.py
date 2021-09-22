"""
The primary GUI interface for the imager encoding application

The default application corresponds to the class EncoderApp.  This app supports the
steganography part of the assignment. This class is the root controller for each of the 
View components defined in encoder.kv.  The View (encoder.kv) and this Controller module 
(encoder.py) have the same name because they are so tightly interconnected.

Based on an original file by Dexter Kozen (dck10) and Walker White (wmw2)

Author: Walker M. White (wmw2)
Date:   October 20, 2017 (Python 3 Version)
"""
# We have to configure the window before everything else
from kivy.config import Config
#Config.set('kivy', 'log_level', 'error')
Config.set('graphics', 'width', '1056')
Config.set('graphics', 'height', '556')
Config.set('graphics', 'resizable', '0') # make not resizable

from kivy.clock import Clock, mainthread
from kivy.properties import *
from kivy.app import App

from menus import *
from dialogs import *
from guibase import *


class EncoderPanel(AppPanel):
    """
    This class is a controller for the encoder application
    
    This controller manages all of the buttons and text fields of the application. 
    It can handle both image and text files, supporting the final task in the assignment.
    
    The View for this controller is defined in imager.kv.
    """
    # These fields are 'hooks' to connect to the imager.kv file
    # The menu bar
    menubar   = ObjectProperty(None)
    # The text box
    textpanel = ObjectProperty(None)
    
    # The image drop-down menu
    pictdrop  = ObjectProperty(None)
    # The text drop-down menu
    textdrop  = ObjectProperty(None)
    # The edit drop-down menu
    editdrop  = ObjectProperty(None)
    
    def config(self):
        """
        Configures the application at start-up.
    
        Controllers are responsible for initializing the application and creating all of 
        the other objects. This method does just that. It loads the currently selected 
        image file, and creates an editor for that file (if possible).
        """
        super().config()
        
        self.pictdrop  = FileDropDown( choices=['load','save'], 
                                       save=[self.save_image], load=[self.load_image])
        self.textdrop  = FileDropDown( choices=['load','save'], 
                                       save=[self.save_text], load=[self.load_text])
        self.editdrop  = EditDropDown( choices=['undo','reset'],
                                       undo=[self.undo], reset=[self.clear])
    
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
        super().place_image(path,filename)
        self.decode()
    
    def undo(self):
        """
        Undos the last edit to the image.
        
        This method will undo the last edit to the image.  If the ImageHistory class
        is not implemented correctly, this will display an error message onscreen as
        well as in the command line.
        """
        super().undo()
        self.decode()
    
    def clear(self):
        """
        Clears all edits to the image.
        
        This method will remove all edits to the image.  If the ImageHistory class
        is not implemented correctly, this will display an error message onscreen as
        well as in the command line.
        """
        super().clear()
        self.decode()
    
    def encode(self):
        """
        Encodes the message provided in the text panel into the image.
        
        This will not save the image, but it will store the result on the edit stack.
        """
        try:
            self.workspace.increment()
            if not self.workspace.encode(self.textpanel.hidden.text):
                self.error('The message could not be encoded')
                self.workspace.undo()
            else:
                self.workimage.update(self.workspace.getCurrent())
        except:
            traceback.print_exc()
            self.error('The message could not be encoded')
        
        self.textpanel.select(False)
    
    def decode(self):
        """
        Decodes the message from the image, and stores it in the text panel.
        
        This will display an error message if there is no hidden message.
        """
        try:
            message = self.workspace.decode()
            if message is None:
                self.error('No message was detected')
                self.textpanel.hidden.text = ''
            else:
                from kivy.metrics import sp
                self.textpanel.hidden.text = message
                height = max((message.count('\n')+1)*20*sp(1),self.textpanel.height)
                self.textpanel.hidden.height = height
        except:
            traceback.print_exc()
            self.error('The message could not be decoded')
        
        self.textpanel.select(False)
    
    def load_image(self):
        """
        Opens a dialog to load an image file.
        
        The dialog will take up most of the Window, and last until the user dismisses it.
        """
        self.load('Load image',self.place_image)
    
    def save_image(self):
        """
        Opens a dialog to save an image file.
        
        The dialog will take up most of the Window, and last until the user dismisses it.
        """
        self.save('Save image',self.check_save_png)
    
    def load_text(self):
        """
        Opens a dialog to load an image file.
        
        The dialog will take up most of the Window, and last until the user dismisses it.
        """
        self.load('Load message',self.place_text,['*.txt','*.py'])
    
    def save_text(self):
        """
        Opens a dialog to save an image file.
        
        The dialog will take up most of the Window, and last until the user dismisses it.
        """
        self.save('Save message',self.check_save_txt,['*.txt'])
    
    # Text loading helpers
    def place_text(self, path, filename):
        """
        Loads the text from file and stores the result in the text editor
        
        If it cannot read the text, this method does nothing.
        
        Parameter path: The base path to the file
        Precondition: path is a string
        
        Parameter filename: An absolute or relative filename
        Precondition: filename is a string
        """
        from kivy.metrics import sp
        
        import os.path
        self.dismiss_popup()
        
        if os.path.isabs(filename):
            file = filename
        else:
            file = os.path.join(path,filename)
        
        try:
            handle = open(file)
            text = handle.read()
            handle.close()
        except:
            traceback.print_exc()
            self.error('Could not load the text file')
            text = ''
        
        height = max((text.count('\n')+1)*20*sp(1),self.textpanel.height)
        
        self.textpanel.hidden.text = text
        self.textpanel.hidden.height = height
        self.textpanel.select(True)
    
    # Text saving helpers
    def check_save_txt(self, path, filename):
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
        
        if file.lower().endswith('.txt'):
            self.save_txt(file)
        else:
            file = os.path.splitext(file)[0]+'.txt'
            msg = 'File will be saved as {} in .txt format.\nProceed?'
            self.warn(msg.format(os.path.split(file)[1]), file, self.save_txt)

    def save_txt(self, filename):
        """
        Saves the current message text to a file, checking first if the file exists.
        
        If the file exist, this will display a warning.
        
        Parameter filename: An absolute filename
        Precondition: filename is a string
        """
        import os.path
        assert filename.lower().endswith('.png')
        self.dismiss_popup()
        if os.path.isfile(filename):
            msg = 'File {} exists.\nOverwrite?'
            self.warn(msg.format(os.path.split(filename)[1]), filename, self.force_txt)
        else:
            self.force_txt(filename)

    def force_txt(self, filename):
        """
        Saves the current message text, without user confirmation.
        
        Parameter filename: An absolute filename
        Precondition: filename is a string
        """
        self.dismiss_popup()
        
        # prepare image for saving
        text = self.textpanel.hidden.text
        try:
            file = open(filename,'w')
            file.write(text)
            file.close()
        except:
            self.error('Cannot save text file ' + os.path.split(filename)[1])


class EncoderApp(App):
    """
    This class is the imager encoder application.
    
    This class corresponds to the Kivy window and is charge of processing the primary
    event loop.  It is the root class for the application.
    """
    
    def __init__(self,file):
        """
        Initializer: Creates a new application window.
        
        If file is None, it will use the default application image (the instructor).
        
        Parameter file: The location of the initial image file.
        Precondition: file is a string or None.
        """
        super().__init__()
        self.source = file
    
    def build(self):
        """
        Reads kivy file and performs any initial layout
        """
        panel = EncoderPanel()
        if self.source:
            panel.source = self.source
        return panel

    def on_start(self):
        """
        Starts up the app and initializes values
        """
        super().on_start()
        self.root.config()


def launch(image):
    """
    Launches the application with the given image file.
    
    If file is None, it will use the default application image (the instructor).
    
    Parameter file: The location of the initial image file.
    Precondition: file is a string or None.
    """
    EncoderApp(image).run()
