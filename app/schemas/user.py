from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str  

class UserOut(BaseModel):
    id: str
    name: str

    class Config:
        from_attributes = True