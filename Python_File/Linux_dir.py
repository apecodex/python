# -*- coding: utf-8 -*-

import os
from stat import *
import pwd
from datetime import datetime


Owner = {600:"-rw-------",
        644:"-rw-r--r--",
        700:"-rwx------",
        755:"-rwxr-xr-x",
        711:"-rwx--x--x",
        666:"-rw-rw-rw-",
        777:"-rwxrwxrwx"}


for i in os.listdir("."):
    file_chmod = oct(os.stat(i)[ST_MODE])[-3:]
    file_chmod_int = int(file_chmod)
    if file_chmod_int in Owner:
        print(Owner[file_chmod_int],pwd.getpwuid(os.stat(i).st_uid).pw_name,pwd.getpwuid(os.stat(i).st_uid).pw_name,os.path.getsize(i),datetime.fromtimestamp(os.stat(i).st_mtime).strftime("%m月 %d  %H:%M"),i)
        