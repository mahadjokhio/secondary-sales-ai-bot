"""
Input validation functions for the Secondary Sales AI Bot.

This module provides comprehensive validation functions for user inputs,
data integrity, and business rule enforcement.
"""

import re
import json
from typing import Any, Dict, List, Optional, Union, Tuple
from pathlib import Path
from datetime import datetime, date
from utils.exceptions import DataValidationError


class ValidationResult:
    """Result of a validation operation."""
    
    def __init__(self, is_valid: bool, message: str = "", suggestions: Optional[List[str]] = None):
        self.is_valid = is_valid
        self.message = message
        self.suggestions = suggestions or []


def validate_email(email: str) -> ValidationResult:
    """
    Validate email format.
    
    Args:
        email: Email address to validate
        
    Returns:
        ValidationResult with validation status and message
    """
    if not email:
        return ValidationResult(False, "Email cannot be empty")
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return ValidationResult(True, "Valid email format")
    else:
        return ValidationResult(False, "Invalid email format")


def validate_phone_number(phone: str) -> ValidationResult:
    """
    Validate phone number format (Pakistani format).
    
    Args:
        phone: Phone number to validate
        
    Returns:
        ValidationResult with validation status and message
    """
    if not phone:
        return ValidationResult(False, "Phone number cannot be empty")
    
    # Remove spaces and special characters
    cleaned_phone = re.sub(r'[^\d+]', '', phone)
    
    # Pakistani phone number patterns
    patterns = [
        r'^\+92[0-9]{10}$',  # +92XXXXXXXXXX
        r'^92[0-9]{10}$',    # 92XXXXXXXXXX
        r'^0[0-9]{10}$',     # 0XXXXXXXXXX
    ]
    
    for pattern in patterns:
        if re.match(pattern, cleaned_phone):
            return ValidationResult(True, "Valid phone number format")
    
    return ValidationResult(
        False, 
        "Invalid phone number format. Expected formats: +92XXXXXXXXXX, 92XXXXXXXXXX, or 0XXXXXXXXXX"
    )


def validate_product_name(product_name: str, available_products: List[str]) -> ValidationResult:
    """
    Validate product name against available products.
    
    Args:
        product_name: Product name to validate
        available_products: List of available product names
        
    Returns:
        ValidationResult with validation status and suggestions
    """
    if not product_name:
        return ValidationResult(False, "Product name cannot be empty")
    
    # Exact match
    if product_name in available_products:
        return ValidationResult(True, "Valid product name")
    
    # Fuzzy matching for suggestions
    suggestions = []
    product_lower = product_name.lower()
    
    for product in available_products:
        if product_lower in product.lower() or product.lower() in product_lower:
            suggestions.append(product)
    
    if suggestions:
        return ValidationResult(
            False, 
            f"Product '{product_name}' not found",
            suggestions[:5]  # Limit to 5 suggestions
        )
    else:
        return ValidationResult(False, f"Product '{product_name}' not found")


def validate_quantity(quantity: Union[int, str], min_qty: int = 1, max_qty: int = 10000) -> ValidationResult:
    """
    Validate order quantity.
    
    Args:
        quantity: Quantity to validate
        min_qty: Minimum allowed quantity
        max_qty: Maximum allowed quantity
        
    Returns:
        ValidationResult with validation status and message
    """
    try:
        qty = int(quantity)
    except (ValueError, TypeError):
        return ValidationResult(False, "Quantity must be a valid number")
    
    if qty < min_qty:
        return ValidationResult(False, f"Quantity must be at least {min_qty}")
    
    if qty > max_qty:
        return ValidationResult(False, f"Quantity cannot exceed {max_qty}")
    
    return ValidationResult(True, "Valid quantity")


def validate_price(price: Union[float, str]) -> ValidationResult:
    """
    Validate price value.
    
    Args:
        price: Price to validate
        
    Returns:
        ValidationResult with validation status and message
    """
    try:
        price_val = float(price)
    except (ValueError, TypeError):
        return ValidationResult(False, "Price must be a valid number")
    
    if price_val < 0:
        return ValidationResult(False, "Price cannot be negative")
    
    if price_val > 1000000:  # 1 million PKR
        return ValidationResult(False, "Price seems unusually high")
    
    return ValidationResult(True, "Valid price")


