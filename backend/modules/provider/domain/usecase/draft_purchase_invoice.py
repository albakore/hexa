from dataclasses import dataclass
from typing import Sequence

from core.db import Transactional
from modules.provider.domain.command import CreateDraftPurchaseInvoiceCommand
from modules.provider.domain.entity import PurchaseInvoiceService
from modules.provider.domain.entity.draft_purchase_invoice import DraftPurchaseInvoice
from modules.provider.domain.exception import (
	DraftPurchaseInvoiceAwbRequiredException,
	DraftPurchaseInvoiceConceptTooShortException,
	DraftPurchaseInvoiceCurrencyNotFoundException,
	DraftPurchaseInvoiceDetailFileRequiredException,
	DraftPurchaseInvoiceIssueDateNotFoundException,
	DraftPurchaseInvoiceItemsRequiredException,
	DraftPurchaseInvoiceKgRequiredException,
	DraftPurchaseInvoiceNumberNotFoundException,
	DraftPurchaseInvoiceProviderNotFoundException,
	DraftPurchaseInvoiceReceiptDateNotFoundException,
	DraftPurchaseInvoiceReceiptFileNotFoundException,
	DraftPurchaseInvoiceServiceNotFoundException,
	DraftPurchaseInvoiceUnitPriceNotFoundException,
)
from modules.provider.domain.repository.draft_purchase_invoice import (
	DraftPurchaseInvoiceRepository,
)


@dataclass
class GetProviderDraftInvoicesListUseCase:
	draft_purchase_invoice_repository: DraftPurchaseInvoiceRepository

	async def __call__(
		self, id_provider: int, limit: int = 50, page: int = 0
	) -> list[DraftPurchaseInvoice] | Sequence[DraftPurchaseInvoice]:
		return await self.draft_purchase_invoice_repository.get_provider_draft_invoices_list(
			id_provider, limit, page
		)


@dataclass
class GetDraftPurchaseInvoicesByIdUseCase:
	draft_purchase_invoice_repository: DraftPurchaseInvoiceRepository

	async def __call__(
		self, id_draft_purchase_invoice: int
	) -> DraftPurchaseInvoice | None:
		return await self.draft_purchase_invoice_repository.get_provider_draft_invoices_by_id(
			id_draft_purchase_invoice
		)


@dataclass
class CreateDraftPurchaseInvoiceUseCase:
	def __call__(
		self, command: CreateDraftPurchaseInvoiceCommand
	) -> DraftPurchaseInvoice:
		return DraftPurchaseInvoice.model_validate(command)


@dataclass
class SaveDraftPurchaseInvoicesUseCase:
	draft_purchase_invoice_repository: DraftPurchaseInvoiceRepository

	@Transactional()
	async def __call__(
		self, draft_purchase_invoice: DraftPurchaseInvoice
	) -> DraftPurchaseInvoice:
		return await self.draft_purchase_invoice_repository.save_draft_invoice(
			draft_purchase_invoice
		)


@dataclass
class DeleteDraftPurchaseInvoicesUseCase:
	draft_purchase_invoice_repository: DraftPurchaseInvoiceRepository

	@Transactional()
	async def __call__(self, draft_purchase_invoice: DraftPurchaseInvoice) -> None:
		return await self.draft_purchase_invoice_repository.delete_draft_invoice(
			draft_purchase_invoice
		)


