

class MyEmail:
    def __init__(self, email):
        self.email = email

    def send(self):
        print(f"Sending email to {self.email}")