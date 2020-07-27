import json

#a encriptação da senha deverá ser feita no app onde o usuário está acessando o meu
#backend de modo a evitar que ele a envie de forma insegura pela rede e depois pelo
#controlador de autenticações
#A encriptação pelo app pode seguir qualquer algoritmo de hash
#A encriptação no controlador de autenticações deve ser do tipo SHA256

class UserLoginInfos:
    def __init__(self,name,email,password_encrypted,linked_token_id):
        self.name = name
        self.email = email
        self.password_encrypted = password_encrypted
        self.linked_token_id = linked_token_id
    
    def jsonify(self):
        d = {}
        d['name'] = self.name
        d['email'] = self.email
        d['password_encrypted'] = self.password_encrypted
        d['linked_token_id'] = self.linked_token_id
        return json.dumps(d)