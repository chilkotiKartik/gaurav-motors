"""
Input Validation and Sanitization Utilities
Provides secure validation for user inputs
"""
import re
from datetime import datetime, date
from typing import Optional, Any

class ValidationError(Exception):
    """Custom validation error"""
    pass

class Validator:
    """Input validation utilities"""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        if not email:
            return False
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Validate phone number (Indian format)"""
        if not phone:
            return False
        # Remove spaces, dashes, parentheses
        cleaned = re.sub(r'[\s\-\(\)]', '', phone)
        # Check for 10 digits or +91 followed by 10 digits
        pattern = r'^(\+91)?[6-9]\d{9}$'
        return bool(re.match(pattern, cleaned))
    
    @staticmethod
    def validate_username(username: str) -> bool:
        """Validate username (alphanumeric, 3-20 chars)"""
        if not username:
            return False
        pattern = r'^[a-zA-Z0-9_]{3,20}$'
        return bool(re.match(pattern, username))
    
    @staticmethod
    def validate_password_strength(password: str) -> tuple[bool, str]:
        """
        Validate password strength
        Returns: (is_valid, message)
        """
        if len(password) < 8:
            return False, "Password must be at least 8 characters"
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter"
        if not re.search(r'[a-z]', password):
            return False, "Password must contain at least one lowercase letter"
        if not re.search(r'[0-9]', password):
            return False, "Password must contain at least one number"
        return True, "Password is strong"
    
    @staticmethod
    def validate_vin(vin: str) -> bool:
        """Validate Vehicle Identification Number"""
        if not vin:
            return True  # VIN is optional
        # VIN should be 17 characters (alphanumeric, no I, O, Q)
        pattern = r'^[A-HJ-NPR-Z0-9]{17}$'
        return bool(re.match(pattern, vin.upper()))
    
    @staticmethod
    def validate_license_plate(plate: str) -> bool:
        """Validate Indian vehicle license plate"""
        if not plate:
            return True  # Optional
        # Common Indian format: AB12CD1234 or AB-12-CD-1234
        pattern = r'^[A-Z]{2}[-\s]?\d{1,2}[-\s]?[A-Z]{1,2}[-\s]?\d{1,4}$'
        return bool(re.match(pattern, plate.upper()))
    
    @staticmethod
    def sanitize_string(text: str, max_length: int = 500) -> str:
        """Sanitize and trim string input"""
        if not text:
            return ""
        # Remove leading/trailing whitespace
        text = text.strip()
        # Truncate to max length
        if len(text) > max_length:
            text = text[:max_length]
        return text
    
    @staticmethod
    def validate_date(date_str: str, min_date: Optional[date] = None) -> Optional[date]:
        """
        Validate and parse date string
        Returns: date object or None
        """
        try:
            parsed_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            if min_date and parsed_date < min_date:
                return None
            return parsed_date
        except (ValueError, TypeError):
            return None
    
    @staticmethod
    def validate_amount(amount: Any) -> Optional[float]:
        """Validate monetary amount"""
        try:
            value = float(amount)
            if value < 0:
                return None
            # Round to 2 decimal places
            return round(value, 2)
        except (ValueError, TypeError):
            return None
    
    @staticmethod
    def validate_rating(rating: Any) -> Optional[int]:
        """Validate rating (1-5)"""
        try:
            value = int(rating)
            if 1 <= value <= 5:
                return value
            return None
        except (ValueError, TypeError):
            return None

class Sanitizer:
    """HTML and SQL injection prevention"""
    
    @staticmethod
    def escape_html(text: str) -> str:
        """Escape HTML special characters"""
        if not text:
            return ""
        replacements = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#x27;',
            '/': '&#x2F;'
        }
        for char, replacement in replacements.items():
            text = text.replace(char, replacement)
        return text
    
    @staticmethod
    def remove_sql_keywords(text: str) -> str:
        """Remove common SQL injection keywords"""
        if not text:
            return ""
        sql_keywords = ['DROP', 'DELETE', 'INSERT', 'UPDATE', 'SELECT', 'UNION', 'EXEC', '--', ';']
        for keyword in sql_keywords:
            text = re.sub(f'\\b{keyword}\\b', '', text, flags=re.IGNORECASE)
        return text

# Quick access functions
def is_valid_email(email: str) -> bool:
    return Validator.validate_email(email)

def is_valid_phone(phone: str) -> bool:
    return Validator.validate_phone(phone)

def is_strong_password(password: str) -> tuple[bool, str]:
    return Validator.validate_password_strength(password)
