# 🔍 Telegram Online Status Tracker Bot

<div align="center">
  
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white)](https://python.org)
[![Telethon](https://img.shields.io/badge/Telethon-1.28+-0088CC?logo=telegram)](https://docs.telethon.dev)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

</div>

<p align="center">
  <img src="https://camo.githubusercontent.com/2f2b0c82cb9dc05f15a7b3724637a4862a98f06ad90260c6577fa873571475e6/68747470733a2f2f646f776e6c6f61642e6c6f676f2e77696e652f6c6f676f2f54656c656772616d5f28736f667477617265292f54656c656772616d5f28736f667477617265292d4c6f676f2e77696e652e706e67" width="150" alt="">
</p>

Мониторинг активности пользователей Telegram с системой уведомлений о совпадениях онлайн-статуса.

## ✨ Особенности

- 🕵️‍♂️ **Трекинг статусов** в реальном времени
- 👥 **Детектор пар** (когда два пользователя онлайн одновременно)
- ⏱ **Адаптивные интервалы** проверки (экономят ресурсы)
- 📨 **Умные уведомления** через Telegram-бота
- 📊 **Подробное логгирование** всех сессий
- ♻️ **Горячая перезагрузка** конфига без перезапуска

## 🚀 Быстрый старт

### Предварительные требования
- Python 3.8+
- Аккаунт Telegram
- API ключи (см. [Конфигурация](#%EF%B8%8F-конфигурация))

```bash
# 1. Клонировать репозиторий
git clone https://github.com/Lado20101/telegram-status-tracker.git
cd telegram-status-tracker

# 2. Установить зависимости
pip install -r requirements.txt

# 3. Настроить config.json
cp config.example.json config.json

# 4. Запустить бота
python status_tracker.py
```

## ⚙️ Конфигурация

Создайте `config.json` по образцу:

```json
{
  "api_id": 1234567,
  "api_hash": "ваш_api_hash_из_telegram",
  "usernames": ["username1", "username2"],
  "pairs": [
    ["username1", "username2"]
  ],
  "timing": {
    "default_interval": 60,
    "active_interval": 30,
    "inactive_interval": 120,
    "error_delay": 60
  },
  "notification_bot": {
    "api_id": 123456,
    "api_hash": "api_hash_бота",
    "bot_token": "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11",
    "chat_id": -1001234567890
  }
}
```

### 🔑 Получение ключей
| Ключ | Где получить |
|------|-------------|
| API ID/Hash | [my.telegram.org](https://my.telegram.org) |
| Токен бота | [@BotFather](https://t.me/BotFather) |
| Chat ID | [@userinfobot](https://t.me/userinfobot) |

## 📊 Примеры работы

### Уведомления в боте
```
🔥 ПАРА ОНЛАЙН
👤 User1 + User2
🕒 15:30:45
────────────────
⏱ Длительность: 00:25:17
```

### Логи в файле
```log
[2023-11-20] Пара User1 и User2
   🕒 В сети: [15:30:45 - 15:56:02]
   ⏱ Длительность: 00:25:17
```

## 📂 Структура проекта
```
telegram-status-tracker/
├── status_tracker.py    # Основной скрипт
├── config.json          # Конфигурация (не в репозитории)
├── session_logs.log     # Логи сессий (автосоздается)
├── requirements.txt     # Зависимости
└── README.md            # Этот файл
```

## 🛠 Технологии
- [Telethon](https://docs.telethon.dev) - Асинхронный клиент Telegram MTProto API
- Python 3.8+ - Базовый язык
- Logging - Система логгирования

## ❓ FAQ

### ❔ Как добавить новых пользователей?
Просто отредактируйте `config.json` и добавьте usernames в массив `usernames` и пары в `pairs`.

### ❔ Бот не запускается, что делать?
1. Проверьте правильность API ключей
2. Убедитесь что сессия не заблокирована (удалите *.session файлы)
3. Запустите с ключом `--debug` для подробного вывода

## 📜 Лицензия
Этот проект распространяется под лицензией MIT. Подробнее см. в файле [LICENSE](LICENSE).

---
<div align="center">
  
Made with ❤️ and Python
