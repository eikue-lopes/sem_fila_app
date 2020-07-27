import shelve
from db2_models import UserLoginInfos


class DB2Controller:
    def __init__(self,address_db,create_schema):
        self.dir_db = address_db
        if create_schema == True:
            self.__create_schema()
        
    def __open_db(self):
        self.db = shelve.open(self.dir_db)
    
    def __create_schema(self):
        self.__open_db()
        self.db['users_login_infos'] = {}
        self.db['email_verification_data'] = {}
        self.db['mailing_list'] = []
        self.__close_db()
    
    def __close_db(self):
        self.db.close()
    
    #adiciona um par app_user,user_login_infos linkado a um dado código de verificação de email
    def add_infos_user_register(self,is_stabilishment,user_login_infos,email_verification_code,timestamp):
        email_verification_code = str(email_verification_code)
        
        #o código de verificação não pode existir previamente, o token_id não pode estar vinculado a nenhum cadastro e o email também não pode estar vinculado a nenhum cadastro
        if self.__email_verification_code_already_exists(email_verification_code=email_verification_code) == False and self.get_user_login_infos_by_linked_token_id(linked_token_id=user_login_infos.linked_token_id) == None and self.email_already_exists(email=user_login_infos.email) == False:
            self.__open_db()
            evd = self.db['email_verification_data']
            
            evd[email_verification_code] = {"is_stabilishment":is_stabilishment,"user_login_infos":user_login_infos,"timestamp":timestamp}
            
            self.db['email_verification_data'] = evd
            self.__close_db()
            return True
        else:
            return False
    
    #retorna um par app_user,user_login_infos dado um código de verificação de email linkado a esse par
    def get_infos_user_register_linked_by_email_verification_code(self,email_verification_code):
        email_verification_code = str(email_verification_code)
        
        if self.__email_verification_code_already_exists(email_verification_code=email_verification_code) == True:
            self.__open_db()
            evd = self.db['email_verification_data']
            self.__close_db()
            
            is_stabilishment = evd[str(email_verification_code)]['is_stabilishment'] 
            user_login_infos = evd[str(email_verification_code)]['user_login_infos']
            timestamp = evd[str(email_verification_code)]['timestamp']
            
            return is_stabilishment , user_login_infos , timestamp
        else:
            return None,None,None
    
    def delete_infos_user_register_linked_by_email_verification_code(self,email_verification_code):
        email_verification_code = str(email_verification_code)
        
        if self.__email_verification_code_already_exists(email_verification_code=email_verification_code) == True:
            self.__open_db()
            evd = self.db['email_verification_data']
            del(evd[email_verification_code])
            self.db['email_verification_data'] = evd
            self.__close_db()
            return True
        else:
            return False
    
    def __email_verification_code_already_exists(self,email_verification_code):
        email_verification_code = str(email_verification_code)
        
        self.__open_db()
        evd = self.db['email_verification_data']
        self.__close_db()
        
        return email_verification_code in evd.keys()
    
    def email_verification_code_is_valid(self,email_verification_code):
        email_verification_code = str(email_verification_code)
        return self.__email_verification_code_already_exists(email_verification_code=email_verification_code)
    
    def add_user_login_infos(self,user_login_infos,also_add_to_mailing_list):
        linked_token_id = str(user_login_infos.linked_token_id)
        
        #se ainda não existe na base de dados infos linkadas ao token_id do user passado
        #se ainda não existe uma conta com o email passado
        if self.get_user_login_infos_by_linked_token_id(linked_token_id=linked_token_id) == None and not self.email_already_exists(email=user_login_infos.email):
            self.__open_db()
            users_login_infos = self.db['users_login_infos']
            users_login_infos[linked_token_id] = user_login_infos
            self.db['users_login_infos'] = users_login_infos
            self.__close_db()
            
            #para fins comerciais...
            if also_add_to_mailing_list == True:
                self.__add_email_to_mailing_list(email=user_login_infos.email)
            
            return user_login_infos
        else:
            return None
    
    def remove_user_login_infos(self,linked_token_id):
        linked_token_id = str(linked_token_id)
        
        self.__open_db()
        users_login_infos = self.db['users_login_infos']
        
        if linked_token_id in users_login_infos.keys():
            del(users_login_infos[linked_token_id])
            self.db['users_login_infos'] = users_login_infos
            self.__close_db()
            return True
        else:
            self.__close_db()
            return False


    #não existe a possibilidade de atualizar o token_id associado a uma conta de usuário
    #só posso atualizar nome, email e/ou senha
    def update_user_login_infos_name(self,linked_token_id,new_name):
        linked_token_id = str(linked_token_id)
        
        self.__open_db()
        users_login_infos = self.db['users_login_infos']
        
        if linked_token_id in users_login_infos.keys():
            users_login_infos[linked_token_id].name = new_name
            self.db['users_login_infos'] = users_login_infos
            self.__close_db()
            return True
        else:
            self.__close_db()
            return False
    
    def update_user_login_infos_email(self,linked_token_id,new_email):
        linked_token_id = str(linked_token_id)
        
        self.__open_db()
        users_login_infos = self.db['users_login_infos']
        
        if linked_token_id in users_login_infos.keys():
            users_login_infos[linked_token_id].email = new_email
            self.db['users_login_infos'] = users_login_infos
            self.__close_db()
            self.__add_email_to_mailing_list(email=new_email)
            return True
        else:
            self.__close_db()
            return False
    
    def update_user_login_infos_password_encrypted(self,linked_token_id,new_password_encrypted):
        linked_token_id = str(linked_token_id)
        
        self.__open_db()
        users_login_infos = self.db['users_login_infos']
        
        if linked_token_id in users_login_infos.keys():
            users_login_infos[linked_token_id].password_encrypted = new_password_encrypted
            self.db['users_login_infos'] = users_login_infos
            self.__close_db()
            return True
        else:
            self.__close_db()
            return False
    
    def get_user_login_infos_by_linked_token_id(self,linked_token_id):
        linked_token_id = str(linked_token_id)
        
        self.__open_db()
        users_login_infos = self.db['users_login_infos']
        self.__close_db()
        if linked_token_id in users_login_infos.keys():
            return users_login_infos[linked_token_id]
        else:
            return None
    
    def get_user_login_infos_by_name(self,name):
        self.__open_db()
        users_login_infos = self.db['users_login_infos']
        self.__close_db()

        for uli in users_login_infos.values():
            if uli.name == name:
                return uli
        
        return None
        
    def get_linked_token_id(self,email,password_encrypted):
        self.__open_db()
        users_login_infos = self.db['users_login_infos']
        self.__close_db()
        
        
        for uli in users_login_infos.values():
            if uli.email == email and uli.password_encrypted == password_encrypted:
                return uli.linked_token_id
        
        return None

    def email_already_exists(self,email):
        self.__open_db()
        users_login_infos = self.db['users_login_infos']
        self.__close_db()
        
        for uli in users_login_infos.values():
            if uli.email == email:
                return True

        return False
    
    def get_num_users_login_infos(self):
        self.__open_db()
        users_login_infos = self.db['users_login_infos']
        self.__close_db()
    
        return len(users_login_infos)

    def __add_email_to_mailing_list(self,email):
        self.__open_db()
        mailing_list = self.db['mailing_list']
        mailing_list.append(email)
        self.db['mailing_list'] = mailing_list
        self.__close_db() 
    
    def get_mailing_list(self):
        self.__open_db()
        mailing_list = self.db['mailing_list']
        self.__close_db() 
        return mailing_list
    
    def get_all_users_login_infos(self):
        self.__open_db()
        users_login_infos = self.db['users_login_infos']
        self.__close_db() 
        return users_login_infos