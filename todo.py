import json
from pathlib import Path
from datetime import date

BASE_DIR = Path(__file__).parent
TASKS_FILE = BASE_DIR / "tasks.json"
PRIORITY_NAMES = {1: "Высокий", 2: "Средний", 3: "Низкий"}

def show_tasks(tasks):
    if tasks:
        for index, task in enumerate(tasks, start=1):
            checkbox = "✅" if task['done'] else "⬜"
            print(f"[{PRIORITY_NAMES[task['priority']]} приоритет] {index}. {task['title']} {checkbox} Дата: {task['date']}\n")
    else:
        print("Задачи отсутствуют")

def add_task(tasks):
    title = input("Введите задачу: ").strip()
    print("")
    if title:
        try:
            priority = int(input("Задайте приоритет: (1 - высокий, 2 - средний, 3 - низкий) "))
            print("")
            if 1 <= priority <= 3:
                task_date = ask_due_date()
                tasks.append({"title": title, "done": False, "priority": priority, "date": task_date})
                save_tasks(tasks)
                print(f"Добавлена задача: {title}")
            else:
                print("Приоритет вне диапазона")
        except ValueError:
            print("Вы ввели не целое число")
    else:
        print("Название не может быть пустым")

def ask_due_date():
    date_str = input("Введите дату для задачи: (Формат YYYY-MM-DD) ")
    print()
    if not date_str.strip():
        return None
    try:
        date.fromisoformat(date_str)
        return date_str
    except ValueError:
        print("Неверный формат даты. Дата не установлена\n")
        return None
    
def done_task(tasks):
    number = ask_task_number(tasks)
    if number is not None:
        tasks[number - 1]["done"] = True
        save_tasks(tasks)
        print(f"Выполнена задача: {tasks[number - 1]['title']}✅")
      
def delete_task(tasks):
    number = ask_task_number(tasks)
    if number is not None:
        print(f"Удалена задача: {tasks[number - 1]['title']}")
        del tasks[number - 1]
        save_tasks(tasks)

def clear_tasks(tasks):
    before = len(tasks)
    tasks[:] = [task for task in tasks if not task["done"]]
    after = len(tasks)
    print(f"Очищено задач: {before - after}")
    save_tasks(tasks)
    
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

def ask_task_number(tasks):
    try:
        number = int(input("Выберите номер задачи: "))
        print("")
    except ValueError:
        print("Вы ввели не целое число")
        return None
    if not 1 <= number <= len(tasks):
        print("Номер вне диапазона")
        return None
    return number

def exit_program():
    print("Выходим из программы...")
    return False
    

tasks = load_tasks()
program_running = True

print("""Меню:
show - показать задачи
add - добавить задачу
done - выполнить задачу
delete - удалить задачу
clear - очистить выполненные задачи
exit - выход из программы""")

while program_running:
    choice = input("\nВыберите действие: ").lower()
    print("")

    match choice:
        case "show":
            show_tasks(tasks)
        case "add":
            add_task(tasks)
        case "done":
            done_task(tasks)
        case "delete":
            delete_task(tasks)
        case "clear":
            clear_tasks(tasks)
        case "exit":
            program_running = exit_program()
        case _:
            print("Неизвестная команда")