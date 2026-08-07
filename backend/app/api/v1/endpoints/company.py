from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies.auth import get_current_user, require_admin
from app.dependencies.company import get_company_service
from app.exceptions.company import CompanyAlreadyExistsException, CompanyNotFoundException
from app.schemas.company import CompanyCreate, CompanyResponse, CompanyUpdate
from app.services.company import CompanyService

router = APIRouter()


@router.post(
    "",
    response_model=CompanyResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new company",
    description="Registers a new company in the system. Restricted to administrators.",
)
async def create_company(
    company_in: CompanyCreate,
    company_service: CompanyService = Depends(get_company_service),
    _: None = Depends(require_admin),
) -> CompanyResponse:
    """
    Create a new company.
    """
    try:
        company = await company_service.create_company(company_in)
        return CompanyResponse.model_validate(company)
    except CompanyAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message,
        )


@router.get(
    "",
    response_model=list[CompanyResponse],
    status_code=status.HTTP_200_OK,
    summary="List all companies",
    description="Retrieves a list of all registered companies with optional pagination. Accessible to all authenticated users.",
)
async def list_companies(
    skip: int = 0,
    limit: int = 100,
    company_service: CompanyService = Depends(get_company_service),
    _: None = Depends(get_current_user),
) -> list[CompanyResponse]:
    """
    Retrieve all companies.
    """
    companies = await company_service.get_all_companies(skip=skip, limit=limit)
    return [CompanyResponse.model_validate(c) for c in companies]


@router.get(
    "/{id}",
    response_model=CompanyResponse,
    status_code=status.HTTP_200_OK,
    summary="Get company by ID",
    description="Retrieves the details of a specific company by its UUID. Accessible to all authenticated users.",
)
async def get_company(
    id: UUID,
    company_service: CompanyService = Depends(get_company_service),
    _: None = Depends(get_current_user),
) -> CompanyResponse:
    """
    Retrieve a specific company.
    """
    try:
        company = await company_service.get_company(id)
        return CompanyResponse.model_validate(company)
    except CompanyNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )


@router.put(
    "/{id}",
    response_model=CompanyResponse,
    status_code=status.HTTP_200_OK,
    summary="Update company details",
    description="Updates the details of an existing company. Restricted to administrators.",
)
async def update_company(
    id: UUID,
    company_in: CompanyUpdate,
    company_service: CompanyService = Depends(get_company_service),
    _: None = Depends(require_admin),
) -> CompanyResponse:
    """
    Update a company's details.
    """
    try:
        company = await company_service.update_company(id, company_in)
        return CompanyResponse.model_validate(company)
    except CompanyNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except CompanyAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message,
        )


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a company",
    description="Deletes a company from the system. Restricted to administrators.",
)
async def delete_company(
    id: UUID,
    company_service: CompanyService = Depends(get_company_service),
    _: None = Depends(require_admin),
) -> None:
    """
    Delete a company.
    """
    try:
        await company_service.delete_company(id)
    except CompanyNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
