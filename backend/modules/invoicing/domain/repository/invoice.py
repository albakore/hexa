from abc import ABC, abstractmethod


class InvoiceRepository(ABC):

    @abstractmethod
    def save_draft(self, draft: DraftInvoice) -> DraftInvoice:
        pass

    @abstractmethod
    def update_draft(self, invoice_id: int, data: dict) -> None:
        pass

    @abstractmethod
    def delete_draft(self, invoice_id: int) -> None:
        pass

    @abstractmethod
    def get_draft(self, draft_id: int) -> DraftInvoice:
        pass

    @abstractmethod
    def save_emitted(self, invoice: Invoice) -> Invoice:
        pass

    @abstractmethod
    def get_by_id(self, invoice_id: int) -> Invoice:
        pass