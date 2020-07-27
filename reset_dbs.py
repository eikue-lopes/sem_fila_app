from db1_controller import DB1Controller
from db2_controller import DB2Controller
from constants import ADDRESS_DB1 , ADDRESS_DB2

def reset_dbs():
    DB1Controller(address_db=ADDRESS_DB1,create_schema=True)
    DB2Controller(address_db=ADDRESS_DB2,create_schema=True)



print("APAGANDO TODOS OS REGISTRO DOS BANCOS DE DADOS")
reset_dbs()