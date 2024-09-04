from uuid import UUID
from starlette import status
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_db_context, get_db_context
from models.company import CompanyModel, CompanyViewModel
from services.exception import ResourceNotFoundError
from services import company as CompanyService

router = APIRouter(prefix="/companies", tags=["Companies"])

@router.get("", response_model=list[CompanyViewModel])
async def get_all_companies(async_db: AsyncSession = Depends(get_async_db_context)):
    return await CompanyService.get_company(async_db)


@router.get("/{company_id}", status_code=status.HTTP_200_OK, response_model=CompanyViewModel)
async def get_company_by_id(company_id: UUID, db: Session = Depends(get_db_context)):    
    company = CompanyService.get_company_by_id(db, company_id)

    if company is None:
        raise ResourceNotFoundError()

    return company


@router.post("", status_code=status.HTTP_201_CREATED, response_model=CompanyViewModel)
async def create_company(request: CompanyModel, db: Session = Depends(get_db_context)):
    return CompanyService.add_new_company(db, request)


@router.put("/{company_id}", status_code=status.HTTP_200_OK, response_model=CompanyViewModel)
async def update_company(
    company_id: UUID,
    request: CompanyModel,
    db: Session = Depends(get_db_context),
    ):
        return CompanyService.update_company(db, company_id, request)


@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(company_id: UUID, db: Session = Depends(get_db_context)):
    CompanyService.delete_company(db, company_id)
