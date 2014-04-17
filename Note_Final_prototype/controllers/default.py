# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################


def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Welcome to Sky-Note!")
    return dict(message=T('Hello World'))


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

def contact_us():
    return dict()
def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())


from gluon.tools import Mail
mail = Mail()
mail.settings.server = 'smtp.gmail.com:587'
mail.settings.sender = 'sky_notes'
mail.settings.login = 'skynote009@gmail.com:skynote15'
@auth.requires_login()
def create():
    return dict()


@auth.requires_login()
def table_update():
    title = request.get_vars['Title'];
    info =request.get_vars['Info'];
    modified =request.get_vars['Modified'];
    creator=auth.user.id

    db.Notes.insert(Creator=creator,Title=title,Info=info,Modified=modified,Tags=None)
    return dict(j="True")

@auth.requires_login()
def auto_suggestion():
    suggestion=request.get_vars['sug']
    if suggestion is not ' ':
        rows=db(db.Notes.Info.contains(suggestion)).select()
        ans='{"names":['
        count=0
        for i in rows:
            if(int(i.Creator) == auth.user.id):
                if(count!=0):
                    ans+= ","
                ans+= '"'+ i["Title"] +'"'
                count+=1
        ans+= "]}"
          
    return dict(ans=ans)

@auth.requires_login()
def auto_suggestion_by_title():
    suggestion=request.get_vars['sug']
    rows=db(db.Notes.Title.contains(suggestion)).select()
    ans='{"names":['
    count=0
    for i in rows:
            if(int(i.Creator) == auth.user.id):
                if(count!=0):
                    ans+= ","
                ans+= '"'+ i["Title"] +'"'
                count+=1
    ans+= "]}"  
    return dict(ans=ans)


@auth.requires_login()
def auto_suggestion_by_tags():
    suggestion=request.get_vars['sug']
    if suggestion is not ' ':
        rows=db(db.Notes.Tags.contains(suggestion)).select()
        ans='{"names":['
        count=0
        for i in rows:
            if(int(i.Creator) == auth.user.id):
                if(count!=0):
                    ans+= ","
                ans+= '"'+ i["Title"] +'"'
                count+=1
        ans+= "]}"
          
    return dict(ans=ans)

@auth.requires_login()
def auto_suggestion_by_title():
    suggestion=request.get_vars['sug']
    rows=db(db.Notes.Title.contains(suggestion)).select()
    ans='{"names":['
    count=0
    for i in rows:
            if(int(i.Creator) == auth.user.id):
                if(count!=0):
                    ans+= ","
                ans+= '"'+ i["Title"] +'"'
                count+=1
    ans+= "]}"
          
    return dict(ans=ans)


@auth.requires_login()
def secret_content():
    ans=request.get_vars["head"]
    db.Request_arg.truncate('RESTART IDENTITY CASCADE')
    db.Request_arg.insert(Arg1=ans)
    return dict(ans=ans)

@auth.requires_login()
def secret_title():
    ans=request.get_vars["head"]
    rows=db(db.Notes.Tags.contains(ans)).select()
    for i in rows:
        if(int(i.Creator) == auth.user.id):
                ans=i["Title"]
    db.Request_arg.truncate('RESTART IDENTITY CASCADE')
    db.Request_arg.insert(Arg1=ans)
    return dict(ans=ans)

@auth.requires_login()
def secret_tag():
    ans=request.get_vars["head"]
    rows=db(db.Notes.Tags.contains(ans)).select()
    for i in rows:
        if(int(i.Creator) == auth.user.id):
                ans=i["Title"]
    db.Request_arg.truncate('RESTART IDENTITY CASCADE')
    db.Request_arg.insert(Arg1=ans)
    return dict(ans=ans)

@auth.requires_login() 
def manage(): 
    rows=db(db.Request_arg.id>0).select()
    for i in rows:
        title=i["Arg1"]
    redirect(URL("open",args=title))
    return dict()



@auth.requires_login()
def check_title():
    title = request.get_vars["Title"]
    var = db(db.Notes.Creator == auth.user.id).select()
    temp="True"
    for i in var:
        if(i.Title==title):
           temp = "False"
    return dict(j=temp)

@auth.requires_login()       
def open():
    temp = request.args(0);
    var=db(db.Notes.Creator == auth.user.id).select()
    title = ""
    ans = temp.strip()
    for i in ans:
        if i is '_':
            title+=' '
        else:
            title+=i
    

    for j in var:
        if j.Title == title:
            content = j.Info
            modified = j.Modified

    return dict(ans=title, ans2=content, modified = modified)

@auth.requires_login()
def view_all():
    var = db(db.Notes.Creator == auth.user.id).select(orderby='<random>')
    return dict(notes=var)

@auth.requires_login()
def delete_note():
    temp = request.args(0)
    title = ""
    ans = temp.strip()
    for i in ans:
        if i is '_':
            title+=' '
        else:
            title+=i
    
    temp_note = db(db.Notes.Creator==auth.user.id).select()
    for i in temp_note:
        if(i.Title == title):
            i.delete_record()
    redirect(URL('view_all'))

@auth.requires_login()
def edit_note():
    temp = request.args(0)
    title = ""
    ans = temp.strip()
    for i in ans:
        if i is '_':
            title+=' '
        else:
            title+=i
    ans=[]
    temp_note = db(db.Notes.Creator == auth.user.id).select()
    for i in temp_note:
        if(i.Title==title):
         ans.append(i)
    return dict(var=ans)

@auth.requires_login()
def update_note():
    title = request.get_vars['Title']
    info =request.get_vars['Info']
    modified=request.get_vars['Modified']
    temp_note = db(db.Notes.Creator==auth.user.id).select()
    for i in temp_note:
        if(i.Title ==title):
            i.update_record(Info =info, Modified=modified)
    return dict(j="True")


#db(db.mytable.myfield.contains('text')).select() 
# relational database 
#db(db.mytable.myfield.contains('text')).select() 

#Home page for each user where he decides what to do ..... then goes to main page cooresponding to that.
#index is promotional page
#add requires login later on.
@auth.requires_login()    
def main():
  return dict()

@auth.requires_login() 
def calendar():
    return dict()

@auth.requires_login() 
def trail():
    return dict()

#temporarily redirected to home
def index():
    if(auth.user):
       redirect(URL('view_all'))
    return dict()

@auth.requires_login() 
def try_now():
    return dict()

@auth.requires_login()    
def save_tags():
    title = request.get_vars['Title'];
    tag=request.get_vars['Tags'];
    
    var=db().select(db.Notes.ALL)

    temp_note = db(db.Notes.Creator==auth.user.id).select()
    for i in temp_note:
        if(i.Title == title):
            i.update_record(Tags = tag)
    return dict(j="Tag inserted")

@auth.requires_login()   
def sendmail():
    title= request.get_vars['Title'];
    reciever= request.get_vars['Reciever'];
    var = db(db.Notes.Creator == auth.user.id).select()
    for i in var:
        if i.Title==title:
            content=i.Info

    temp='skynote:'+title
    mail.send(to=[reciever],
          subject=temp,
          # If reply_to is omitted, then mail.settings.sender is used
          reply_to='skynote009@gmail.com',
          message=content)
    return dict(j="Mail Sent")
 
@auth.requires_login()  
def go():
    return dict()