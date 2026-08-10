from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies.auth import get_current_user, require_admin
from app.dependencies.lead import get_lead_service
from app.exceptions.lead import LeadNotFoundException, InvalidLeadRelationshipException
from app.schemas.lead import LeadCreate, LeadResponse, LeadUpdate
from app.services.lead import LeadService

router = APIRouter()


@router.post(
    "",
    response_model=LeadResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new lead",
    description="Registers a new lead in the CRM system. Restricted to administrators.",
)
async def create_lead(
    lead_in: LeadCreate,
    lead_service: LeadService = Depends(get_lead_service),
    _: None = Depends(require_admin),
) -> LeadResponse:
    """
    Create a new lead.
    """
    try:
        lead = await lead_service.create_lead(lead_in)
        return LeadResponse.model_validate(lead)
    except InvalidLeadRelationshipException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )


@router.get(
    "",
    response_model=list[LeadResponse],
    status_code=status.HTTP_200_OK,
    summary="List all leads",
    description="Retrieves a list of all leads with optional filtering and pagination. Accessible to all authenticated users.",
)
async def list_leads(
    company_id: UUID | None = None,
    customer_id: UUID | None = None,
    assigned_to: UUID | None = None,
    status: str | None = None,
    skip: int = 0,
    limit: int = 100,
    lead_service: LeadService = Depends(get_lead_service),
    _: None = Depends(get_current_user),
) -> list[LeadResponse]:
    """
    Retrieve all leads.
    """
    leads = await lead_service.get_all_leads(
        company_id=company_id,
        customer_id=customer_id,
        assigned_to=assigned_to,
        status=status,
        skip=skip,
        limit=limit,
    )
    return [LeadResponse.model_validate(l) for l in leads]


@router.get(
    "/{id}",
    response_model=LeadResponse,
    status_code=status.HTTP_200_OK,
    summary="Get lead by ID",
    description="Retrieves the details of a specific lead by their UUID. Accessible to all authenticated users.",
)
async def get_lead(
    id: UUID,
    lead_service: LeadService = Depends(get_lead_service),
    _: None = Depends(get_current_user),
) -> LeadResponse:
    """
    Retrieve a specific lead.
    """
    try:
        lead = await lead_service.get_lead(id)
        return LeadResponse.model_validate(lead)
    except LeadNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )


@router.put(
    "/{id}",
    response_model=LeadResponse,
    status_code=status.HTTP_200_OK,
    summary="Update lead details",
    description="Updates the details of an existing lead. Restricted to administrators.",
)
async def update_lead(
    id: UUID,
    lead_in: LeadUpdate,
    lead_service: LeadService = Depends(get_lead_service),
    _: None = Depends(require_admin),
) -> LeadResponse:
    """
    Update a lead's details.
    """
    try:
        lead = await lead_service.update_lead(id, lead_in)
        return LeadResponse.model_validate(lead)
    except LeadNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except InvalidLeadRelationshipException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a lead",
    description="Deletes a lead from the system. Restricted to administrators.",
)
async def delete_lead(
    id: UUID,
    lead_service: LeadService = Depends(get_lead_service),
    _: None = Depends(require_admin),
) -> None:
    """
    Delete a lead.
    """
    try:
        await lead_service.delete_lead(id)
    except LeadNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
