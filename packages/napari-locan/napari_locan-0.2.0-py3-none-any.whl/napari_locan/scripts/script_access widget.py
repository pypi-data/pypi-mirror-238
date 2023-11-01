"""
Say hello!
"""
from napari_locan import MyWidget  # noqa F401

instance_of_mywidget = MyWidget.instance()

print("File type:", instance_of_mywidget.file_type)
