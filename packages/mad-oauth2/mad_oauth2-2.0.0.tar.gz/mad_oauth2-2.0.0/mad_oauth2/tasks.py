from celery import shared_task
from oauth2_provider.models import get_access_token_model
from django.utils import timezone
import logging
logger = logging.getLogger(__name__)

@shared_task(name="Periodic: Remove Expired Tokens")
def removeExpiredTokens():
    try:
        get_access_token_model().objects.filter(expires__lt=timezone.now()).delete()
        return "Expired token clean up completed successfully."
    except Exception as e:
        logger.error("Error deleting Expired Tokens: " + str(e))
        return "Error: " + str(e)