@dataclass
class ValidateDraftPurchaseInvoiceUseCase:
	"""
	Use case to finalize a draft purchase invoice.

	Validates all required fields according to business rules before marking
	the draft as finalized and ready for processing by external consumers.

	This use case enforces domain invariants ensuring that a finalized draft
	contains all necessary information for downstream invoice processing.
	"""

	async def __call__(
		self,
		draft_purchase_invoice: DraftPurchaseInvoice,
		service: PurchaseInvoiceService,
	):
		"""
		Validates a draft purchase invoice.

		Business rules for a finalized draft (always required):
		- Must have invoice number (number)
		- Must be associated with a provider (fk_provider)
		- Must have a service type (fk_invoice_service)
		- Must have a receipt file attached (id_receipt_file)
		- Must specify currency (currency)
		- Must have issue date (issue_date)
		- Must have receipt date (receipt_date)
		- Must have unit price (unit_price)

		Dynamic validations based on service configuration:
		- AWB (if service.require_awb is True)
		- Kilograms (if service.require_kg is True)
		- Items (if service.require_items is True)
		- Detail file (if service.require_detail_file is True)

		Args:
			draft_purchase_invoice: The draft to validate and finalize
			service: The service type with dynamic requirements configuration

		Raises:
			DraftPurchaseInvoiceNumberNotFoundException: If invoice number is missing
			DraftPurchaseInvoiceProviderNotFoundException: If provider is missing
			DraftPurchaseInvoiceServiceNotFoundException: If service is missing
			DraftPurchaseInvoiceReceiptFileNotFoundException: If receipt file is missing
			DraftPurchaseInvoiceCurrencyNotFoundException: If currency is missing
			DraftPurchaseInvoiceIssueDateNotFoundException: If issue date is missing
			DraftPurchaseInvoiceReceiptDateNotFoundException: If receipt date is missing
			DraftPurchaseInvoiceUnitPriceNotFoundException: If unit price is missing
			DraftPurchaseInvoiceAwbRequiredException: If AWB required by service but missing
			DraftPurchaseInvoiceKgRequiredException: If Kg required by service but missing
			DraftPurchaseInvoiceItemsRequiredException: If Items required by service but missing
			DraftPurchaseInvoiceDetailFileRequiredException: If detail file required by service but missing
		"""
		# Validate required fields according to domain business rules
		if not draft_purchase_invoice.number:
			raise DraftPurchaseInvoiceNumberNotFoundException

		if not draft_purchase_invoice.fk_provider:
			raise DraftPurchaseInvoiceProviderNotFoundException

		if not draft_purchase_invoice.fk_invoice_service:
			raise DraftPurchaseInvoiceServiceNotFoundException

		if not draft_purchase_invoice.id_receipt_file:
			raise DraftPurchaseInvoiceReceiptFileNotFoundException

		if not draft_purchase_invoice.currency:
			raise DraftPurchaseInvoiceCurrencyNotFoundException

		if not draft_purchase_invoice.issue_date:
			raise DraftPurchaseInvoiceIssueDateNotFoundException

		if not draft_purchase_invoice.receipt_date:
			raise DraftPurchaseInvoiceReceiptDateNotFoundException

		if not draft_purchase_invoice.unit_price:
			raise DraftPurchaseInvoiceUnitPriceNotFoundException

		if len(draft_purchase_invoice.concept) < 1:
			raise DraftPurchaseInvoiceConceptTooShortException

		# Validate service-specific required fields dynamically
		# These validations depend on the service type configuration
		if service.require_awb and not draft_purchase_invoice.awb:
			raise DraftPurchaseInvoiceAwbRequiredException

		if service.require_kg and not draft_purchase_invoice.kg:
			raise DraftPurchaseInvoiceKgRequiredException

		if service.require_items and not draft_purchase_invoice.items:
			raise DraftPurchaseInvoiceItemsRequiredException

		if service.require_detail_file and not draft_purchase_invoice.id_details_file:
			raise DraftPurchaseInvoiceDetailFileRequiredException

		# Note: unit_price is already validated above as a general required field
		# service.require_unit_price is redundant but could be used for
		# additional business logic if needed


@dataclass
class FinalizeDraftPurchaseInvoiceUseCase:
	"""
	Finaliza la draft invoice
	"""

	async def __call__(
		self, draft_purchase_invoice: DraftPurchaseInvoice
	) -> DraftPurchaseInvoice:
		# Mark as finalized
		draft_purchase_invoice.state = "Finalized"
		return draft_purchase_invoice


@dataclass
class DraftPurchaseInvoiceUseCaseFactory:
	draft_purchase_invoice_repository: DraftPurchaseInvoiceRepository

	def __post_init__(self):
		self.get_provider_draft_invoices_list = GetProviderDraftInvoicesListUseCase(
			self.draft_purchase_invoice_repository
		)
		self.get_draft_purchase_invoice_by_id = GetDraftPurchaseInvoicesByIdUseCase(
			self.draft_purchase_invoice_repository
		)
		self.create_draft_purchase_invoice = CreateDraftPurchaseInvoiceUseCase()
		self.save_draft_purchase_invoice = SaveDraftPurchaseInvoicesUseCase(
			self.draft_purchase_invoice_repository
		)
		self.delete_draft_purchase_invoice = DeleteDraftPurchaseInvoicesUseCase(
			self.draft_purchase_invoice_repository
		)
		self.validate_draft_purchase_invoice = ValidateDraftPurchaseInvoiceUseCase()
		self.finalize_draft_purchase_invoice = FinalizeDraftPurchaseInvoiceUseCase()
