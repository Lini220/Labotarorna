import requests
import pytest

BASE_URL = "http://localhost:5000/api/tasks"

@pytest.fixture(autouse=True)
def setup_tasks():
    pass 


def test_1_create_task():
    """Створюємо завдання і перевіряємо статус 201 та вміст відповіді."""
    print("\n--- Запуск тесту 1: Створення завдання (POST) ---")
    payload = {"title": "Lab5 Task 1", "done": False}
    r = requests.post(BASE_URL, json=payload)

    assert r.status_code == 201
    
    assert r.json()["title"] == "Lab5 Task 1"
    
    pytest.task_id = r.json()["id"]

def test_2_get_tasks():
    """Отримуємо список усіх завдань і перевіряємо, що це список, і він не порожній."""
    print("\n--- Запуск тесту 2: Отримання завдань (GET) ---")
    r = requests.get(BASE_URL)
    
    assert r.status_code == 200

    assert isinstance(r.json(), list)
    
    assert len(r.json()) > 0 

def test_3_update_task():
    """Оновлюємо статус завдання з ID, отриманим у Тесті 1."""
    task_to_update_id = getattr(pytest, 'task_id', 1) 
    url = f"{BASE_URL}/{task_to_update_id}"
    
    print(f"\n--- Запуск тесту 3: Оновлення завдання (PUT) для ID={task_to_update_id} ---")
    r = requests.put(url, json={"done": True})
    
    assert r.status_code == 200

    assert r.json()["done"] is True
    
    r_check = requests.get(url) 
