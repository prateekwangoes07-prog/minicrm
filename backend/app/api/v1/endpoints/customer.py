from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies.auth import get_current_user, require_admin
from app.dependencies.customer import get_customer_service
from app.exceptions.customer import CustomerNotFoundException, CustomerAlreadyExistsException
from app.exceptions.company import CompanyNotFoundException
from app.schemas.customer import CustomerCreate, CustomerResponse, CustomerUpdate
from app.services.customer import CustomerService

router = APIRouter()


@router.post(
    "",
    response_model=CustomerResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new customer",
    description="Registers a new customer in the system. Restricted to administrators.",
)
async def create_customer(
    customer_in: CustomerCreate,
    customer_service: CustomerService = Depends(get_customer_service),
    _: None = Depends(require_admin),
) -> CustomerResponse:
    """
    Create a new customer.
    """
    try:
        customer = await customer_service.create_customer(customer_in)
        return CustomerResponse.model_validate(customer)
    except CompanyNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except CustomerAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message,
        )


@router.get(
    "",
    response_model=list[CustomerResponse],
    status_code=status.HTTP_200_OK,
    summary="List all customers",
    description="Retrieves a list of all registered customers with optional pagination. Accessible to all authenticated users.",
)
async def list_customers(
    skip: int = 0,
    limit: int = 100,
    customer_service: CustomerService = Depends(get_customer_service),
    _: None = Depends(get_current_user),
) -> list[CustomerResponse]:
    """
    Retrieve all customers.
    """
    customers = await customer_service.get_all_customers(skip=skip, limit=limit)
    return [CustomerResponse.model_validate(c) for c in customers]


@router.get(
    "/{id}",
    response_model=CustomerResponse,
    status_code=status.HTTP_200_OK,
    summary="Get customer by ID",
    description="Retrieves the details of a specific customer by their UUID. Accessible to all authenticated users.",
)
async def get_customer(
    id: UUID,
    customer_service: CustomerService = Depends(get_customer_service),
    _: None = Depends(get_current_user),
) -> CustomerResponse:
    """
    Retrieve a specific customer.
    """
    try:
        customer = await customer_service.get_customer(id)
        return CustomerResponse.model_validate(customer)
    except CustomerNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )


@router.put(
    "/{id}",
    response_model=CustomerResponse,
    status_code=status.HTTP_200_OK,
    summary="Update customer details",
    description="Updates the details of an existing customer. Restricted to administrators.",
)
async def update_customer(
    id: UUID,
    customer_in: CustomerUpdate,
    customer_service: CustomerService = Depends(get_customer_service),
    _: None = Depends(require_admin),
) -> CustomerResponse:
    """
    Update a customer's details.
    """
    try:
        customer = await customer_service.update_customer(id, customer_in)
        return CustomerResponse.model_validate(customer)
    except CustomerNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except CompanyNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except CustomerAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message,
        )


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a customer",
    description="Deletes a customer from the system. Restricted to administrators.",
)
async def delete_customer(
    id: UUID,
    customer_service: CustomerService = Depends(get_customer_service),
    _: None = Depends(require_admin),
) -> None:
    """
    Delete a customer.
    """
    try:
        await customer_service.delete_customer(id)
    except CustomerNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
