from app_controller import AppController

print("CRIANDO INSTÂNCIA DE AppController")
ac = AppController()
print("Escolha um método pra testar:")
print("\t1-sign_in\n\t2-sign_up\n\t3-sign_up_confirmation\n\t4-jump_to_next_client_in_queue\n\t5-search_for_queues")
print("\t6-entry_on_queue\n\t7-search_for_queues_where_i_am\n\t8-exit_from_queue")
print("\t9-update_profile_name\n\t10-update_profile_email\n\t11-update_profile_password")
option = input(">> ")


if option.lower() == '1':
    print("TESTANDO MÉTODO sign_in")
    email = input("Seu email de login: ")
    password = input("Sua senha de login: ")

    r = ac.sign_in(email=email,password=password)

    print("RESPOSTA DA CHAMADA A sign_in:",r)
elif option.lower() == '2':
    print("TESTANDO MÉTODO sign_up")
    name = input("Seu nome: ")
    email = input("Seu email: ")
    password = input("Sua senha: ")
    is_stabilishment = input("É um estabelecimento? ")
    is_stabilishment =  is_stabilishment.lower() == 's'

    r = ac.sign_up(name=name,email=email,password=password,is_stabilishment=is_stabilishment)
    print("RESPOSTA DA CHAMADA A sign_up:",r)
elif option.lower() == '3':
    print("TESTANDO MÉTODO sign_up_confirmation")
    verification_code = input("Seu código de verificação: ")

    r = ac.sign_up_confirmation(verification_code=verification_code)
    print("RESPOSTA DA CHAMADA A sign_up_confirmation:",r)
elif option.lower() == '4':
    print("TESTANDO MÉTODO jump_to_next_client_in_queue")
    print("SOMENTE ESTABELECIMENTOS PODEM ACESSAR ESSA FUNCIONALIDADE")
    print("O TOKEN_ID PASSADO DEVE SER VÁLIDO")

    token_id = input("Seu token id: ")
    r = ac.jump_to_next_client_in_queue(token_id=token_id)
    print("RESPOSTA DA CHAMADA A jump_to_next_client_in_queue:",r)
elif option.lower() == '5':
    print("TESTANDO MÉTODO search_for_queues")
    print("CLIENTES E ESTABELECIMENTOS PODEM ACESSAR ESSA FUNCIONALIDADE")

    name_stabilishment_owner_queue = input("Nome do estabelecimento dono da fila: ")
    r = ac.search_for_queues(name_stabilishment_owner_queue=name_stabilishment_owner_queue)
    print("RESPOSTA DA CHAMADA A search_for_queues:",r)
elif option.lower() == '6':
    print("TESTANDO MÉTODO entry_on_queue")
    print("CLIENTES E ESTABELECIMENTOS PODEM ACESSAR ESSA FUNCIONALIDADE")
    print("O TOKEN_ID E O TOKEN_ID DO ESTABELECIMENTO PASSADOS DEVEM SER VÁLIDOS")

    token_id = input("Seu token: ")
    token_id_stabilishment_owner_queue = input("Token do estabelecimento dono da fila: ")

    r = ac.entry_on_queue(token_id=token_id,token_id_stabilishment_owner_queue=token_id_stabilishment_owner_queue)
    print("RESPOSTA DA CHAMADA A entry_on_queue:",r)
elif option.lower() == '7':
    print("TESTANDO MÉTODO search_for_queues_where_i_am")
    print("CLIENTES E ESTABELECIMENTOS PODEM ACESSAR ESSA FUNCIONALIDADE")
    print("O TOKEN_ID PASSADO DEVE SER VÁLIDO")

    token_id = input("Seu token: ")
    r = ac.search_for_queues_where_i_am(token_id=token_id)
    print("RESPOSTA DA CHAMADA A search_for_queues_where_i_am:",r)
elif option.lower() == '8':
    print("TESTANDO MÉTODO exit_from_queue")
    print("CLIENTES E ESTABELECIMENTOS PODEM ACESSAR ESSA FUNCIONALIDADE")
    print("O TOKEN_ID PASSADO DEVE SER VÁLIDO")

    token_id = input("Seu token: ")
    token_id_stabilishment_owner_queue = input("Token do dono da fila: ")
    r = ac.exit_from_queue(token_id=token_id,token_id_stabilishment_owner_queue=token_id_stabilishment_owner_queue)
    print("RESPOSTA DA CHAMADA A exit_from_queue:",r) 
elif option.lower() == '9':
    print("TESTANDO MÉTODO update_profile_name")
    print("CLIENTES E ESTABELECIMENTOS PODEM ACESSAR ESSA FUNCIONALIDADE")
    print("O TOKEN_ID PASSADO DEVE SER VÁLIDO")

    token_id = input("Seu token: ")
    new_name = input("Novo nome: ")
    r = ac.update_profile_name(token_id=token_id,new_name=new_name)
    print("RESPOSTA DA CHAMADA A update_profile_name:",r) 
elif option.lower() == '10':
    print("TESTANDO MÉTODO update_profile_email")
    print("CLIENTES E ESTABELECIMENTOS PODEM ACESSAR ESSA FUNCIONALIDADE")
    print("O TOKEN_ID PASSADO DEVE SER VÁLIDO")

    token_id = input("Seu token: ")
    new_email = input("Novo email: ")
    r = ac.update_profile_email(token_id=token_id,new_email=new_email)
    print("RESPOSTA DA CHAMADA A update_profile_email:",r) 
elif option.lower() == '11':
    print("TESTANDO MÉTODO update_profile_password")
    print("CLIENTES E ESTABELECIMENTOS PODEM ACESSAR ESSA FUNCIONALIDADE")
    print("O TOKEN_ID PASSADO DEVE SER VÁLIDO")

    token_id = input("Seu token: ")
    old_password = input("Senha antiga: ")
    new_password = input("Senha atual: ")
    r = ac.update_profile_password(token_id=token_id,old_password=old_password,new_password=new_password)
    print("RESPOSTA DA CHAMADA A update_profile_password:",r) 
