from src.Project.Base import Base
from src.Project.Open import Open
from src.Project.Extract import Extract
from src.Project.Compress import Compress

class Project(Base, Open, Extract, Compress):
    pass
