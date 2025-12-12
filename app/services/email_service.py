class EmailService:
    @staticmethod
    def send_email(to, subject, body):
        print("----------- EMAIL NOTIFICATION -----------")
        print(f"To: {to}")
        print(f"Subject: {subject}")
        print(f"Body: {body}")
        print("------------------------------------------")
