"""
The main class for our imager application.

This modules contains a single class.  Instances of this class support an edit history.
An edit history keeps track of all modifications of an original history.  It allows for 
(step-by-step) undos of any changes.

Based on an original file by Dexter Kozen (dck10) and Walker White (wmw2)

Author: Walker White (wmw2), Philip Cipollina(pjc272), Luke Marcinkiewicz(lam365)
Date:   October 20, 2017, November 16, 2017 (Assignment)
"""
import a6image

class ImageHistory(object):
    """
    A class that keeps track of edits from an original image.
    
    This class is what allows us to implement the Undo functionality in our application.
    The attribute _history stores all of the edits (up to a maximum of MAX_HISTORY edits)
    in order.  So the last element of _history is the most recent edit.
    
    IMMUTABLE ATTRIBUTES (Fixed after initialization)
        _original: The original image [Image object]
        _history:  The edit history   [non-empty list of Image objects]
    In addition, the length of _history should never be longer than the class attribute 
    MAX_HISTORY.
    """
    
    # The number of edits that we are allowed to keep track of.
    # (THIS GOES IN CLASS FOLDER)
    MAX_HISTORY = 20
    
    # GETTERS
    def getOriginal(self):
        """
        Returns: The original image
        """
        return self._original
    
    def getCurrent(self):
        """
        Returns: The most recent edit
        """
        return self._history[-1]
    
    # INITIALIZER
    def __init__(self,original):
        """
        Initializer: Creates an edit history for the given image.
        
        The edit history starts with exactly one element, which is an (unedited) copy
        of the original image.
        
        Parameter original: The image to edit
        Precondition: original is an Image object
        """
        assert isinstance(original,a6image.Image)
        self._original=original
        self._history=[original.copy()]
    
    # EDIT METHODS
    def undo(self):
        """
        Returns: True if the latest edit can be undone, False otherwise.
        
        This method attempts to undo the latest element by removing the last element
        of the edit history.  However, the invariant of _history specifies that the
        list can never be empty.  So in that case, it does not remove anything and
        returns False instead.
        """
        if len(self._history)==1:
            return False
        else:
            self=self._history.pop()
            return True
    
    def clear(self):
        """
        Deletes the entire edit history, retoring the original image.
        
        When this method completes, the object should have the same values that it did
        when it was first initialized.
        """
        self._history=[self.getOriginal().copy()]
        self=self.getOriginal()
    
    def increment(self):
        """
        Adds a new copy of the image to the edit history.
        
        This method copies the most recent edit and adds it to the end of the
        history. This provides a new image for editing, while the previous edit is
        preserved. If this method causes the history to grow to larger (greater than 
        MAX_HISTORY), this method deletes the oldest edit to ensure the invariant is 
        satisfied.
        """
        if len(self._history)>=ImageHistory.MAX_HISTORY:
            del self._history[0]
        self._history=self._history + [self.getCurrent().copy()]

