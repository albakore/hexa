from dataclasses import dataclass
from typing import Any

# Interfaces externas al caso de uso
from app.invoicing.repositories.invoice_repository import InvoiceRepository
from app.invoicing.services.invoice_emitter import InvoiceEmitter
from app.invoicing.models import DraftInvoice, Invoice
from modules.invoicing.domain.dto import DraftInvoiceCreateDTO

# ─────────────────────────────────────────────
# Casos de uso individuales
# ─────────────────────────────────────────────

@dataclass
class CreateDraftInvoice:
    repo: InvoiceRepository

    def __call__(self, dto: DraftInvoiceCreateDTO) -> DraftInvoice:
        draft = DraftInvoice(**dto.model_dump())
        return self.repo.save_draft(draft)


@dataclass
class UpdateDraftInvoice:
    repo: InvoiceRepository

    def __call__(self, invoice_id: int, data: dict) -> None:
        self.repo.update_draft(invoice_id, data)


@dataclass
class DeleteDraftInvoice:
    repo: InvoiceRepository

    def __call__(self, invoice_id: int) -> None:
        self.repo.delete_draft(invoice_id)


@dataclass
class IssueInvoice:
    repo: InvoiceRepository
    emitter: InvoiceEmitter

    def __call__(self, draft_id: int) -> Invoice:
        draft = self.repo.get_draft(draft_id)
        emitted = self.emitter.emit(draft)
        return self.repo.save_emitted(emitted)


@dataclass
class CalculateInvoiceTotals:
    def __call__(self, draft: DraftInvoice) -> dict:
        subtotal = sum(item.amount for item in draft.items)
        tax = subtotal * 0.21  # ejemplo: IVA 21%
        total = subtotal + tax
        return {"subtotal": subtotal, "tax": tax, "total": total}


@dataclass
class GetInvoiceDetail:
    repo: InvoiceRepository

    def __call__(self, invoice_id: int) -> Invoice:
        return self.repo.get_by_id(invoice_id)


# ─────────────────────────────────────────────
# Fábrica de casos de uso
# ─────────────────────────────────────────────

@dataclass
class InvoicingUseCaseFactory:
    invoice_repo: InvoiceRepository
    invoice_emitter: InvoiceEmitter
    
    def __post_init__(self):
        self.create_draft_invoice = CreateDraftInvoice(self.invoice_repo)
        self.update_draft_invoice = UpdateDraftInvoice(self.invoice_repo)
        self.delete_draft_invoice = DeleteDraftInvoice(self.invoice_repo)
        self.issue_invoice = IssueInvoice(self.invoice_repo, self.invoice_emitter)
        self.calculate_invoice_totals = CalculateInvoiceTotals()
        self.get_invoice_detail = GetInvoiceDetail(self.invoice_repo)