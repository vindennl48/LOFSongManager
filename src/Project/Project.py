from src.Project.Base import Base
from src.Project.Upload import Upload
from src.Project.Download import Download
from src.Project.Extract import Extract
from src.Project.Compress import Compress
from src.Project.Open import Open

class Project(Base, Upload, Download, Extract, Compress, Open):
    pass
