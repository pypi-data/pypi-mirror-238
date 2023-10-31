import wx

from wx.lib.embeddedimage import PyEmbeddedImage as py_embedded_image

"""
icons serves as a central repository for icons and other assets. These are all processed as PyEmbeddedImages which is
extended from the wx.lib utility of the same name. We allow several additional modifications to these assets. For
example we allow resizing and inverting this allows us to easily reuse the icons and to use the icons for dark themed
guis. We permit rotation of the icons, so as to permit reusing these icons and coloring the icons to match a particular
colored object, for example the icons in the tree for operations using color specific matching.
"""

DARKMODE = False

STD_ICON_SIZE = 50

_MIN_ICON_SIZE = 0
_GLOBAL_FACTOR = 1.0


def set_icon_appearance(factor, min_size):
    global _MIN_ICON_SIZE
    global _GLOBAL_FACTOR
    _MIN_ICON_SIZE = min_size
    _GLOBAL_FACTOR = factor


def get_default_icon_size():
    return int(_GLOBAL_FACTOR * STD_ICON_SIZE)


def get_default_scale_factor():
    return _GLOBAL_FACTOR


class PyEmbeddedImage(py_embedded_image):
    def __init__(self, data):
        super().__init__(data)

    def GetBitmap(
        self,
        use_theme=True,
        resize=None,
        color=None,
        rotate=None,
        noadjustment=False,
        keepalpha=False,
    ):
        """
        Assumes greyscale icon black on transparent background using alpha for shading
        Ready for Dark Theme
        If color is provided, the black is changed to this
        If color is close to background, alpha is removed and negative background added
        so, we don't get black icon on black background or white on white background.

        @param use_theme:
        @param resize:
        @param color:
        @param rotate:
        @param noadjustment: Disables size adjustment based on global factor
        @param keepalpha: maintain the alpha from the original asset
        @return:
        """

        image = py_embedded_image.GetImage(self)
        if not noadjustment and _GLOBAL_FACTOR != 1.0:
            oldresize = resize
            wd, ht = image.GetSize()
            if resize is not None:
                if isinstance(resize, int) or isinstance(resize, float):
                    resize *= _GLOBAL_FACTOR
                    if 0 < _MIN_ICON_SIZE < oldresize:
                        if resize < _MIN_ICON_SIZE:
                            resize = _MIN_ICON_SIZE
                elif isinstance(resize, tuple):  # (tuple wd ht)
                    resize = [oldresize[0], oldresize[1]]
                    for i in range(2):
                        resize[i] *= _GLOBAL_FACTOR
                        if 0 < _MIN_ICON_SIZE < oldresize[i]:
                            if resize[i] < _MIN_ICON_SIZE:
                                resize[i] = _MIN_ICON_SIZE
            else:
                resize = [wd, ht]
                oldresize = (wd, ht)
                for i in range(2):
                    resize[i] *= _GLOBAL_FACTOR
                    if 0 < _MIN_ICON_SIZE < oldresize[i]:
                        if resize[i] < _MIN_ICON_SIZE:
                            resize[i] = _MIN_ICON_SIZE
            # print ("Will adjust from %s to %s (was: %s)" % ((wd, ht), resize, oldresize))

        if resize is not None:
            if isinstance(resize, int) or isinstance(resize, float):
                image = image.Scale(int(resize), int(resize))
            else:
                image = image.Scale(int(resize[0]), int(resize[1]))
        if rotate is not None:
            if rotate == 1:
                image = image.Rotate90()
            elif rotate == 2:
                image = image.Rotate180()
            elif rotate == 3:
                image = image.Rotate90(False)
        if (
            color is not None
            and color.red is not None
            and color.green is not None
            and color.blue is not None
        ):
            image.Replace(0, 0, 0, color.red, color.green, color.blue)
            if DARKMODE and use_theme:
                reverse = color.distance_to("black") <= 200
                black_bg = False
            else:
                reverse = color.distance_to("white") <= 200
                black_bg = True
            if reverse and not keepalpha:
                self.RemoveAlpha(image, black_bg=black_bg)
        elif DARKMODE and use_theme:
            image.Replace(0, 0, 0, 255, 255, 255)
        return wx.Bitmap(image)

    def RemoveAlpha(self, image, black_bg=False):
        if not image.HasAlpha():
            return
        bg_rgb = 0 if black_bg else 255
        for x in range(image.GetWidth()):
            for y in range(image.GetHeight()):
                a = image.GetAlpha(x, y)
                bg = int((255 - a) * bg_rgb / 255)
                r = int(image.GetRed(x, y) * a / 255) + bg
                g = int(image.GetGreen(x, y) * a / 255) + bg
                b = int(image.GetBlue(x, y) * a / 255) + bg
                image.SetRGB(x, y, r, g, b)
                image.SetAlpha(x, y, wx.IMAGE_ALPHA_OPAQUE)
        image.ClearAlpha()

