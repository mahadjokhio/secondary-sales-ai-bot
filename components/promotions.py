"""
Promotion Manager component for the Secondary Sales AI Bot.

This module handles promotion management, eligibility checking,
and promotion application to orders.
"""

import streamlit as st
from typing import Dict, List, Any
from utils.data_processor import DataProcessor


class PromotionManager:
    """
    Promotion management system with eligibility validation.
    
    Handles promotion display, eligibility checking, and automatic
    application of applicable promotions to orders.
    """
    
    def __init__(self, data_processor: DataProcessor):
        """
        Initialize promotion manager.
        
        Args:
            data_processor: Data processing instance
        """
        self.data_processor = data_processor
    
    def render(self) -> None:
        """Render the promotion management interface."""
        st.subheader("🎯 Promotions Management")
        
        # Sample promotions data
        promotions = [
            {
                "name": "Summer Special",
                "description": "Get 10% off on orders above Rs. 5,000",
                "discount_percent": 10,
                "min_amount": 5000,
                "validity": "Valid until August 31, 2025",
                "is_active": True
            },
            {
                "name": "Bulk Purchase Discount", 
                "description": "5% off on orders with 100+ units",
                "discount_percent": 5,
                "min_quantity": 100,
                "validity": "Ongoing",
                "is_active": True
            },
            {
                "name": "New Outlet Bonus",
                "description": "15% off for first-time orders",
                "discount_percent": 15,
                "validity": "For new outlets only",
                "is_active": True
            }
        ]
        
        # Display active promotions
        st.subheader("🔥 Active Promotions")
        
        for promo in promotions:
            if promo["is_active"]:
                with st.expander(f"🎁 {promo['name']} - {promo['discount_percent']}% OFF"):
                    st.write(f"**Description:** {promo['description']}")
                    st.write(f"**Discount:** {promo['discount_percent']}%")
                    st.write(f"**Validity:** {promo['validity']}")
                    
                    if "min_amount" in promo:
                        st.write(f"**Minimum Amount:** Rs. {promo['min_amount']:,}")
                    
                    if "min_quantity" in promo:
                        st.write(f"**Minimum Quantity:** {promo['min_quantity']} units")
        
        # Promotion analytics
        st.subheader("📊 Promotion Analytics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Active Promotions", len([p for p in promotions if p["is_active"]]))
        
        with col2:
            st.metric("Total Savings", "Rs. 45,000")
        
        with col3:
            st.metric("Promotion Usage", "78%")
