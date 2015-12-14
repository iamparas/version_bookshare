import webapp2
import jinja2
import re
import json
import urllib2
import random
from string import letters
import base
import db
import bookhandler

class MainHandler(base.Handler):
    '''Handles Signup and Signin Request'''

    def get(self):
        user=""
        if self.user:
           user=self.user.username
        self.render("index.html", userperson=user)

    def post(self):
        error="The Username you provided already exist"
        chk=self.request.get('process')
        #Request from same page to check signup/ sign in request
        if chk == "signup":
            username=self.request.get("username")
            password=self.request.get("password")
            repass=self.request.get('repassword')
            email=self.request.get("email")
            if password !=repass:
                self.render('index.html', pass_message="Password do not match")
            else:
                p=db.user_acc.by_name(username)
                if p:
                    self.render("index.html",message=error)
                else: #
                    p=db.user_acc.register(username=username,password=password,email=email)
                    p.put()
                    self.set_secure_cookie('user_id',str(p.key().id()))
                    self.redirect('/start')
        elif chk =='signin':
            username=self.request.get("uname")
            password=self.request.get("pass")
            u = db.user_acc.login(username,password)
            if u:
                self.login(u)
                self.redirect('/start')
            else:
                msg="Invalid Login Info"
                self.redirect('/')

class Logout(base.Handler):
    '''Handles user logout request'''

    def get(self):
        self.logout()
        self.redirect('/')

class MyBooks(base.Handler):
    '''Handles user request for list of books in their have list and wish list'''

    def get(self):
        if self.user:
            cursor = db.user_book.get_all(self.user.username)
            book_list = list(cursor)
            self.render("mybs.html", book_list=book_list, username=self.user.username)
        else:
            self.redirect('/')

class Repository(base.Handler):
    '''Handles books repository database result'''

    def get(self):
        search_query=self.request.get('query')
        if search_query:
                result = db.user_book.get_by_query(search_query)
                book_list = list(result)
        self.render("repo.html")
         
class Match(base.Handler):
    '''Handles user's book match page'''

    def get(self):
        if self.user:
            match=db.user_match.get_all(self.user.username)
            self.render("match.html", match=match)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/start',bookhandler.BookHandler),
    ('/repository',Repository),
    ('/logout',Logout),
	('/mbs',MyBooks),
    ('/match',Match),
], debug=True)
