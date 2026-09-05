from aiokafka import AIOKafkaConsumer
import json
import asyncio
from app.config import settings

class VaccinationConsumer:
    def __init__(self):
        self.consumer = None
        self.running = False
    
    async def start(self):
        """Запустить Kafka Consumer"""
        self.consumer = AIOKafkaConsumer(
            settings.KAFKA_TOPIC_VACCINATIONS,
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            group_id="vaccination_group",
            value_deserializer=lambda v: json.loads(v.decode('utf-8')),
            auto_offset_reset="earliest"
        )
        await self.consumer.start()
        self.running = True
        print("Kafka consumer started")
    
    async def consume(self):
        """Потреблять сообщения"""
        if not self.consumer:
            await self.start()
        
        async for msg in self.consumer:
            try:
                event = msg.value
                print(f"Received event: {event}")
                
                # Обработка события
                if event.get("event_type") == "vaccination_created":
                    await self.handle_vaccination_created(event)
                    
            except Exception as e:
                print(f"Error processing message: {e}")
    
    async def handle_vaccination_created(self, event):
        """Обработка события создания вакцинации"""
        # Здесь можно добавить логику:
        # - Отправка уведомлений
        # - Обновление статистики
        # - Интеграция с другими системами
        print(f"Processing vaccination #{event['vaccination_id']} for patient #{event['patient_id']}")
    
    async def stop(self):
        """Остановить Consumer"""
        self.running = False
        if self.consumer:
            await self.consumer.stop()
            print("Kafka consumer stopped")