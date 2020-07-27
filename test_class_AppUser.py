from db1_models import AppUser
from time import time
print("CRIANDO DOIS CLIENTES")
client = AppUser(is_stabilishment=False,generate_token_id=True)

client2 = AppUser(is_stabilishment=False,generate_token_id=True)


print("\nCRIANDO UM ESTABELECIMENTO")
stabilishment = AppUser(is_stabilishment=True,generate_token_id=True)


print("\nADICIONANDO UM CLIENTE NA FILA DO ESTABELECIMENTO CRIADO")
stabilishment.queue.add(token_id=client.token_id)

print("\nMOSTRANDO OS DOIS CLIENTES NO FORMATO JSON")
print(client.jsonify())
print(client2.jsonify())

print("\nMOSTRANDO O ESTABELECIMENTO NO FORMATO JSON")
print(stabilishment.jsonify())