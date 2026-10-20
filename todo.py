import json
from pathlib import Path

BASE_DIR = Path(__file__).parent
TASKS_FILE = BASE_DIR / "tasks.json"

def show_tasks(tasks):
    if tasks:
        for index, task in enumerate(tasks, start=1):
            checkbox = "✅" if task['done'] else "⬜"
            print(f"{index}. {task['title']}: {checkbox}\n")
    else:
        print("Задачи отсутствуют")

def add_task(tasks, title):
    tasks.append({"title": title, "done": False})

def done_task(tasks, number):
    tasks[number - 1]["done"] = True

def delete_task(tasks, number):
    del tasks[number - 1]

def save_tasks(tasks):
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

def load_tasks():
    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            return json.load(f) 
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("Файл tasks.json повреждён. Исправьте или удалите его и запустите программу снова.")
        raise SystemExit

tasks = load_tasks()

print("""Меню:
show - показать задачи
add - добавить задачу
done - выполнить задачу
delete - удалить задачу
exit - выход из программы
""")

while True:
    choice = input("Выберите действие:").lower()

    if choice == "show":
        show_tasks(tasks)
    elif choice == "add":
        title = input("Введите задачу: ")
        add_task(tasks, title)
        save_tasks(tasks)
        print(f"Добавлена задача: {title}")
    elif choice == "done":
        try:
            number = int(input("Введите номер задачи: "))
            if 1 <= number <= len(tasks):
                done_task(tasks, number)
                save_tasks(tasks)
            else:
                print("Номер вне диапазона")
        except ValueError:
            print("Вы ввели не число")
    elif choice == "delete":
        try:
            number = int(input("Введите номер задачи: "))
            if 1 <= number <= len(tasks):
                delete_task(tasks, number)
                save_tasks(tasks)
            else:
                print("Номер вне диапазона")
        except ValueError:
            print("Вы ввели не число")
    elif choice == "exit":
        break
    else:
        print("Неизвестная команда")

    
