```python
# src/utils/helpers.py

import random
from datetime import datetime, timedelta

def generate_random_user_data():
    """
    Generate realistic user data for educational verification.
    
    Returns:
        dict: Dictionary containing first_name, last_name, email, organization, birthdate
    """
    # Common first names
    first_names = [
        "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
        "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph",
        "Jessica", "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Nancy",
        "Daniel", "Lisa", "Matthew", "Betty", "Anthony", "Helen", "Mark", "Sandra",
        "Donald", "Donna", "Steven", "Carol", "Paul", "Ruth", "Andrew", "Sharon"
    ]
    
    # Common last names
    last_names = [
        "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
        "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
        "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
        "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker",
        "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill"
    ]
    
    # Educational institutions
    organizations = [
        "Harvard University", "Stanford University", "MIT", "California Institute of Technology",
        "University of Cambridge", "University of Oxford", "Columbia University", "University of Chicago",
        "University of Pennsylvania", "Yale University", "Princeton University", "University of Michigan",
        "University of California, Berkeley", "UCLA", "University of Virginia", "Duke University",
        "Northwestern University", "University of North Carolina", "New York University",
        "University of Texas at Austin", "University of Washington", "Cornell University",
        "University of Illinois Urbana-Champaign", "Georgia Institute of Technology",
        "University of Wisconsin-Madison", "University of Southern California",
        "Boston University", "University of Maryland", "Penn State University",
        "Ohio State University", "University of Florida", "Michigan State University"
    ]
    
    # Generate random name
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    
    # Generate realistic age (18-25 for education)
    age = random.randint(18, 25)
    current_year = datetime.now().year
    birth_year = current_year - age
    
    # Generate random month and day
    birth_month = random.randint(1, 12)
    birth_day = random.randint(1, 28)  # Keeping it safe to avoid invalid dates
    
    birthdate = f"{birth_year}-{birth_month:02d}-{birth_day:02d}"
    
    # Generate email based on name
    domain = random.choice(["gmail.com", "yahoo.com", "outlook.com", "edu.mail.com"])
    email = f"{first_name.lower()}.{last_name.lower()}{random.randint(10, 999)}@{domain}"
    
    # Select organization
    organization = random.choice(organizations)
    
    return {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "organization": organization,
        "birthdate": birthdate
    }

def clean_url(url: str) -> str:
    """
    Clean and format URLs for consistent usage.
    
    Args:
        url (str): Raw URL string
        
    Returns:
        str: Cleaned URL
    """
    if not url:
        return ""
        
    # Remove whitespace
    url = url.strip()
    
    # Add protocol if missing
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
        
    # Remove trailing slashes
    url = url.rstrip("/")
    
    return url

def validate_birthdate(birthdate: str) -> bool:
    """
    Validate if birthdate produces an age within educational range (15-30).
    
    Args:
        birthdate (str): Date string in YYYY-MM-DD format
        
    Returns:
        bool: True if valid educational age
    """
    try:
        birth_dt = datetime.strptime(birthdate, "%Y-%m-%d")
        age = (datetime.now() - birth_dt).days // 365
        return 15 <= age <= 30
    except ValueError:
        return False
```