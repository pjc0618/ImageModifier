"""
Dialog box support for the imager application

Because of the complexity of this application, we have spread the GUI code across several
modules.  This makes the code easier to read and comprehend.

This module contains all of the drop-down menus.  Because of the way that Kivy is 
structured, each dialog (load, save, error, etc) needs its own class.

Based on an original file by Dexter Kozen (dck10) and Walker White (wmw2)

Author: Walker M. White (wmw2)
Date:   October 20, 2017 (Python 3 Version)
"""
# These are the kivy parent classes
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import *

class LoadDialog(BoxLayout):
    """
    A controller for a LoadDialog, a pop-up dialog to load a file.
    
    The View for this controller is defined in imager.kv.  This class simply contains
    the hooks for the view properties
    """
    # These fields are 'hooks' to connect to the imager.kv file
    # The point-and-click file navigator
    filechooser = ObjectProperty(None)
    # The text box (for the file name)
    textinput   = ObjectProperty(None)
    # The load button
    loadchoice  = ObjectProperty(None)
    # The cancel button
    exitchoice  = ObjectProperty(None)


class SaveDialog(BoxLayout):
    """
    A controller for a SaveDialog, a pop-up dialog to save a file.
    
    The View for this controller is defined in imager.kv.  This class simply contains
    the hooks for the view properties
    """
    # These fields are 'hooks' to connect to the imager.kv file
    # The point-and-click file navigator
    filechooser = ObjectProperty(None)
    # The text box (for the file name)
    textinput   = ObjectProperty(None)
    # The save button
    savechoice  = ObjectProperty(None)
    # The cancel button
    exitchoice  = ObjectProperty(None)


class ErrorDialog(BoxLayout):
    """
    A controller for an ErrorDialog, a pop-up dialog to notify the user of an error.
    
    The View for this controller is defined in imager.kv.  This class simply contains
    the hooks for the view properties
    """
    # These fields are 'hooks' to connect to the imager.kv file
    # The error message
    message  = StringProperty('')
    # A confirmation button
    okchoice = ObjectProperty(None)


class WarningDialog(BoxLayout):
    """
    A controller for a WarningDialog, a pop-up dialog to warn the user.
    
    It differs from ErrorDialog in that it may be nested inside of another pop-up dialog.
    The warning can be dismissed and ignored.
    
    The View for this controller is defined in imager.kv.  This class simply contains
    the hooks for the view properties
    """
    # These fields are 'hooks' to connect to the imager.kv file
    # The error message
    message = StringProperty('')
    # The data that caused the problem.
    payload = StringProperty('')
    # A confirmation button (to ignore the warning).
    okchoice   = ObjectProperty(None)
    # The cancel button
    exitchoice = ObjectProperty(None)