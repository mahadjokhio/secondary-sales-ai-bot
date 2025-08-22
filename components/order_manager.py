"""
Order Manager component for the Secondary Sales AI Bot.

This module handles complete order processing including product search,
quantity validation, price calculation, credit limit verification,
order status tracking, and invoice generation.
"""

import streamlit as st
import uuid
from datetime import datetime, date
from typing import Dict, List, Optional, Tuple, Any
from utils.data_processor import DataProcessor, Order, OrderItem, Product, Outlet
from utils.exceptions import (
    OrderProcessingError, 
    InvalidProductError, 
    InsufficientStockError, 
    CreditLimitExceededError,
    InvalidOutletError
)
from utils.validators import (
    validate_quantity, 
    validate_product_name, 
    validate_outlet_name,
    validate_credit_limit
)
from components.voice_handler import VoiceHandler


class OrderManager:
    """
    Complete order processing system with validation and error handling.
    
    Handles product search, order creation, validation, invoice generation,
    and order history management with comprehensive business rule enforcement.
    """
    
    def __init__(self, data_processor: DataProcessor, voice_handler: VoiceHandler):
        """
        Initialize order manager.
        
        Args:
            data_processor: Data processing instance
            voice_handler: Voice handling instance
        """
        self.data_processor = data_processor
        self.voice_handler = voice_handler
        self._initialize_session_state()
    
    def _initialize_session_state(self) -> None:
        """Initialize order-related session state variables."""
        if 'current_order_items' not in st.session_state:
            st.session_state.current_order_items = []
        if 'selected_outlet_id' not in st.session_state:
            st.session_state.selected_outlet_id = None
        if 'order_notes' not in st.session_state:
            st.session_state.order_notes = ""
        if 'discount_percent' not in st.session_state:
            st.session_state.discount_percent = 0.0
    
    def render(self) -> None:
        """Render the complete order management interface."""
        try:
            # Load data
            products = self.data_processor.load_products()
            outlets = self.data_processor.load_outlets()
            orders = self.data_processor.load_orders()
            
            # Main tabs
            tab1, tab2, tab3, tab4 = st.tabs([
                "📝 Create Order", 
                "📋 Order History", 
                "🔍 Search Orders",
                "📊 Order Analytics"
            ])
            
            with tab1:
                self._render_order_creation(products, outlets)
            
            with tab2:
                self._render_order_history(orders, outlets)
            
            with tab3:
                self._render_order_search(orders, products, outlets)
            
            with tab4:
                self._render_order_analytics(orders)
                
        except Exception as e:
            st.error(f"Order management error: {e}")
    
    def _render_order_creation(self, products: Dict[str, Product], outlets: Dict[str, Outlet]) -> None:
        """Render order creation interface."""
        st.subheader("📝 Create New Order")
        
        # Voice command section
        if st.session_state.get('voice_mode', False):
            self._render_voice_order_interface()
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            self._render_order_form(products, outlets)
        
        with col2:
            self._render_order_summary()
    
    def _render_voice_order_interface(self) -> None:
        """Render voice command interface for orders."""
        st.markdown("### 🎤 Voice Commands")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🎯 Voice Order", key="voice_order_btn"):
                try:
                    command = self.voice_handler.listen_for_command()
                    if command:
                        self._process_voice_order_command(command)
                except Exception as e:
                    st.error(f"Voice command error: {e}")
        
        with col2:
            st.info("Say: 'Add 10 Pepsi 500ml to order'")
        
        st.markdown("---")
    
    def _process_voice_order_command(self, command: str) -> None:
        """Process voice command for order operations."""
        is_valid, intent, data = self.voice_handler.process_voice_command(command)
        
        if is_valid and intent == "add_product":
            quantity = data.get('quantity', 1)
            product_name = data.get('product', '')
            
            try:
                self._add_product_to_order(product_name, quantity)
                self.voice_handler.speak_text(f"Added {quantity} {product_name} to order")
            except Exception as e:
                st.error(f"Failed to add product: {e}")
                self.voice_handler.speak_text("Failed to add product to order")
    
    def _render_order_form(self, products: Dict[str, Product], outlets: Dict[str, Outlet]) -> None:
        """Render order creation form."""
        # Outlet selection
        outlet_names = ["Select Outlet"] + [outlet.name for outlet in outlets.values() if outlet.is_active]
        selected_outlet_name = st.selectbox(
            "Select Outlet *",
            outlet_names,
            key="outlet_selector"
        )
        
        if selected_outlet_name != "Select Outlet":
            # Find outlet by name
            selected_outlet = None
            for outlet in outlets.values():
                if outlet.name == selected_outlet_name:
                    selected_outlet = outlet
                    st.session_state.selected_outlet_id = outlet.outlet_id
                    break
            
            if selected_outlet:
                # Display outlet info
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Credit Limit", f"Rs. {selected_outlet.credit_limit:,.0f}")
                with col2:
                    st.metric("Outstanding", f"Rs. {selected_outlet.outstanding_amount:,.0f}")
                with col3:
                    available_credit = selected_outlet.credit_limit - selected_outlet.outstanding_amount
                    st.metric("Available Credit", f"Rs. {available_credit:,.0f}")
                
                st.markdown("---")
        
        # Product selection
        self._render_product_selection(products)
        
        # Order notes and discount
        st.markdown("### Additional Information")
        col1, col2 = st.columns(2)
        
        with col1:
            st.session_state.order_notes = st.text_area(
                "Order Notes",
                value=st.session_state.order_notes,
                height=100
            )
        
        with col2:
            st.session_state.discount_percent = st.number_input(
                "Discount %",
                min_value=0.0,
                max_value=50.0,
                value=st.session_state.discount_percent,
                step=0.5
            )
    
    def _render_product_selection(self, products: Dict[str, Product]) -> None:
        """Render product selection interface."""
        st.markdown("### Add Products to Order")
        
        # Product search
        search_query = st.text_input("🔍 Search Products", placeholder="Type product name...")
        
        if search_query:
            search_results = self.data_processor.search_products(products, search_query)
            
            if search_results:
                st.write(f"Found {len(search_results)} products:")
                
                for product in search_results[:5]:  # Show top 5 results
                    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                    
                    with col1:
                        st.write(f"**{product.name}** ({product.size})")
                        st.caption(f"{product.category} - Stock: {product.stock}")
                    
                    with col2:
                        st.write(f"Rs. {product.price}")
                    
                    with col3:
                        quantity = st.number_input(
                            "Qty",
                            min_value=1,
                            max_value=min(product.stock, 1000),
                            value=1,
                            key=f"qty_{product.product_id}"
                        )
                    
                    with col4:
                        if st.button("Add", key=f"add_{product.product_id}"):
                            try:
                                self._add_product_to_order_by_id(product.product_id, quantity, products)
                                st.success(f"Added {quantity} x {product.name}")
                            except Exception as e:
                                st.error(f"Error adding product: {e}")
            else:
                st.warning("No products found matching your search.")
        
        # Category filter
        categories = list(set(p.category for p in products.values() if p.is_active))
        if categories:
            selected_category = st.selectbox("Filter by Category", ["All Categories"] + sorted(categories))
            
            if selected_category != "All Categories":
                filtered_products = [p for p in products.values() if p.category == selected_category and p.is_active]
                
                st.write(f"Products in {selected_category}:")
                for product in filtered_products[:10]:
                    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                    
                    with col1:
                        st.write(f"**{product.name}** ({product.size})")
                    
                    with col2:
                        st.write(f"Rs. {product.price}")
                    
                    with col3:
                        quantity = st.number_input(
                            "Qty",
                            min_value=1,
                            max_value=min(product.stock, 1000),
                            value=1,
                            key=f"cat_qty_{product.product_id}"
                        )
                    
                    with col4:
                        if st.button("Add", key=f"cat_add_{product.product_id}"):
                            try:
                                self._add_product_to_order_by_id(product.product_id, quantity, products)
                                st.success(f"Added {quantity} x {product.name}")
                            except Exception as e:
                                st.error(f"Error adding product: {e}")
    
    def _add_product_to_order_by_id(self, product_id: str, quantity: int, products: Dict[str, Product]) -> None:
        """Add product to order by product ID."""
        if product_id not in products:
            raise InvalidProductError(f"Product ID {product_id} not found")
        
        product = products[product_id]
        
        # Validate quantity
        validation = validate_quantity(quantity, min_qty=1, max_qty=product.stock)
        if not validation.is_valid:
            raise OrderProcessingError(validation.message)
        
        # Check stock
        if quantity > product.stock:
            raise InsufficientStockError(
                f"Insufficient stock for {product.name}. Available: {product.stock}"
            )
        
        # Create order item
        total_price = product.price * quantity
        
        order_item = {
            'product_id': product_id,
            'product_name': product.name,
            'quantity': quantity,
            'unit_price': product.price,
            'total_price': total_price,
            'size': product.size,
            'category': product.category
        }
        
        # Check if product already in order
        existing_item_index = None
        for i, item in enumerate(st.session_state.current_order_items):
            if item['product_id'] == product_id:
                existing_item_index = i
                break
        
        if existing_item_index is not None:
            # Update existing item
            st.session_state.current_order_items[existing_item_index]['quantity'] += quantity
            st.session_state.current_order_items[existing_item_index]['total_price'] += total_price
        else:
            # Add new item
            st.session_state.current_order_items.append(order_item)
    
    def _add_product_to_order(self, product_name: str, quantity: int) -> None:
        """Add product to order by name (for voice commands)."""
        products = self.data_processor.load_products()
        
        # Find product by name
        product_id = None
        for pid, product in products.items():
            if product.name.lower() == product_name.lower():
                product_id = pid
                break
        
        if not product_id:
            raise InvalidProductError(f"Product '{product_name}' not found")
        
        self._add_product_to_order_by_id(product_id, quantity, products)
    
    def _render_order_summary(self) -> None:
        """Render current order summary."""
        st.subheader("📋 Current Order")
        
        if not st.session_state.current_order_items:
            st.info("No items in order")
            return
        
        # Display order items
        total = 0
        for i, item in enumerate(st.session_state.current_order_items):
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.write(f"**{item['product_name']}** ({item['size']})")
                st.caption(f"Rs. {item['unit_price']} x {item['quantity']}")
            
            with col2:
                st.write(f"Rs. {item['total_price']:,.2f}")
            
            with col3:
                if st.button("🗑️", key=f"remove_{i}", help="Remove item"):
                    st.session_state.current_order_items.pop(i)
                    st.experimental_rerun()
            
            total += item['total_price']
        
        st.markdown("---")
        
        # Order totals
        discount_amount = total * (st.session_state.discount_percent / 100)
        tax_amount = (total - discount_amount) * 0.0  # No tax for now
        final_total = total - discount_amount + tax_amount
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Subtotal:**")
            if st.session_state.discount_percent > 0:
                st.write(f"**Discount ({st.session_state.discount_percent}%):**")
            st.write("**Total:**")
        
        with col2:
            st.write(f"Rs. {total:,.2f}")
            if st.session_state.discount_percent > 0:
                st.write(f"-Rs. {discount_amount:,.2f}")
            st.write(f"**Rs. {final_total:,.2f}**")
        
        # Action buttons
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🗑️ Clear Order", use_container_width=True):
                st.session_state.current_order_items = []
                st.experimental_rerun()
        
        with col2:
            if st.button("✅ Confirm Order", use_container_width=True, type="primary"):
                self._confirm_order(final_total)
    
    def _confirm_order(self, total_amount: float) -> None:
        """Confirm and save the current order."""
        try:
            if not st.session_state.current_order_items:
                st.error("No items in order")
                return
            
            if not st.session_state.selected_outlet_id:
                st.error("Please select an outlet")
                return
            
            # Load data
            outlets = self.data_processor.load_outlets()
            orders = self.data_processor.load_orders()
            
            outlet = outlets.get(st.session_state.selected_outlet_id)
            if not outlet:
                st.error("Selected outlet not found")
                return
            
            # Validate credit limit
            credit_validation = validate_credit_limit(
                total_amount, 
                outlet.outstanding_amount, 
                outlet.credit_limit
            )
            
            if not credit_validation.is_valid:
                st.error(credit_validation.message)
                return
            
            # Create order
            order_id = str(uuid.uuid4())
            
            # Convert session items to OrderItem objects
            order_items = []
            for item in st.session_state.current_order_items:
                order_items.append(OrderItem(
                    product_id=item['product_id'],
                    product_name=item['product_name'],
                    quantity=item['quantity'],
                    unit_price=item['unit_price'],
                    total_price=item['total_price'],
                    size=item['size'],
                    category=item['category']
                ))
            
            # Calculate totals
            subtotal = sum(item.total_price for item in order_items)
            discount_amount = subtotal * (st.session_state.discount_percent / 100)
            tax_amount = 0  # No tax for now
            
            order = Order(
                order_id=order_id,
                outlet_id=outlet.outlet_id,
                outlet_name=outlet.name,
                salesperson_id="current_user",  # TODO: Implement user management
                items=order_items,
                subtotal=subtotal,
                discount_amount=discount_amount,
                tax_amount=tax_amount,
                total_amount=total_amount,
                status="confirmed",
                created_date=datetime.now().isoformat(),
                notes=st.session_state.order_notes
            )
            
            # Save order
            orders[order_id] = order
            self.data_processor.save_orders(orders)
            
            # Update outlet outstanding amount
            outlet.outstanding_amount += total_amount
            outlet.last_order_date = date.today().isoformat()
            outlets[outlet.outlet_id] = outlet
            self.data_processor.save_outlets(outlets)
            
            # Clear current order
            st.session_state.current_order_items = []
            st.session_state.selected_outlet_id = None
            st.session_state.order_notes = ""
            st.session_state.discount_percent = 0.0
            
            st.success(f"✅ Order {order_id[:8]} confirmed successfully!")
            
            # Voice feedback
            if st.session_state.get('voice_mode', False):
                self.voice_handler.speak_text(f"Order confirmed for {outlet.name}")
            
        except Exception as e:
            st.error(f"Failed to confirm order: {e}")
    
    def _render_order_history(self, orders: Dict[str, Order], outlets: Dict[str, Outlet]) -> None:
        """Render order history interface."""
        st.subheader("📋 Order History")
        
        if not orders:
            st.info("No orders found")
            return
        
        # Filter options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            status_filter = st.selectbox(
                "Status",
                ["All", "draft", "confirmed", "delivered", "cancelled"]
            )
        
        with col2:
            outlet_filter = st.selectbox(
                "Outlet",
                ["All Outlets"] + [outlet.name for outlet in outlets.values()]
            )
        
        with col3:
            date_filter = st.date_input("From Date", value=date.today())
        
        # Filter orders
        filtered_orders = []
        for order in orders.values():
            include = True
            
            if status_filter != "All" and order.status != status_filter:
                include = False
            
            if outlet_filter != "All Outlets" and order.outlet_name != outlet_filter:
                include = False
            
            order_date = datetime.fromisoformat(order.created_date).date()
            if order_date < date_filter:
                include = False
            
            if include:
                filtered_orders.append(order)
        
        # Sort by date (newest first)
        filtered_orders.sort(key=lambda x: x.created_date, reverse=True)
        
        # Display orders
        for order in filtered_orders:
            with st.expander(f"Order {order.order_id[:8]} - {order.outlet_name} - Rs. {order.total_amount:,.2f}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Outlet:** {order.outlet_name}")
                    st.write(f"**Status:** {order.status.title()}")
                    st.write(f"**Date:** {order.created_date[:10]}")
                    if order.notes:
                        st.write(f"**Notes:** {order.notes}")
                
                with col2:
                    st.write(f"**Subtotal:** Rs. {order.subtotal:,.2f}")
                    if order.discount_amount > 0:
                        st.write(f"**Discount:** Rs. {order.discount_amount:,.2f}")
                    st.write(f"**Total:** Rs. {order.total_amount:,.2f}")
                
                # Order items
                st.write("**Items:**")
                for item in order.items:
                    st.write(f"• {item.product_name} ({item.size}) - Qty: {item.quantity} - Rs. {item.total_price:,.2f}")
    
    def _render_order_search(self, orders: Dict[str, Order], products: Dict[str, Product], outlets: Dict[str, Outlet]) -> None:
        """Render order search interface."""
        st.subheader("🔍 Search Orders")
        
        search_query = st.text_input("Search orders (order ID, outlet name, product name)")
        
        if search_query:
            matching_orders = []
            query_lower = search_query.lower()
            
            for order in orders.values():
                if (query_lower in order.order_id.lower() or
                    query_lower in order.outlet_name.lower() or
                    any(query_lower in item.product_name.lower() for item in order.items)):
                    matching_orders.append(order)
            
            if matching_orders:
                st.write(f"Found {len(matching_orders)} orders:")
                for order in matching_orders:
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.write(f"**{order.order_id[:8]}**")
                    
                    with col2:
                        st.write(order.outlet_name)
                    
                    with col3:
                        st.write(f"Rs. {order.total_amount:,.2f}")
                    
                    with col4:
                        st.write(order.created_date[:10])
            else:
                st.warning("No orders found matching your search.")
    
    def _render_order_analytics(self, orders: Dict[str, Order]) -> None:
        """Render order analytics interface."""
        st.subheader("📊 Order Analytics")
        
        if not orders:
            st.info("No order data available")
            return
        
        # Generate analytics
        analytics = self.data_processor.get_sales_analytics(orders)
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Orders", analytics['total_orders'])
        
        with col2:
            st.metric("Total Revenue", f"Rs. {analytics['total_revenue']:,.0f}")
        
        with col3:
            st.metric("Avg Order Value", f"Rs. {analytics['avg_order_value']:,.0f}")
        
        with col4:
            pending_orders = len([o for o in orders.values() if o.status == 'draft'])
            st.metric("Pending Orders", pending_orders)
        
        # Top products
        if analytics['product_sales']:
            st.subheader("🏆 Top Products")
            
            top_products = sorted(
                analytics['product_sales'].items(),
                key=lambda x: x[1]['revenue'],
                reverse=True
            )[:5]
            
            for product_name, sales_data in top_products:
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.write(f"**{product_name}**")
                
                with col2:
                    st.write(f"{sales_data['quantity']} units")
                
                with col3:
                    st.write(f"Rs. {sales_data['revenue']:,.0f}")
        
        # Top outlets
        if analytics['outlet_sales']:
            st.subheader("🏪 Top Outlets")
            
            top_outlets = sorted(
                analytics['outlet_sales'].items(),
                key=lambda x: x[1]['revenue'],
                reverse=True
            )[:5]
            
            for outlet_name, sales_data in top_outlets:
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.write(f"**{outlet_name}**")
                
                with col2:
                    st.write(f"{sales_data['orders']} orders")
                
                with col3:
                    st.write(f"Rs. {sales_data['revenue']:,.0f}")
