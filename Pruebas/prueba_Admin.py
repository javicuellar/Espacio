import ctypes, os
from sys import exit
 
 
def is_admin():
    is_admin = False
    try:
        #  Para Linux
        is_admin = os.getuid() == 0
    except AttributeError:
        print("Windows")
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
 
    print ("Admin privileges: {}".format(is_admin))
    return is_admin

is_admin()