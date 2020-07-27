from db1_models import Queue
from time import time

q = Queue()

print("ADICIONANDO 3 TOKENS")

q.add(token_id='123')
q.add(token_id='456')
q.add(token_id='789')

print("\nMOSTRANDO FILA NO FORMATO JSON")
print(q.jsonify())

print("\nREMOVENDO UM ELEMENTO DA FILA")
q.remove()

print("\nMOSTRANDO FILA NO FORMATO JSON")
print(q.jsonify())

print("\nADICIONANDO 4 TOKENS")
q.add(token_id = '101112')
q.add(token_id = '131415')
q.add(token_id = '161718')
q.add(token_id = '192021')

print("\nMOSTRANDO FILA NO FORMATO JSON")
print(q.jsonify())

print("\nPEGANDO O PRIMEIRO ELEMENTO DA FILA")
token,element = q.get_first()
print("token:",token,"element:",element)

print("\nPEGANDO O ÚLTIMO ELEMENTO DA FILA")
token,element = q.get_last()
print("token:",token,"element:",element)

print("\nPEGANDO ELEMENTO PELO TOKEN PASSADO")
token,element = q.get_by_token_id(token_id='131415')
print("token:",token,"element:",element)

print("\nPEGANDO ELEMENTO PELA POSIÇÃO PASSADA")
token,element = q.get_by_position(position=2)
print("token:",token,"element:",element)

print("\nRETORNANDO POSIÇÃO DE UM DETERMINADO ELEMENTO DADO UM TOKEN_ID")
position_element = q.get_position(token_id='101112')
print("position:",position_element)

print("\nRETORNANDO TOKEN_ID DE UM DETERMINADO ELEMENTO DADA UMA POSIÇÃO")
token = q.get_token_id(position=3)
print("token:",token)

print("\n\nRETORNANDO TAMANHO DA FILA")
size = q.get_size()
print("size:",size)

print("\n\nRETORNANDO SE A FILA ESTÁ VAZIA OU NÃO")
r = q.is_empty()
print("is empty?",r)