def validate_outlet_name(outlet_name: str, available_outlets: List[str]) -> ValidationResult:
    """
    Validate outlet name against available outlets.
    
    Args:
        outlet_name: Outlet name to validate
        available_outlets: List of available outlet names
        
    Returns:
        ValidationResult with validation status and suggestions
    """
    if not outlet_name:
        return ValidationResult(False, "Outlet name cannot be empty")
    
    # Exact match
    if outlet_name in available_outlets:
        return ValidationResult(True, "Valid outlet name")
    
    # Fuzzy matching for suggestions
    suggestions = []
    outlet_lower = outlet_name.lower()
    
    for outlet in available_outlets:
        if outlet_lower in outlet.lower() or outlet.lower() in outlet_lower:
            suggestions.append(outlet)
    
    if suggestions:
        return ValidationResult(
            False, 
            f"Outlet '{outlet_name}' not found",
            suggestions[:5]  # Limit to 5 suggestions
        )
    else:
        return ValidationResult(False, f"Outlet '{outlet_name}' not found")


def validate_date_range(start_date: str, end_date: str) -> ValidationResult:
    """
    Validate date range.
    
    Args:
        start_date: Start date string (YYYY-MM-DD)
        end_date: End date string (YYYY-MM-DD)
        
    Returns:
        ValidationResult with validation status and message
    """
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d').date()
        end = datetime.strptime(end_date, '%Y-%m-%d').date()
    except ValueError:
        return ValidationResult(False, "Invalid date format. Use YYYY-MM-DD")
    
    if start > end:
        return ValidationResult(False, "Start date cannot be after end date")
    
    today = date.today()
    if start > today:
        return ValidationResult(False, "Start date cannot be in the future")
    
    # Check if date range is too large (more than 1 year)
    if (end - start).days > 365:
        return ValidationResult(False, "Date range cannot exceed 1 year")
    
    return ValidationResult(True, "Valid date range")


def validate_json_data(data: str) -> ValidationResult:
    """
    Validate JSON data format.
    
    Args:
        data: JSON string to validate
        
    Returns:
        ValidationResult with validation status and message
    """
    if not data:
        return ValidationResult(False, "JSON data cannot be empty")
    
    try:
        json.loads(data)
        return ValidationResult(True, "Valid JSON format")
    except json.JSONDecodeError as e:
        return ValidationResult(False, f"Invalid JSON format: {e}")


def validate_file_path(file_path: Union[str, Path]) -> ValidationResult:
    """
    Validate file path exists and is accessible.
    
    Args:
        file_path: File path to validate
        
    Returns:
        ValidationResult with validation status and message
    """
    try:
        path = Path(file_path)
        
        if not path.exists():
            return ValidationResult(False, f"File does not exist: {file_path}")
        
        if not path.is_file():
            return ValidationResult(False, f"Path is not a file: {file_path}")
        
        # Check if file is readable
        with open(path, 'r') as f:
            f.read(1)
        
        return ValidationResult(True, "Valid file path")
    except PermissionError:
        return ValidationResult(False, f"Permission denied: {file_path}")
    except Exception as e:
        return ValidationResult(False, f"File validation error: {e}")


def validate_credit_limit(order_total: float, current_outstanding: float, credit_limit: float) -> ValidationResult:
    """
    Validate if order is within credit limit.
    
    Args:
        order_total: Total amount of the order
        current_outstanding: Current outstanding amount
        credit_limit: Maximum credit limit
        
    Returns:
        ValidationResult with validation status and message
    """
    total_exposure = current_outstanding + order_total
    
    if total_exposure > credit_limit:
        available_credit = credit_limit - current_outstanding
        return ValidationResult(
            False, 
            f"Order exceeds credit limit. Available credit: Rs. {available_credit:,.2f}"
        )
    
    return ValidationResult(True, "Within credit limit")


