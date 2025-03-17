from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json

class ActiveNowConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("active_users", self.channel_name)
        await self.accept()
        await self.send_active_users()  # Send initial data on connect

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("active_users", self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')
        if action in ['start_timer', 'stop_timer']:
            await self.send_active_users()  # Update all clients on timer events

    @database_sync_to_async
    def get_active_users(self):
        from django.db.models import Sum
        from datetime import date
        from django.utils import timezone
        from .models import TrackedTimeDB, myUserDB, Course, Topic

        today = date.today()
        active_timers = TrackedTimeDB.objects.filter(endTime__isnull=True).select_related('user', 'course', 'topic')
        active_users_data = {}
        for timer in active_timers:
            user = timer.user
            total_duration = TrackedTimeDB.objects.filter(
                user=user,
                startTime__date=today
            ).aggregate(total=Sum('duration'))['total'] or 0
            if timer.duration:
                total_duration += (timezone.now() - timer.startTime)
            active_users_data[user.username] = {
                'username': user.username,
                'total_active_today': str(total_duration),
                'current_course': timer.course.name if timer.course else 'None',
                'current_topic': timer.topic.name if timer.topic else 'None',
                'current_session': timer.session or 'None'
            }
        return list(active_users_data.values())

    async def send_active_users(self):
        active_users = await self.get_active_users()
        await self.channel_layer.group_send(
            "active_users",
            {
                'type': 'active_users_update',
                'data': {'active_users': active_users}
            }
        )

    async def active_users_update(self, event):
        await self.send(text_data=json.dumps(event['data']))