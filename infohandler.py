import webapp2, jinja2, os, logging, time, datetime
from google.appengine.api import users
from google.appengine.ext import ndb

import classes

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
#tells which directory file is in
jinja_environment = jinja2.Environment(
  loader=jinja2.FileSystemLoader(template_dir))

class InfoHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template("welcome.html")
        html = template.render({})
        self.response.write(html)

        logging.info("info get")

        #getting current user key
        user = users.get_current_user().user_id()

        contact_query = classes.Contact.query(classes.Contact.userID == user)
        contacts = contact_query.fetch() #.filter(contact_query.userid == user) #.fetch()

        for contact in contacts:

            #if today's date is the same as the date of the reminder
            if datetime.datetime.today().date() == datetime.datetime.combine(contact.dateOfReminder, datetime.time.min).date():
                self.response.write("<script> alert('CALL " + contact.contactName.upper() + "'); </script>")

            template = jinja_environment.get_template("info.html")
            html = template.render({"contactName": contact.contactName,
                                    "phoneNumber": contact.phoneNumber,
                                    "numberOfCalls": contact.numberOfCalls,
                                    "dateOfLastCall": contact.dateOfLastCall})
            self.response.write(html)
