# 🔍 Telegram Online Status Tracker Bot

<div align="center">
  
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white)](https://python.org)
[![Telethon](https://img.shields.io/badge/Telethon-1.28+-0088CC?logo=telegram)](https://docs.telethon.dev)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

</div>

<p align="center">
  <img src="https://camo.githubusercontent.com/2f2b0c82cb9dc05f15a7b3724637a4862a98f06ad90260c6577fa873571475e6/68747470733a2f2f646f776e6c6f61642e6c6f676f2e77696e652f6c6f676f2f54656c656772616d5f28736f667477617265292f54656c656772616d5f28736f667477617265292d4c6f676f2e77696e652e706e67" width="150" alt="Telegram Logo">
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
git clone https://github.com/ваш-username/telegram-status-tracker.git
cd telegram-status-tracker

# 2. Установить зависимости
pip install -r requirements.txt

# 3. Настроить config.json
cp config.example.json config.json

# 4. Запустить бота
python status_tracker.py
