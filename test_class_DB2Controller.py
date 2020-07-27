from db2_controller import DB2Controller as DB
from db2_models import UserLoginInfos
from constants import ADDRESS_DB2
from db1_models import AppUser
from time import time

print("CRIANDO UM OBJETO DB")
db = DB(address_db=ADDRESS_DB2,create_schema=True)

print("\nADICIONANDO 3 INFORMAÇÕES DE LOGIN (USUÁRIOS)")
user1 = UserLoginInfos(name="Eikue",email="eikue@gmail.com",password_encrypted="abcdef",linked_token_id="123")
user2 = UserLoginInfos(name="Ademe",email="ademe@hotmail.com",password_encrypted="ghijkl",linked_token_id="456")
user3 = UserLoginInfos(name="Joelma",email="mjoelma@yahoo.com",password_encrypted="mnopqr",linked_token_id="789")

r = db.add_user_login_infos(user1,True)
r2 = db.add_user_login_infos(user2,True)
r3 = db.add_user_login_infos(user3,True)

print("RETORNOS DAS CHAMADAS add_user_login_infos:",r,r2,r3)

print("\nPEGANDO QUANTIDADE TOTAL DE USUÁRIOS")
nu = db.get_num_users_login_infos()
print("qtd users:",nu)


print("\nTESTANDO email_already_exists COM EMAIL EXISTENTE")
exists = db.email_already_exists(email="ademe@hotmail.com")
print("RETORNO DA CHAMADA email_already_exists:",exists)

print("\nTESTANDO email_already_exists COM EMAIL INEXISTENTE")
exists = db.email_already_exists(email="emailinexistente@yahoo.com.br")
print("RETORNO DA CHAMADA email_already_exists:",exists)

print("\nTESTANDO MÉTODO get_user_login_infos_by_linked_token_id")
user = db.get_user_login_infos_by_linked_token_id(linked_token_id=user3.linked_token_id)
print("user login info:",user)


print("\nADICIONANDO MAIS UMA INFORMAÇÃO DE LOGIN (USUÁRIO) PARA REMOVÊ-LA DEPOIS")
user4 = UserLoginInfos(name="Toquinho",email="toquinho@gmail.com",password_encrypted="stuvxz",linked_token_id="101112")
r = db.add_user_login_infos(user4,True)
print("RETORNO DA CHAMADA add_user_login_infos:",r)

print("\nPEGANDO QUANTIDADE TOTAL DE USUÁRIOS ANTES DA REMOÇÃO DO USUÁRIO CRIADO ACIMA")
nu = db.get_num_users_login_infos()
print("qtd users:",nu)

print("\nTESTANDO MÉTODO remove_user_login_infos")
r = db.remove_user_login_infos(linked_token_id=user4.linked_token_id)
print("RETORNO DA CHAMADA remove_user_login_infos:",r)

print("\nPEGANDO QUANTIDADE TOTAL DE USUÁRIOS APÓS A REMOÇÃO DO USUÁRIO FEITA ACIMA ")
nu = db.get_num_users_login_infos()
print("qtd users:",nu)

print("\nTESTANDO MÉTODO get_linked_token_id PARA DADOS EXISTENTES NA BASE DE DADOS")
linked_token_id = db.get_linked_token_id(email="eikue@gmail.com",password_encrypted="abcdef")
print("linked token id:",linked_token_id)

print("\nTESTANDO MÉTODO get_linked_token_id PARA DADOS INEXISTENTES NA BASE DE DADOS")
linked_token_id = db.get_linked_token_id(email="email.inexistente@gmail.com",password_encrypted="abcdef")
print("linked token id:",linked_token_id)

print("\nTESTANDO MÉTODO update_user_login_infos_name")
r = db.update_user_login_infos_name(linked_token_id="123",new_name="Ruby")
print("RETORNO DA CHAMADA update_user_login_infos_name:",r)

print("\nTESTANDO MÉTODO update_user_login_infos_email")
r = db.update_user_login_infos_email(linked_token_id="123",new_email="cat_ruby@outlook.com.br")
print("RETORNO DA CHAMADA update_user_login_infos_email:",r)

print("\nTESTANDO MÉTODO update_user_login_infos_password_encrypted")
r = db.update_user_login_infos_password_encrypted(linked_token_id="123",new_password_encrypted="567890")
print("RETORNO DA CHAMADA update_user_login_infos_password_encrypted:",r)

print("\nTESTANDO MÉTODO add_user_login_infos COM LINKED_TOKEN_ID JÁ EXISTENTE (DEVE RETORNAR NONE)")
user5 = UserLoginInfos(name="Lia",email="gatinha.lia2020@gmail.com",password_encrypted="345rty@#d",linked_token_id="456")
r = db.add_user_login_infos(user5,True)
print("RETORNO DA CHAMADA add_user_login_infos:",r)


