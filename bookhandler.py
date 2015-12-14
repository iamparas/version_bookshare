import webapp2
import urllib2
import base
import os
import json
import db
class BookHandler(base.Handler):
    '''Handles all the request involving generating books from Google Book Database and adding to user list'''

    def get(self):
        if self.user:
        	self.render("start.html", userperson = self.user.username)

    def post(self):
        if(self.request.get("book")):
            base_url="https://www.googleapis.com/books/v1/volumes?q="
            query=self.request.get("field-keywords")
            #sends request to Google Book API to get books from user requested title
            try:
                content = urllib2.urlopen(base_url+query).read()
            except:
                return
            if content:
                js = json.loads(content)
                items = self.retrieve_summary(js)
                self.render("start.html", userperson=self.user.username, items=items)
        else:
            bookInfo = self.request.get('postvar')
            books = json.load(bookInfo)
            for book in books:
                booktitle = book
                author = books[book][0]
                imageurl = books[book][1]
                iswish = books[book][2]
                self._update_match(booktitle, iswish)
                bookdb = db.user_book(booktitle=booktitle, author=author,username=self.user.username,iswish=iswish)
                bookdb.put()

    def _update_match(self, booktitle, iswish):
        matches = self.check_match(booktitle, iswish)
        for e in matches[1]:
            if ret[0]:
                match = db.user_match(user_wish=self.user.username, user_have= e.username, booktitle=e.booktitle)
                match.put()
            else: #if it is for user wishlist
                match = db.user_match(user_have=self.user.username, user_wish= e.username, booktitle=e.booktitle)
                match.put() 

    def retrieve_summary(self, json_data):
        items = []
        for item in json_data['items']:
            title = item['volumeInfo']['title']
            img_url = item['volumeInfo']['imageLinks']['thumbnail']
            authors = item['volumeInfo']['authors'] if 'authors' in item['volumeInfo'] else ""
            authors = ', '.join(authors)
            description = item['volumeInfo']['description'][:300] if 'description' in item['volumeInfo']  else ""

            items.append([title,authors, img_url, description])
        return items
