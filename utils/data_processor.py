"""
Data manipulation and validation utilities for the Secondary Sales AI Bot.

This module handles JSON file operations, data filtering, sorting,
mathematical calculations, and data persistence with comprehensive error handling.
"""

import json
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import pandas as pd
from utils.exceptions import DatabaseError, DataValidationError, FileCorruptionError, BackupError
from config.settings import get_settings


@dataclass
class OrderItem:
    """Order item data structure."""
    product_id: str
    product_name: str
    quantity: int
    unit_price: float
    total_price: float
    size: str = ""
    category: str = ""


@dataclass
class Order:
    """Order data structure."""
    order_id: str
    outlet_id: str
    outlet_name: str
    salesperson_id: str
    items: List[OrderItem]
    subtotal: float
    discount_amount: float
    tax_amount: float
    total_amount: float
    status: str
    created_date: str
    delivery_date: Optional[str] = None
    notes: Optional[str] = None


@dataclass
class Product:
    """Product data structure."""
    product_id: str
    name: str
    price: float
    category: str
    brand: str
    size: str
    stock: int
    description: str = ""
    is_active: bool = True


@dataclass
class Outlet:
    """Outlet data structure."""
    outlet_id: str
    name: str
    location: str
    contact_person: str
    phone: str
    email: str
    credit_limit: float
    outstanding_amount: float
    last_order_date: Optional[str] = None
    performance_rating: float = 0.0
    is_active: bool = True


