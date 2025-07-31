import re

def password_valid(password):
    error = []
    
    if len(password) < 8:
        error.append("Password must be at least 8 characters long.")
    
    if not re.search(r'[A-Z]', password):
        error.append("Password must contain at least one uppercase letter.")
        
    if not re.search(r'[a-z]', password):
        error.append("Password must contain at least one lowercase letter.")
        
    if not re.search(r'[0-9]', password):
        error.append("Password must contain at least one digit.")
        
    return (True,) if not error else (False, error)

        
    
    

    