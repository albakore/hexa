from passlib.context import CryptContext
from faker import Faker

faker = Faker()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PasswordHelper:
	@staticmethod
	def verify_password(plain_password: str, hashed_password: str):
		return pwd_context.verify(plain_password, hashed_password)

	@staticmethod
	def get_password_hash(password: str):
		return pwd_context.hash(password)

	@staticmethod
	def generate_password():
		password = faker.password(
			length=4,
			special_chars=False,
			digits=True,
			upper_case=False,
			lower_case=False,
		)
		return password
