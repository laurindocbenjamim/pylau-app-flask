
from datetime import datetime
from flask import request, Request
from .help_message import HelpMessage


class HelpMessageController():


    # Validate the form
    def validate(self,form = Request.form):
        """
        Validate the form
        """
        if form.get('email') and isinstance(form.get('email'), str):
            return True
        return False
    # Save the users help message
    def save(self,form = Request.form):
        """
        
        """

        obj = HelpMessage(
            name = form.get('name'),
            email = form.get('email'),
            subject = form.get('subject'),
            message = form.get('message'),
            date_added = datetime.now().strftime("%Y-%m-%d"),
            datetime_added = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )

        status,h_message_id = obj.create(obj)
        
        if status:
            return status, {"object": obj.serialize()}
        return status, None


    # Delete the  users help message
    def delete(self,email):
        return False