class DataProcessor:
    """
    Handles all data processing operations with error handling and validation.
    
    Provides methods for JSON file operations, data manipulation,
    calculations, and backup management.
    """
    
    def __init__(self):
        """Initialize data processor with settings."""
        self.settings = get_settings()
        self.data_dir = self.settings.DATA_DIRECTORY
        self.backup_enabled = self.settings.BACKUP_ENABLED
        self._ensure_data_directory()
    
    def _ensure_data_directory(self) -> None:
        """Ensure data directory exists."""
        try:
            self.data_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            raise DatabaseError(f"Failed to create data directory: {e}")
    
    def load_json_file(self, filename: str) -> Dict[str, Any]:
        """
        Load JSON data from file with error handling.
        
        Args:
            filename: Name of the JSON file
            
        Returns:
            Dictionary containing the loaded data
            
        Raises:
            FileCorruptionError: If file is corrupted
            DatabaseError: If file cannot be read
        """
        file_path = self.data_dir / filename
        
        try:
            if not file_path.exists():
                # Create empty file if it doesn't exist
                self.save_json_file(filename, {})
                return {}
            
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            return data
            
        except json.JSONDecodeError as e:
            raise FileCorruptionError(
                f"Corrupted JSON file {filename}: {e}",
                error_code="JSON_CORRUPT",
                details={"file": str(file_path), "error": str(e)}
            )
        except Exception as e:
            raise DatabaseError(
                f"Failed to load file {filename}: {e}",
                error_code="FILE_READ_ERROR",
                details={"file": str(file_path), "error": str(e)}
            )
    
    def save_json_file(self, filename: str, data: Dict[str, Any]) -> None:
        """
        Save data to JSON file with backup.
        
        Args:
            filename: Name of the JSON file
            data: Data to save
            
        Raises:
            DatabaseError: If file cannot be saved
        """
        file_path = self.data_dir / filename
        
        try:
            # Create backup if enabled and file exists
            if self.backup_enabled and file_path.exists():
                self._create_backup(filename)
            
            # Write to temporary file first
            temp_path = file_path.with_suffix('.tmp')
            with open(temp_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            # Replace original file
            temp_path.replace(file_path)
            
        except Exception as e:
            raise DatabaseError(
                f"Failed to save file {filename}: {e}",
                error_code="FILE_WRITE_ERROR",
                details={"file": str(file_path), "error": str(e)}
            )
    
    def _create_backup(self, filename: str) -> None:
        """
        Create backup of a file.
        
        Args:
            filename: Name of the file to backup
            
        Raises:
            BackupError: If backup creation fails
        """
        try:
            source_path = self.data_dir / filename
            backup_dir = self.data_dir / "backups"
            backup_dir.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"{Path(filename).stem}_{timestamp}.json"
            backup_path = backup_dir / backup_filename
            
            shutil.copy2(source_path, backup_path)
            
            # Clean old backups (keep last 10)
            self._cleanup_old_backups(backup_dir, Path(filename).stem)
            
        except Exception as e:
            raise BackupError(
                f"Failed to create backup for {filename}: {e}",
                error_code="BACKUP_FAILED",
                details={"file": filename, "error": str(e)}
            )
    
    def _cleanup_old_backups(self, backup_dir: Path, base_name: str) -> None:
        """Clean up old backup files, keeping only the latest 10."""
        try:
            pattern = f"{base_name}_*.json"
            backup_files = list(backup_dir.glob(pattern))
            backup_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            
            # Remove files beyond the first 10
            for old_backup in backup_files[10:]:
                old_backup.unlink()
                
        except Exception:
            # Non-critical error, just ignore
            pass
    
    def load_products(self) -> Dict[str, Product]:
        """
        Load products from JSON file.
        
        Returns:
            Dictionary of product_id -> Product objects
        """
        try:
            data = self.load_json_file("products.json")
            products = {}
            
            for product_id, product_data in data.items():
                products[product_id] = Product(
                    product_id=product_id,
                    name=product_data.get("name", ""),
                    price=float(product_data.get("price", 0)),
                    category=product_data.get("category", ""),
                    brand=product_data.get("brand", ""),
                    size=product_data.get("size", ""),
                    stock=int(product_data.get("stock", 0)),
                    description=product_data.get("description", ""),
                    is_active=product_data.get("is_active", True)
                )
            
            return products
            
        except Exception as e:
            raise DataValidationError(
                f"Failed to load products: {e}",
                error_code="PRODUCT_LOAD_ERROR"
            )
    
    def save_products(self, products: Dict[str, Product]) -> None:
        """
        Save products to JSON file.
        
        Args:
            products: Dictionary of product_id -> Product objects
        """
        try:
            data = {}
            for product_id, product in products.items():
                data[product_id] = asdict(product)
            
            self.save_json_file("products.json", data)
            
        except Exception as e:
            raise DatabaseError(
                f"Failed to save products: {e}",
                error_code="PRODUCT_SAVE_ERROR"
            )
    
    def load_outlets(self) -> Dict[str, Outlet]:
        """
        Load outlets from JSON file.
        
        Returns:
            Dictionary of outlet_id -> Outlet objects
        """
        try:
            data = self.load_json_file("outlets.json")
            outlets = {}
            
            for outlet_id, outlet_data in data.items():
                outlets[outlet_id] = Outlet(
                    outlet_id=outlet_id,
                    name=outlet_data.get("name", ""),
                    location=outlet_data.get("location", ""),
                    contact_person=outlet_data.get("contact_person", ""),
                    phone=outlet_data.get("phone", ""),
                    email=outlet_data.get("email", ""),
                    credit_limit=float(outlet_data.get("credit_limit", 0)),
                    outstanding_amount=float(outlet_data.get("outstanding_amount", 0)),
                    last_order_date=outlet_data.get("last_order_date"),
                    performance_rating=float(outlet_data.get("performance_rating", 0)),
                    is_active=outlet_data.get("is_active", True)
                )
            
            return outlets
            
        except Exception as e:
            raise DataValidationError(
                f"Failed to load outlets: {e}",
                error_code="OUTLET_LOAD_ERROR"
            )
    
    def save_outlets(self, outlets: Dict[str, Outlet]) -> None:
        """
        Save outlets to JSON file.
        
        Args:
            outlets: Dictionary of outlet_id -> Outlet objects
        """
        try:
            data = {}
            for outlet_id, outlet in outlets.items():
                data[outlet_id] = asdict(outlet)
            
            self.save_json_file("outlets.json", data)
            
        except Exception as e:
            raise DatabaseError(
                f"Failed to save outlets: {e}",
                error_code="OUTLET_SAVE_ERROR"
            )
    
    def load_orders(self) -> Dict[str, Order]:
        """
        Load orders from JSON file.
        
        Returns:
            Dictionary of order_id -> Order objects
        """
        try:
            data = self.load_json_file("orders.json")
            orders = {}
            
            for order_id, order_data in data.items():
                # Convert items
                items = []
                for item_data in order_data.get("items", []):
                    items.append(OrderItem(
                        product_id=item_data.get("product_id", ""),
                        product_name=item_data.get("product_name", ""),
                        quantity=int(item_data.get("quantity", 0)),
                        unit_price=float(item_data.get("unit_price", 0)),
                        total_price=float(item_data.get("total_price", 0)),
                        size=item_data.get("size", ""),
                        category=item_data.get("category", "")
                    ))
                
                orders[order_id] = Order(
                    order_id=order_id,
                    outlet_id=order_data.get("outlet_id", ""),
                    outlet_name=order_data.get("outlet_name", ""),
                    salesperson_id=order_data.get("salesperson_id", ""),
                    items=items,
                    subtotal=float(order_data.get("subtotal", 0)),
                    discount_amount=float(order_data.get("discount_amount", 0)),
                    tax_amount=float(order_data.get("tax_amount", 0)),
                    total_amount=float(order_data.get("total_amount", 0)),
                    status=order_data.get("status", "draft"),
                    created_date=order_data.get("created_date", ""),
                    delivery_date=order_data.get("delivery_date"),
                    notes=order_data.get("notes")
                )
            
            return orders
            
        except Exception as e:
            raise DataValidationError(
                f"Failed to load orders: {e}",
                error_code="ORDER_LOAD_ERROR"
            )
    
    def save_orders(self, orders: Dict[str, Order]) -> None:
        """
        Save orders to JSON file.
        
        Args:
            orders: Dictionary of order_id -> Order objects
        """
        try:
            data = {}
            for order_id, order in orders.items():
                order_dict = asdict(order)
                data[order_id] = order_dict
            
            self.save_json_file("orders.json", data)
            
        except Exception as e:
            raise DatabaseError(
                f"Failed to save orders: {e}",
                error_code="ORDER_SAVE_ERROR"
            )
    
    def calculate_order_total(self, items: List[OrderItem], discount_percent: float = 0, tax_percent: float = 0) -> Tuple[float, float, float, float]:
        """
        Calculate order totals.
        
        Args:
            items: List of order items
            discount_percent: Discount percentage (0-100)
            tax_percent: Tax percentage (0-100)
            
        Returns:
            Tuple of (subtotal, discount_amount, tax_amount, total_amount)
        """
        try:
            subtotal = sum(item.total_price for item in items)
            discount_amount = subtotal * (discount_percent / 100)
            taxable_amount = subtotal - discount_amount
            tax_amount = taxable_amount * (tax_percent / 100)
            total_amount = subtotal - discount_amount + tax_amount
            
            return subtotal, discount_amount, tax_amount, total_amount
            
        except Exception as e:
            raise DataValidationError(
                f"Failed to calculate order total: {e}",
                error_code="CALCULATION_ERROR"
            )
    
    def filter_products(self, products: Dict[str, Product], **filters) -> Dict[str, Product]:
        """
        Filter products based on criteria.
        
        Args:
            products: Dictionary of products
            **filters: Filter criteria (category, brand, is_active, etc.)
            
        Returns:
            Filtered dictionary of products
        """
        filtered = {}
        
        for product_id, product in products.items():
            include = True
            
            for key, value in filters.items():
                if hasattr(product, key):
                    product_value = getattr(product, key)
                    if isinstance(value, str):
                        if value.lower() not in str(product_value).lower():
                            include = False
                            break
                    elif product_value != value:
                        include = False
                        break
            
            if include:
                filtered[product_id] = product
        
        return filtered
    
    def get_sales_analytics(self, orders: Dict[str, Order], date_range: Optional[Tuple[str, str]] = None) -> Dict[str, Any]:
        """
        Generate sales analytics from orders.
        
        Args:
            orders: Dictionary of orders
            date_range: Optional tuple of (start_date, end_date) in YYYY-MM-DD format
            
        Returns:
            Dictionary containing analytics data
        """
        try:
            filtered_orders = orders
            
            # Filter by date range if provided
            if date_range:
                start_date, end_date = date_range
                filtered_orders = {}
                for order_id, order in orders.items():
                    order_date = order.created_date[:10]  # Extract date part
                    if start_date <= order_date <= end_date:
                        filtered_orders[order_id] = order
            
            # Calculate analytics
            total_orders = len(filtered_orders)
            total_revenue = sum(order.total_amount for order in filtered_orders.values())
            avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
            
            # Product performance
            product_sales = {}
            for order in filtered_orders.values():
                for item in order.items:
                    if item.product_name not in product_sales:
                        product_sales[item.product_name] = {
                            "quantity": 0,
                            "revenue": 0
                        }
                    product_sales[item.product_name]["quantity"] += item.quantity
                    product_sales[item.product_name]["revenue"] += item.total_price
            
            # Outlet performance
            outlet_sales = {}
            for order in filtered_orders.values():
                if order.outlet_name not in outlet_sales:
                    outlet_sales[order.outlet_name] = {
                        "orders": 0,
                        "revenue": 0
                    }
                outlet_sales[order.outlet_name]["orders"] += 1
                outlet_sales[order.outlet_name]["revenue"] += order.total_amount
            
            return {
                "total_orders": total_orders,
                "total_revenue": total_revenue,
                "avg_order_value": avg_order_value,
                "product_sales": product_sales,
                "outlet_sales": outlet_sales,
                "date_range": date_range
            }
            
        except Exception as e:
            raise DataValidationError(
                f"Failed to generate analytics: {e}",
                error_code="ANALYTICS_ERROR"
            )
    
    def search_products(self, products: Dict[str, Product], query: str) -> List[Product]:
        """
        Search products by name or description.
        
        Args:
            products: Dictionary of products
            query: Search query
            
        Returns:
            List of matching products
        """
        query_lower = query.lower()
        results = []
        
        for product in products.values():
            if (query_lower in product.name.lower() or 
                query_lower in product.description.lower() or
                query_lower in product.category.lower() or
                query_lower in product.brand.lower()):
                results.append(product)
        
        # Sort by relevance (exact name matches first)
        results.sort(key=lambda p: (
            0 if query_lower == p.name.lower() else 1,
            0 if query_lower in p.name.lower() else 1,
            p.name
        ))
        
        return results
    
    def get_low_stock_products(self, products: Dict[str, Product], threshold: int = 10) -> List[Product]:
        """
        Get products with stock below threshold.
        
        Args:
            products: Dictionary of products
            threshold: Stock threshold
            
        Returns:
            List of low stock products
        """
        low_stock = []
        
        for product in products.values():
            if product.is_active and product.stock <= threshold:
                low_stock.append(product)
        
        # Sort by stock level (lowest first)
        low_stock.sort(key=lambda p: p.stock)
        
        return low_stock
