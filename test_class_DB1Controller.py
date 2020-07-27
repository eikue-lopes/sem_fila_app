from db1_controller import DB1Controller as DB
from db1_models import AppUser , Queue
from constants import ADDRESS_DB1

print("CRIANDO UM OBJETO DB")
db = DB(address_db=ADDRESS_DB1,create_schema=True)

print("\nADICIONANDO 2 USUÁRIOS CLIENTES E 1 USUÁRIO ESTABELECIMENTO")
client = AppUser(is_stabilishment=False,generate_token_id=True)
client2 = AppUser(is_stabilishment=False,generate_token_id=True)
stabilishment = AppUser(is_stabilishment=True,generate_token_id=True)
r = db.add_user(client)
r2 = db.add_user(client2)
r3 = db.add_user(stabilishment)
print("RETORNOS DAS CHAMADAS add_user:",r,r2,r3)

print("\nPEGANDO QUANTIDADE TOTAL DE USUÁRIOS (CLIENTES + ESTABELECIMENTOS)")
nu = db.get_num_users()
print("qtd users:",nu)

print("\nPEGANDO QUANTIDADE DE CLIENTES")
nc = db.get_num_clients()
print("qtd clients:",nc)

print("\nPEGANDO QUANTIDADE DE ESTABELECIMENTOS")
ns = db.get_num_stabilishments()
print("qtd stabilishments:",ns)

print("\nTESTANDO MÉTODO is_client PARA UM CLIENTE")
print("is client?",db.is_client(token_id=client.token_id))

print("\nTESTANDO MÉTODO is_client PARA UM ESTABELECIMENTO")
print("is client?",db.is_client(token_id=stabilishment.token_id))

#print("\nTESTANDO MÉTODO is_client PARA UM TOKEN INVÁLIDO")
#print("is client?",db.is_client(token_id='token invalido'))



print("\nTESTANDO MÉTODO is_stabilishment PARA UM ESTABELECIMENTO")
print("is stabilishment?",db.is_stabilishment(token_id=stabilishment.token_id))

print("\nTESTANDO MÉTODO is_stabilishment PARA UM CLIENTE")
print("is stabilishment?",db.is_stabilishment(token_id=client.token_id))

#print("\nTESTANDO MÉTODO is_stabilishment PARA UM TOKEN INVÁLIDO")
#print("is stabilishment?",db.is_stabilishment(token_id='token invalido'))



print("\nTESTANDO MÉTODO get_only_clients")
clients = db.get_only_clients()
print("clients:",clients)

print("\nTESTANDO MÉTODO get_only_stabilishments")
stabilishments = db.get_only_stabilishments()
print("stabilishments:",stabilishments)


print("\nTESTANDO MÉTODO get_user")
user = db.get_user(token_id=client2.token_id)
print("user:",user)

print("\nADICIONANDO MAIS UM CLIENTE PARA REMOVÊ-LO DEPOIS")
client3 = AppUser(is_stabilishment=False,generate_token_id=True)
r4 = db.add_user(client3)
print("RETORNO DA CHAMADA add_user:",r4)

print("\nPEGANDO QUANTIDADE TOTAL DE USUÁRIOS (CLIENTES + ESTABELECIMENTOS) ANTES DA REMOÇÃO DO CLIENTE")
nu = db.get_num_users()
print("qtd users:",nu)

print("\nTESTANDO MÉTODO remove_user")
r5 = db.remove_user(token_id=client3.token_id)
print("RETORNO DA CHAMADA remove_user:",r5)

print("\nPEGANDO QUANTIDADE TOTAL DE USUÁRIOS (CLIENTES + ESTABELECIMENTOS) APÓS A REMOÇÃO DO CLIENTE FEITA ACIMA ")
nu = db.get_num_users()
print("qtd users:",nu)

print("\nTESTANDO O MÉTODO update_queue_stabilishment COM UMA FILA DE 2 CLIENTES EM NOSSO ÚNICO ESTABELECIMENTO NA BASE DE DADOS")
new_queue = Queue()
new_queue.add(token_id=client.token_id)
new_queue.add(token_id=client2.token_id)
r6 = db.update_queue_stabilishment(token_id=stabilishment.token_id,new_queue_stabilishment=new_queue)
print("\nRETORNO DA CHAMADA update_queue_stabilishment:",r6)

print("\nTESTANDO O MÉTODO update_queue_stabilishment COM UMA FILA DE 2 CLIENTES EM UM CLIENTE (O QUE DEVE GERAR RETORNO FALSE) NA BASE DE DADOS")
new_queue = Queue()
new_queue.add(token_id=client.token_id)
new_queue.add(token_id=client2.token_id)
r7 = db.update_queue_stabilishment(token_id=client.token_id,new_queue_stabilishment=new_queue)
print("\nRETORNO DA CHAMADA update_queue_stabilishment:",r7)



