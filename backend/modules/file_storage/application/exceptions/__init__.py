from core.exceptions import CustomException

class FileStorageUploadException(CustomException):
	code = 400
	error_code = "FILE_STORAGE__UPLOAD_ERROR"
	message = "Hubo un error al subir el archivo"

class FileStorageDownloadException(CustomException):
	code = 400
	error_code = "FILE_STORAGE__DOWNLOAD_ERROR"
	message = "Hubo un error al descargar el archivo"