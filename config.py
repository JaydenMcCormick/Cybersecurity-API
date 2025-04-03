from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    sqlalchemy_string: str = "postgresql://user:passwordp@host/db" # example login, need to replace with ours
    
settings = Settings()