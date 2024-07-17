import os
import sys
os.chdir(sys.path[0])
from view import GridView

gui = GridView(20, 12, 50)
gui.mainloop()
