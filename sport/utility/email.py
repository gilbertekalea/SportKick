from dataclasses import dataclass
from flask_mail import Message
from jinja2 import Environment, select_autoescape, PackageLoader
from flask import flash, get_flashed_messages


@dataclass
class UserRelevantData:
    """
    Dataclass containing relevant data that facilitates sending of emails.
    """
    username: str
    email: str
    first_name: str

class ManageEmailTemplate(UserRelevantData):
    '''
    A class to manage html email templates
    
    param:
            name -> str: represents the name of the templates to be rendered. 
            meta_data -> dict: relevant information that can be passed to the object when user takes an action.
            >>> if a user registers for a team, we can pass team_name, player_sport, and skills. 
    '''
    # initializing parameters for looking up templates
    env = Environment(
        loader=PackageLoader("sport", "templates\emails_templates"),
        autoescape=select_autoescape(["html", "xml"]),
    )

    def __init__(self, name: str, meta_data: dict = None, *args, **kwargs):
        self.name = name
        self.meta_data = meta_data
        super().__init__(*args, **kwargs)
        
    def __str__(self):
        return self.name
    
    # class instance methods
    def get_account_creation_email_template(self):
        return self.env.get_template("account_creation.html")

    def get_sport_registration_email_template(self):
        return self.env.get_template("registration.html")

    def get_general_email_template(self):
        return self.env.get_template("general_email.html")
    
    # prepare, compose and render the correct html pages. 
        #! THIS METHOD CAN BE IMPROVED : FOR EXAMPLE  WRITING FUNCTIONS THAT HANDLES SPECIFIC EXECUTION 
            #* SUCH AS FOCUS ON REGISTRATIION, LOGIN, SIGNUP ETC.
    
    
    def email_channel_composer(self) -> Message:
        if self.name =='registration':
            msg = Message(
            subject="CONFIRMATION EMAIL: Registration Info",
            sender="gilbertekale@gmail.com",
            recipients=['gilbertekalea@gmail.com'],
            html=self.get_sport_registration_email_template().render(username=self.username, meta_data=self.meta_data),
            charset="utf-8"
            )
            return msg
    
        elif self.name == 'account-creation':
            msg = Message(
            subject="CORNFIRMATION EMAIL: Account Created Successfully",
            sender="gilbertekale@gmail.com",
            recipients=[self.email],
            html=self.get_account_creation_email_template().render(username=self.username, ),
            charset="utf-8"
            )
            return msg
        
        elif self.name == 'general':
            msg = Message(
            subject="ANNOUNCEMENT-GENERAL EMAIL!",
            sender="gilbertekale@gmail.com",
            recipients=['gilbertekalea@gmail.com'],
            html=self.get_general_email_template().render(username=self.username),
            charset="utf-8"
            )
            return msg
        else:
            flash('Unfortunately, we do not understand that command.', category='danger')
            

    
   
    