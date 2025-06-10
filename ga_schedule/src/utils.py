from typing import List
from schedule import Schedule, Lesson
from config import NUM_TEACHERS, NUM_GROUPS, NUM_ROOMS

def print_schedule(schedule: Schedule):
    """Печать расписания в удобном формате"""
    days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница"]
    slots = [f"{i+1} пара" for i in range(6)]
    
    # Создаем таблицу расписания
    schedule_table = {}
    for day in range(5):
        for slot in range(6):
            schedule_table[(day, slot)] = []

    # Заполняем таблицу
    for lesson in schedule.lessons:
        schedule_table[(lesson.day, lesson.slot)].append(lesson)

    # Печатаем расписание
    print("\nРасписание занятий:")
    print("-" * 80)
    
    for day in range(5):
        print(f"\n{days[day]}:")
        print("-" * 80)
        for slot in range(6):
            lessons = schedule_table[(day, slot)]
            if lessons:
                print(f"\n{slots[slot]}:")
                for lesson in lessons:
                    print(f"  Группа {lesson.group_id + 1} | "
                          f"Предмет: {lesson.subject} | "
                          f"Преподаватель: {lesson.teacher_id + 1} | "
                          f"Аудитория: {lesson.room_id + 1}")
            else:
                print(f"\n{slots[slot]}: Нет занятий")

def print_conflicts(schedule: Schedule):
    """Печать информации о конфликтах в расписании"""
    print("\nАнализ конфликтов:")
    print("-" * 80)
    
    # Проверяем конфликты у преподавателей
    teacher_conflicts = 0
    for teacher_id in range(NUM_TEACHERS):
        lessons = schedule.get_teacher_lessons(teacher_id)
        time_slots = set((l.day, l.slot) for l in lessons)
        if len(time_slots) != len(lessons):
            teacher_conflicts += 1
            print(f"Конфликт у преподавателя {teacher_id + 1}")
    
    # Проверяем конфликты у групп
    group_conflicts = 0
    for group_id in range(NUM_GROUPS):
        lessons = schedule.get_group_lessons(group_id)
        time_slots = set((l.day, l.slot) for l in lessons)
        if len(time_slots) != len(lessons):
            group_conflicts += 1
            print(f"Конфликт у группы {group_id + 1}")
    
    # Проверяем конфликты в аудиториях
    room_conflicts = 0
    for room_id in range(NUM_ROOMS):
        lessons = schedule.get_room_lessons(room_id)
        time_slots = set((l.day, l.slot) for l in lessons)
        if len(time_slots) != len(lessons):
            room_conflicts += 1
            print(f"Конфликт в аудитории {room_id + 1}")
    
    print(f"\nВсего конфликтов:")
    print(f"У преподавателей: {teacher_conflicts}")
    print(f"У групп: {group_conflicts}")
    print(f"В аудиториях: {room_conflicts}") 