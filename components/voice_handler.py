"""
Voice Handler component for the Secondary Sales AI Bot.

This module handles speech recognition, text-to-speech, voice command processing,
and audio quality validation with comprehensive error handling.
"""

import streamlit as st
import threading
from typing import Optional, Dict, Any, Tuple
from utils.exceptions import (
    VoiceProcessingError, 
    AudioProcessingError, 
    SpeechRecognitionError, 
    TextToSpeechError
)
from utils.validators import validate_voice_command
from config.settings import get_settings

try:
    import speech_recognition as sr
    import pyttsx3
    from streamlit_mic_recorder import mic_recorder
    VOICE_DEPENDENCIES_AVAILABLE = True
except ImportError:
    VOICE_DEPENDENCIES_AVAILABLE = False


class VoiceHandler:
    """
    Handles voice input/output with error recovery and quality validation.
    
    Provides speech-to-text, text-to-speech, voice command processing,
    and microphone availability checking with comprehensive error handling.
    """
    
    def __init__(self):
        """Initialize voice handler with configuration."""
        self.settings = get_settings()
        self.recognizer = None
        self.microphone = None
        self.tts_engine = None
        self.is_available = False
        
        if VOICE_DEPENDENCIES_AVAILABLE:
            self._initialize_voice_components()
        else:
            st.warning("Voice dependencies not available. Install with: pip install speechrecognition pyttsx3 pyaudio streamlit-mic-recorder")
    
    def _initialize_voice_components(self) -> None:
        """Initialize speech recognition and TTS components."""
        try:
            # Initialize speech recognition
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            
            # Initialize text-to-speech
            self.tts_engine = pyttsx3.init()
            self.tts_engine.setProperty('rate', self.settings.TTS_RATE)
            
            # Set voice gender if available
            voices = self.tts_engine.getProperty('voices')
            if voices:
                voice_id = 0 if self.settings.TTS_VOICE.lower() == 'male' else 1
                if len(voices) > voice_id:
                    self.tts_engine.setProperty('voice', voices[voice_id].id)
            
            self.is_available = True
            
        except Exception as e:
            st.warning(f"Voice initialization failed: {e}")
            self.is_available = False
    
    def check_microphone_availability(self) -> bool:
        """
        Check if microphone is available and accessible.
        
        Returns:
            True if microphone is available, False otherwise
        """
        if not self.is_available:
            return False
        
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            return True
        except Exception as e:
            st.error(f"Microphone not available: {e}")
            return False
    
    def listen_for_command(self, timeout: int = 5, phrase_time_limit: int = 10) -> Optional[str]:
        """
        Listen for voice command with timeout and error handling.
        
        Args:
            timeout: Seconds to wait for speech to start
            phrase_time_limit: Maximum seconds for phrase
            
        Returns:
            Recognized text or None if failed
            
        Raises:
            SpeechRecognitionError: If speech recognition fails
        """
        if not self.is_available:
            raise VoiceProcessingError("Voice processing not available")
        
        try:
            with self.microphone as source:
                st.info("🎤 Listening... Speak now!")
                
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                
                # Listen for audio
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout, 
                    phrase_time_limit=phrase_time_limit
                )
                
                st.info("🔄 Processing speech...")
                
                # Recognize speech using Google
                text = self.recognizer.recognize_google(
                    audio, 
                    language=self.settings.VOICE_LANGUAGE
                )
                
                return text.strip()
                
        except sr.WaitTimeoutError:
            raise SpeechRecognitionError("No speech detected within timeout period")
        except sr.UnknownValueError:
            raise SpeechRecognitionError("Could not understand the audio")
        except sr.RequestError as e:
            raise SpeechRecognitionError(f"Speech recognition service error: {e}")
        except Exception as e:
            raise VoiceProcessingError(f"Unexpected voice processing error: {e}")
    
    def speak_text(self, text: str, blocking: bool = False) -> None:
        """
        Convert text to speech with threading support.
        
        Args:
            text: Text to speak
            blocking: Whether to block until speech is complete
            
        Raises:
            TextToSpeechError: If TTS fails
        """
        if not self.is_available or not text:
            return
        
        def _speak():
            try:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            except Exception as e:
                st.error(f"Text-to-speech error: {e}")
        
        if blocking:
            _speak()
        else:
            thread = threading.Thread(target=_speak, daemon=True)
            thread.start()
    
    def process_voice_command(self, command: str) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Process and validate voice command.
        
        Args:
            command: Voice command text
            
        Returns:
            Tuple of (is_valid, intent, extracted_data)
        """
        try:
            is_valid, intent, data = validate_voice_command(command)
            
            if is_valid:
                # Log successful command processing
                st.success(f"✅ Command recognized: {intent}")
                
                # Provide audio feedback
                if intent == "create_order":
                    feedback = f"Creating order for {data.get('outlet', 'selected outlet')}"
                elif intent == "add_product":
                    feedback = f"Adding {data.get('quantity', 0)} {data.get('product', 'items')} to order"
                elif intent == "price_query":
                    feedback = "Looking up price information"
                elif intent == "show_promotions":
                    feedback = "Displaying current promotions"
                else:
                    feedback = "Processing your request"
                
                self.speak_text(feedback)
                
            else:
                st.warning(f"⚠️ Command not recognized: {command}")
                self.speak_text("I didn't understand that command. Please try again.")
            
            return is_valid, intent, data
            
        except Exception as e:
            st.error(f"Command processing error: {e}")
            return False, "error", {"error": str(e)}
    
    def render_voice_input_widget(self) -> Optional[str]:
        """
        Render voice input widget in Streamlit.
        
        Returns:
            Recognized voice command or None
        """
        if not VOICE_DEPENDENCIES_AVAILABLE:
            st.warning("Voice input not available. Please install voice dependencies.")
            return None
        
        if not self.is_available:
            st.error("Voice system not initialized")
            return None
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            # Voice input button
            if st.button("🎤 Start Voice Command", key="voice_input_btn", use_container_width=True):
                try:
                    with st.spinner("🎤 Listening for command..."):
                        command = self.listen_for_command()
                    
                    if command:
                        st.success(f"🎯 Voice Command: {command}")
                        return command
                    else:
                        st.warning("No voice command detected")
                        
                except SpeechRecognitionError as e:
                    st.error(f"Speech recognition error: {e}")
                except VoiceProcessingError as e:
                    st.error(f"Voice processing error: {e}")
                except Exception as e:
                    st.error(f"Unexpected error: {e}")
        
        return None
    
    def render_mic_recorder_widget(self) -> Optional[str]:
        """
        Render microphone recorder widget using streamlit-mic-recorder.
        
        Returns:
            Recognized text from recorded audio or None
        """
        if not VOICE_DEPENDENCIES_AVAILABLE:
            return None
        
        try:
            # Use streamlit-mic-recorder for better audio capture
            audio_data = mic_recorder(
                start_prompt="🎤 Click to start recording",
                stop_prompt="⏹️ Click to stop recording",
                just_once=True,
                use_container_width=True,
                callback=None,
                args=(),
                kwargs={},
                key="voice_recorder"
            )
            
            if audio_data:
                try:
                    # Convert audio data to text
                    with st.spinner("🔄 Converting speech to text..."):
                        # Note: This is a simplified implementation
                        # In production, you'd convert the audio_data['bytes'] to the format
                        # expected by speech_recognition
                        text = "Voice command from recording"  # Placeholder
                        
                    return text
                    
                except Exception as e:
                    st.error(f"Audio processing error: {e}")
                    return None
            
        except Exception as e:
            st.error(f"Microphone recorder error: {e}")
            return None
        
        return None
    
    def get_voice_status(self) -> Dict[str, Any]:
        """
        Get current voice system status.
        
        Returns:
            Dictionary containing voice system status information
        """
        return {
            "dependencies_available": VOICE_DEPENDENCIES_AVAILABLE,
            "system_available": self.is_available,
            "microphone_available": self.check_microphone_availability() if self.is_available else False,
            "language": self.settings.VOICE_LANGUAGE,
            "tts_rate": self.settings.TTS_RATE,
            "tts_voice": self.settings.TTS_VOICE
        }
    
    def render_voice_status_widget(self) -> None:
        """Render voice system status widget."""
        status = self.get_voice_status()
        
        st.subheader("🔊 Voice System Status")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if status["dependencies_available"]:
                st.success("✅ Dependencies installed")
            else:
                st.error("❌ Dependencies missing")
            
            if status["system_available"]:
                st.success("✅ System initialized")
            else:
                st.error("❌ System not initialized")
        
        with col2:
            if status["microphone_available"]:
                st.success("✅ Microphone available")
            else:
                st.warning("⚠️ Microphone not available")
            
            st.info(f"Language: {status['language']}")
        
        # Voice settings
        with st.expander("Voice Settings"):
            st.write(f"**TTS Rate:** {status['tts_rate']} words/min")
            st.write(f"**TTS Voice:** {status['tts_voice']}")
            st.write(f"**Recognition Language:** {status['language']}")
    
    def test_voice_system(self) -> bool:
        """
        Test voice system functionality.
        
        Returns:
            True if all tests pass, False otherwise
        """
        if not self.is_available:
            return False
        
        try:
            # Test TTS
            self.speak_text("Voice system test", blocking=True)
            
            # Test microphone availability
            mic_available = self.check_microphone_availability()
            
            return mic_available
            
        except Exception:
            return False
