from pydantic import (
    BaseModel, 
    EmailStr,
    field_validator
)


class User(BaseModel):
    name: str
    username: str
    email: EmailStr
    password: str
    phone_number: str

    @field_validator('password')
    @classmethod
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password Length must be greater that 8")
        
        return value
        
    @field_validator('phone_number')
    @classmethod
    def validate_phone_number(cls, value):
        country_code, actual_number = value.split('-')
        if len(actual_number) != 10:
            raise ValueError("Phone number should be exactly 10 digits")
        
        return value