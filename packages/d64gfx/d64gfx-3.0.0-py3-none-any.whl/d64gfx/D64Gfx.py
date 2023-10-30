import logging
from PyQt6.QtCore import QSize, QPoint
from PyQt6.QtGui import QImage, QPixmap
from d64py.base import DirEntry
from d64py.base.Constants import FontOffsets
from d64py.utility import D64Utility

def getGeosIcon(dirEntry: DirEntry):
    """
    Given a directory entry, get the icon for a GEOS file from the file header
    as a Qt6 QImage.
    :param dirEntry: The directory entry.
    :return: The icon.
    """
    iconData = dirEntry.getGeosFileHeader().getIconData()
    rawImage = QImage(QSize(24, 21), QImage.Format.Format_Mono)
    rawImage.fill(0)  # clear it
    index = 0
    while index < len(iconData):
        y = index // 3
        card = index % 3  # icon is three bytes across
        bit = 0
        while bit < 8:
            mask = (1 << bit)
            data = 0 if iconData[index] & mask else 1
            x = (7 - bit) + (card * 8)
            rawImage.setPixel(QPoint(x, y), data)
            bit += 1
        index += 1
    rawImage = rawImage.scaled(QSize(48, 42))
    return QPixmap.fromImage(rawImage)

def getFontPreviewImage(text: str, recordData: bytearray, doubleSize: bool) -> QPixmap:
    """
    Generate a preview image of a GEOS font.
    :param text: The text to render.
    :param recordData: The VLIR record containing the font data.
    :param doubleSize: Whether to render the image at double size.
    :return: A QPixmap.
    """
    textWidth = D64Utility.getStringWidth(text, recordData)
    height = recordData[FontOffsets.F_HEIGHT.value]
    rawImage = QImage(QSize(textWidth, height), QImage.Format.Format_Mono)
    setWidth = D64Utility.makeWord(recordData, FontOffsets.F_SETWD.value)
    row = 0
    while (row < height):
        rasterX = 0 # X pixel position of image
        for char in text:
            width = D64Utility.getCharWidth(char, recordData)
            bitIndex = D64Utility.getCharacterBitOffset(char, recordData)
            byteIndex = bitIndex // 8
            byteIndex += D64Utility.getFontDataOffset(recordData)
            byteIndex += setWidth * row
            bitOffset = bitIndex % 8
            bitsCopied = 0

            while bitsCopied < width:
                if byteIndex >= len(recordData):
                    # Shouldn't happen but I've seen fonts (AGATHA) where it does.
                    logging.debug(f"*** NOT ENOUGH DATA: byte index: {byteIndex}, record length: {len(recordData)}")
                    byte = 0
                else:
                    byte = recordData[byteIndex]
                fontBits = min(8 - bitOffset, width - bitsCopied)
                i = bitOffset
                while i < bitOffset + fontBits:
                    mask = 1 << 7 - i
                    rawImage.setPixel(QPoint(rasterX, row), 0 if byte & mask else 1)
                    rasterX += 1
                    i += 1
                bitsCopied += fontBits
                bitOffset = 0 # for bytes after the first one
                byteIndex += 1
        row += 1
    if doubleSize:
        rawImage = rawImage.scaled(QSize(textWidth * 2, height * 2))
    image = QPixmap.fromImage(rawImage)
    return image

def getMegaFontPreviewImage(text: str, megaFontData: bytearray, doubleSize: bool) -> QPixmap:
    """
    Generate a preview image of a GEOS mega font.
    :param text: The text to render.
    :param recordData: The font data from all the mega font records.
    :param doubleSize: Whether to render the image at double size.
    :return: A QPixmap.
    """
    height = megaFontData.get(54)[FontOffsets.F_HEIGHT.value]
    textWidth = D64Utility.getMegaStringWidth(text, megaFontData)
    rawImage = QImage(QSize(textWidth, height), QImage.Format.Format_Mono)
    row = 0
    while row < height:
        rasterX = 0
        for char in text:
            recordNo = D64Utility.getMegaRecordNo(char)
            recordData = megaFontData.get(recordNo)
            setWidth = D64Utility.makeWord(recordData, FontOffsets.F_SETWD.value)
            width = D64Utility.getCharWidth(char, recordData)
            bitIndex = D64Utility.getCharacterBitOffset(char, recordData)
            byteIndex = bitIndex // 8
            byteIndex += D64Utility.getFontDataOffset(recordData)
            byteIndex += setWidth * row
            bitOffset= bitIndex % 8
            bitsCopied = 0

            while bitsCopied < width:
                if byteIndex >= len(recordData):
                    # Shouldn't happen, but I've seen fonts
                    # (MEGA BRUSHSTROKE) where it does.
                    byte = 0
                else:
                    byte = recordData[byteIndex]
                fontBits = min(8 - bitOffset, width - bitsCopied)
                i = bitOffset
                while i < bitOffset + fontBits:
                    mask = 1 << (7 - i)
                    rawImage.setPixel(QPoint(rasterX, row), 0 if byte & mask else 1)
                    i += 1; rasterX += 1
                bitsCopied += fontBits
                bitOffset= 0 # for bytes after the first one
                byteIndex += 1
        row += 1
    if doubleSize:
        rawImage = rawImage.scaled(QSize(textWidth * 2, height * 2))
    image = QPixmap.fromImage(rawImage)
    return image
