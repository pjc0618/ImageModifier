"""
Test cases for Tasks 1 and 2

You cannot even start to process images until the base classes are done. These classes
provide you with some test cases to get you started.

Author: Walker M. White (wmw2)
Date:   October 20, 2017
"""
import cornell
import pixels


def test_assert(func,args,message):
    """
    Tests that the given function raises an assert on those arguments.
    
    This uses some advanced Python.  Do not worry about how it works.
    
    Parameter func: The function/method being tested
    Precondition: func is callable
    
    Parameter args: The function arguments
    Precondition: args is a list of arguments for func
    
    Parameter message: The message to display on failure
    Precondition: message is a string
    """
    try:
        func(*args)
    except AssertionError:
        return True
    except:
        pass
    
    print(message+' for '+func.__name__)
    return False


def test_image_init():
    """
    Tests the __init__ method and getters for class Image
    """
    print('Testing image initializer')
    import a6image
    p = pixels.Pixels(6)
    
    image = a6image.Image(p,3)
    cornell.assert_equals(id(p),id(image.getPixels()))
    cornell.assert_equals(6,image.getLength())
    cornell.assert_equals(3,image.getWidth())
    cornell.assert_equals(2,image.getHeight())

    image = a6image.Image(p,2)
    cornell.assert_equals(id(p),id(image.getPixels()))
    cornell.assert_equals(6,image.getLength())
    cornell.assert_equals(2,image.getWidth())
    cornell.assert_equals(3,image.getHeight())

    image = a6image.Image(p,1)
    cornell.assert_equals(id(p),id(image.getPixels()))
    cornell.assert_equals(6,image.getLength())
    cornell.assert_equals(1,image.getWidth())
    cornell.assert_equals(6,image.getHeight())
    
    # Test enforcement
    good = test_assert(a6image.Image,['aaa',3],'You are not enforcing the precondition on data')
    good = good and test_assert(a6image.Image,[p,'a'],'You are not enforcing the precondition on width type')
    good = good and test_assert(a6image.Image,[p, 5],'You are not enforcing the precondition on width validity')
    if not good:
        exit()
    



def test_image_setters():
    """
    Tests the setters for class Image
    """
    print('Testing image setters')
    import a6image
    p = pixels.Pixels(6)
    
    image = a6image.Image(p,3)
    cornell.assert_equals(3,image.getWidth())
    cornell.assert_equals(2,image.getHeight())
    
    image.setWidth(2)
    cornell.assert_equals(2,image.getWidth())
    cornell.assert_equals(3,image.getHeight())
    
    image.setHeight(1)
    cornell.assert_equals(6,image.getWidth())
    cornell.assert_equals(1,image.getHeight())
    
    image.setWidth(1)
    cornell.assert_equals(1,image.getWidth())
    cornell.assert_equals(6,image.getHeight())
    
    # Test enforcement
    good = test_assert(image.setWidth, ['a'], 'You are not enforcing the precondition on width type')
    good = good and test_assert(image.setWidth, [5], 'You are not enforcing the precondition on width validity')
    good = good and test_assert(image.setHeight, ['a'], 'You are not enforcing the precondition on height type')
    good = good and test_assert(image.setHeight, [5], 'You are not enforcing the precondition on height validity')
    if not good:
        exit()


