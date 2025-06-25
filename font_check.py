import os

path = "E:/Aalap Shah/anesthesia_report/DejaVuSans.ttf"
print("Exists:", os.path.exists(path))
print("Readable:", os.access(path, os.R_OK))