def validate_promotion_eligibility(
    order_items: List[Dict[str, Any]], 
    promotion: Dict[str, Any]
) -> ValidationResult:
    """
    Validate if order is eligible for a promotion.
    
    Args:
        order_items: List of order items
        promotion: Promotion details
        
    Returns:
        ValidationResult with validation status and message
    """
    if not promotion.get('is_active', True):
        return ValidationResult(False, "Promotion is not active")
    
    # Check minimum quantity requirement
    min_quantity = promotion.get('min_quantity', 0)
    if min_quantity > 0:
        total_quantity = sum(item.get('quantity', 0) for item in order_items)
        if total_quantity < min_quantity:
            return ValidationResult(
                False, 
                f"Minimum quantity requirement not met. Required: {min_quantity}"
            )
    
    # Check minimum amount requirement
    min_amount = promotion.get('min_amount', 0)
    if min_amount > 0:
        total_amount = sum(
            item.get('quantity', 0) * item.get('price', 0) 
            for item in order_items
        )
        if total_amount < min_amount:
            return ValidationResult(
                False, 
                f"Minimum amount requirement not met. Required: Rs. {min_amount:,.2f}"
            )
    
    # Check applicable products
    applicable_products = promotion.get('applicable_products', [])
    if applicable_products:
        order_products = [item.get('product_name', '') for item in order_items]
        eligible_products = [p for p in order_products if p in applicable_products]
        if not eligible_products:
            return ValidationResult(
                False, 
                f"No eligible products for this promotion. Applicable: {', '.join(applicable_products)}"
            )
    
    return ValidationResult(True, "Eligible for promotion")


def sanitize_input(user_input: str) -> str:
    """
    Sanitize user input to prevent injection attacks.
    
    Args:
        user_input: Raw user input
        
    Returns:
        Sanitized input string
    """
    if not user_input:
        return ""
    
    # Remove potentially dangerous characters
    sanitized = re.sub(r'[<>"\';\\]', '', user_input)
    
    # Limit length
    sanitized = sanitized[:1000]
    
    # Strip whitespace
    sanitized = sanitized.strip()
    
    return sanitized


def validate_voice_command(command: str) -> Tuple[bool, str, Dict[str, Any]]:
    """
    Validate and parse voice command.
    
    Args:
        command: Voice command string
        
    Returns:
        Tuple of (is_valid, intent, extracted_data)
    """
    if not command:
        return False, "empty", {}
    
    command_lower = command.lower().strip()
    
    # Order creation patterns
    order_patterns = [
        r'create order for (.+)',
        r'new order for (.+)',
        r'place order for (.+)',
    ]
    
    for pattern in order_patterns:
        match = re.search(pattern, command_lower)
        if match:
            outlet_name = match.group(1).strip()
            return True, "create_order", {"outlet": outlet_name}
    
    # Product addition patterns
    add_patterns = [
        r'add (\d+) (.+) to (?:cart|order)',
        r'(\d+) (.+) to the order',
        r'include (\d+) (.+)',
    ]
    
    for pattern in add_patterns:
        match = re.search(pattern, command_lower)
        if match:
            quantity = int(match.group(1))
            product = match.group(2).strip()
            return True, "add_product", {"quantity": quantity, "product": product}
    
    # Query patterns
    query_patterns = [
        (r'what.*price.*(.+)', "price_query"),
        (r'show.*promotion', "show_promotions"),
        (r'display.*report', "show_reports"),
        (r'outlet.*performance', "outlet_performance"),
    ]
    
    for pattern, intent in query_patterns:
        if re.search(pattern, command_lower):
            return True, intent, {"query": command}
    
    # Navigation patterns
    nav_patterns = [
        (r'go to dashboard', "navigate_dashboard"),
        (r'open order', "navigate_orders"),
        (r'show outlet', "navigate_outlets"),
    ]
    
    for pattern, intent in nav_patterns:
        if re.search(pattern, command_lower):
            return True, intent, {}
    
    return False, "unknown", {"command": command}
