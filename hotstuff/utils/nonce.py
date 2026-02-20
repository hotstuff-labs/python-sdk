"""Nonce management utility."""
import time


class NonceManager:
    """Manages nonces for transactions."""
    
    def __init__(self):
        """Initialize the nonce manager."""
        self._last_nonce = 0
    
    def get_nonce(self) -> int:
        """
        Get a new nonce.
        
        Returns:
            int: A new nonce value
        """
        current_time = int(time.time() * 1000)
        if current_time <= self._last_nonce:
            self._last_nonce += 1
        else:
            self._last_nonce = current_time
        return self._last_nonce
