import cv2
import numpy as np
import win32gui, win32ui, win32con, win32api
import threading
import logging
__LOCK = threading.Lock()

def grab_screen(region=None, use_channel_rgb=True):
    '''
    region: a array-like of (x1, y1, x2, y2).
            x1 and y1 is the left-top coordinates, x2 and y2 is the right-bottom coordinates
    use_rgb_channel: Specifies whether convert the output image to RGB format
            if True (default): returns RGB image
            if False: returns BGR image

    returns
    an image of a numpy array
    '''
    __LOCK.acquire()
    try:
        hwin = win32gui.GetDesktopWindow()

        if region:
            left, top, x2, y2 = region
            width = x2 - left + 1
            height = y2 - top + 1
        else:
            width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
            height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
            left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
            top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

        hwindc = win32gui.GetWindowDC(hwin)
        srcdc = win32ui.CreateDCFromHandle(hwindc)
        memdc = srcdc.CreateCompatibleDC()
        bmp = win32ui.CreateBitmap()
        bmp.CreateCompatibleBitmap(srcdc, width, height)
        memdc.SelectObject(bmp)
        memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), win32con.SRCCOPY)

        signedIntsArray = bmp.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype='uint8')
        img.shape = (height, width, 4)

        srcdc.DeleteDC()
        memdc.DeleteDC()
        win32gui.ReleaseDC(hwin, hwindc)
        win32gui.DeleteObject(bmp.GetHandle())

        if use_channel_rgb:
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
        else:
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        return img
    except Exception as e:
        logging.exception(e)
    finally:
        __LOCK.release()
    # return img