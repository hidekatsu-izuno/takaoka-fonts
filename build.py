import os
import urllib.request
import tarfile
import zipfile
import re
from fontTools.ttLib import TTFont
from fontTools.pens.ttGlyphPen import TTGlyphPen

srcDir = "build/base"
destDir = "build/dest"
releaseDir = "build/release"
takaoFontUrl = "https://launchpad.net/takao-fonts/trunk/15.03/+download/TakaoFonts_00303.01.tar.xz"

def downloadTakaoFonts():
    os.makedirs(srcDir, exist_ok = True)

    fontFiles = [filename for filename in os.listdir(srcDir) if re.search(r'\.ttf', filename)]
    if not fontFiles:
        archiveName = f"{srcDir}/TakaoFonts.tar.xz"
        urllib.request.urlretrieve(takaoFontUrl, archiveName)

        with tarfile.open(archiveName) as tf:
            for member in tf.getmembers():
                m = re.fullmatch(r"[^/]*/(Takao(?:Gothic|Mincho).ttf)", member.name)
                if m:
                    with tf.extractfile(member) as reader:
                        with open(f"{srcDir}/{m.group(1)}", "wb") as writer:
                            writer.write(reader.read())

        os.remove(archiveName)

def replaceNameRecord(font, fontFile):
    nameTable = font["name"]
    for name in nameTable.names:
        if name.nameID == 0:
            nameTable.setName(
                re.sub(r"You must accept", r"Copyright (c) Hidekatsu Izuno, 2020. \0", name.toUnicode()),
                name.nameID,
                name.platformID,
                name.platEncID,
                name.langID
            )
        elif name.nameID in (1, 3, 4, 6):
            nameTable.setName(
                re.sub(r"Takao", r"Takaoka", name.toUnicode()),
                name.nameID,
                name.platformID,
                name.platEncID,
                name.langID
            )
        elif name.nameID == 11:
            nameTable.setName(
                "https://github.com/hidekatsu-izuno/takaoka-fonts",
                name.nameID,
                name.platformID,
                name.platEncID,
                name.langID
            )
    nameTable.compile(font)

def replaceGlyphRecord(font, fontFile):
    glyfTable = font["glyf"]
    for key in glyfTable.keys():
        glyf = glyfTable[key]
        if fontFile == "TakaoGothic.ttf" and key == "aj247":
            ttPen = TTGlyphPen(glyfTable)
            ttPen.moveTo((512, 1579))
            ttPen.qCurveTo((910, 1579), (910, 821))
            ttPen.qCurveTo((910, 63), (512, 63))
            ttPen.qCurveTo((115, 63), (115, 821))
            ttPen.qCurveTo((115, 1579), None)
            ttPen.closePath()
            ttPen.moveTo((510, 1438))
            ttPen.qCurveTo((283, 1438), (283, 204), (512, 204))
            ttPen.qCurveTo((742, 204), (742, 823))
            ttPen.qCurveTo((742, 1438), None)
            ttPen.closePath()
            glyf = ttPen.glyph()
            glyfTable[key] = glyf

        coordinates = glyf.getCoordinates(glyfTable)
        coordinates[0].translate((0, -137))
        glyf.removeHinting()
    glyfTable.compile(font)

def generateFont(font, fontFile):
    os.makedirs(destDir, exist_ok = True)
    destFontFile = re.sub(r"Takao", r"Takaoka", fontFile)
    font.save(f"{destDir}/{destFontFile}")

def createRelease():
    os.makedirs(releaseDir, exist_ok = True)
    with zipfile.ZipFile(f"{releaseDir}/TakaokaFonts.zip", "w", zipfile.ZIP_DEFLATED) as zf:
        for filename in os.listdir(destDir):
            zf.write(f"{destDir}/{filename}", filename)

        zf.write("IPA_Font_License_Agreement_v1.0.txt", "LICENSE")

if __name__ == "__main__":
    downloadTakaoFonts()

    fontFiles = [filename for filename in os.listdir(srcDir) if re.search(r"\.ttf", filename)]
    for fontFile in fontFiles:
        font = TTFont(f"{srcDir}/{fontFile}")
        replaceNameRecord(font, fontFile)
        replaceGlyphRecord(font, fontFile)
        del font["cvt "]
        del font["fpgm"]
        generateFont(font, fontFile)

    createRelease()
