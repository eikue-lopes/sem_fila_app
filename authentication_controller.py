from db1_controller import DB1Controller
from db2_controller import DB2Controller
from db1_models import AppUser
from db2_models import UserLoginInfos
from constants import ADDRESS_DB1 , ADDRESS_DB2 , APP_EMAIL, APP_PASSWORD_EMAIL , SSL_EMAIL_HOST , SSL_EMAIL_HOST_PORT
from hashlib import sha256
from random import randrange
import smtplib
from email.mime.text import MIMEText
from time import time

class AuthenticationController:
    def __init__(self):
        self.db1c = DB1Controller(address_db=ADDRESS_DB1,create_schema=False)
        self.db2c = DB2Controller(address_db=ADDRESS_DB2,create_schema=False)
    

    def login_user(self,email,password):
        """
            Recebe o email e senha do app controller e retorna
            o token_id associado a essa conta se ela existir
            se não existir retorna None
        """
        
        password_encrypted = self.__encrypt_password(password=password)
        token_id = self.db2c.get_linked_token_id(email=email,password_encrypted=password_encrypted)
        
        return token_id
    
    #quando o usuário registra seu nome, email, senha e se ele é um estabelecimento no formulário de cadastro do app
    def register_user_step1(self,name,email,password,is_stabilishment):
        """
            Recebe um nome , um email, uma senha,  e uma flag dizendo se o usuário 
            é um estabelecimento, gera um código de verificação desse email,
            envia esse código ao email passado, salva as infos de cadastro linkadas 
            ao código de verificação gerado na base de dados 2
            Retorna True se tudo ocorreu bem e False se deu algum erro.
        """
        code = self.__generate_email_verification_code()

        password_encrypted = self.__encrypt_password(password=password)
        
        token_id = AppUser(is_stabilishment=is_stabilishment,generate_token_id=True).token_id
        user_login_infos_aux = UserLoginInfos(name=name,email=email,password_encrypted=password_encrypted,linked_token_id=token_id)

        response = self.db2c.add_infos_user_register(is_stabilishment=is_stabilishment,user_login_infos=user_login_infos_aux,email_verification_code=code,timestamp=time())
        
        if response == True:
            response2 = self.__send_email_verification_code(user_email=email,code=code)
            return response2
        else:
            return False

    #quando o usuário do app pega o código de verificação no seu email e o insere na tela de confirmação de email
    def register_user_step2(self,email_verification_code):
        """
            Recebe um código de verificação de email e, se esse código for válido, faz o cadastro do novo usuário
            na base de dados 2
            Retorna True se o cadastro foi realizado com sucesso e False se ocorreu algum erro.
        """
        if self.db2c.email_verification_code_is_valid(email_verification_code=email_verification_code) == True:
            is_stabilishment,user_login_infos,_ = self.db2c.get_infos_user_register_linked_by_email_verification_code(email_verification_code=email_verification_code)

            if user_login_infos != None:
                self.db2c.delete_infos_user_register_linked_by_email_verification_code(email_verification_code=email_verification_code)
                
                app_user = AppUser(is_stabilishment=is_stabilishment,generate_token_id=False)
                app_user.token_id = user_login_infos.linked_token_id
                
                response = self.__register_user(app_user=app_user,user_login_infos=user_login_infos)
                
                return response
            else:
                return False
        else:
            return False
    
    def __generate_email_verification_code(self):
        """
            Retorna um código aleatório de verificação com 6 dígitos.
        """
        return randrange(100000,1000000)
    
    def __send_email_verification_code(self,user_email,code):
        try:
            message = MIMEText('<p>Seu código de verificação no App SemFila:</p> <p><b>%s</b></p>'%code,_subtype='html')
            message['subject'] = "Verificação de Email SemFila App"
            message['from'] = APP_EMAIL
            message['to'] = user_email
            server = smtplib.SMTP_SSL(SSL_EMAIL_HOST,SSL_EMAIL_HOST_PORT)
            server.login(APP_EMAIL,APP_PASSWORD_EMAIL)
            server.sendmail(APP_EMAIL,user_email,message.as_string())
            server.quit()
            return True
        except:
            return False
    
    def __register_user(self,app_user,user_login_infos):
        """
            Recebe um objeto app_user e um objeto user_login_infos e
            tenta registrar esse novo usuário no banco de dados 1 e 2
            Retorna True se deu certo o registro ou False se deu algum erro
        """
    

        response_db2c = self.db2c.add_user_login_infos(user_login_infos=user_login_infos,also_add_to_mailing_list=True)
        
        if response_db2c == False:
            return False
        
        response_db1c = self.db1c.add_user(user=app_user)
        
        if response_db1c == False:
            #se deu erro ao adicionar o user no db1 então eu apago o que já tinha inserido no db2
            response = self.db2c.remove_user_login_infos(linked_token_id=user_login_infos.linked_token_id)
            
            #se não consegui evitar a inconsistência de dados, levanto uma exceção
            if response == False:
                raise Exception("Inconsitência de dados entre os Bancos de Dados acaba de ser criada (TOKEN:%s está no db2, porém não está no db1)(MÉTODO register_user(...) em authentication_controller"%user_login_infos.linked_token_id)
        
            return False
        
        return True

    def delete_user(self,token_id):
        """
            Apaga o usuário com o token_id passado da base de dados 1 e 2
            Retorna True se deu certo a operação ou False se deu algum erro.
        """
        response_db2c = self.db2c.remove_user_login_infos(linked_token_id=token_id)
        
        if response_db2c == False:
            return False
        
        
        response_db1c = self.db1c.remove_user(token_id=token_id)
        
        #se eu apaguei o usuário do db2, mas não consegui apagá-lo do db1, levanto uma exceção
        if response_db1c == False:
            raise Exception("Inconsitência de dados entre os Bancos de Dados acaba de ser criada (TOKEN:%s foi apagado do db2, porém não foi apagado do db1)(MÉTODO delete_user(...) em authentication_controller"%token_id)

        return True
    
    def update_name_user(self,token_id,new_name):
        """
            Atualiza o nome do usuário com o token_id passado.
            Retorna True se deu certo a operação ou False se deu algum erro.
        """
        response = self.db2c.update_user_login_infos_name(linked_token_id=token_id,new_name=new_name)
        return response
    
    def update_email_user(self,token_id,new_email):
        """
            Atualiza o email do usuário com o token_id passado.
            Retorna True se deu certo a operação ou False se deu algum erro.
        """
        response = self.db2c.update_user_login_infos_email(linked_token_id=token_id,new_email=new_email)
        return response
    
    def update_password_user(self,token_id,old_password,new_password):
        """
            Atualiza a senha do usuário com o token_id passado.
            Retorna True se deu certo a operação ou False se deu algum erro.
        """
        
        user_login_info = self.db2c.get_user_login_infos_by_linked_token_id(linked_token_id=token_id)
        
        if user_login_info == None:
            return False
        
        if self.__encrypt_password(password=old_password) != user_login_info.password_encrypted:
            return False
        
        response = self.db2c.update_user_login_infos_password_encrypted(linked_token_id=token_id,new_password_encrypted=self.__encrypt_password(password=new_password))
        
        return response
    
    #lembrando que o password deverá vir com uma encriptação feita no frontend
    #e aqui no backend essa senha já encriptada recebe mais uma camada de encriptação
    def __encrypt_password(self,password):
        return sha256(str(password).encode()).hexdigest()