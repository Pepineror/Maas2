from agno.tools import Toolkit
from typing import Optional, Dict, Any
import httpx
import logging
from backend.core.config import settings

logger = logging.getLogger(__name__)

class OpenWebUITools(Toolkit):
    """
    Tools to interact with OpenWebUI API.
    Enables agents to send notifications or update chat state.
    """
    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        super().__init__(name="openwebui_tools")
        self.base_url = base_url or settings.OPENWEBUI_BASE_URL
        self.api_key = api_key or settings.OPENWEBUI_API_KEY
        self.register(self.send_notification)

    def send_notification(self, user_id: str, message: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Sends a notification or message to a user in OpenWebUI.
        
        Args:
            user_id: The OpenWebUI user ID.
            message: The message text to send.
            metadata: Optional additional data.
            
        Returns:
            Status message.
        """
        if not self.base_url:
            return "Error: OpenWebUI base URL not configured."

        url = f"{self.base_url}/api/v1/notifications" # Hypothetical endpoint, adjust to actual OpenWebUI API
        headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
        
        payload = {
            "user_id": user_id,
            "message": message,
            "metadata": metadata or {}
        }
        
        try:
            # We use an async client but here it's called from a sync tool context if not using async agents
            with httpx.Client() as client:
                response = client.post(url, json=payload, headers=headers, timeout=10)
                response.raise_for_status()
                return "Notification sent successfully."
        except Exception as e:
            logger.error(f"Failed to send OpenWebUI notification: {e}")
            return f"Error sending notification: {str(e)}"
