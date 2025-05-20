import json
import asyncio
import os
from telethon import TelegramClient
from telethon.tl.types import UserStatusOnline, UserStatusRecently, UserStatusOffline
from datetime import datetime, timedelta

class StatusTracker:
    def __init__(self):
        self.config = self.load_config()
        self.client = None
        self.notification_client = None
        self.log_file = "session_logs.log"
        self.user_online_since = {}
        self.pair_online_since = {}
        self.last_check = datetime.now()
        self.config_mtime = os.path.getmtime('config.json')

    def load_config(self):
        try:
            with open('config.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Ошибка загрузки конфига: {e}")
            raise

    async def init_notification_bot(self):
        if 'notification_bot' in self.config:
            try:
                self.notification_client = TelegramClient(
                    'notification_session',
                    self.config['notification_bot']['api_id'],
                    self.config['notification_bot']['api_hash']
                )
                await self.notification_client.start(bot_token=self.config['notification_bot']['bot_token'])
                print("✅ Успешно подключен к боту-нотификатору")
            except Exception as e:
                print(f"❌ Ошибка инициализации бота-нотификатора: {e}")

    def reload_config(self):
        try:
            new_config = self.load_config()
            self.config = new_config
            print("🔄 Конфиг успешно перезагружен")
        except Exception as e:
            print(f"❌ Ошибка перезагрузки конфига: {e}")

    def print_separator(self):
        print("\n" + "=" * 40 + "\n")

    def format_duration(self, duration: timedelta) -> str:
        total_seconds = int(duration.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    async def send_notification(self, message: str):
        if self.notification_client and 'notification_bot' in self.config:
            try:
                await self.notification_client.send_message(
                    self.config['notification_bot']['chat_id'],
                    message
                )
            except Exception as e:
                print(f"❌ Ошибка отправки уведомления: {e}")

    def log_session(self, entity: str, start: datetime, end: datetime, is_pair: bool = False):
        start_str = start.strftime("%H:%M:%S")
        end_str = end.strftime("%H:%M:%S")
        duration = self.format_duration(end - start)
        
        log_entry = (
            f"[{datetime.now().strftime('%Y-%m-%d')}] "
            f"{'Пара' if is_pair else 'Пользователь'} {entity}\n"
            f"   🕒 В сети: [{start_str} - {end_str}]\n"
            f"   ⏱ Длительность: {duration}\n"
        )
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry + "\n")

    def get_status_icon(self, status):
        if isinstance(status, UserStatusOnline):
            return "🟢 ONLINE"
        elif isinstance(status, UserStatusRecently):
            return "🟡 RECENTLY"
        elif isinstance(status, UserStatusOffline):
            return "🔴 OFFLINE"
        return "⚪ UNKNOWN"

    async def check_users(self):
        try:
            now = datetime.now()
            online_users = set()
            any_pairs_online = False
            any_users_online = False
            
            self.print_separator()
            print("🕒 Текущие статусы:")

            # Проверка пользователей
            for username in self.config['usernames']:
                try:
                    user = await self.client.get_entity(username)
                    status_str = self.get_status_icon(user.status)
                    print(f"{user.first_name} (@{username}): {status_str}")
                    
                    if isinstance(user.status, UserStatusOnline):
                        online_users.add(username)
                        any_users_online = True
                        if username not in self.user_online_since:
                            self.user_online_since[username] = now
                            await self.send_notification(
                                f"👤 Пользователь {user.first_name} (@{username}) в сети!\n"
                                f"🕒 Время: {now.strftime('%H:%M:%S')}"
                            )
                    else:
                        if username in self.user_online_since:
                            start_time = self.user_online_since.pop(username)
                            duration = self.format_duration(now - start_time)
                            self.log_session(user.first_name, start_time, now)
                            await self.send_notification(
                                f"👤 Пользователь {user.first_name} (@{username}) вышел из сети\n"
                                f"⏱ Был онлайн: {duration}\n"
                                f"🕒 Время выхода: {now.strftime('%H:%M:%S')}"
                            )
                            
                except Exception as e:
                    print(f"❗ Ошибка проверки {username}: {str(e)[:50]}")

            # Проверка пар
            active_pairs = []
            for user1, user2 in self.config['pairs']:
                try:
                    if user1 in online_users and user2 in online_users:
                        any_pairs_online = True
                        active_pairs.append(f"🔥 {user1} & {user2}")
                        if (user1, user2) not in self.pair_online_since:
                            self.pair_online_since[(user1, user2)] = now
                            user1_name = (await self.client.get_entity(user1)).first_name
                            user2_name = (await self.client.get_entity(user2)).first_name
                            await self.send_notification(
                                f"🔥 Пара онлайн: {user1_name} и {user2_name}\n"
                                f"🕒 Время: {now.strftime('%H:%M:%S')}"
                            )
                    else:
                        if (user1, user2) in self.pair_online_since:
                            start_time = self.pair_online_since.pop((user1, user2))
                            name1 = (await self.client.get_entity(user1)).first_name
                            name2 = (await self.client.get_entity(user2)).first_name
                            duration = self.format_duration(now - start_time)
                            self.log_session(f"{name1} и {name2}", start_time, now, is_pair=True)
                            await self.send_notification(
                                f"💤 Пара вышла из сети: {name1} и {name2}\n"
                                f"⏱ Был онлайн: {duration}\n"
                                f"🕒 Время выхода: {now.strftime('%H:%M:%S')}"
                            )
                except Exception as e:
                    print(f"❗ Ошибка проверки пары {user1}-{user2}: {str(e)[:50]}")

            # Вывод информации о парах
            if active_pairs:
                print("\n🔥 Активные пары:")
                for pair in active_pairs:
                    print(pair)
            else:
                print("\n💤 Нет активных пар")

            self.print_separator()
            return any_pairs_online, any_users_online

        except Exception as e:
            print(f"❌ Ошибка в check_users: {e}")
            return False, False

    async def run(self):
        print("🔹 Трекер запущен")
        await self.init_notification_bot()
        self.client = TelegramClient('session', 
            self.config['api_id'], 
            self.config['api_hash']
        )
        
        try:
            await self.client.start()
            print("✅ Успешно подключен к Telegram")
            
            while True:
                try:
                    # Проверка обновления конфига
                    current_mtime = os.path.getmtime('config.json')
                    if current_mtime != self.config_mtime:
                        self.reload_config()
                        self.config_mtime = current_mtime
                        await self.init_notification_bot()

                    any_pairs_online, any_users_online = await self.check_users()
                    
                    # Динамический интервал проверки
                    if any_pairs_online:
                        interval = self.config['timing']['active_interval']
                    elif any_users_online:
                        interval = self.config['timing']['default_interval']
                    else:
                        interval = self.config['timing']['inactive_interval']
                        
                    print(f"⏳ Следующая проверка через {interval} сек...")
                    await asyncio.sleep(interval)
                    
                except KeyboardInterrupt:
                    print("\n🛑 Остановка по запросу пользователя")
                    break
                except Exception as e:
                    print(f"❌ Ошибка: {e}")
                    await asyncio.sleep(self.config['timing']['error_delay'])
                    
        except Exception as e:
            print(f"❌ Критическая ошибка: {e}")
        finally:
            # Фиксация оставшихся сессий
            now = datetime.now()
            
            # Логирование пользователей
            for username, start_time in self.user_online_since.items():
                user = await self.client.get_entity(username)
                self.log_session(user.first_name, start_time, now)
                await self.send_notification(
                    f"👤 Пользователь {user.first_name} (@{username}) был онлайн при остановке бота\n"
                    f"🕒 Общее время: {self.format_duration(now - start_time)}"
                )
            
            # Логирование пар
            for (user1, user2), start_time in self.pair_online_since.items():
                name1 = (await self.client.get_entity(user1)).first_name
                name2 = (await self.client.get_entity(user2)).first_name
                self.log_session(f"{name1} и {name2}", start_time, now, is_pair=True)
                await self.send_notification(
                    f"🔥 Пара {name1} и {name2} была онлайн при остановке бота\n"
                    f"🕒 Общее время: {self.format_duration(now - start_time)}"
                )
            
            await self.client.disconnect()
            if self.notification_client:
                await self.notification_client.disconnect()
            print("🔹 Трекер остановлен")

if __name__ == "__main__":
    tracker = StatusTracker()
    asyncio.run(tracker.run())