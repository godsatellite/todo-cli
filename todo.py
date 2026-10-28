import json
from pathlib import Path
from datetime import date

BASE_DIR = Path(__file__).parent
TASKS_FILE = BASE_DIR / "tasks.json"
PRIORITY_NAMES = {1: "Высокий", 2: "Средний", 3: "Низкий", None: "Пустой"}

def show_tasks(tasks):
    if tasks:
        for index, task in enumerate(tasks, start=1):
            checkbox = "✅" if task['done'] else "⬜"
            print(f"[{PRIORITY_NAMES[task['priority']]} приоритет] {index}. {task['title']} {checkbox} Дата: {task['date'] or 'нет'}")
    else:
        print("Задачи отсутствуют")

def show_for_do(tasks):
    if tasks:
        for index, task in enumerate(tasks, start=1):
            print(f"{index}. {task['title']}\n")
    else:
        print("Задачи отсутствуют")

def add_task(tasks):
    title = input("Введите задачу: ").strip()
    print()
    if title:
        priority = (input("Задайте приоритет: (1 - высокий, 2 - средний, 3 - низкий (или введите пустоту/не цифру, если приоритет неопределён)) "))
        print()
        try:
            if 1 <= int(priority) <= 3:
                priority = int(priority)
            else:
                print("Приоритет вне диапазона. Установлен пустой приоритет")
                priority = None
        except ValueError:
            print("Установлен пустой приоритет по умолчанию\n")
            priority = None
        temp_date = ask_due_date()
        if temp_date == "-":
            task_date = None
        else:
            task_date = temp_date
        tasks.append({"title": title, "done": False, "priority": priority, "date": task_date})
        sort_tasks(tasks)
        save_tasks(tasks)
        print(f"Добавлена задача: {title}")

    else:
        print("Название не может быть пустым")

def edit_date(tasks):
    show_for_do(tasks)
    if tasks:
        number = ask_task_number(tasks)
        if number is None:
            return
        print("Оставьте поле пустым для отмены изменения или поставьте '-' для очистки даты")
        edited_date = ask_due_date()
        if edited_date is None:
            print("Дата не изменена")
            return
        elif edited_date == "-":
            tasks[number - 1]["date"] = None
            print("Дата успешно удалена")
            sort_tasks(tasks)
            save_tasks(tasks)
            return
        tasks[number - 1]["date"] = edited_date
        print(f"Обновлена дата для {tasks[number -1]['title']}. Новая дата: {tasks[number - 1]['date']}")
        sort_tasks(tasks)
        save_tasks(tasks)

def ask_due_date():
    date_str = input("Введите дату для задачи: (Формат YYYY-MM-DD) ").strip()
    print()
    if not date_str.strip():
        return None
    elif date_str == "-":
        return "-"
    try:
        return date.fromisoformat(date_str).isoformat()
    except ValueError:
        print("Неверный формат даты. Дата не установлена\n")
        return None

def edit_priority(tasks):
    show_for_do(tasks)
    if tasks:
        number = ask_task_number(tasks)
        if number is None:
            return
        try:
            priority = int(input("Введите приоритет для задачи: (1 - высокий, 2 - средний, 3 - низкий) "))
            print()
            if 1 <= priority <= 3:
                tasks[number - 1]["priority"] = priority
                print(f"Успешно изменен приоритет задачи {tasks[number - 1]['title']} на {PRIORITY_NAMES[priority]}")
                sort_tasks(tasks)
                save_tasks(tasks)
            else:
                print("Введён приоритет вне диапазона")

        except ValueError:
            print("Ошибка ввода")

    
def done_task(tasks):
    show_for_do(tasks)
    if tasks:
        number = ask_task_number(tasks)
        if number is not None:
            tasks[number - 1]["done"] = True
            print(f"Выполнена задача: {tasks[number - 1]['title']}✅")
            sort_tasks(tasks)
            save_tasks(tasks)
      
def delete_task(tasks):
    show_for_do(tasks)
    if tasks:
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
        print()
    except ValueError:
        print("Вы ввели не целое число")
        return None
    if not 1 <= number <= len(tasks):
        print("Номер вне диапазона")
        return None
    return number

def sort_tasks(tasks):
    tasks.sort(key=lambda t: (t["done"], t["date"] or "9999-12-31", t["priority"] or 4))

def exit_program():
    print("Выходим из программы...")
    return False
    

tasks = load_tasks()
sort_tasks(tasks)
program_running = True

print("""Меню:
show - показать задачи
add - добавить задачу
done - выполнить задачу
edit_date - редактировать дату задачи
edit_priority - редактировать приоритет задачи
delete - удалить задачу
clear - очистить выполненные задачи
exit - выход из программы""")

while program_running:
    choice = input("\nВыберите действие: ").lower().strip()
    print()

    match choice:
        case "show":
            show_tasks(tasks)
        case "add":
            add_task(tasks)
        case "done":
            done_task(tasks)
        case "edit_date":
            edit_date(tasks)
        case "edit_priority":
            edit_priority(tasks)
        case "delete":
            delete_task(tasks)
        case "clear":
            clear_tasks(tasks)
        case "exit":
            program_running = exit_program()
        case _:
            print("Неизвестная команда")