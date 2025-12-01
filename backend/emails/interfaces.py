class EmailServiceInterface:
    def send_email(self, to, subject, body):
        raise NotImplementedError
    
    def scan_email(self, content):
        raise NotImplementedError
