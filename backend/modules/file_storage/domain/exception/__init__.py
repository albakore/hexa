from core.exceptions import CustomException


class FileMetadataNotFoundException(CustomException):
	code = 404
	error_code = "FILE_METADATA__NOT_FOUND_ERROR"
	message = "File metadata not found"