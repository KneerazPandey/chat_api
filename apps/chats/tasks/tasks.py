# apps/chats/tasks.py
from celery import shared_task
from django.contrib.auth import get_user_model
from apps.chats.models import Message

User = get_user_model()

@shared_task
def mark_message_as_read_in_db(message_id, user_id):
    try:
        
        print(f"✅ Database updated: Message {message_id} marked read by User {user_id}")
    except Exception as e:
        print(f"❌ Failed to write read-receipt to DB: {e}")