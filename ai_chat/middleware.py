from django.utils import timezone
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)


class CleanupOldChatsMiddleware:
    """Deletes AI chat conversations older than 7 days. Runs once per request."""

    def __init__(self, get_response):
        self.get_response = get_response
        self._last_cleanup = None
        self._cleanup_interval = timedelta(hours=1)

    def __call__(self, request):
        if self._should_cleanup():
            self._do_cleanup()
        return self.get_response(request)

    def _should_cleanup(self):
        now = timezone.now()
        if self._last_cleanup is None:
            return True
        return (now - self._last_cleanup) > self._cleanup_interval

    def _do_cleanup(self):
        try:
            from .models import Conversation
            cutoff = timezone.now() - timedelta(days=7)
            deleted, _ = Conversation.objects.filter(updated_at__lt=cutoff).delete()
            if deleted:
                logger.info(f"Cleaned up {deleted} old AI chat conversations")
            self._last_cleanup = timezone.now()
        except Exception:
            logger.exception("Failed to cleanup old AI chats")
