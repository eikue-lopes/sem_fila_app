import shelve
from db1_models import AppUser

class DB1Controller:
    def __init__(self,address_db,create_schema):
        self.dir_db = address_db
        if create_schema == True:
            self.__create_schema()
        
    def __open_db(self):
        self.db = shelve.open(self.dir_db)
    
    def __create_schema(self):
        self.__open_db()
        self.db['users'] = {}
        self.__close_db()
    
    def __close_db(self):
        self.db.close()
    
    def add_user(self,user):
        token_id = str(user.token_id)
        
        #se o user ainda não existe na base de dados
        if self.get_user(token_id=token_id) == None:
            self.__open_db()
            users = self.db['users']
            users[token_id] = user
            self.db['users'] = users
            self.__close_db()
            return user
        else:
            return None
    
    def remove_user(self,token_id):
        token_id = str(token_id)
        
        self.__open_db()
        users = self.db['users']
        
        if token_id in users.keys():
            del(users[token_id])
            self.db['users'] = users
            self.__close_db()
            return True
        else:
            self.__close_db()
            return False

    
    #não existe a possibilidade de atualizar nada em um cliente
    #não existe a possibilidade de atualizar o token_id seja de um cliente ou estabelecimento
    #logo, só atualizo a fila do estabelecimento
    def update_queue_stabilishment(self,token_id,new_queue_stabilishment):
        token_id = str(token_id)
        
        self.__open_db()
        users = self.db['users']
        
        if token_id in users.keys():
            if users[token_id].is_stabilishment == True:
                users[token_id].queue = new_queue_stabilishment
                self.db['users'] = users
                self.__close_db()
                return True
                
        self.__close_db()
        return False
 
    def get_user(self,token_id):
        token_id = str(token_id)
        
        self.__open_db()
        users = self.db['users']
        self.__close_db()
        
        if token_id in users:
            return users[token_id]
 
        return None
    
    def get_num_users(self):
        self.__open_db()
        users = self.db['users']
        self.__close_db()
        return len(users)
    
    def get_only_clients(self):
        self.__open_db()
        users = self.db['users']
        self.__close_db()
        
        clients = []
        
        for user in users.values():
            #se for um cliente
            if user.is_stabilishment == False:
                clients.append(user)
        
        return clients

    def get_only_stabilishments(self):
        self.__open_db()
        users = self.db['users']
        self.__close_db()
        
        stabilishments = []
        
        for user in users.values():
            #se for um estabelecimento
            if user.is_stabilishment == True:
                stabilishments.append(user)
        
        return stabilishments
    
    def is_client(self,token_id):
        token_id = str(token_id)
        user = self.get_user(token_id=token_id)
        if user != None:
            return user.is_stabilishment == False
        else:
            raise Exception("[Erro] Usuário não existe, portanto não dá pra saber se é um cliente ou estabelecimento.")
    
    def is_stabilishment(self,token_id):
        token_id = str(token_id)
        
        user = self.get_user(token_id=token_id)
        if user != None:
            return user.is_stabilishment == True
        else:
            raise Exception("[Erro] Usuário não existe, portanto não dá pra saber se é um cliente ou estabelecimento.")
    
    def get_num_clients(self):
        return len(self.get_only_clients())
    
    def get_num_stabilishments(self):
        return len(self.get_only_stabilishments())
    
    
    
    
    