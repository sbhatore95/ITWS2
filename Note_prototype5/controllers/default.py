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
    response.flash = T("Welcome to web2py!sdfsd")
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

def table_update():
    title = request.get_vars['Title'];
    info =request.get_vars['Info'];
    modified =request.get_vars['Modified'];
    tag=request.get_vars['Tags'];
    db.Notes.insert(Title=title,Info=info,Modified=modified,Tags=tag)
    return dict(j="True")


def auto_suggestion():
    suggestion=request.get_vars['sug']
    if suggestion is not ' ':
        rows=db(db.Notes.Info.contains(suggestion)).select()
        ans='{"names":['
        count=0
        for i in rows:
            if(count!=0):
              ans+= ","
            ans+= '"'+ i["Title"] +'"'
            count+=1
        ans+= "]}"

          
    return dict(ans=ans)



def auto_suggestion_by_tags():
    suggestion=request.get_vars['sug']
    rows=db(db.Notes.Tags.contains(suggestion)).select()
    ans='{"names":['
    count=0
    for i in rows:
        if(count!=0):
          ans+= ","
        ans+= '"'+ i["Title"] +'"'
        count+=1
    ans+= "]}"

      
    return dict(ans=ans)


def manage():  
    rows=db(db.Request_arg.id>0).select()
    for i in rows:
        title=i["Arg1"]
        j=title

    title=db(db.Notes.Title.contains(title)).select()
    content=title
    for i in title:
      content=title[0]["Info"]
      modified=title[0]["Modified"]

    return dict(heading=j,content=content,modified=modified)


def secret():
    ans=request.get_vars["head"]
    db.Request_arg.truncate('RESTART IDENTITY CASCADE')
    db.Request_arg.insert(Arg1=ans)
    return dict(ans=ans)


def open():
    temp = request.args(0);
    var=db().select(db.Notes.ALL)
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

    return dict(ans=title, ans2=content)

def view_all():
    var = db().select(db.Notes.ALL)
    return dict(notes=var)

def delete_note():
    temp = request.args(0)
    title = ""
    ans = temp.strip()
    for i in ans:
        if i is '_':
            title+=' '
        else:
            title+=i
    db(db.Notes.Title==title).delete()
    redirect(URL('view_all'))


def edit_note():
    temp = request.args(0)
    title = ""
    ans = temp.strip()
    for i in ans:
        if i is '_':
            title+=' '
        else:
            title+=i
    var = db(db.Notes.Title==title).select()
    return dict(var=var)

def update_note():
    title = request.get_vars['Title']
    info =request.get_vars['Info']
    db(db.Notes.Title==title).update(Info=info)
    return dict(j="True")

#db(db.mytable.myfield.contains('text')).select() 
# relational database 
#db(db.mytable.myfield.contains('text')).select() 

@auth.requires_login()    
def main():
    response.flash = T("Welcome to SKYNOTE")
    return dict()

def index():
    return dict()


def save_tags():
    title = request.get_vars['Title'];
    tag=request.get_vars['Tags'];
    
    var=db().select(db.Notes.ALL)

    db(db.Notes.Title == title).update(Tags=tag)
    return dict(j="Tag inserted")


def sendmail():
    title= request.get_vars['Title'];
    reciever= request.get_vars['Reciever'];
    var = db().select(db.Notes.ALL)
    for i in var:
        if i.Title==title:
            content=i.Info

    temp='skynote:'+title
    mail.send(to=[reciever],
          subject=temp,
          # If reply_to is omitted, then mail.settings.sender is used
          reply_to='skynote009@gmail.com',
          message=content)
    return dict(j="mail sent")
    