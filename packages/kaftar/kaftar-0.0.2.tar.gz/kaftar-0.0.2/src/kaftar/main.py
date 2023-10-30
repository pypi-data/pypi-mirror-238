import os
from celery import Celery


class Notification:
    def __init__(self,
                 service_name: str,
                 broker_env_key: str = 'CELERY_BROKER') -> None:
        self.app = Celery(service_name, broker=os.environ.get(broker_env_key))
        self.service_name = service_name

    def send_notification(self,
                          body: dict,
                          recipients: list[dict],
                          send_datetime: str) -> None:
        self.app.send_task('notification.notification.send_notification',
                           (body,
                            recipients,
                            self.service_name,
                            send_datetime),
                           queue='notification')
