"""
The primary GUI interface for the imager filter application

The default application corresponds to the class FilterApp.  This app supports all of the
image processing other than the steganography exercise. This class is the root controller
for each of the View components defined in filter.kv.  The View (filter.kv) and this 
Controller module (filter.py) have the same name because they are so tightly
interconnected.

Based on an original file by Dexter Kozen (dck10) and Walker White (wmw2)

Author: Walker M. White (wmw2)
Date:   October 20, 2017 (Python 3 Version)
"""
# We have to configure the window before everything else
from kivy.config import Config
#Config.set('kivy', 'log_level', 'error')
Config.set('graphics', 'width', '1056')
Config.set('graphics', 'height', '587')
Config.set('graphics', 'resizable', '0') # make not resizable


from kivy.clock import Clock, mainthread
from kivy.properties import *
from kivy.app import App

from menus import *
from dialogs import *
from guibase import *


class FilterPanel(AppPanel):
    """
    This class is a controller for the imager filter application.
    
    This controller manages all of the buttons and text fields of the application. It 
    supports all parts of the assignment except the stegonagraphy challenge.
    
    The view for this application is defined the appropriate .kv file.
    """
    # These fields are 'hooks' to connect to the imager.kv file
    # The original image file (this will never change)
    origimage = ObjectProperty(None,allownone=True)
    # The menu bar
    menubar   = ObjectProperty(None)
    # The progress bar
    progress  = ObjectProperty(None)
    
    # The file drop-down menu
    filedrop  = ObjectProperty(None)
    # The edit drop-down menu
    editdrop  = ObjectProperty(None)
    # The reflect drop-down menu
    axisdrop  = ObjectProperty(None)
    # The monochromify drop-down menu
    greydrop  = ObjectProperty(None)
    # The rotate drop-down menu
    turndrop  = ObjectProperty(None)
    # The pixellate drop-down menu
    blockdrop = ObjectProperty(None)
    
    def config(self):
        """
        Configures the application at start-up.
    
        Controllers are responsible for initializing the application and creating all of 
        the other objects. This method does just that. It loads the currently selected 
        image file, and creates an editor for that file (if possible).
        """
        super().config()
        
        self.filedrop  = FileDropDown( choices=['load','save'], 
                                       save=[self.save_image], load=[self.load_image])
        self.editdrop  = EditDropDown( choices=['undo','reset'],
                                       undo=[self.undo], reset=[self.clear])
        self.axisdrop  = AxisDropDown( choices=['horizontal','vertical'],
                                       horizontal=[self.do_async,'reflectHori'], 
                                       vertical=[self.do_async,'reflectVert'])
        self.greydrop  = GreyDropDown( choices=['greyscale','sepia'],
                                       greyscale=[self.do_async,'monochromify',False], 
                                       sepia=[self.do_async,'monochromify',True])
        self.turndrop  = TurnDropDown( choices=['left','right'],
                                       left= [self.do_async,'rotateLeft'],
                                       right=[self.do_async,'rotateRight'])
        self.blockdrop = BlockDropDown(choices=['p10','p20','p50','p100', 'p200'],
                                       p10=[self.do_async,'pixellate',10],
                                       p20=[self.do_async,'pixellate',20],
                                       p50=[self.do_async,'pixellate',50],
                                       p100=[self.do_async,'pixellate',100],
                                       p200=[self.do_async,'pixellate',200])
        self.async_action = None
        self.async_thread = None
    
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
            if self.workspace.getOriginal():
                self.origimage.setImage(self.workspace.getOriginal())
            else:
                self.origimage.setImage(self.picture)
        except:
            self.workspace = None
            self.workimage.setImage(None)
            self.origimage.setImage(self.picture)
        self.canvas.ask_update()
    
    def do_async(self,*action):
        """
        Launchs the given action in an asynchronous thread
        
        The action parameters are an expanded list where the first element is a callable
        and any other elements are parameters to the callable.
        
        The thread progress is monitored by async_monitor.  When the thread is done, it
        will call async_complete in the main event thread.
        
        Parameter(s) *action: An expanded list defining the action
        Precondition: The first element of action is callable
        """
        import threading
        self.menubar.disabled = True
        self.workspace.increment()
        self.progress.value = 0
        self.async_action = Clock.schedule_interval(self.async_monitor,0.02)
        self.async_thread = threading.Thread(target=self.async_work,args=action)
        self.async_thread.start()

    def async_work(self,*action):
        """
        Performs the given action asynchronously.
        
        The action parameters are an expanded list where the first element is a callable
        and any other elements are parameters to the callable.
        
        This is the function that is launched in a separate thread.  Even if the action
        fails, it is guaranteed to call async_complete for clean-up
        
        Parameter(s) *action: An expanded list defining the action
        Precondition: The first element of action is callable
        """
        try:
            getattr(self.workspace,action[0])(*action[1:])
        except:
            traceback.print_exc()
            self.error('Action '+action[0]+' could not be completed')
        self.async_complete()
    
    def async_monitor(self,dt):
        """
        Updates the progress bar to represent the current processing state.
        
        This assumes that the worker thread is updating the pixels of the current image.
        If the student is (mistakenly) modifying another image, it will not work.
        """
        if self.async_action:
            image = self.workspace.getCurrent()
            self.progress.value = int(image.getPixels().progress()*self.progress.max)
     
    @mainthread
    def async_complete(self):
        """
        Cleans up an asynchronous thread after completion.
        """
        self.progress.value = self.progress.max
        self.workimage.update(self.workspace.getCurrent())
        self.async_thread.join()
        Clock.unschedule(self.async_action)
        self.async_thread = None
        self.async_action = None
        self.menubar.disabled = False
        self.canvas.ask_update()
    
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


class FilterApp(App):
    """
    This class is the imager filter application.
    
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
        panel = FilterPanel()
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
    FilterApp(image).run()
