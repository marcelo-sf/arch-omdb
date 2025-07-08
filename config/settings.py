from pydantic import BaseSettings, validator

class Settings(BaseSettings):
    database_url: str
    omdb_api_key: str
    backoff_base: int = 1  # Default base delay for retries (1 second)
    backoff_cap: int = 10  # Default max delay cap for retries (10 seconds)
    retry_attempts: int = 5  # Default maximum retry attempts

    class Config:
        env_file = ".env"

    @validator("backoff_base", "backoff_cap", "retry_attempts", pre=True, always=True)
    def validate_positive_numbers(cls, value, field):
        """
        Ensure all numeric environment configurations are valid positive integers.
        """
        try:
            value = int(value)
            if value <= 0:
                raise ValueError(f"{field.name} must be a positive integer.")
        except (ValueError, TypeError):
            raise ValueError(f"Invalid value for {field.name}. It must be a positive integer.")
        return value