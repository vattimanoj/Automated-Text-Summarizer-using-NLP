import re
import os
from fastapi import HTTPException

def validate_password(password: str):
    """
    Validates that password has at least 8 characters and one special character.
    """
    if len(password) < 8:
        raise HTTPException(
            status_code=400,
            detail="Password must be at least 8 characters long"
        )
    
    # Check for at least one special character
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        raise HTTPException(
            status_code=400,
            detail="Password must contain at least one special character"
        )
    
    # Check for at least one uppercase letter
    if not re.search(r"[A-Z]", password):
        raise HTTPException(
            status_code=400,
            detail="Password must contain at least one uppercase letter"
        )
    
    # Check for at least one digit
    if not re.search(r"\d", password):
        raise HTTPException(
            status_code=400,
            detail="Password must contain at least one number"
        )
    
    return True

def get_safe_filename(filename: str) -> str:
    """
    Returns a safe version of the filename, replacing non-ASCII characters
    to prevent encoding issues in logs and some file systems.
    """
    if not filename:
        return "unnamed_file"
    
    # Extract extension
    base, ext = os.path.splitext(filename)
    
    # Keep only alphanumeric chars, dots, and underscores for the base name
    # We use a simple replacement for non-ASCII to keep it readable if possible
    # but safe for logs. If it's all non-ASCII, we'll get an empty string.
    safe_base = re.sub(r'[^a-zA-Z0-9._-]', '_', base)
    
    if not safe_base.strip('_'):
        safe_base = "file"
        
    return f"{safe_base}{ext}"
