from core.exceptions import CustomException

class ProviderNotFoundException(CustomException):
	code = 404
	error_code = "PROVIDER__NOT_FOUND_ERROR"
	message = "Provider not found"

class DraftPurchaseInvoiceNotFoundException(CustomException):
	code = 404
	error_code = "DRAFT_PURCHASE_INVOICE__NOT_FOUND_ERROR"
	message = "Draft purchase invoice not found"