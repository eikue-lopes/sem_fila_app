from constants import ADDRESS_DB1
from authentication_controller import AuthenticationController
from db1_controller import DB1Controller
import json

"""
DB1:
    
    update_queue_stabilishment -> Quando estabelecimento tira cliente de sua fila ou quando cliente deseja sair de uma determinada fila
    get_user -> Quando eu quero o registro de um dado cliente no db1
    get_only_clients -> Quando eu quero pegar somente os clientes no db1
    get_only_stabilishments -> Quando eu quero pegar somente os estabelecimentos no db1 (na listagem de filas por exemplo)
    is_client -> Quando eu quero confirmar se um user é um cliente ou não
    is_stabilishment -> Quando eu quero confirmar se um user é um estabelecimento ou não
    get_num_clients -> Quando quero saber o número de clientes em db1
    get_num_stabilishments -> Quando quero saber o número de estabelecimentos em db1

Auth:
    
    login_user -> Quando eu quero logar um usuário 
    register_user_step1 -> Quando usuário insere seus dados para cadastro e deve ser gerado e enviado ao seu email um código de verificação
    register_user_step2 -> Quando o usuário insere o código que foi enviado ao seu email e eu confirmo o cadastro dele
    delete_user -> Quando usuário pede pra apagar sua conta cadastrada no sistema
    update_name_user -> Quando usuário deseja mudar seu nome no sistema
    update_email_user -> Quando usuário deseja mudar seu email no sistema
    update_password_user -> Quando usuário deseja mudar sua senha no sistema
"""
class AppController:
    """
        Provê todos os métodos necessários ao recebimento, processamento e entrega de dados da Api às bases de dados.
    """

    def __init__(self):
        self.auth = AuthenticationController()
        self.db1c = DB1Controller(address_db=ADDRESS_DB1,create_schema=False)
    
    def sign_in(self,email,password):
        """
        Recebe email e senha do usuário e retorna seu id de acesso ao sistema
        """
        r = self.auth.login_user(email=email,password=password)
        return r
    
    def sign_up(self,name,email,password,is_stabilishment):
        """
        Recebe nome, email , senha e flag que indica se é estabelecimento e realiza a primeira parte do processo
        de cadastro de novo usuário no sistema.
        """
        r = self.auth.register_user_step1(name=name,email=email,password=password,is_stabilishment=is_stabilishment)
        return r
    
    def sign_up_confirmation(self,verification_code):
        """
        Recebe um código de verificação de email passado pelo usuário e realiza a segunda parte do processo de cadastro
        de novo usuário no sistema.
        """
        r = self.auth.register_user_step2(email_verification_code=verification_code)
        return r
    
    def jump_to_next_client_in_queue(self,token_id):
        """
            Requisição feita por somente ESTABELECIMENTOS
            
            Recebe da Api um token_id do usuário que está utilizando o app e, se esse usuário for um estabelecimento,
            faz a ação de avançar sua própria fila pro próximo cliente da mesma. Em resumo, esse método deve ser chamado
            quando um estabelecimento acabou de atender um cliente da fila e deve chamar o próximo cliente dessa fila.
        """
        logged_user = self.db1c.get_user(token_id=token_id)
        
        if logged_user == None:
            return False

        if logged_user.is_stabilishment == False:
            return False
        
        r = logged_user.queue.remove()
        
        if r == False:
            return False
        
        r = self.db1c.update_queue_stabilishment(token_id=logged_user.token_id,new_queue_stabilishment=logged_user.queue)
       
        return r
    
    def search_for_queues(self,name_stabilishment_owner_queue):
        """
            Requisição feita por CLIENTES e ESTABELECIMENTOS
            
            Recebe da Api o nome de um estabelecimento e retorna no formato JSON a fila desse estabelecimento para
            que o app consiga listar o resultado da busca pelo nome do mesmo.
        """
        user_login_info = self.auth.db2c.get_user_login_infos_by_name(name=name_stabilishment_owner_queue)
        
        if user_login_info == None:
            return None

        user = self.db1c.get_user(token_id=user_login_info.linked_token_id)
        
        if user == None:
            return None
        
        if user.is_stabilishment == False:
            return None
        
        return user.queue.clients_tokens
    
    def search_for_queues_where_i_am(self,token_id):
        """
            Requisição feita por CLIENTES e ESTABELECIMENTOS
            
            Recebe da Api o token_id de quem fez a requisição e retorna no formato JSON todas as filas em que esse usuário
            se encontra (id do dono da fila e nome do mesmo), a sua respectiva posição na fila e o timestamp em que entrou na mesma.
        """
        queues = {}
        stabilishments = self.db1c.get_only_stabilishments()
        
        for s in stabilishments:
            user_login_info = self.auth.db2c.get_user_login_infos_by_linked_token_id(linked_token_id=s.token_id)
            
            if user_login_info == None:
                return None
        
            token , element_in_queue =  s.queue.get_by_token_id(token_id=token_id)
            if token != None and element_in_queue != None:
                element_in_queue['name_stabilishment_owner'] = user_login_info.name
                queues[s.token_id] = element_in_queue
        
        return json.dumps(queues)

    def entry_on_queue(self,token_id,token_id_stabilishment_owner_queue):
        """
            Requisição feita por CLIENTES e ESTABELECIMENTOS
            
            Recebe da Api o token_id do estabelecimento que contém a fila em que o usuário (cliente ou outro estabelecimento) 
            deseja entrar e executa a ação de inserir o usuário que fez a requisição dentro dessa fila.
        """

        #evitando que usuário entre em sua própria fila
        if token_id == token_id_stabilishment_owner_queue:
            return False
        
        user_logged = self.db1c.get_user(token_id=token_id)
        
        if user_logged == None:
            return False
        
        user_owner_queue = self.db1c.get_user(token_id=token_id_stabilishment_owner_queue)
        
        if user_owner_queue == None:
            return False
        
        if user_owner_queue.is_stabilishment == False:
            return False
        
        user_owner_queue.queue.add(token_id=token_id)

        r = self.db1c.update_queue_stabilishment(token_id=user_owner_queue.token_id,new_queue_stabilishment=user_owner_queue.queue)
        return r

    def exit_from_queue(self,token_id,token_id_stabilishment_owner_queue):
        """
            Requisição feita por CLIENTES e ESTABELECIMENTOS
            
            Recebe da Api o token_id do estabelecimento que contém a fila em que o usuário (cliente ou estabelecimento)
            deseja sair e executa a ação de remover esse usuário dessa fila (aqui a remoção foje a regra da fila, ou seja,
            deve ser feita em qualquer posição da mesma)
            
        """
        user_client = self.db1c.get_user(token_id=token_id)
        user_stabilishment = self.db1c.get_user(token_id=token_id_stabilishment_owner_queue)
        
        if user_client == None or user_stabilishment == None:
            return False
        
        if user_stabilishment.is_stabilishment == False:
            return False
        
        queue = user_stabilishment.queue
        
        if token_id not in queue.clients_tokens:
            return False

        del(queue.clients_tokens[token_id])
        
        r = self.db1c.update_queue_stabilishment(token_id=token_id_stabilishment_owner_queue,new_queue_stabilishment=queue)
        return r

    def update_profile_name(self,token_id,new_name):
        """
            Requisição feita por CLIENTES e ESTABELECIMENTOS
            
            Recebe da Api o token_id do usuário que está fazendo a requisição e muda o nome desse usuário 
            para new_name.
        """
        r = self.auth.update_name_user(token_id=token_id,new_name=new_name)
        return r
    
    def update_profile_email(self,token_id,new_email):
        """
            Requisição feita por CLIENTES e ESTABELECIMENTOS
            
            Recebe da Api o token_id do usuário que está fazendo a requisição e muda o email desse usuário 
            para new_email.
        """
        r = self.auth.update_email_user(token_id=token_id,new_email=new_email)
        return r
    
    def update_profile_password(self,token_id,old_password,new_password):
        """
            Requisição feita por CLIENTES e ESTABELECIMENTOS
            
            Recebe da Api o token_id e a antiga senha do usuário que está fazendo a requisição e muda a senha desse usuário para 
            new_password se a antiga senha bater (db2 já faz tal validação) com o registrado em db2.
        """
        r = self.auth.update_password_user(token_id=token_id,old_password=old_password,new_password=new_password)
        return r
    
    
    
    
    
    
