from pydantic import BaseModel, EmailStr, constr, field_validator

class RegistrationRequest(BaseModel):
    name: str
    email: EmailStr
    password: str

    @field_validator('name')
    def name_must_be_provided(cls, v):
        if not v:
            raise ValueError('name must be provided')
        return v

    @field_validator('password')
    def password_must_be_provided(cls, v):
        if not v:
            raise ValueError('Password must be provided')
        return v

    @field_validator('password')
    def password_complexity_check(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(char.islower() for char in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one digit')
        return v
    

class RegistrationRequestCompany(BaseModel):
    company_name: str
    employer_name: str
    company_email: EmailStr
    password: str

    @field_validator('company_name')
    def name_must_be_provided(cls, v):
        if not v:
            raise ValueError('name must be provided')
        return v
    
    @field_validator('employer_name')
    def name_must_be_provided(cls, v):
        if not v:
            raise ValueError('name must be provided')
        return v

    @field_validator('password')
    def password_must_be_provided(cls, v):
        if not v:
            raise ValueError('Password must be provided')
        return v

    @field_validator('password')
    def password_complexity_check(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(char.islower() for char in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one digit')
        return v

       
