from pydantic import BaseModel, ConfigDict


class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    category: str
    price: float
    stock: int
    unit: str
    brand: str | None = None


class ProductResponse(ProductCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)