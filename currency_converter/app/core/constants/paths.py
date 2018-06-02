from os      import sep as os_sep
from os.path import (join     as path_join,
	                 normpath as path_normpath,
	                 realpath as path_realpath )
#
# Basic used directories
#
PACKAGE_DIR = path_join('/', *path_normpath(path_realpath(__file__)).split(os_sep)[:-4])
APP_DIR     = path_join(PACKAGE_DIR, 'app')
STORE_DIR   = path_join(PACKAGE_DIR, 'store')

#
# Database
#
DATABASE_DIR = path_join(STORE_DIR, 'db')
DATABASE_FILE = path_join(DATABASE_DIR, 'cache.sqlite')
