from pydantic import BaseModel
from modules.provider.domain.command import CreateProviderCommand, UpdateProviderCommand


class ProviderCreateRequest(CreateProviderCommand): ...


class ProviderUpdateRequest(UpdateProviderCommand): ...
