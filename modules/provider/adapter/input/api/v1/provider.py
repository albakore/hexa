from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Form, Response


provider_router = APIRouter()
