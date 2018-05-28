from core.initializer import Initializer
from core.converter import Converter

ini = Initializer()
con = Converter()

# ini.init_metadata_database()

print(con.convert('USD', 'EUR', 10))
