import requests
import pytest

# Базова URL для звернення до нашого API 
# (використовуємо localhost, оскільки тести запускаються поряд з контейнером)
BASE_URL = "http://localhost:5000/api/tasks"

@pytest.fixture(autouse=True)
def setup_tasks():
    # Цей фікстур потрібен, щоб можна було зберігати task_id між тестами
    pass 

def test_1_create_task():
    """Створюємо завдання і перевіряємо статус 201 та вміст відповіді."""
    print("\n--- Запуск тесту 1: Створення завдання (POST) ---")
    payload = {"title": "Lab5 Task 1", "done": False}
    # Звертаємося до API
    r = requests.post(BASE_URL, json=payload)

    # 1. Перевірка статусу відповіді
    assert r.status_code == 201
    
    # 2. Перевірка вмісту відповіді
    assert r.json()["title"] == "Lab5 Task 1"
    
    # Зберігаємо ID для наступних тестів
    pytest.task_id = r.json()["id"]

def test_2_get_tasks():
    """Отримуємо список усіх завдань і перевіряємо, що це список, і він не порожній."""
    print("\n--- Запуск тесту 2: Отримання завдань (GET) ---")
    r = requests.get(BASE_URL)
    
    # 1. Перевірка статусу
    assert r.status_code == 200

    # 2. Перевірка типу (має бути список)
    assert isinstance(r.json(), list)
    
    # 3. Перевіряємо, що список містить принаймні одне завдання (те, яке ми створили)
    assert len(r.json()) > 0 

def test_3_update_task():
    """Оновлюємо статус завдання з ID, отриманим у Тесті 1."""
    # Отримуємо ID, якщо він не був встановлений, використовуємо 1 як резервний
    task_to_update_id = getattr(pytest, 'task_id', 1) 
    url = f"{BASE_URL}/{task_to_update_id}"
    
    print(f"\n--- Запуск тесту 3: Оновлення завдання (PUT) для ID={task_to_update_id} ---")
    # Змінюємо статус 'done' на True
    r = requests.put(url, json={"done": True})
    
    # 1. Перевірка статусу
    assert r.status_code == 200

    # 2. Перевірка, що статус оновився
    assert r.json()["done"] is True
    
    # Додаткова перевірка (необов'язкова, але корисна)
    requests.get(url) 
