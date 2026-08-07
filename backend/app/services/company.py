from uuid import UUID
from app.exceptions.company import CompanyAlreadyExistsException, CompanyNotFoundException
from app.models.company import Company
from app.repositories.company import CompanyRepository
from app.schemas.company import CompanyCreate, CompanyUpdate


class CompanyService:
    """
    Service layer containing business logic for Company management.
    """
    def __init__(self, company_repo: CompanyRepository) -> None:
        self.company_repo = company_repo

    async def get_company(self, company_id: UUID) -> Company:
        """
        Retrieve a company by its ID or raise a NotFound exception.
        """
        company = await self.company_repo.get_by_id(company_id)
        if not company:
            raise CompanyNotFoundException(str(company_id))
        return company

    async def get_all_companies(self, skip: int = 0, limit: int = 100) -> list[Company]:
        """
        Retrieve all companies with pagination.
        """
        return await self.company_repo.get_all(skip=skip, limit=limit)

    async def create_company(self, company_in: CompanyCreate) -> Company:
        """
        Create a new company, verifying duplicate names and email addresses.
        """
        existing_name = await self.company_repo.get_by_name(company_in.name)
        if existing_name:
            raise CompanyAlreadyExistsException(f"Company with name '{company_in.name}' already exists.")

        existing_email = await self.company_repo.get_by_email(company_in.email)
        if existing_email:
            raise CompanyAlreadyExistsException(f"Company with email '{company_in.email}' already exists.")

        db_company = Company(
            name=company_in.name,
            email=company_in.email,
            phone=company_in.phone,
            address=company_in.address,
            website_url=company_in.website_url,
            industry=company_in.industry,
        )
        created_company = await self.company_repo.create(db_company)
        await self.company_repo.db.commit()
        return created_company

    async def update_company(self, company_id: UUID, company_in: CompanyUpdate) -> Company:
        """
        Update an existing company, verifying uniqueness constraints if they are modified.
        """
        company = await self.company_repo.get_by_id(company_id)
        if not company:
            raise CompanyNotFoundException(str(company_id))

        if company_in.name is not None and company_in.name != company.name:
            existing_name = await self.company_repo.get_by_name(company_in.name)
            if existing_name:
                raise CompanyAlreadyExistsException(f"Company with name '{company_in.name}' already exists.")
            company.name = company_in.name

        if company_in.email is not None and company_in.email != company.email:
            existing_email = await self.company_repo.get_by_email(company_in.email)
            if existing_email:
                raise CompanyAlreadyExistsException(f"Company with email '{company_in.email}' already exists.")
            company.email = company_in.email

        if company_in.phone is not None:
            company.phone = company_in.phone
        if company_in.address is not None:
            company.address = company_in.address
        if company_in.website_url is not None:
            company.website_url = company_in.website_url
        if company_in.industry is not None:
            company.industry = company_in.industry
        if company_in.is_active is not None:
            company.is_active = company_in.is_active

        updated_company = await self.company_repo.update(company)
        await self.company_repo.db.commit()
        return updated_company

    async def delete_company(self, company_id: UUID) -> None:
        """
        Delete an existing company.
        """
        company = await self.company_repo.get_by_id(company_id)
        if not company:
            raise CompanyNotFoundException(str(company_id))

        await self.company_repo.delete(company)
        await self.company_repo.db.commit()
