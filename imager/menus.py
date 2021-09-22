"""
Drop-down menu support for the imager application

Because of the complexity of this application, we have spread the GUI code across several
modules.  This makes the code easier to read and comprehend.

This module contains all of the drop-down menus.  Because of the way that Kivy is 
structured, each menu (File..., Restore..., Reflect..., etc) needs its own class.
However, they all extend a base class with common functionality.

Based on an original file by Dexter Kozen (dck10) and Walker White (wmw2)

Author: Walker M. White (wmw2)
Date:   October 20, 2017 
"""
# These are the kivy parent classes
from kivy.uix.dropdown import DropDown
from kivy.properties import *

class MenuDropDown(DropDown):
    """
    The parent class for all drop-down menus.
    
    This class contains unified logic for all of the drop-down menus in this application.
    This includes the code for opening and closing the menu.
    """
    # These fields are 'hooks' to connect to the imager.kv file
    # The possible choices from the drop down menu
    options = DictProperty({})
    # The size of the drop down menu (set dynamically)
    rowspan = NumericProperty(0)
    
    def __init__(self,**keywords):
        """
        Initializer: Creates a new drop-down menu
        
        Drop-down menus take the same keywords as other widgets.  However, they have
        an important additional keyword: choices. This lists the possible valid responsese
        of this drop-down menu.
        
        In addition, each element of 'choices' is also a valid keyword of this drop-down
        menu.  This specifies the call function as a tuple.  The first element stores
        the function, while the remaining elements are the arguments.
        
        Parameter keyword: The Kivy (and drop-down menu) keyword arguments
        Precondition: keyword is a dictionary with string keys
        """
        if 'choices' in keywords:
            for choice in keywords['choices']:
                if choice in keywords:
                    self.options[choice] = keywords[choice]
                    del keywords[choice] # Gobble
            del keywords['choices'] # Gobble
        super().__init__(**keywords)
        self.bind(on_select=self.dochoice)
    
    def dochoice(self,instance,value):
        """
        Performs a call-back (provided one exists) based on the menu item selected
        
        The extra parameter instance is an artifact of how Kivy does things.  It is
        not used at all since it is the same as self. 
        
        Parameter instance: A reference to this object
        Precondition: instance is the same as self
        
        Parameter value: The menu option chosen
        Precondition: value is a string
        """
        if value in self.options:
            callback = self.options[value]
            func = callback[0]
            func(*callback[1:])
    
    def open(self,widget):
        """
        Opens this drop-down, making the provided widget its parent.
        
        The drop-down will be arranged vertically, either up or down, depending on
        the parent.
        
        Parameter widget: The parent widget to open the drop-down
        Precondition: widget is a Kivy Widget
        """
        self.rowspan = widget.height
        super().open(widget)


class FileDropDown(MenuDropDown):
    """
    A controller for the File drop-down, providing options for the File menu
    
    The View for this controller is defined in imager.kv.  This class simply contains
    the hooks for the view properties
    """
    # These fields are 'hooks' to connect to the imager.kv file
    # Load an image
    loadchoice = ObjectProperty(None)
    # Save an image
    savechoice = ObjectProperty(None)


class EditDropDown(MenuDropDown):
    """
    A controller for the Edit drop-down, providing options for the Edit menu
    
    The View for this controller is defined in imager.kv.  This class simply contains
    the hooks for the view properties
    """
    # These fields are 'hooks' to connect to the imager.kv file
    # Undo one edit step
    undochoice  = ObjectProperty(None)
    # Undo all edits
    clearchoice = ObjectProperty(None)


class AxisDropDown(MenuDropDown):
    """
    A controller for an Reflect drop-down, providing a choice between image axes.
    
    The View for this controller is defined in imager.kv.  This class simply contains
    the hooks for the view properties
    """
    # These fields are 'hooks' to connect to the imager.kv file
    # Flip horizontally
    horichoice = ObjectProperty(None)
    # Flip vertically
    vertchoice = ObjectProperty(None)

class TurnDropDown(MenuDropDown):
    """
    A controller for an Rotate drop-down, providing a choice of left or right
    
    The View for this controller is defined in imager.kv.  This class simply contains
    the hooks for the view properties
    """
    # These fields are 'hooks' to connect to the imager.kv file
    # Rotate left
    leftchoice = ObjectProperty(None)
    # Rotate right
    rghtchoice = ObjectProperty(None)

class GreyDropDown(MenuDropDown):
    """
    A controller for a Mono drop-down, providing a choice between monochromatic styles
    
    The View for this controller is defined in imager.kv.  This class simply contains
    the hooks for the view properties
    """
    # These fields are 'hooks' to connect to the imager.kv file
    # Make it traditional greyscale
    greychoice  = ObjectProperty(None)
    # Make it sepia tone
    sepiachoice = ObjectProperty(None)

class BlockDropDown(MenuDropDown):
    """
    A controller for a Pixellate drop-down, providing options for the block size
    
    The View for this controller is defined in imager.kv.  This class simply contains
    the hooks for the view properties
    """
    # These fields are 'hooks' to connect to the imager.kv file
    # 10 pixel block
    choice10 = ObjectProperty(None)
    # 20 pixel block
    choice20 = ObjectProperty(None)
    # 50 pixel block
    choice50 = ObjectProperty(None)
    # 100 pixel block
    choice100 = ObjectProperty(None)
    # 200 pixel block
    choice200 = ObjectProperty(None)