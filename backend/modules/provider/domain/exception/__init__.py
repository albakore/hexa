from core.exceptions.base import CustomException


class PurchaseInvoiceServiceNotFoundException(CustomException):
	code = 404
	error_code = "INVOICE_SERVICE__NOT_FOUND_ERROR"
	message = "Invoice service not found"
