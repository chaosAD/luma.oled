# -*- coding: utf-8 -*-
# Copyright (c) 2014-20 Richard Hull and contributors
# See LICENSE.rst for details.

"""
Collection of serial interfaces to OLED devices.
"""

# Example usage:
#
#   from luma.core.interface.serial import i2c, spi
#   from luma.core.render import canvas
#   from luma.oled.device import ssd1306, sh1106
#   from PIL import ImageDraw
#
#   serial = i2c(port=1, address=0x3C)
#   device = ssd1306(serial)
#
#   with canvas(device) as draw:
#      draw.rectangle(device.bounding_box, outline="white", fill="black")
#      draw.text(30, 40, "Hello World", fill="white")
#
# As soon as the with-block scope level is complete, the graphics primitives
# will be flushed to the device.
#
# Creating a new canvas is effectively 'carte blanche': If you want to retain
# an existing canvas, then make a reference like:
#
#    c = canvas(device)
#    for X in ...:
#        with c as draw:
#            draw.rectangle(...)
#
# As before, as soon as the with block completes, the canvas buffer is flushed
# to the device

from time import sleep
from luma.core.device import device, parallel_device
from luma.core.virtual import character
from luma.oled.device.color import color_device
from luma.oled.device.greyscale import greyscale_device
import luma.core.error
from luma.core.framebuffer import full_frame
from luma.core.bitmap_font import embedded_fonts
import luma.oled.const
from luma.oled.device.framebuffer_mixin import __framebuffer_mixin

__all__ = ["ssd1306", "ssd1309", "ssd1322", "ssd1362", "ssd1322_nhd", "ssd1325", "ssd1327", "ssd1331", "ssd1351", "sh1106", "ws0010", "winstar_weh"]


class sh1106(device):
    """
    Serial interface to a monochrome SH1106 OLED display.

    On creation, an initialization sequence is pumped to the display
    to properly configure it. Further control commands can then be called to
    affect the brightness and other settings.
    """

    def __init__(self, serial_interface=None, width=128, height=64, rotate=0, **kwargs):
        super(sh1106, self).__init__(luma.oled.const.sh1106, serial_interface)
        self.capabilities(width, height, rotate)
        self._pages = self._h // 8

        settings = {
            (128, 128): dict(multiplex=0xFF, displayoffset=0x02),
            (128, 64): dict(multiplex=0x3F, displayoffset=0x00),
            (128, 32): dict(multiplex=0x20, displayoffset=0x0F)
        }.get((width, height))

        if settings is None:
            raise luma.core.error.DeviceDisplayModeError(
                f"Unsupported display mode: {width} x {height}")

        self.contrast(0x7F)
#        self.clear()
#        self.show()

    def display(self, image):
        """
        Takes a 1-bit :py:mod:`PIL.Image` and dumps it to the SH1106
        OLED display.

        :param image: Image to display.
        :type image: :py:mod:`PIL.Image`
        """
        assert(image.mode == self.mode)
        assert(image.size == self.size)

        image = self.preprocess(image)

        image_data = image.getdata()

        print(type(image))
        print(type(image_data))
        image.show()
