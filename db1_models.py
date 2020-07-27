from hashlib import sha256
from time import time
from random import randrange
import json

class Queue:
    def __init__(self):
        #será um dicionário de dicionários: {'token-id':{'timestamp_insertion':exemplo_timestamp,'position':exemplo_position},...}   
        self.clients_tokens = {}
    
    #estou deixando aberta a possibilidade de estabelecimentos entrarem na fila de outros
    #estabelecimentos
    #caso seja um comportamento indesejado mais a frente 
    #buscar maneiras de evitar isso
    def add(self,token_id):
        try:
            self.clients_tokens[token_id] = {'timestamp_insertion':time(),'position':len(self.clients_tokens)+1}
            return True
        except:
            return False
    def remove(self):
        try:
            token_first , _ = self.get_first()
            del(self.clients_tokens[token_first])
        
            #subtraio 1 em cada posição...
            for key in self.clients_tokens.keys():
                self.clients_tokens[key]['position'] -= 1
            
            return True
        except:
            return False
        
    def get_first(self):
        
        for key in self.clients_tokens.keys():
            if self.clients_tokens[key]['position'] == 1:
                return key , self.clients_tokens[key]
        
        return None,None
    
    def get_last(self):
        for key in self.clients_tokens.keys():
            if self.clients_tokens[key]['position'] == len(self.clients_tokens):
                return key , self.clients_tokens[key]
        
        return None,None

    def get_by_token_id(self,token_id):
        for key in self.clients_tokens.keys():
            if key == token_id:
                return key , self.clients_tokens[key]
        
        return None,None
    
    def get_by_position(self,position):
        for key in self.clients_tokens.keys():
            if self.clients_tokens[key]['position'] == position:
                return key , self.clients_tokens[key]
        
        return None,None
    
    def get_position(self,token_id):
        _ , client = self.get_by_token_id(token_id=token_id)
        if client != None:
            return client['position']
        else:
            return None
    
    def get_token_id(self,position):
        token_id , _ = self.get_by_position(position=position)
        if token_id != None:
            return token_id
        else:
            return None
        
    def get_size(self):
        return len(self.clients_tokens)
    
    def is_empty(self):
        return len(self.clients_tokens) == 0
        

class AppUser:
    def __init__(self,is_stabilishment,generate_token_id):
        if generate_token_id == True:
            self.token_id = self.__generate_user_token_id()
        else:
            self.token_id = None
            
        self.is_stabilishment = is_stabilishment
        
        #se o usuário for um estabelecimento, então ele possui uma fila...
        if is_stabilishment == True:
            self.queue = Queue()
    
    #o usuário será conhecido e se comunicará com a api através do seu token_id que será armazenado em um cookie por exemplo...
    #esse token_id é permantemente armazenado...
    def __generate_user_token_id(self):
        string = str(id(self)) + str(time()) + str(randrange(1000000000))
        return sha256(string.encode()).hexdigest()
    
    def jsonify(self):
        d = {}
        d['token_id'] = self.token_id
        d['is_stabilishment'] = self.is_stabilishment
        
        if self.is_stabilishment == True:
            #não uso o método jsonify da queue aqui porque não quero converte-la em json duas vezes
            d['queue'] = self.queue.clients_tokens
            
        return json.dumps(d)
        
        
        