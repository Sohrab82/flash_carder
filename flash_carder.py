# ! c:\\Users\\sohra\\AppData\\Local\\Programs\\Python\\Python38\\pythonw.exe

from ui_main import Ui_MainWindow
from dict_funs import DictHandler

dh = DictHandler()
dh.load_dict()

m = Ui_MainWindow(dh)
m.run()
dh.save_dict()
dh.export_as_word()
