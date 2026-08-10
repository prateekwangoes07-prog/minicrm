from uuid import UUID
from app.exceptions.lead import LeadNotFoundException, InvalidLeadRelationshipException
from app.models.lead import Lead
from app.repositories.lead import LeadRepository
from app.repositories.company import CompanyRepository
from app.repositories.customer import CustomerRepository
from app.repositories.user import UserRepository
from app.schemas.lead import LeadCreate, LeadUpdate


class LeadService:
    """
    Service layer containing business logic for Lead management.
    """
    def __init__(
        self,
        lead_repo: LeadRepository,
        company_repo: CompanyRepository,
        customer_repo: CustomerRepository,
        user_repo: UserRepository,
    ) -> None:
        self.lead_repo = lead_repo
        self.company_repo = company_repo
        self.customer_repo = customer_repo
        self.user_repo = user_repo

    async def get_lead(self, lead_id: UUID) -> Lead:
        """
        Retrieve a lead by their ID or raise LeadNotFoundException.
        """
        lead = await self.lead_repo.get_by_id(lead_id)
        if not lead:
            raise LeadNotFoundException(str(lead_id))
        return lead

    async def get_all_leads(
        self,
        company_id: UUID | None = None,
        customer_id: UUID | None = None,
        assigned_to: UUID | None = None,
        status: str | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Lead]:
        """
        Retrieve leads with optional filtering and pagination.
        """
        return await self.lead_repo.get_all(
            company_id=company_id,
            customer_id=customer_id,
            assigned_to=assigned_to,
            status=status,
            skip=skip,
            limit=limit,
        )

    async def create_lead(self, lead_in: LeadCreate) -> Lead:
        """
        Create a new lead after validating company, customer, and assigned user relationships.
        """
        # Validate company exists
        company = await self.company_repo.get_by_id(lead_in.company_id)
        if not company:
            raise InvalidLeadRelationshipException(f"Company with ID '{lead_in.company_id}' not found.")

        # Validate customer exists if supplied
        if lead_in.customer_id is not None:
            customer = await self.customer_repo.get_by_id(lead_in.customer_id)
            if not customer:
                raise InvalidLeadRelationshipException(f"Customer with ID '{lead_in.customer_id}' not found.")

        # Validate assigned user exists if supplied
        if lead_in.assigned_to is not None:
            user = await self.user_repo.get_by_id(lead_in.assigned_to)
            if not user:
                raise InvalidLeadRelationshipException(f"User with ID '{lead_in.assigned_to}' not found.")

        db_lead = Lead(
            company_id=lead_in.company_id,
            customer_id=lead_in.customer_id,
            assigned_to=lead_in.assigned_to,
            name=lead_in.name,
            email=lead_in.email,
            phone=lead_in.phone,
            requirement=lead_in.requirement,
            status=lead_in.status,
            source=lead_in.source,
            notes=lead_in.notes,
        )

        created = await self.lead_repo.create(db_lead)
        await self.lead_repo.db.commit()
        return created

    async def update_lead(self, lead_id: UUID, lead_in: LeadUpdate) -> Lead:
        """
        Update an existing lead, validating company, customer, and assigned user relationships if changed.
        """
        lead = await self.lead_repo.get_by_id(lead_id)
        if not lead:
            raise LeadNotFoundException(str(lead_id))

        # Validate company exists if changing
        if lead_in.company_id is not None and lead_in.company_id != lead.company_id:
            company = await self.company_repo.get_by_id(lead_in.company_id)
            if not company:
                raise InvalidLeadRelationshipException(f"Company with ID '{lead_in.company_id}' not found.")
            lead.company_id = lead_in.company_id

        # Validate customer exists if changing
        if lead_in.customer_id is not None and lead_in.customer_id != lead.customer_id:
            customer = await self.customer_repo.get_by_id(lead_in.customer_id)
            if not customer:
                raise InvalidLeadRelationshipException(f"Customer with ID '{lead_in.customer_id}' not found.")
            lead.customer_id = lead_in.customer_id
        elif lead_in.customer_id is None and "customer_id" in lead_in.model_fields_set:
            lead.customer_id = None

        # Validate assigned user exists if changing
        if lead_in.assigned_to is not None and lead_in.assigned_to != lead.assigned_to:
            user = await self.user_repo.get_by_id(lead_in.assigned_to)
            if not user:
                raise InvalidLeadRelationshipException(f"User with ID '{lead_in.assigned_to}' not found.")
            lead.assigned_to = lead_in.assigned_to
        elif lead_in.assigned_to is None and "assigned_to" in lead_in.model_fields_set:
            lead.assigned_to = None

        # Update fields
        if lead_in.name is not None:
            lead.name = lead_in.name
        if lead_in.email is not None:
            lead.email = lead_in.email
        if lead_in.phone is not None:
            lead.phone = lead_in.phone
        if lead_in.requirement is not None:
            lead.requirement = lead_in.requirement
        if lead_in.status is not None:
            lead.status = lead_in.status
        if lead_in.source is not None:
            lead.source = lead_in.source
        if lead_in.notes is not None:
            lead.notes = lead_in.notes

        updated = await self.lead_repo.update(lead)
        await self.lead_repo.db.commit()
        return updated

    async def delete_lead(self, lead_id: UUID) -> None:
        """
        Delete a lead.
        """
        lead = await self.lead_repo.get_by_id(lead_id)
        if not lead:
            raise LeadNotFoundException(str(lead_id))

        await self.lead_repo.delete(lead)
        await self.lead_repo.db.commit()
