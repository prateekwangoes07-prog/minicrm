from fastapi import APIRouter

from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.company import router as company_router
from app.api.v1.endpoints.employee import router as employee_router
from app.api.v1.endpoints.customer import router as customer_router
from app.api.v1.endpoints.lead import router as lead_router

api_router = APIRouter()
api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
api_router.include_router(company_router, prefix="/companies", tags=["Companies"])
api_router.include_router(employee_router, prefix="/employees", tags=["Employees"])
api_router.include_router(customer_router, prefix="/customers", tags=["Customers"])
api_router.include_router(lead_router, prefix="/leads", tags=["Leads"])



