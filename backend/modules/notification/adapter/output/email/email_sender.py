from core.config.settings import env
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from modules.notification.domain.repository.sender_provider import SenderProviderPort


class EmailSender(SenderProviderPort):

	def __init__(self,server,port,email_login,password_login, mail_sender):
		self.email_login = email_login
		self.password_login = password_login
		self.server_name = server
		self.port = port
		self.mail_sender = mail_sender
		# Start the SMTP session
		self.server = None

	async def send(self, notification: dict) -> None:
		# Create a MIMEText object to represent the email
		
		msg = MIMEMultipart()

		msg['From'] = self.mail_sender
		msg['To'] = ', '.join(notification['to'])
		msg['Subject'] = notification['subject']

		msg.attach(MIMEText(notification['body'], 'html'))

		# Send the email
		self.server = SMTP(self.server_name, self.port)
		self.server.connect(self.server_name,self.port)

		self.server.ehlo()
		self.server.starttls()
		self.server.ehlo()

		status, response = self.server.login(self.email_login, self.password_login)
		print(f"Connection Login: {status} - {response}")
		self.server.sendmail(env.EMAIL_SMTP_MAILSENDER, notification['to'], msg.as_string())
		self.server.quit()

	# async def send(self, from_: str | None, to: list[str], subject: str, body: str | dict) -> None:
	# 	# Create a MIMEText object to represent the email
	# 	msg = MIMEMultipart()

	# 	msg['From'] = self.mail_sender
	# 	msg['To'] = ', '.join(to)
	# 	msg['Subject'] = subject

	# 	if isinstance(body, dict):
	# 		body = str(body)

	# 	msg.attach(MIMEText(body, 'html'))

	# 	# Send the email
	# 	self.server = SMTP(self.server_name, self.port)
	# 	self.server.connect(self.server_name,self.port)

	# 	self.server.ehlo()
	# 	self.server.starttls()
	# 	self.server.ehlo()

	# 	status, response = self.server.login(self.email_login, self.password_login)
	# 	print(f"Connection Login: {status} - {response}")
	# 	self.server.sendmail(env.EMAIL_SMTP_MAILSENDER, to, msg.as_string())
	# 	self.server.quit()
