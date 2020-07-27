from authentication_controller import AuthenticationController as Auth



def get_all_infos_user(auth,token_id):
    db1c = auth.db1c
    db2c = auth.db2c
    app_user = db1c.get_user(token_id=token_id)
    user_login_infos = db2c.get_user_login_infos_by_linked_token_id(linked_token_id=token_id)
    return app_user.jsonify() , user_login_infos.jsonify()


#PARA TESTAR ESSA CLASSE DEVO TER DATABASE1 E DATABASE2 JÁ PRÉ-EXISTENTES

auth = Auth()

opc = input("Testar flow de cadastro ou pular pra operações com um cadastro existente? (S/N)")
if opc.lower() == 's':
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
        
        if r == True:
            print("TENTANDO LOGAR NA CONTA RECÉM CRIADA")
            email = input("Seu email: ")
            password = input("Sua senha: ")
            r = auth.login_user(email=email,password=password)
            print("RETORNO DA CHAMADA login_user (token do usuário):",r)
            if r != None:
                print("Infos Usuário:\n",get_all_infos_user(auth,token_id=r),"\n")
                
                
else:
    print("\nTESTANDO MÉTODO delete_user")
    r = auth.delete_user(token_id=r)
    print("RETORNO DA CHAMADA delete_user:",r)


            