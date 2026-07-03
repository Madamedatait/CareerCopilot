from backend.repositories.company_repository import get_or_create_company

company_id = get_or_create_company("Scalingo")

print(company_id)