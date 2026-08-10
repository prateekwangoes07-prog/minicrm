from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies.auth import get_current_user, require_admin
from app.dependencies.employee import get_employee_service
from app.exceptions.employee import EmployeeNotFoundException, EmployeeAlreadyExistsException
from app.exceptions.company import CompanyNotFoundException
from app.schemas.employee import EmployeeCreate, EmployeeResponse, EmployeeUpdate
from app.services.employee import EmployeeService

router = APIRouter()


@router.post(
    "",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new employee",
    description="Registers a new employee (user) in the system and associates them with a company. Restricted to administrators.",
)
async def create_employee(
    employee_in: EmployeeCreate,
    employee_service: EmployeeService = Depends(get_employee_service),
    _: None = Depends(require_admin),
) -> EmployeeResponse:
    """
    Create a new employee.
    """
    try:
        employee = await employee_service.create_employee(employee_in)
        return EmployeeResponse.model_validate(employee)
    except CompanyNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except EmployeeAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message,
        )


@router.get(
    "",
    response_model=list[EmployeeResponse],
    status_code=status.HTTP_200_OK,
    summary="List all employees",
    description="Retrieves a list of all registered employees with optional pagination. Accessible to all authenticated users.",
)
async def list_employees(
    skip: int = 0,
    limit: int = 100,
    employee_service: EmployeeService = Depends(get_employee_service),
    _: None = Depends(get_current_user),
) -> list[EmployeeResponse]:
    """
    Retrieve all employees.
    """
    employees = await employee_service.get_all_employees(skip=skip, limit=limit)
    return [EmployeeResponse.model_validate(e) for e in employees]


@router.get(
    "/{id}",
    response_model=EmployeeResponse,
    status_code=status.HTTP_200_OK,
    summary="Get employee by ID",
    description="Retrieves the details of a specific employee by their UUID. Accessible to all authenticated users.",
)
async def get_employee(
    id: UUID,
    employee_service: EmployeeService = Depends(get_employee_service),
    _: None = Depends(get_current_user),
) -> EmployeeResponse:
    """
    Retrieve a specific employee.
    """
    try:
        employee = await employee_service.get_employee(id)
        return EmployeeResponse.model_validate(employee)
    except EmployeeNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )


@router.put(
    "/{id}",
    response_model=EmployeeResponse,
    status_code=status.HTTP_200_OK,
    summary="Update employee details",
    description="Updates the details of an existing employee. Restricted to administrators.",
)
async def update_employee(
    id: UUID,
    employee_in: EmployeeUpdate,
    employee_service: EmployeeService = Depends(get_employee_service),
    _: None = Depends(require_admin),
) -> EmployeeResponse:
    """
    Update an employee's details.
    """
    try:
        employee = await employee_service.update_employee(id, employee_in)
        return EmployeeResponse.model_validate(employee)
    except EmployeeNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except CompanyNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except EmployeeAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message,
        )


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an employee",
    description="Deletes an employee from the system. Restricted to administrators.",
)
async def delete_employee(
    id: UUID,
    employee_service: EmployeeService = Depends(get_employee_service),
    _: None = Depends(require_admin),
) -> None:
    """
    Delete an employee.
    """
    try:
        await employee_service.delete_employee(id)
    except EmployeeNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
