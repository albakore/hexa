from smtplib import SMTP, SMTPException
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
from typing import Optional

from modules.notification.domain.repository.sender_provider import SenderProviderPort

logger = logging.getLogger(__name__)


class EmailSender(SenderProviderPort):
	"""
	Email sender with persistent SMTP connection.
	Maintains a single connection that is reused across multiple sends.
	"""

	def __init__(self, server: str, port: int, email_login: str, password_login: str, mail_sender: str):
		self.email_login = email_login
		self.password_login = password_login
		self.server_name = server
		self.port = port
		self.mail_sender = mail_sender
		self._server: Optional[SMTP] = None
		self._is_connected = False

	def _connect(self) -> None:
		"""Establishes SMTP connection and authenticates."""
		try:
			logger.info(f"Connecting to SMTP server {self.server_name}:{self.port}")
			self._server = SMTP(self.server_name, self.port)
			self._server.ehlo()
			self._server.starttls()
			self._server.ehlo()

			status, response = self._server.login(self.email_login, self.password_login)
			logger.info(f"SMTP Login successful: {status} - {response.decode() if isinstance(response, bytes) else response}")
			self._is_connected = True
		except SMTPException as e:
			logger.error(f"Failed to connect to SMTP server: {e}")
			self._is_connected = False
			raise

	def _disconnect(self) -> None:
		"""Closes SMTP connection."""
		if self._server:
			try:
				self._server.quit()
				logger.info("SMTP connection closed")
			except SMTPException as e:
				logger.warning(f"Error closing SMTP connection: {e}")
			finally:
				self._server = None
				self._is_connected = False

	def _is_alive(self) -> bool:
		"""Checks if the SMTP connection is still alive."""
		if not self._server or not self._is_connected:
			return False

		try:
			# Send NOOP command to check if connection is alive
			status = self._server.noop()[0]
			return status == 250
		except (SMTPException, OSError, ConnectionError, AttributeError):
			# Connection is dead or broken
			self._is_connected = False
			return False

	def _ensure_connection(self) -> None:
		"""Ensures SMTP connection is established and alive."""
		if not self._is_alive():
			if self._server:
				self._disconnect()
			self._connect()

	async def send(self, notification: dict) -> None:
		"""
		Sends an email notification using persistent SMTP connection.
		Automatically reconnects if connection is lost.
		"""
		# Create email message
		msg = MIMEMultipart()
		msg['From'] = self.mail_sender
		msg['To'] = ', '.join(notification['to'])
		msg['Subject'] = notification['subject']
		msg.attach(MIMEText(notification['body'], 'html'))

		# Send the email with retry logic
		max_retries = 2
		for attempt in range(max_retries):
			try:
				# Ensure connection is alive before sending
				self._ensure_connection()

				# Validate that server connection exists
				if not self._server:
					raise SMTPException("SMTP server connection not established")

				self._server.sendmail(self.mail_sender, notification['to'], msg.as_string())
				logger.info(f"Email sent successfully to {notification['to']}")
				break
			except (SMTPException, OSError, ConnectionError) as e:
				# OSError and ConnectionError catch network-level issues
				logger.warning(f"Failed to send email (attempt {attempt + 1}/{max_retries}): {e}")
				# Mark connection as dead
				self._is_connected = False

				if attempt < max_retries - 1:
					# Reconnect and retry
					self._disconnect()
					logger.info("Attempting to reconnect...")
				else:
					logger.error(f"Failed to send email after {max_retries} attempts")
					# Clean up before raising
					self._disconnect()
					raise

	def __del__(self):
		"""Cleanup SMTP connection on object destruction."""
		self._disconnect()
