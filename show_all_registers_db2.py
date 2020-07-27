from db2_controller import DB2Controller
from constants import ADDRESS_DB2
from os import system


db2c = DB2Controller(address_db=ADDRESS_DB2,create_schema=False)

while True:
    system("cls")
    all_users_login_infos = db2c.get_all_users_login_infos()

    print("\n\nINFORMAÇÕES DE LOGIN TODOS OS USUÁRIOS")

    for uli in all_users_login_infos.values():
        print("-"*100)
        print("name:",uli.name)
        print("email:",uli.email)
        print("password_encrypted:",uli.password_encrypted)
        print("token_id:",uli.linked_token_id)
        print("-"*100)

    print("\n\n")
    input("[ENTER PARA ATUALIZAR]")