def test_image_access():
    """
    Tests the methods get/setPixel and get/setFlatPixel in class Image
    """
    print('Testing image pixel access')
    import a6image
    p =  pixels.Pixels(6)
    
    p[0] = (255,0,0)
    p[1] = (0,255,0)
    p[2] = (0,0,255)
    p[3] = (0,255,255)
    p[4] = (255,0,255)
    p[5] = (255,255,0)
    rgb1 = (255,255,255)
    rgb2 = (64,128,192)
    
    image = a6image.Image(p,2)
    for n in range(6):
        cornell.assert_equals(p[n],image.getFlatPixel(n))
        cornell.assert_equals(id(p[n]),id(image.getFlatPixel(n)))
    
    image.setFlatPixel(4,rgb1)
    cornell.assert_equals(rgb1,image.getFlatPixel(4))
    image.setFlatPixel(4,rgb2)
    cornell.assert_equals(rgb2,image.getFlatPixel(4))
    
    for n in range(6):
        cornell.assert_equals(p[n],image.getPixel(n // 2, n % 2))
        cornell.assert_equals(id(p[n]),id(image.getPixel(n // 2, n % 2)))
    
    image.setPixel(2,1,rgb1)
    cornell.assert_equals(rgb1,image.getPixel(2,1))
    
    image.setPixel(2,1,rgb2)
    cornell.assert_equals(rgb2,image.getPixel(2,1))
    
    # Test enforcement
    good = test_assert(image.getPixel, ['a', 1], 'You are not enforcing the precondition on row type')
    good = good and test_assert(image.getPixel, [8, 1], 'You are not enforcing the precondition on row value')
    good = good and test_assert(image.getPixel, [2, 'a'], 'You are not enforcing the precondition on col value')
    good = good and test_assert(image.getPixel, [2, 8], 'You are not enforcing the precondition on col value')
    good = good and test_assert(image.setPixel, ['a', 1, p], 'You are not enforcing the precondition on row type')
    good = good and test_assert(image.setPixel, [8, 1, p], 'You are not enforcing the precondition on row value')
    good = good and test_assert(image.setPixel, [2, 'a', p], 'You are not enforcing the precondition on col value')
    good = good and test_assert(image.setPixel, [2, 8, p], 'You are not enforcing the precondition on col value')
    if not good:
        exit()


def test_image_str():
    """
    Tests the __str__ method in class Image
    """
    print('Testing image __str__ method')
    import a6image
    p =  pixels.Pixels(6)
    
    p[0] = (255,  64,   0)
    p[1] = (  0, 255,  64)
    p[2] = ( 64,   0, 255)
    p[3] = ( 64, 255, 128)
    p[4] = (128,  64, 255)
    p[5] = (255, 128,  64)
    
    str0 = '[['+str(p[0])+', '+str(p[1])+'],  ['+str(p[2])+', '+str(p[3])+']]'
    str1 = '[['+str(p[0])+', '+str(p[1])+'],  ['+str(p[2])+', '+str(p[3])+'],  ['+str(p[4])+', '+str(p[5])+']]'
    str2 = '[['+str(p[0])+', '+str(p[1])+', '+str(p[2])+'],  ['+str(p[3])+', '+str(p[4])+', '+str(p[5])+']]'
    str3 = '[['+str(p[0])+', '+str(p[1])+', '+str(p[2])+', '+str(p[3])+', '+str(p[4])+', '+str(p[5])+']]'
    str4 = '[['+str(p[0])+'],  ['+str(p[1])+'],  ['+str(p[2])+'],  ['+str(p[3])+'],  ['+str(p[4])+'],  ['+str(p[5])+']]'
    
    image = a6image.Image(p[:4],2)
    cornell.assert_equals(str0,str(image))
    
    image = a6image.Image(p,2)
    cornell.assert_equals(str1,str(image))
    image.setWidth(3)
    cornell.assert_equals(str2,str(image))
    image.setWidth(6)
    cornell.assert_equals(str3,str(image))
    image.setWidth(1)
    cornell.assert_equals(str4,str(image))
    
def test_image_other():
    """
    Tests the copy and swapPixel methods in class Image
    """
    print('Testing image extras')
    import a6image
    p =  pixels.Pixels(6)
    
    p[0] = (255,  64,   0)
    p[1] = (  0, 255,  64)
    p[2] = ( 64,   0, 255)
    p[3] = ( 64, 255, 128)
    p[4] = (128,  64, 255)
    p[5] = (255, 128,  64)
    q = p[:]  # Need to copy this
    
    # Test the copy
    image = a6image.Image(p,2)
    copy  = image.copy()
    cornell.assert_equals(image.getLength(),copy.getLength())
    cornell.assert_equals(image.getWidth(),copy.getWidth())
    cornell.assert_not_equals(id(image), id(copy))
    cornell.assert_not_equals(id(image.getPixels()), id(copy.getPixels()))
    for pos in range(copy.getLength()):
        cornell.assert_equals(image.getPixels()[pos],copy.getPixels()[pos])
    
    # Test swap pixels
    image.swapPixels(0,0,2,1)
    cornell.assert_equals(q[5],image.getPixel(0,0))
    cornell.assert_equals(q[0],image.getPixel(2,1))
    image.swapPixels(0,0,2,1)
    cornell.assert_equals(q[0],image.getPixel(0,0))
    cornell.assert_equals(q[5],image.getPixel(2,1))
    image.swapPixels(0,1,2,0)
    cornell.assert_equals(q[4],image.getPixel(0,1))
    cornell.assert_equals(q[1],image.getPixel(2,0))
    image.swapPixels(0,1,2,0)
    cornell.assert_equals(q[1],image.getPixel(0,1))
    cornell.assert_equals(q[4],image.getPixel(2,0))
    image.swapPixels(0,0,0,0)
    cornell.assert_equals(q[0],image.getPixel(0,0))
    
    # Test enforcement
    good = test_assert(image.swapPixels, ['a', 1, 0, 0], 'You are not enforcing the precondition on row type')
    good = good and test_assert(image.swapPixels, [8, 1, 0, 0],   'You are not enforcing the precondition on row value')
    good = good and test_assert(image.swapPixels, [0, 1, 'a', 0], 'You are not enforcing the precondition on row type')
    good = good and test_assert(image.swapPixels, [0, 1, 8, 0],   'You are not enforcing the precondition on row value')
    good = good and test_assert(image.swapPixels, [0, 'a', 0, 0], 'You are not enforcing the precondition on column type')
    good = good and test_assert(image.swapPixels, [0, 8, 0, 0],   'You are not enforcing the precondition on column value')
    good = good and test_assert(image.swapPixels, [0, 1, 0, 'a'], 'You are not enforcing the precondition on column type')
    good = good and test_assert(image.swapPixels, [0, 1, 0, 8],   'You are not enforcing the precondition on column value')
    if not good:
        exit()


def test_hist_init():
    """
    Tests the __init__ method and getters in ImageHistory
    """
    print('Testing history initializer')
    import a6image
    import a6history
    p =  pixels.Pixels(6)
    
    p[0] = (255,0,0)
    p[1] = (0,255,0)
    p[2] = (0,0,255)
    p[3] = (0,255,255)
    p[4] = (255,0,255)
    p[5] = (255,255,0)
    
    image = a6image.Image(p,2)
    hist  = a6history.ImageHistory(image)
    cornell.assert_equals(id(image),id(hist.getOriginal()))
    cornell.assert_equals(type(image),type(hist.getCurrent()))
    cornell.assert_not_equals(id(image),id(hist.getCurrent()))
    
    current = hist.getCurrent()
    cornell.assert_not_equals(id(p), id(current.getPixels()))
    for pos in range(current.getLength()):
        cornell.assert_equals(p[pos],current.getPixels()[pos])
    
    cornell.assert_true(hasattr(hist, '_history'))
    cornell.assert_equals(list,type(hist._history))
    cornell.assert_equals(1,len(hist._history))


def test_hist_edit():
    """
    Tests the edit (increment/undo/clear) methods in ImageHistory
    """
    print('Testing history edit methods')
    import a6image
    import a6history
    p =  pixels.Pixels(6)
    
    p[0] = (255,0,0)
    p[1] = (0,255,0)
    p[2] = (0,0,255)
    p[3] = (0,255,255)
    p[4] = (255,0,255)
    p[5] = (255,255,0)
    
    image = a6image.Image(p,2)
    hist  = a6history.ImageHistory(image)
    
    bottom  = hist.getCurrent()
    bottom.setPixel(0,0,(64,128,192))
    hist.increment()
    
    current = hist.getCurrent()    
    cornell.assert_equals(bottom.getLength(),current.getLength())
    cornell.assert_equals(bottom.getWidth(),current.getWidth())
    cornell.assert_not_equals(id(bottom), id(current))
    cornell.assert_not_equals(id(bottom.getPixels()), id(current.getPixels()))
    for pos in range(current.getLength()):
        cornell.assert_equals(bottom.getPixels()[pos],current.getPixels()[pos])
    
    hist.undo()
    cornell.assert_equals(id(bottom),id(hist.getCurrent()))
    
    hist.increment()
    hist.increment()
    hist.increment()
    cornell.assert_equals(4,len(hist._history))
    current = hist.getCurrent()
    cornell.assert_equals(bottom.getLength(),current.getLength())
    cornell.assert_equals(bottom.getWidth(),current.getWidth())
    cornell.assert_not_equals(id(bottom), id(current))
    cornell.assert_not_equals(id(bottom.getPixels()), id(current.getPixels()))
    for pos in range(current.getLength()):
        cornell.assert_equals(bottom.getPixels()[pos],current.getPixels()[pos])
    
    hist.clear()
    cornell.assert_not_equals(id(bottom),id(hist.getCurrent()))
    cornell.assert_equals(1,len(hist._history))
    
    original = hist.getOriginal()
    current  = hist.getCurrent()
    cornell.assert_equals(original.getLength(),current.getLength())
    cornell.assert_equals(original.getWidth(),current.getWidth())
    cornell.assert_not_equals(id(original), id(current))
    cornell.assert_not_equals(id(original.getPixels()), id(current.getPixels()))
    for pos in range(current.getLength()):
        cornell.assert_equals(original.getPixels()[pos],current.getPixels()[pos])
    
    bottom  = hist.getCurrent()
    bottom.setPixel(0,0,(64,128,192))
    for step in range(hist.MAX_HISTORY+1):
        hist.increment()
    
    cornell.assert_equals(hist.MAX_HISTORY,len(hist._history))
    cornell.assert_not_equals(id(bottom), id(hist._history[0]))


def test_all():
    """
    Execute all of the test cases.
    
    This function is called by __main__.py
    """
    test_image_init()
    test_image_setters()
    test_image_access()
    test_image_str()
    test_image_other()
    print('Class Image appears to be working correctly')
    print()
    test_hist_init()
    test_hist_edit()
    print('Class ImageHistory appears to be working correctly')
