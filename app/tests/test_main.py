#
# Copyright (C) 2021
#
# Author: hacktribe <hacktribe.org>
#


import pytest
from app.main import app
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_root():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        response = await ac.get("/docs")

    assert response.status_code == 200