print("\nTESTANDO MÉTODO add_user_login_infos COM EMAIL JÁ EXISTENTE (DEVE RETORNAR NONE)")
user6 = UserLoginInfos(name="Lia",email="cat_ruby@outlook.com.br",password_encrypted="345rty@#d",linked_token_id="565758")
r = db.add_user_login_infos(user6,True)
print("RETORNO DA CHAMADA add_user_login_infos:",r)



user = AppUser(is_stabilishment=False,generate_token_id=True)

#REGISTROS DE CÓDIGO DE VERIFICAÇÃO

print("\nTESTANDO MÉTODO add_infos_user_register PARA ATRIBUTOS TOTALMENTE INEDITOS (DEVE RETORNAR TRUE )")
user_login_infos = UserLoginInfos(name="joão das neves",email="joao2013@hotmail.com",password_encrypted="123abc",linked_token_id=user.token_id)
r = db.add_infos_user_register(is_stabilishment=user.is_stabilishment,user_login_infos=user_login_infos,email_verification_code=123456,timestamp=time())
print("RETORNO DA CHAMADA add_infos_user_register:",r)


print("\nTESTANDO MÉTODO add_infos_user_reggister COM UM CÓDIGO DE VERIFICAÇÃO JÁ EXISTENTE (DEVE RETORNAR FALSE)")
user_login_infos = UserLoginInfos(name="Pedro Caipira",email="caipira.daroca@gmail.com",password_encrypted="12fsd3abc",linked_token_id='45245246546578787fgsfgf')
r = db.add_infos_user_register(is_stabilishment=user.is_stabilishment,user_login_infos=user_login_infos,email_verification_code=123456,timestamp=time())
print("RETORNO DA CHAMADA add_infos_user_register:",r)


print("\nTESTANDO MÉTODO add_infos_user_reggister COM UM EMAIL JÁ ASSOCIADO A ALGUMA CONTA EXISTENTE (DEVE RETORNAR FALSE)")
user_login_infos = UserLoginInfos(name="Rubens Barrichelo",email="cat_ruby@outlook.com.br",password_encrypted="1fsfd3323abc",linked_token_id='fdsljfjdiofjslkejureureru493857eiu')
r = db.add_infos_user_register(is_stabilishment=user.is_stabilishment,user_login_infos=user_login_infos,email_verification_code=857439,timestamp=time())
print("RETORNO DA CHAMADA add_infos_user_register:",r)


print("\nTESTANDO MÉTODO add_infos_user_reggister COM UM TOKEN_ID JÁ ASSOCIADO A ALGUMA CONTA EXISTENTE (DEVE RETORNAR FALSE)")
user_login_infos = UserLoginInfos(name="Serjão Berranteiro",email="berranterio_serjao@gmail.com.br",password_encrypted="dfsdfe343c",linked_token_id="123")
r = db.add_infos_user_register(is_stabilishment=user.is_stabilishment,user_login_infos=user_login_infos,email_verification_code=111909,timestamp=time())
print("RETORNO DA CHAMADA add_infos_user_register:",r)


print("\nTESTANDO MÉTODO get_infos_user_register_linked_by_email_verification_code PARA CÓDIGO DE VERIFICAÇÃO EXISTENTE")
user , user_li , timestamp = db.get_infos_user_register_linked_by_email_verification_code(email_verification_code=123456)
print("RETORNO DA CHAMADA get_infos_user_register_linked_by_email_verification_code:",user,user_li,timestamp)

print("\nTESTANDO MÉTODO get_infos_user_register_linked_by_email_verification_code PARA CÓDIGO DE VERIFICAÇÃO INEXISTENTE")
user , user_li , timestamp = db.get_infos_user_register_linked_by_email_verification_code(email_verification_code=999999)
print("RETORNO DA CHAMADA get_infos_user_register_linked_by_email_verification_code:",user,user_li,timestamp)

print("\nTESTANDO MÉTODO email_verification_code_is_valid PARA CÓDIGO EXISTENTE")
r = db.email_verification_code_is_valid(email_verification_code=123456)
print("RETORNO DA CHAMADA email_verification_code_is_valid:",r)

print("\nTESTANDO MÉTODO email_verification_code_is_valid PARA CÓDIGO INEXISTENTE")
r = db.email_verification_code_is_valid(email_verification_code=999999)
print("RETORNO DA CHAMADA email_verification_code_is_valid:",r)

print("\nTESTANDO MÉTODO delete_infos_user_register_linked_by_email_verification_code PARA CÓDIGO EXISTENTE")
r = db.delete_infos_user_register_linked_by_email_verification_code(email_verification_code=123456)
print("RETORNO DA CHAMADA delete_infos_user_register_linked_by_email_verification_code:",r)

print("\nTESTANDO MÉTODO delete_infos_user_register_linked_by_email_verification_code PARA CÓDIGO INEXISTENTE")
r = db.delete_infos_user_register_linked_by_email_verification_code(email_verification_code=990984)
print("RETORNO DA CHAMADA delete_infos_user_register_linked_by_email_verification_code:",r)

print("\nTESTANDO MÉTODO get_mainling_list")
ml = db.get_mainling_list()
print("RETORNO DA CHAMADA get_mainling_list:",ml)

