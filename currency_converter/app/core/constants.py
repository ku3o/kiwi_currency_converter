from os      import sep as os_sep
from os.path import (join     as path_join,
	                 normpath as path_normpath,
	                 realpath as path_realpath )
#
# Basic used directories
#
PACKAGE_DIR = path_join(*path_normpath(path_realpath(__file__)).split(os_sep)[:-3])
APP_DIR     = path_join(PACKAGE_DIR, 'app')
STORE_DIR   = path_join(PACKAGE_DIR, 'store')

#
# Currency cache directory and file
#
CURRENCY_CACHE_DIR  = path_join(STORE_DIR, 'cache')
CURRENCY_CACHE_FILE = path_join(CURRENCY_CACHE_DIR, 'cache.json')
