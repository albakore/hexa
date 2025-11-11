import pytest
from modules.yiqi_erp.container import YiqiContainer


@pytest.mark.asyncio
async def test_yiqi_services_list():
	repo = YiqiContainer().repository()
	result = await repo.get_services_list()
	assert result.status_code == 200


@pytest.mark.asyncio
async def test_yiqi_get_provider():
	repo = YiqiContainer().repository()
	result = await repo.get_provider_by_id(7639)
	assert result.status_code == 200


@pytest.mark.asyncio
async def test_yiqi_currency_list():
	repo = YiqiContainer().repository()
	result = await repo.get_currency_list()
	assert result.status_code == 200
