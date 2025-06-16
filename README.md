Galactic API 🚀
REST API для управления операциями межзвездного флота на Python Flask

Возможности
Управление космическими кораблями

Планирование миссий

Организация экипажа

Полноценный RESTful интерфейс

Установка:
bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows
pip install -r requirements.txt

Запуск:
bash
flask run

Документация API
Описание конечных точек API доступно в API_DOCS.md

Дополнительно можно добавить:

Конфигурация
Создайте файл .env в корне проекта:

ini
FLASK_APP=app.py
FLASK_ENV=development

Тестирование
Для тестирования API можно использовать:

bash
pytest tests/
