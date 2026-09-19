from pydantic import (BaseModel,Field,AnyUrl,field_validator,model_validator,computed_field)
from typing import Annotated,Literal,List,Optional
from uuid import UUID

class Product(BaseModel):
    id:str
    sku:Annotated[
        str,
        Field(min_length=6,max_length=30,title="SKU",description="stock keeping unit",examples=["asd-rtf-ert-34g"])
    ]
    price:Annotated[int,Field(min=1,description="Product price")]
    name:Annotated[
        str,
        Field(min_length=5,max_length=80,title="Product Name",description="Redable product name")
    ]
    category:Annotated[
        str,
        Field(min_length=3,max_length=10,title="Product Category",description="redable Product Category")
    ]
    in_stock:Annotated[bool,Field(description="Product available or not")]
    tags:Annotated[Optional[List[str]],Field(default=None,max_length=10,description="Upto 10 tags")]
    stock:Annotated[int,Field(min=1,description="In Stock Quantity")]

    @field_validator("sku",mode="after")
    @classmethod
    def validate_sku_formats(cls,value:str):
        if("-" not in value):
            raise ValueError("SKU must have '-' ")

        last=value.split("-")[-1]
        if not (len(last)==3 and last.isdigit()):
            raise ValueError("SKU must ends with 3 digit sequence like -234")
        return value

    @model_validator(mode="after")
    @classmethod
    def validate_business_rule(cls,model:"Product"):
        if (model.in_stock == True and model.stock <= 0):
            raise ValueError("If in_stock is true then stock should be greater than 0")

        return model

    @computed_field
    @property
    def final_price(self)->float:
        return round(self.price * (1- 10/100),2)
        