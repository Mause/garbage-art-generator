import sys
import tkMessageBox as tkm
import Image             # Only if you need and use the PIL library.

if sys.platform.startswith('win'):
    # Image grab comes from PIL (Python Imaging Library)
    import ImageGrab
    # We use wx to copy to the clipboard on windows machines.  The PySimpleApp line initializes wx.  There does not appear to be
    # a conflict between wx started this way and Tk.  Note that if you don't want the copy to clipboard or read from clipboard capability,
    # you can just delete the two lines below (and all the associated wx routines).
    import wx
    app = wx.PySimpleApp()

def grab_image(widget=None, bbox=None, offset1=2, offset2=2):
    # widget = the Tk widget to copy to the clipboard
    # bbox = the bounding box containing the area to copy to the clipboard.  Should be a tuple of 4 integers.
    # either widget or bbox must not be None.  If both are not None, widget is used.
    # Note that if widget is used, the screen will be updated.  It can't do that if only bbox is used, so that should be done by the caller
    # offset1 & offset2 determine the amount to expand the box beyond the widget in order to make sure the whole widget is captured
    #         they are used because some widgets (such as canvases) appear to be a bit wonky in whether borders are copied or not
    im = ""
    if widget:
        # The guts of this routine were originally provided by Fredrik Lundh
        widget.update()
        x0 = widget.winfo_rootx()
        y0 = widget.winfo_rooty()
        x1 = x0 + widget.winfo_width()
        y1 = y0 + widget.winfo_height()
        im = ImageGrab.grab((x0-offset1, y0-offset1, x1+offset2, y1+offset2))
    elif bbox:
        im = ImageGrab.grab(bbox)
    return im

def copy_to_clipboard(**keyw):
    # Copies an image of a widget or screen area to the clipboard. 
    #
    # Any arguments to this routine are passed directly to grab_image, so see that routine for possible useful arguments
    # In particular, either widget or bbox must be supplied by the user
    #
    if sys.platform.startswith('win'):
        im = grab_image(**keyw)
        if im:
            bitmap = pil_to_bitmap(im)
            clipboard_bitmap = wx.BitmapDataObject(bitmap)
            if wx.TheClipboard.Open():
                wx.TheClipboard.SetData(clipboard_bitmap)
                wx.TheClipboard.Close()
    else:
        tkm.showerror('Clipboard Copy Error', 'Clipboard copy not implemented on this platform')

def copy_to_file(filename, **keyw):
    # Copies an image of a widget or screen area to a file.  The file type can be any that the Python Imaging Library supports, and the
    # file type is determined by the extension of filename.
    #
    # filename = name of file to save the image to.  The file name extension is used to determine the image type.
    #
    # Any arguments to this routine are passed directly to grab_image, so see that routine for possible useful arguments
    # In particular, either widget= or bbox= must be supplied by the user
    #
    if sys.platform.startswith('win'):
        im = grab_image(**keyw)
        if im:
            im.save(filename)
    else:
        tkm.showerror('Image Grab Error', 'Image grab not implemented on this platform')

def get_bitmap_from_clipboard():
    # Returns a PIL image from the clipboard, which should have bitmap data in it
    # The PIL image can be used in Tk widgets by converting it using ImageTk.PhotoImage(PIL image)
    bm = wx.BitmapDataObject()
    if wx.TheClipboard.GetData(bm):
        wxbmp = bm.GetBitmap()
        try:
            pilimage = bitmap_to_pil(wxbmp)
            return pilimage
        except:
            tkm.showerror('Clipboard Paste Error', 'Clipboard bitmap data could not be converted to an image')
            return False
    else:
        tkm.showerror('Clipboard Paste Error', 'Clipboard data is not a recognized bitmap format')
        return False

########################################
# Start of routines taken from 
#http://wiki.wxpython.org/index.cgi/WorkingWithImages
########################################
def bitmap_to_pil(bitmap):
    return wximage_to_pil(bitmap_to_wximage(bitmap))

def bitmap_to_wximage(bitmap):
    return wx.ImageFromBitmap(bitmap)

def pil_to_bitmap(pil):
    return wximage_to_bitmap(pil_to_wximage(pil))

def pil_to_wximage(pil):
    image = wx.EmptyImage(pil.size[0], pil.size[1])
    image.SetData(pil.convert('RGB').tostring())
    return image

#Or, if you want to copy alpha channels too (available from wxPython 2.5)
def piltoimage(pil,alpha=True):
   if alpha:
       image = apply( wx.EmptyImage, pil.size )
       image.SetData( pil.convert( "RGB").tostring() )
       image.SetAlphaData(pil.convert("RGBA").tostring()[3::4])
   else:
       image = wx.EmptyImage(pil.size[0], pil.size[1])
       new_image = pil.convert('RGB')
       data = new_image.tostring()
       image.SetData(data)
   return image

def wximage_to_pil(image):
    pil = Image.new('RGB', (image.GetWidth(), image.GetHeight()))
    pil.fromstring(image.GetData())
    return pil

def wximage_to_bitmap(image):
    return image.ConvertToBitmap()

########################################
# End of routines taken from 
#http://wiki.wxpython.org/index.cgi/WorkingWithImages
########################################

if __name__ == '__main__':
    def copy_canvas():
        copy_to_clipboard(widget=canvas)
    def copy_canvas_file():
        copy_to_file('testimage.jpg', widget=canvas)
    print 'testing'
    import Tkinter as Tk
    root = Tk.Tk()
    canvas = Tk.Canvas(root, bg='white')
    canvas.pack()
    canvas.create_oval(150, 50, 180, 150, fill='red')
    canvas.create_line(3, 3, 100, 120, fill='blue', width=4)
    button1 = Tk.Button(root, text='copy to clipboard', command=copy_canvas)
    button1.pack(pady=5)
    button2 = Tk.Button(root, text='copy to testimage.jpg', 
command=copy_canvas_file)
    button2.pack()
    root.mainloop()