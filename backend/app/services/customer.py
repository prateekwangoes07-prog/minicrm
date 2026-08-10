from uuid import UUID
from app.exceptions.customer import CustomerNotFoundException, CustomerAlreadyExistsException
from app.exceptions.company import CompanyNotFoundException
from app.models.customer import Customer
from app.repositories.customer import CustomerRepository
from app.repositories.company import CompanyRepository
from app.schemas.customer import CustomerCreate, CustomerUpdate


class CustomerService:
    """
    Service layer containing business logic for Customer management.
    """
    def __init__(
        self,
        customer_repo: CustomerRepository,
        company_repo: CompanyRepository,
    ) -> None:
        self.customer_repo = customer_repo
        self.company_repo = company_repo

    async def get_customer(self, customer_id: UUID) -> Customer:
        """
        Retrieve a customer by their ID or raise CustomerNotFoundException.
        """
        customer = await self.customer_repo.get_by_id(customer_id)
        if not customer:
            raise CustomerNotFoundException(str(customer_id))
        return customer

    async def get_all_customers(self, skip: int = 0, limit: int = 100) -> list[Customer]:
        """
        Retrieve all customers with pagination.
        """
        return await self.customer_repo.get_all(skip=skip, limit=limit)

    async def create_customer(self, customer_in: CustomerCreate) -> Customer:
        """
        Create a new customer after verifying target company existence and email uniqueness.
        """
        # Validate company exists
        company = await self.company_repo.get_by_id(customer_in.company_id)
        if not company:
            raise CompanyNotFoundException(str(customer_in.company_id))

        # Check email uniqueness
        existing_customer = await self.customer_repo.get_by_email(customer_in.email)
        if existing_customer:
            raise CustomerAlreadyExistsException(f"Customer with email '{customer_in.email}' already exists.")

        db_customer = Customer(
            company_id=customer_in.company_id,
            first_name=customer_in.first_name,
            last_name=customer_in.last_name,
            email=customer_in.email,
            phone=customer_in.phone,
            address=customer_in.address,
            notes=customer_in.notes,
        )

        created = await self.customer_repo.create(db_customer)
        await self.customer_repo.db.commit()
        return created

    async def update_customer(self, customer_id: UUID, customer_in: CustomerUpdate) -> Customer:
        """
        Update an existing customer, validating target company and uniqueness constraints.
        """
        customer = await self.customer_repo.get_by_id(customer_id)
        if not customer:
            raise CustomerNotFoundException(str(customer_id))

        # Validate company exists if company_id is changing
        if customer_in.company_id is not None and customer_in.company_id != customer.company_id:
            company = await self.company_repo.get_by_id(customer_in.company_id)
            if not company:
                raise CompanyNotFoundException(str(customer_in.company_id))
            customer.company_id = customer_in.company_id

        # Validate email uniqueness if email is changing
        if customer_in.email is not None and customer_in.email != customer.email:
            existing_customer = await self.customer_repo.get_by_email(customer_in.email)
            if existing_customer:
                raise CustomerAlreadyExistsException(f"Customer with email '{customer_in.email}' already exists.")
            customer.email = customer_in.email

        # Update other fields
        if customer_in.first_name is not None:
            customer.first_name = customer_in.first_name
        if customer_in.last_name is not None:
            customer.last_name = customer_in.last_name
        if customer_in.phone is not None:
            customer.phone = customer_in.phone
        if customer_in.address is not None:
            customer.address = customer_in.address
        if customer_in.notes is not None:
            customer.notes = customer_in.notes
        if customer_in.is_active is not None:
            customer.is_active = customer_in.is_active

        updated = await self.customer_repo.update(customer)
        await self.customer_repo.db.commit()
        return updated

    async def delete_customer(self, customer_id: UUID) -> None:
        """
        Delete a customer.
        """
        customer = await self.customer_repo.get_by_id(customer_id)
        if not customer:
            raise CustomerNotFoundException(str(customer_id))

        await self.customer_repo.delete(customer)
        await self.customer_repo.db.commit()
