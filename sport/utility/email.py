from dataclasses import dataclass
from flask_mail import Message
from jinja2 import Environment, FileSystemLoader,select_autoescape, PackageLoader

# write a program to send customized email when user creates account; registers for sports or general marketing emails.
@dataclass
class GetUserToSendEmailsTo:
    """
    Class to collect relevant user information to for successfull execution of emails.
    """
    username: str
    email: str
    first_name: str

class ManageEmailTemplate:
    env = Environment(
        loader=PackageLoader('sport', 'templates\emails'),
        autoescape= select_autoescape(['html', 'xml'])
    )
    
    @staticmethod
    def account_creation_email():
        return ManageEmailTemplate.env.get_template('account_creation.html')
    
    @staticmethod
    def sport_registration_email():
        return ManageEmailTemplate.env.get_template('sport_registration.html')
    
    @staticmethod
    def general_email():
        return ManageEmailTemplate.env.get_template('general_email.html')
    
class ManageEmailContext(GetUserToSendEmailsTo):
    
    def compose_email_content(self) -> Message:
        msg = Message(
            subject="[UPDATE: [Account Creation: CORNFIRMATION EMAIL]",
            sender="gilbertekale@gmail.com",
            recipients=['gilbertekalea@gmail.com'],
            html= ManageEmailTemplate.account_creation_email().render(username=self.username),
            charset='utf-8'
            )
        return msg