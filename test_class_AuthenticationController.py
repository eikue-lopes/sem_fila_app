from authentication_controller import AuthenticationController as Auth

#PARA TESTAR ESSA CLASSE DEVO TER DATABASE1 E DATABASE2 JÁ PRÉ-EXISTENTES


def get_all_infos_user(auth,token_id):
    db1c = auth.db1c
    db2c = auth.db2c
    app_user = db1c.get_user(token_id=token_id)
    user_login_infos = db2c.get_user_login_infos_by_linked_token_id(linked_token_id=token_id)
    return app_user.jsonify() , user_login_infos.jsonify()


auth = Auth()

opc = input("Testar flow de cadastro (C)\nTestar flow de login (L)\nPular pra operações com um cadastro existente (O) \n>> ")
if opc.lower() == 'c':
    print("\nTESTANDO ETAPAS DE CADASTRO DE UMA NOVA CONTA\n")
    name = input("Seu nome: ")
    email = input("Seu email: ")
    password = input("Sua senha: ")
    is_stabilishment = input("Você é um estabelecimento? ")

    if is_stabilishment.lower() == 's':
        is_stabilishment = True
    else:
        is_stabilishment = False

    r = auth.register_user_step1(name=name,email=email,password=password,is_stabilishment=is_stabilishment)
    print("RETORNO DA CHAMADA register_user_step1:",r)

    if r == True:
        verification_code = input("Digite o código de verificação que enviamos ao seu email: ")
        r = auth.register_user_step2(email_verification_code=verification_code)
        print("RETORNO DA CHAMADA register_user_step2:",r)
        
elif opc.lower() == 'l':
            print("TESTANDO OPERAÇÃO DE LOGIN")
            email = input("Seu email: ")
            password = input("Sua senha: ")
            r = auth.login_user(email=email,password=password)
            print("RETORNO DA CHAMADA login_user (token do usuário):",r)
            if r != None:
                print("Infos Usuário:\n",get_all_infos_user(auth,token_id=r),"\n")

else:
    opc = input("Testar o método delete (D)\nTestar o método update_name (UN)\nTestar o método update_email (UE)\nTestar o método update_password (UP)\n>>")
    if opc.lower() == 'd':
        print("\nTESTANDO MÉTODO delete_user")
        token_id = input("Token do usuário que você deseja apagar:")
        r = auth.delete_user(token_id=token_id)
        print("RETORNO DA CHAMADA delete_user:",r)
    
    elif opc.lower() == 'un':
        print("\nTESTANDO MÉTODO update_name_user")
        token_id = input("Token do usuário que você deseja atualizar:")
        new_name = input("Novo nome:")
        r = auth.update_name_user(token_id=token_id,new_name=new_name)
        print("RETORNO DA CHAMADA update_name_user:",r)
    
    elif opc.lower() == 'ue':
        print("\nTESTANDO MÉTODO update_email_user")
        token_id = input("Token do usuário que você deseja atualizar:")
        new_email = input("Novo email:")
        r = auth.update_email_user(token_id=token_id,new_email=new_email)
        print("RETORNO DA CHAMADA update_email_user:",r)
    
    elif opc.lower() == 'up':
        print("\nTESTANDO MÉTODO update_password_user")
        token_id = input("Token do usuário que você deseja atualizar:")
        old_password = input("Senha antiga:")
        new_password = input("Nova senha:")
        r = auth.update_password_user(token_id=token_id,old_password=old_password,new_password=new_password)
        print("RETORNO DA CHAMADA update_password_user:",r)


            