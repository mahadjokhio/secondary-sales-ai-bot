"""
Secondary Sales AI Bot - Main Application Entry Point

A comprehensive Streamlit application for secondary sales management
with voice recognition, AI chat, and complete order processing capabilities.
"""

import streamlit as st
import sys
import os
from pathlib import Path

# Add project root to Python path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from streamlit_option_menu import option_menu
    OPTION_MENU_AVAILABLE = True
except ImportError:
    OPTION_MENU_AVAILABLE = False
    st.warning("streamlit-option-menu not available. Using basic navigation.")

try:
    from config.settings import get_settings, ConfigError
    from utils.exceptions import BotException
    from components.voice_handler import VoiceHandler
    from components.order_manager import OrderManager
    from components.chat_interface import ChatInterface
    from components.promotions import PromotionManager
    from components.outlets import OutletManager
    from components.reports import ReportGenerator
    from utils.data_processor import DataProcessor
except ImportError as e:
    st.error(f"Import error: {e}")
    st.error("Please ensure all dependencies are installed: pip install -r requirements.txt")
    st.stop()


class SalesBot:
    """Main application class for the Secondary Sales AI Bot."""
    
    def __init__(self):
        """Initialize the application with error handling."""
        try:
            self.settings = get_settings()
            self.data_processor = DataProcessor()
            self.voice_handler = VoiceHandler()
            self._initialize_session_state()
            self._configure_page()
        except ConfigError as e:
            st.error(f"Configuration error: {e}")
            st.stop()
        except Exception as e:
            st.error(f"Initialization error: {e}")
            st.stop()
    
    def _initialize_session_state(self) -> None:
        """Initialize Streamlit session state variables."""
        default_states = {
            'chat_history': [],
            'current_order': [],
            'voice_mode': False,
            'selected_outlet': None,
            'order_total': 0.0,
            'user_authenticated': True,  # Simplified for demo
            'current_page': 'Dashboard'
        }
        
        for key, value in default_states.items():
            if key not in st.session_state:
                st.session_state[key] = value
    
    def _configure_page(self) -> None:
        """Configure Streamlit page settings."""
        st.set_page_config(
            page_title=self.settings.APP_TITLE,
            page_icon="🤖",
            layout="wide",
            initial_sidebar_state="expanded",
            menu_items={
                'Get Help': 'https://github.com/your-repo/sales-bot',
                'Report a bug': 'https://github.com/your-repo/sales-bot/issues',
                'About': f"{self.settings.APP_TITLE} - AI-powered sales assistant"
            }
        )
    
    def render_sidebar(self) -> str:
        """
        Render sidebar navigation.
        
        Returns:
            Selected page name
        """
        with st.sidebar:
            st.title("🤖 Sales Bot")
            st.markdown("---")
            
            # Navigation menu
            if OPTION_MENU_AVAILABLE:
                selected = option_menu(
                    menu_title="Navigation",
                    options=[
                        "Dashboard", 
                        "Orders", 
                        "Promotions", 
                        "Outlets", 
                        "Reports", 
                        "AI Chat"
                    ],
                    icons=[
                        "speedometer2", 
                        "cart-plus", 
                        "gift", 
                        "shop", 
                        "bar-chart", 
                        "robot"
                    ],
                    menu_icon="cast",
                    default_index=0,
                    styles={
                        "container": {"padding": "5!important", "background-color": "#fafafa"},
                        "icon": {"color": "orange", "font-size": "25px"}, 
                        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
                        "nav-link-selected": {"background-color": "#02ab21"},
                    }
                )
            else:
                # Fallback to radio buttons
                selected = st.radio(
                    "Navigation",
                    [
                        "Dashboard", 
                        "Orders", 
                        "Promotions", 
                        "Outlets", 
                        "Reports", 
                        "AI Chat"
                    ]
                )
            
            st.markdown("---")
            
            # Voice mode toggle
            voice_mode = st.toggle(
                "🎤 Voice Mode", 
                value=st.session_state.voice_mode,
                help="Enable voice commands and audio responses"
            )
            st.session_state.voice_mode = voice_mode
            
            if voice_mode:
                st.success("Voice mode is active")
            
            # System status
            st.markdown("### System Status")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Status", "🟢 Online")
            with col2:
                st.metric("Mode", "🔊 Voice" if voice_mode else "⌨️ Text")
            
            # Quick stats
            st.markdown("### Quick Stats")
            try:
                orders = self.data_processor.load_orders()
                products = self.data_processor.load_products()
                
                st.metric("Today's Orders", len(orders))
                st.metric("Products", len(products))
                st.metric("Low Stock", len(self.data_processor.get_low_stock_products(products)))
            except Exception:
                st.warning("Unable to load stats")
        
        return selected
    
    def render_header(self, page_name: str) -> None:
        """
        Render page header with title and breadcrumb.
        
        Args:
            page_name: Current page name
        """
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            st.title(f"📊 {page_name}")
        
        with col2:
            if st.session_state.voice_mode:
                if st.button("🎤 Voice Command", key="voice_btn"):
                    self._handle_voice_command()
        
        with col3:
            st.markdown(f"**User:** Sales Rep")
        
        st.markdown("---")
    
    def _handle_voice_command(self) -> None:
        """Handle voice command input."""
        try:
            with st.spinner("Listening..."):
                command = self.voice_handler.listen_for_command()
                
            if command:
                st.session_state.last_voice_command = command
                st.success(f"Voice command: {command}")
                # Process the command based on current page
                self._process_voice_command(command)
            else:
                st.warning("No voice command detected")
                
        except Exception as e:
            st.error(f"Voice command error: {e}")
    
    def _process_voice_command(self, command: str) -> None:
        """
        Process voice command based on context.
        
        Args:
            command: Voice command text
        """
        # This would integrate with the voice handler's command processing
        # For now, just display the command
        st.info(f"Processing command: {command}")
    
    def render_dashboard(self) -> None:
        """Render the dashboard page."""
        try:
            # KPI Metrics
            col1, col2, col3, col4 = st.columns(4)
            
            orders = self.data_processor.load_orders()
            products = self.data_processor.load_products()
            outlets = self.data_processor.load_outlets()
            
            with col1:
                st.metric("Today's Orders", len(orders), "↑ 12%")
            with col2:
                total_revenue = sum(order.total_amount for order in orders.values())
                st.metric("Total Revenue", f"Rs. {total_revenue:,.0f}", "↑ 8%")
            with col3:
                active_products = len([p for p in products.values() if p.is_active])
                st.metric("Active Products", active_products, "→ 0%")
            with col4:
                active_outlets = len([o for o in outlets.values() if o.is_active])
                st.metric("Active Outlets", active_outlets, "↑ 5%")
            
            st.markdown("---")
            
            # Recent activity and charts
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.subheader("📈 Sales Trends")
                # Placeholder for sales chart
                st.info("Sales trend chart will be displayed here")
            
            with col2:
                st.subheader("⚠️ Alerts")
                low_stock = self.data_processor.get_low_stock_products(products)
                if low_stock:
                    st.warning(f"{len(low_stock)} products have low stock")
                    for product in low_stock[:3]:
                        st.write(f"• {product.name}: {product.stock} units")
                else:
                    st.success("All products well stocked")
                    
        except Exception as e:
            st.error(f"Dashboard error: {e}")
    
    def render_orders(self) -> None:
        """Render the orders page."""
        try:
            order_manager = OrderManager(self.data_processor, self.voice_handler)
            order_manager.render()
        except Exception as e:
            st.error(f"Order management error: {e}")
    
    def render_promotions(self) -> None:
        """Render the promotions page."""
        try:
            promotion_manager = PromotionManager(self.data_processor)
            promotion_manager.render()
        except Exception as e:
            st.error(f"Promotions error: {e}")
    
    def render_outlets(self) -> None:
        """Render the outlets page."""
        try:
            outlet_manager = OutletManager(self.data_processor)
            outlet_manager.render()
        except Exception as e:
            st.error(f"Outlet management error: {e}")
    
    def render_reports(self) -> None:
        """Render the reports page."""
        try:
            report_generator = ReportGenerator(self.data_processor)
            report_generator.render()
        except Exception as e:
            st.error(f"Reports error: {e}")
    
    def render_ai_chat(self) -> None:
        """Render the AI chat page."""
        try:
            chat_interface = ChatInterface(
                self.data_processor, 
                self.voice_handler
            )
            chat_interface.render()
        except Exception as e:
            st.error(f"AI Chat error: {e}")
    
    def run(self) -> None:
        """Run the main application."""
        try:
            # Render sidebar and get selected page
            selected_page = self.render_sidebar()
            
            # Render header
            self.render_header(selected_page)
            
            # Render selected page
            page_renderers = {
                "Dashboard": self.render_dashboard,
                "Orders": self.render_orders,
                "Promotions": self.render_promotions,
                "Outlets": self.render_outlets,
                "Reports": self.render_reports,
                "AI Chat": self.render_ai_chat
            }
            
            renderer = page_renderers.get(selected_page)
            if renderer:
                renderer()
            else:
                st.error(f"Unknown page: {selected_page}")
                
        except Exception as e:
            st.error(f"Application error: {e}")
            if self.settings.DEBUG_MODE:
                st.exception(e)


def main() -> None:
    """Main entry point of the application."""
    try:
        # Initialize and run the application
        app = SalesBot()
        app.run()
        
    except Exception as e:
        st.error(f"Fatal error: {e}")
        st.error("Please check your configuration and try again.")


if __name__ == "__main__":
    main()
