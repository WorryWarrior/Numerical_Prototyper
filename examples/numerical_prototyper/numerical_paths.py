import os
import sys


def resourcePath(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


resourceLocation = "Resources"
imageDirectory = resourcePath(os.path.join(resourceLocation, "Icons"))
saveDirectory = resourcePath(os.path.join(resourceLocation, "Saved Files"))
stylesheetDirectory = resourcePath(os.path.join(resourceLocation, "Stylesheet"))

editor_stylesheet_file = os.path.join(stylesheetDirectory, "nodeeditor.qss")
editor_stylesheet_dark_file = os.path.join(stylesheetDirectory, "nodeeditor-dark.qss")

run_app = os.path.join(imageDirectory, "run-icon.png")
save_file = os.path.join(imageDirectory, "file_save.png")