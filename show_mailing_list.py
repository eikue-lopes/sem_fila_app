from db2_controller import DB2Controller
from constants import ADDRESS_DB2
from os import system


db2c = DB2Controller(address_db=ADDRESS_DB2,create_schema=False)

while True:
    system("cls")
    mailing_list = db2c.get_mailing_list()

    print("\n\nLISTA COM TODOS OS EMAILS CADASTRADOS NO SISTEMA")

    for email in mailing_list:
        print("-"*100)
        print(email)
        print("-"*100)

    print("\n\n")
    input("[ENTER PARA ATUALIZAR]")