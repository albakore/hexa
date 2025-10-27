from core.exceptions import CustomException


class ProviderNotFoundException(CustomException):
	code = 404
	error_code = "PROVIDER__NOT_FOUND_ERROR"
	message = "Provider not found"


class DraftPurchaseInvoiceNotFoundException(CustomException):
	code = 404
	error_code = "DRAFT_PURCHASE_INVOICE__NOT_FOUND_ERROR"
	message = "Draft purchase invoice not found"


class DraftPurchaseInvoiceCurrencyNotFoundException(CustomException):
	code = 404
	error_code = "DRAFT_PURCHASE_INVOICE_CURRENCY__NOT_FOUND_ERROR"
	message = "Currency not found in draft purchase invoice"


class DraftPurchaseInvoiceServiceNotFoundException(CustomException):
	code = 404
	error_code = "DRAFT_PURCHASE_INVOICE_SERVICE__NOT_FOUND_ERROR"
	message = "Service not found in draft purchase invoice"


class DraftPurchaseInvoiceReceiptFileNotFoundException(CustomException):
	code = 400
	error_code = "DRAFT_PURCHASE_INVOICE_RECEIPT_FILE__NOT_FOUND_ERROR"
	message = "Receipt file is required to finalize the draft purchase invoice"


class DraftPurchaseInvoiceNumberNotFoundException(CustomException):
	code = 400
	error_code = "DRAFT_PURCHASE_INVOICE_NUMBER__NOT_FOUND_ERROR"
	message = "Invoice number is required to finalize the draft purchase invoice"


class DraftPurchaseInvoiceProviderNotFoundException(CustomException):
	code = 400
	error_code = "DRAFT_PURCHASE_INVOICE_PROVIDER__NOT_FOUND_ERROR"
	message = "Provider is required to finalize the draft purchase invoice"


class DraftPurchaseInvoiceIssueDateNotFoundException(CustomException):
	code = 400
	error_code = "DRAFT_PURCHASE_INVOICE_ISSUE_DATE__NOT_FOUND_ERROR"
	message = "Issue date is required to finalize the draft purchase invoice"


class DraftPurchaseInvoiceReceiptDateNotFoundException(CustomException):
	code = 400
	error_code = "DRAFT_PURCHASE_INVOICE_RECEIPT_DATE__NOT_FOUND_ERROR"
	message = "Receipt date is required to finalize the draft purchase invoice"


class DraftPurchaseInvoiceUnitPriceNotFoundException(CustomException):
	code = 400
	error_code = "DRAFT_PURCHASE_INVOICE_UNIT_PRICE__NOT_FOUND_ERROR"
	message = "Unit price is required to finalize the draft purchase invoice"


class DraftPurchaseInvoiceAwbRequiredException(CustomException):
	code = 400
	error_code = "DRAFT_PURCHASE_INVOICE_AWB__REQUIRED_ERROR"
	message = "AWB (Air Waybill) is required for this service type"


class DraftPurchaseInvoiceKgRequiredException(CustomException):
	code = 400
	error_code = "DRAFT_PURCHASE_INVOICE_KG__REQUIRED_ERROR"
	message = "Kilograms (Kg) is required for this service type"


class DraftPurchaseInvoiceItemsRequiredException(CustomException):
	code = 400
	error_code = "DRAFT_PURCHASE_INVOICE_ITEMS__REQUIRED_ERROR"
	message = "Items quantity is required for this service type"


class DraftPurchaseInvoiceDetailFileRequiredException(CustomException):
	code = 400
	error_code = "DRAFT_PURCHASE_INVOICE_DETAIL_FILE__REQUIRED_ERROR"
	message = "Detail file is required for this service type"


class DraftPurchaseInvoiceReceiptFileInvalidException(CustomException):
	code = 400
	error_code = "DRAFT_PURCHASE_INVOICE_RECEIPT_FILE__INVALID_ERROR"
	message = "Receipt file does not exist in storage"


class DraftPurchaseInvoiceDetailFileInvalidException(CustomException):
	code = 400
	error_code = "DRAFT_PURCHASE_INVOICE_DETAIL_FILE__INVALID_ERROR"
	message = "Detail file does not exist in storage"
