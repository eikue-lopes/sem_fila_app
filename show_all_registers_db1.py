from db1_controller import DB1Controller
from constants import ADDRESS_DB1
from os import system


db1c = DB1Controller(address_db=ADDRESS_DB1,create_schema=False)

while True:
    system("cls")
    clients = db1c.get_only_clients()
    stabilishments = db1c.get_only_stabilishments()

    print("\n\nCLIENTES")
    for c in clients:
        print("-"*100)
        print("token_id:",c.token_id)
        print("is_stabilishment:",c.is_stabilishment)
        print("-"*100)

    print("ESTABELECIMENTOS")
    for s in stabilishments:
        print("-"*100)
        print("token_id:",s.token_id)
        print("is_stabilishment:",s.is_stabilishment)
        print("-"*100)

    print("\n\n")
    input("[ENTER PARA ATUALIZAR]")