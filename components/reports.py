"""
Report Generator component for the Secondary Sales AI Bot.

This module handles performance reporting with interactive charts,
analytics, and export functionality.
"""

import streamlit as st
from typing import Dict, List, Any
from utils.data_processor import DataProcessor, Order


class ReportGenerator:
    """
    Performance reporting system with charts and analytics.
    
    Provides sales reports, performance metrics, and interactive
    visualizations with export capabilities.
    """
    
    def __init__(self, data_processor: DataProcessor):
        """
        Initialize report generator.
        
        Args:
            data_processor: Data processing instance
        """
        self.data_processor = data_processor
    
    def render(self) -> None:
        """Render the reports interface."""
        st.subheader("📊 Performance Reports")
        
        try:
            orders = self.data_processor.load_orders()
            
            if not orders:
                st.info("No order data available for reporting")
                return
            
            # Report tabs
            tab1, tab2, tab3, tab4 = st.tabs([
                "📈 Sales Overview", 
                "📦 Product Performance", 
                "🏪 Outlet Performance",
                "📅 Time Analysis"
            ])
            
            with tab1:
                self._render_sales_overview(orders)
            
            with tab2:
                self._render_product_performance(orders)
            
            with tab3:
                self._render_outlet_performance(orders)
            
            with tab4:
                self._render_time_analysis(orders)
                
        except Exception as e:
            st.error(f"Error generating reports: {e}")
    
    def _render_sales_overview(self, orders: Dict[str, Order]) -> None:
        """Render sales overview report."""
        st.subheader("📈 Sales Overview")
        
        # Generate analytics
        analytics = self.data_processor.get_sales_analytics(orders)
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Orders", analytics['total_orders'])
        
        with col2:
            st.metric("Total Revenue", f"Rs. {analytics['total_revenue']:,.0f}")
        
        with col3:
            st.metric("Average Order Value", f"Rs. {analytics['avg_order_value']:,.0f}")
        
        with col4:
            confirmed_orders = len([o for o in orders.values() if o.status == 'confirmed'])
            st.metric("Confirmed Orders", confirmed_orders)
        
        # Order status distribution
        st.subheader("Order Status Distribution")
        
        status_counts = {}
        for order in orders.values():
            status_counts[order.status] = status_counts.get(order.status, 0) + 1
        
        col1, col2 = st.columns(2)
        
        with col1:
            for status, count in status_counts.items():
                st.write(f"**{status.title()}:** {count}")
        
        with col2:
            # Placeholder for pie chart
            st.info("📊 Status distribution chart will be displayed here")
    
    def _render_product_performance(self, orders: Dict[str, Order]) -> None:
        """Render product performance report."""
        st.subheader("📦 Product Performance")
        
        # Calculate product sales
        product_sales = {}
        for order in orders.values():
            for item in order.items:
                if item.product_name not in product_sales:
                    product_sales[item.product_name] = {
                        "quantity": 0,
                        "revenue": 0,
                        "orders": 0
                    }
                product_sales[item.product_name]["quantity"] += item.quantity
                product_sales[item.product_name]["revenue"] += item.total_price
                product_sales[item.product_name]["orders"] += 1
        
        # Top products by revenue
        st.subheader("🏆 Top Products by Revenue")
        
        top_products = sorted(
            product_sales.items(),
            key=lambda x: x[1]["revenue"],
            reverse=True
        )[:10]
        
        for i, (product, data) in enumerate(top_products, 1):
            col1, col2, col3, col4 = st.columns([1, 3, 1, 2])
            
            with col1:
                st.write(f"#{i}")
            
            with col2:
                st.write(f"**{product}**")
            
            with col3:
                st.write(f"{data['quantity']} units")
            
            with col4:
                st.write(f"Rs. {data['revenue']:,.0f}")
        
        # Product category performance
        st.subheader("📊 Category Performance")
        
        category_sales = {}
        for order in orders.values():
            for item in order.items:
                category = item.category or "Uncategorized"
                if category not in category_sales:
                    category_sales[category] = 0
                category_sales[category] += item.total_price
        
        for category, revenue in sorted(category_sales.items(), key=lambda x: x[1], reverse=True):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write(f"**{category}**")
            
            with col2:
                st.write(f"Rs. {revenue:,.0f}")
    
    def _render_outlet_performance(self, orders: Dict[str, Order]) -> None:
        """Render outlet performance report."""
        st.subheader("🏪 Outlet Performance")
        
        # Calculate outlet performance
        outlet_performance = {}
        for order in orders.values():
            outlet_name = order.outlet_name
            if outlet_name not in outlet_performance:
                outlet_performance[outlet_name] = {
                    "orders": 0,
                    "revenue": 0,
                    "avg_order_value": 0
                }
            outlet_performance[outlet_name]["orders"] += 1
            outlet_performance[outlet_name]["revenue"] += order.total_amount
        
        # Calculate average order values
        for outlet_data in outlet_performance.values():
            outlet_data["avg_order_value"] = (
                outlet_data["revenue"] / outlet_data["orders"] 
                if outlet_data["orders"] > 0 else 0
            )
        
        # Top outlets by revenue
        st.subheader("🏆 Top Outlets by Revenue")
        
        top_outlets = sorted(
            outlet_performance.items(),
            key=lambda x: x[1]["revenue"],
            reverse=True
        )[:10]
        
        for i, (outlet, data) in enumerate(top_outlets, 1):
            col1, col2, col3, col4, col5 = st.columns([1, 3, 1, 2, 2])
            
            with col1:
                st.write(f"#{i}")
            
            with col2:
                st.write(f"**{outlet}**")
            
            with col3:
                st.write(f"{data['orders']}")
            
            with col4:
                st.write(f"Rs. {data['revenue']:,.0f}")
            
            with col5:
                st.write(f"Rs. {data['avg_order_value']:,.0f}")
    
    def _render_time_analysis(self, orders: Dict[str, Order]) -> None:
        """Render time-based analysis report."""
        st.subheader("📅 Time Analysis")
        
        # Date range selector
        col1, col2 = st.columns(2)
        
        with col1:
            from datetime import date, timedelta
            start_date = st.date_input(
                "From Date",
                value=date.today() - timedelta(days=30)
            )
        
        with col2:
            end_date = st.date_input(
                "To Date",
                value=date.today()
            )
        
        # Filter orders by date range
        date_range = (start_date.isoformat(), end_date.isoformat())
        analytics = self.data_processor.get_sales_analytics(orders, date_range)
        
        # Display metrics for selected period
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Orders in Period", analytics['total_orders'])
        
        with col2:
            st.metric("Revenue in Period", f"Rs. {analytics['total_revenue']:,.0f}")
        
        with col3:
            st.metric("Avg Order Value", f"Rs. {analytics['avg_order_value']:,.0f}")
        
        # Daily sales trend (placeholder)
        st.subheader("📈 Daily Sales Trend")
        st.info("📊 Daily sales trend chart will be displayed here")
        
        # Export functionality
        st.subheader("💾 Export Reports")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📄 Export PDF", use_container_width=True):
                st.info("PDF export functionality coming soon")
        
        with col2:
            if st.button("📊 Export Excel", use_container_width=True):
                st.info("Excel export functionality coming soon")
        
        with col3:
            if st.button("📧 Email Report", use_container_width=True):
                st.info("Email report functionality coming soon")