class EmptyIcon():
    def __init__(self, size, color, msg=None, ptsize=None, **args):
        if size <= 0:
            size = 50
        size = int(size)
        self._size = size
        self._color = color
        bmp = self.populate_image(msg, ptsize)
        self._image = bmp.ConvertToImage()
        # self._image = wx.Image(width=size, height=size, clear=True)
        # for x in range(size):
        #     for y in range(size):
        #         self._image.SetRGB(x, y, color.red, color.green, color.blue)

    def populate_image(self, msg=None, ptsize=None):
        imgBit = wx.Bitmap(self._size, self._size)
        dc = wx.MemoryDC(imgBit)
        dc.SelectObject(imgBit)
        brush = wx.Brush(self._color, wx.BRUSHSTYLE_SOLID)
        dc.SetBackground(brush)
        dc.Clear()
        if msg is not None and msg != "":
            # We only take the very first letter for
            pattern={
                "[red]": wx.RED,
                "[green]": wx.GREEN,
                "[blue]": wx.BLUE,
                "[white]": wx.WHITE,
                "[black]": wx.BLACK,
            }
            txt_color = wx.BLACK
            for pat in pattern:
                if msg.startswith(pat):
                    txt_color = pattern[pat]
                    msg = msg[len(pat):]
            if ptsize is None:
                ptsize = 12
            font = wx.Font(
                ptsize,
                wx.FONTFAMILY_SWISS,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_NORMAL,
            )
            dc.SetTextForeground(txt_color)
            dc.SetFont(font)
            (t_w, t_h) = dc.GetTextExtent(msg)
            x = (self._size - t_w) / 2
            y = (self._size - t_h) / 2
            pt = wx.Point(x, y)
            dc.DrawText(msg, pt)
        # Now release dc
        dc.SelectObject(wx.NullBitmap)
        return imgBit

    def GetBitmap(
        self,
        use_theme=True,
        resize=None,
        color=None,
        rotate=None,
        noadjustment=False,
        keepalpha=False,
    ):
        """
        Assumes greyscale icon black on transparent background using alpha for shading
        Ready for Dark Theme
        If color is provided, the black is changed to this
        If color is close to background, alpha is removed and negative background added
        so, we don't get black icon on black background or white on white background.

        @param use_theme:
        @param resize:
        @param color:
        @param rotate:
        @param noadjustment: Disables size adjustment based on global factor
        @param keepalpha: maintain the alpha from the original asset
        @return:
        """

        image = self._image
        if not noadjustment and _GLOBAL_FACTOR != 1.0:
            oldresize = resize
            wd, ht = image.GetSize()
            if resize is not None:
                if isinstance(resize, int) or isinstance(resize, float):
                    resize *= _GLOBAL_FACTOR
                    if 0 < _MIN_ICON_SIZE < oldresize:
                        if resize < _MIN_ICON_SIZE:
                            resize = _MIN_ICON_SIZE
                elif isinstance(resize, tuple):  # (tuple wd ht)
                    resize = [oldresize[0], oldresize[1]]
                    for i in range(2):
                        resize[i] *= _GLOBAL_FACTOR
                        if 0 < _MIN_ICON_SIZE < oldresize[i]:
                            if resize[i] < _MIN_ICON_SIZE:
                                resize[i] = _MIN_ICON_SIZE
            else:
                resize = [wd, ht]
                oldresize = (wd, ht)
                for i in range(2):
                    resize[i] *= _GLOBAL_FACTOR
                    if 0 < _MIN_ICON_SIZE < oldresize[i]:
                        if resize[i] < _MIN_ICON_SIZE:
                            resize[i] = _MIN_ICON_SIZE
            # print ("Will adjust from %s to %s (was: %s)" % ((wd, ht), resize, oldresize))

        if resize is not None:
            if isinstance(resize, int) or isinstance(resize, float):
                image = image.Scale(int(resize), int(resize))
            else:
                image = image.Scale(int(resize[0]), int(resize[1]))
        if rotate is not None:
            if rotate == 1:
                image = image.Rotate90()
            elif rotate == 2:
                image = image.Rotate180()
            elif rotate == 3:
                image = image.Rotate90(False)
        if (
            color is not None
            and color.red is not None
            and color.green is not None
            and color.blue is not None
        ):
#            image.Replace(0, 0, 0, color.red, color.green, color.blue)
            image.Replace(self._color.red, self._color.green, self._color.blue, color.red, color.green, color.blue)
            if DARKMODE and use_theme:
                reverse = color.distance_to("black") <= 200
                black_bg = False
            else:
                reverse = color.distance_to("white") <= 200
                black_bg = True
            if reverse and not keepalpha:
                self.RemoveAlpha(image, black_bg=black_bg)
        elif DARKMODE and use_theme:
            image.Replace(0, 0, 0, 255, 255, 255)
        return wx.Bitmap(image)

    def RemoveAlpha(self, image, black_bg=False):
        if not image.HasAlpha():
            return
        bg_rgb = 0 if black_bg else 255
        for x in range(image.GetWidth()):
            for y in range(image.GetHeight()):
                a = image.GetAlpha(x, y)
                bg = int((255 - a) * bg_rgb / 255)
                r = int(image.GetRed(x, y) * a / 255) + bg
                g = int(image.GetGreen(x, y) * a / 255) + bg
                b = int(image.GetBlue(x, y) * a / 255) + bg
                image.SetRGB(x, y, r, g, b)
                image.SetAlpha(x, y, wx.IMAGE_ALPHA_OPAQUE)
        image.ClearAlpha()


icons8_barcode_50 = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAYAAAAeP4ixAAAABmJLR0QA/wD/AP+gvaeTAAAA'
    b'4ElEQVRoge3Zuw3CMBSF4R9EzwIwAQswAgtkAjaABVgAqNLBBmnooKOkShcWSJmKCaBxkGXZ'
    b'RkIUF+l8kmX5+nlqg4iIyPcGkdoOmHrjLXADlsAic1YDbIAJsA/mCtcfgHFkb+qOM3AE5sDa'
    b'q7fAKvOW94OeXusfUQb1sF3dullkrtcl9qbuKF29COpN+Ojhp1T/QkGsURBrFMQaBbFGQaxR'
    b'EGsUxBoFsUZBrFEQaxTEGgWxRkGsURBrFMSaUaR2Ae7euHV9DVSZs/o/i0dm3Yn4R0/qjtqb'
    b'ryLrRUREfuIFnSA3JAyP8hcAAAAASUVORK5CYII=')

