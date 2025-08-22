"""
Chat Interface component for the Secondary Sales AI Bot.

This module handles AI chat functionality with memory, context awareness,
and integration with Google Gemini for natural language processing.
"""

import streamlit as st
from typing import List, Dict, Any, Optional
from utils.data_processor import DataProcessor
from components.voice_handler import VoiceHandler


class ChatInterface:
    """
    AI chat interface with memory and context awareness.
    
    Provides natural language conversation capabilities with sales-specific
    context and the ability to execute actions through conversation.
    """
    
    def __init__(self, data_processor: DataProcessor, voice_handler: VoiceHandler):
        """
        Initialize chat interface.
        
        Args:
            data_processor: Data processing instance
            voice_handler: Voice handling instance
        """
        self.data_processor = data_processor
        self.voice_handler = voice_handler
        self._initialize_session_state()
    
    def _initialize_session_state(self) -> None:
        """Initialize chat-related session state variables."""
        if 'chat_messages' not in st.session_state:
            st.session_state.chat_messages = []
        if 'chat_context' not in st.session_state:
            st.session_state.chat_context = {}
    
    def render(self) -> None:
        """Render the chat interface."""
        st.subheader("🤖 AI Sales Assistant")
        
        # Chat history
        chat_container = st.container()
        
        with chat_container:
            for message in st.session_state.chat_messages:
                if message["role"] == "user":
                    st.chat_message("user").write(message["content"])
                else:
                    st.chat_message("assistant").write(message["content"])
        
        # Input area
        col1, col2 = st.columns([4, 1])
        
        with col1:
            user_input = st.chat_input("Ask me about products, orders, outlets, or company information...")
        
        with col2:
            if st.session_state.get('voice_mode', False):
                if st.button("🎤 Voice", use_container_width=True):
                    try:
                        voice_input = self.voice_handler.listen_for_command()
                        if voice_input:
                            user_input = voice_input
                    except Exception as e:
                        st.error(f"Voice input error: {e}")
        
        # Process input
        if user_input:
            self._process_chat_message(user_input)
    
    def _process_chat_message(self, user_input: str) -> None:
        """Process user chat message and generate response."""
        # Add user message
        st.session_state.chat_messages.append({
            "role": "user",
            "content": user_input
        })
        
        # Generate response (placeholder for now)
        response = self._generate_response(user_input)
        
        # Add assistant response
        st.session_state.chat_messages.append({
            "role": "assistant",
            "content": response
        })
        
        # Voice response if enabled
        if st.session_state.get('voice_mode', False):
            self.voice_handler.speak_text(response)
        
        st.rerun()
    
    def _generate_response(self, user_input: str) -> str:
        """
        Generate AI response to user input.
        
        Args:
            user_input: User's message
            
        Returns:
            AI-generated response
        """
        # Placeholder implementation
        # In production, this would integrate with Google Gemini
        
        user_input_lower = user_input.lower()
        
        if "price" in user_input_lower:
            return "I can help you with product pricing. Which product would you like to know about?"
        elif "order" in user_input_lower:
            return "I can assist with order management. Would you like to create a new order or check existing orders?"
        elif "promotion" in user_input_lower:
            return "Let me show you the current promotions available."
        elif "outlet" in user_input_lower:
            return "I can provide outlet information. Which outlet are you interested in?"
        else:
            return f"I understand you're asking about: {user_input}. How can I help you with sales-related tasks?"
