import json
from pathlib import Path

BASE_DIR = Path(__file__).parent
TASKS_FILE = BASE_DIR / "tasks.json"

def show_tasks(tasks):
    if tasks:
        for index, task in enumerate(tasks, start=1):
            checkbox = "✅" if task['done'] else "⬜"
            priority_text = "Высокий приоритет" if task['priority'] == 1 else "Средний приоритет" if task['priority'] == 2 else "Низкий приоритет"
            print(f"[{priority_text}] {index}. {task['title']}: {checkbox}\n")
    else:
        print("Задачи отсутствуют")

def add_task(tasks, title, priority):
    tasks.append({"title": title, "done": False, "priority": priority})

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
exit - выход из программы""")

while True:
    choice = input("\nВыберите действие: ").lower()
    print("")

    if choice == "show":
        show_tasks(tasks)
    elif choice == "add":
        title = input("Введите задачу: ")
        print("")
        try:
            priority = int(input("Задайте приоритет: (1 - высокий, 2 - средний, 3 - низкий) "))
            print("")
            if 1 <= priority <= 3:
                add_task(tasks, title, priority)
                save_tasks(tasks)
                print(f"Добавлена задача: {title}")
            else:
                print("Приоритет вне диапазона")
        except ValueError:
            print("Вы ввели не число")
    elif choice == "done":
        try:
            number = int(input("Выберите номер задачи: "))
            print("")
            if 1 <= number <= len(tasks):
                done_task(tasks, number)
                save_tasks(tasks)
                print(f"Выполнена задача: {tasks[number - 1]['title']}✅")
            else:
                print("Номер вне диапазона")
        except ValueError:
            print("Вы ввели не число")
    elif choice == "delete":
        try:
            number = int(input("Выберите номер задачи: "))
            print("")
            if 1 <= number <= len(tasks):
                print(f"Удалена задача: {tasks[number - 1]['title']}")
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

    
