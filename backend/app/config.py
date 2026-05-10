from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "mysql+pymysql://root:knaveena%4021@localhost:3306/text_summarizer"
    
    # JWT
    SECRET_KEY: str = "your-secret-key-change-in-production-use-env-variable"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours
    
    # Model - Using t5-small to match the trained model
    MODEL_NAME: str = "t5-small"  # t5-small=fast, t5-base=better, facebook/bart-large-cnn=best
    MODEL_CACHE_DIR: str = "./models"
    MAX_INPUT_LENGTH: int = 512  # Reduced for faster processing
    MAX_OUTPUT_LENGTH: int = 256
    
    # Training
    AUTO_TRAINING_ENABLED: bool = True
    MIN_FEEDBACK_RATING: int = 4
    BATCH_SIZE_FOR_TRAINING: int = 8
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow" # Allow extra env vars if needed

settings = Settings()
