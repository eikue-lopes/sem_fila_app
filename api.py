from app_controller import AppController

from flask import Flask , redirect , render_template , request , url_for

app_ctrl = AppController()

app = Flask(__name__)

@app.route("/user/login",methods=["POST"])
def login():
    args = request.args
    email = str(args['email'])
    password = str(args['password'])
    token_id = app_ctrl.sign_in(email=email,password=password)
    if token_id != None:
        return {'request':'login','status':True,'token':token_id}
    else:
        return {'request':url_for('login'),'status':False,'token':token_id}
    

@app.route("/user/sign_up",methods=["POST"])
def sign_up():
    args  = request.args
    name = args['name']
    email = args['email']
    password = args['password']
    
    if 'is_stabilishment' in args.keys():
        is_stabilishment = args['is_stabilishment'] == 'on'
    else:
        is_stabilishment = False
    
    r = app_ctrl.sign_up(name=name,email=email,password=password,is_stabilishment=is_stabilishment)
    return {'request':url_for('sign_up'),'response':r}

@app.route("/user/sign_up_confirmation",methods=["POST"])
def sign_up_confirmation():
    args = request.args
    vc = args["verification_code"]
    r = app_ctrl.sign_up_confirmation(verification_code=vc)
    return {'request':url_for('sign_up_confirmation'),'response':r}

@app.route("/queues/entry",methods=["POST"])
def entry_on_queue():
    args = request.args
    token_client = args['token_client']
    token_stabilishment = args['token_stabilishment']
    r = app_ctrl.entry_on_queue(token_id=token_client,token_id_stabilishment_owner_queue=token_stabilishment)
    return {'request':url_for('entry_on_queue'),'response':r}

@app.route("/queues/exit",methods=["POST"])
def exit_from_queue():
    args = request.args
    token_client = args['token_client']
    token_stabilishment = args['token_stabilishment']
    r = app_ctrl.exit_from_queue(token_id=token_client,token_id_stabilishment_owner_queue=token_stabilishment)
    return {'request':url_for('exit_from_queue'),'response':r}



@app.route("/queues/to_next_client",methods=["POST"])
def jump_to_next_client():
    args = request.args
    token_id = args['token_id']
    r = app_ctrl.jump_to_next_client_in_queue(token_id=token_id)
    return {'request':url_for('jump_to_next_client'),'response':r}

@app.route("/queues/search",methods=["GET"])
def search_for_queue():
    args = request.args
    query_stabilishment_name = args['name_stabilishment']
    r = app_ctrl.search_for_queues(name_stabilishment_owner_queue=query_stabilishment_name)
    return {'request':url_for('search_for_queue'),'response':r}

@app.route("/queues/where_i_am/search",methods=["GET"])
def search_for_queues_where_i_am():
    args = request.args
    token_id = args['token_id']
    r = app_ctrl.search_for_queues_where_i_am(token_id=token_id)
    return {'request':url_for('search_for_queue_where_i_am'),'response':r}

@app.route("/user/update/name",methods=["POST"])
def update_name_user():
    args = request.args
    token_user = args['token_id']
    new_name = args['new_name']
    r = app_ctrl.update_profile_name(token_id=token_user,new_name=new_name)
    return {'request':url_for('update_name_user'),'response':r}


@app.route("/user/update/email",methods=["POST"])
def update_email_user():
    args = request.args
    token_user = args['token_id']
    new_email = args['new_email']
    r = app_ctrl.update_profile_email(token_id=token_user,new_email=new_email)
    return {'request':url_for('update_email_user'),'response':r}


@app.route("/user/update/password",methods=["POST"])
def update_password_user():
    args = request.args
    token_user = args['token_id']
    old_password = args['old_password']
    new_password = args['new_password']
    r = app_ctrl.update_profile_password(token_id=token_user,old_password=old_password,new_password=new_password)
    return {'request':url_for('update_password_user'),'response':r}


if __name__ == "__main__":
    app.run(debug=True)