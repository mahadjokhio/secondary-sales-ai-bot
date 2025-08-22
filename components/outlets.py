"""
Outlet Manager component for the Secondary Sales AI Bot.

This module handles outlet information display, analytics,
and outlet performance tracking.
"""

import streamlit as st
from typing import Dict, List, Any
from utils.data_processor import DataProcessor, Outlet


class OutletManager:
    """
    Outlet information and analytics management system.
    
    Provides outlet search, information display, performance
    metrics, and outlet management functionality.
    """
    
    def __init__(self, data_processor: DataProcessor):
        """
        Initialize outlet manager.
        
        Args:
            data_processor: Data processing instance
        """
        self.data_processor = data_processor
    
    def render(self) -> None:
        """Render the outlet management interface."""
        st.subheader("🏪 Outlet Management")
        
        try:
            outlets = self.data_processor.load_outlets()
            
            if not outlets:
                st.info("No outlets found")
                return
            
            # Tabs for different outlet views
            tab1, tab2, tab3 = st.tabs(["📋 Outlet List", "📊 Analytics", "🔍 Search"])
            
            with tab1:
                self._render_outlet_list(outlets)
            
            with tab2:
                self._render_outlet_analytics(outlets)
            
            with tab3:
                self._render_outlet_search(outlets)
                
        except Exception as e:
            st.error(f"Error loading outlets: {e}")
    
    def _render_outlet_list(self, outlets: Dict[str, Outlet]) -> None:
        """Render list of all outlets."""
        st.subheader("📋 All Outlets")
        
        for outlet in outlets.values():
            if outlet.is_active:
                with st.expander(f"🏪 {outlet.name} - {outlet.location}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Contact Person:** {outlet.contact_person}")
                        st.write(f"**Phone:** {outlet.phone}")
                        st.write(f"**Email:** {outlet.email}")
                        st.write(f"**Location:** {outlet.location}")
                    
                    with col2:
                        st.metric("Credit Limit", f"Rs. {outlet.credit_limit:,.0f}")
                        st.metric("Outstanding", f"Rs. {outlet.outstanding_amount:,.0f}")
                        
                        available_credit = outlet.credit_limit - outlet.outstanding_amount
                        st.metric("Available Credit", f"Rs. {available_credit:,.0f}")
                        
                        if outlet.last_order_date:
                            st.write(f"**Last Order:** {outlet.last_order_date}")
    
    def _render_outlet_analytics(self, outlets: Dict[str, Outlet]) -> None:
        """Render outlet analytics."""
        st.subheader("📊 Outlet Analytics")
        
        # Summary metrics
        total_outlets = len([o for o in outlets.values() if o.is_active])
        total_credit_limit = sum(o.credit_limit for o in outlets.values() if o.is_active)
        total_outstanding = sum(o.outstanding_amount for o in outlets.values() if o.is_active)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Active Outlets", total_outlets)
        
        with col2:
            st.metric("Total Credit Limit", f"Rs. {total_credit_limit:,.0f}")
        
        with col3:
            st.metric("Total Outstanding", f"Rs. {total_outstanding:,.0f}")
        
        with col4:
            credit_utilization = (total_outstanding / total_credit_limit * 100) if total_credit_limit > 0 else 0
            st.metric("Credit Utilization", f"{credit_utilization:.1f}%")
        
        # Top outlets by credit usage
        st.subheader("🏆 Top Outlets by Credit Usage")
        
        outlet_list = [(outlet.name, outlet.outstanding_amount, outlet.credit_limit) 
                      for outlet in outlets.values() if outlet.is_active]
        outlet_list.sort(key=lambda x: x[1], reverse=True)
        
        for name, outstanding, credit_limit in outlet_list[:5]:
            usage_percent = (outstanding / credit_limit * 100) if credit_limit > 0 else 0
            
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.write(f"**{name}**")
            
            with col2:
                st.write(f"Rs. {outstanding:,.0f}")
            
            with col3:
                st.write(f"{usage_percent:.1f}%")
    
    def _render_outlet_search(self, outlets: Dict[str, Outlet]) -> None:
        """Render outlet search interface."""
        st.subheader("🔍 Search Outlets")
        
        search_query = st.text_input("Search by outlet name, location, or contact person")
        
        if search_query:
            query_lower = search_query.lower()
            matching_outlets = []
            
            for outlet in outlets.values():
                if (query_lower in outlet.name.lower() or
                    query_lower in outlet.location.lower() or
                    query_lower in outlet.contact_person.lower()):
                    matching_outlets.append(outlet)
            
            if matching_outlets:
                st.write(f"Found {len(matching_outlets)} outlets:")
                
                for outlet in matching_outlets:
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.write(f"**{outlet.name}**")
                    
                    with col2:
                        st.write(outlet.location)
                    
                    with col3:
                        st.write(outlet.contact_person)
                    
                    with col4:
                        st.write(f"Rs. {outlet.outstanding_amount:,.0f}")
            else:
                st.warning("No outlets found matching your search.")
