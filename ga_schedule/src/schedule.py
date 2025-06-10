from dataclasses import dataclass
from typing import List, Dict, Set
import random
from config import (
    NUM_DAYS, NUM_SLOTS, NUM_ROOMS, NUM_TEACHERS, NUM_GROUPS,
    PENALTY_TEACHER_CONFLICT, PENALTY_GROUP_CONFLICT,
    PENALTY_ROOM_CONFLICT, PENALTY_TEACHER_PREFERENCE
)

@dataclass
class Lesson:
    teacher_id: int
    group_id: int
    subject: str
    room_id: int
    day: int
    slot: int

    def __repr__(self):
        return f"Lesson(teacher={self.teacher_id}, group={self.group_id}, subject={self.subject}, room={self.room_id}, day={self.day}, slot={self.slot})"

class Schedule:
    def __init__(self):
        self.lessons: List[Lesson] = []
        self.teacher_preferences: Dict[int, Set[int]] = {}  # teacher_id -> set of preferred days
        self.teacher_subjects: Dict[int, List[str]] = {}    # teacher_id -> list of subjects
        self.group_subjects: Dict[int, List[str]] = {}      # group_id -> list of subjects

    def add_lesson(self, lesson: Lesson):
        self.lessons.append(lesson)

    def get_teacher_lessons(self, teacher_id: int) -> List[Lesson]:
        return [l for l in self.lessons if l.teacher_id == teacher_id]

    def get_group_lessons(self, group_id: int) -> List[Lesson]:
        return [l for l in self.lessons if l.group_id == group_id]

    def get_room_lessons(self, room_id: int) -> List[Lesson]:
        return [l for l in self.lessons if l.room_id == room_id]

    def has_conflict(self, lesson: Lesson) -> bool:
        # Проверка конфликтов у преподавателя
        teacher_lessons = self.get_teacher_lessons(lesson.teacher_id)
        for l in teacher_lessons:
            if l.day == lesson.day and l.slot == lesson.slot:
                return True

        # Проверка конфликтов у группы
        group_lessons = self.get_group_lessons(lesson.group_id)
        for l in group_lessons:
            if l.day == lesson.day and l.slot == lesson.slot:
                return True

        # Проверка конфликтов в аудитории
        room_lessons = self.get_room_lessons(lesson.room_id)
        for l in room_lessons:
            if l.day == lesson.day and l.slot == lesson.slot:
                return True

        return False

    def calculate_penalty(self) -> float:
        penalty = 0.0

        # Проверка конфликтов
        for lesson in self.lessons:
            if self.has_conflict(lesson):
                penalty += (PENALTY_TEACHER_CONFLICT + 
                          PENALTY_GROUP_CONFLICT + 
                          PENALTY_ROOM_CONFLICT)

        # Проверка предпочтений преподавателей
        for lesson in self.lessons:
            teacher_preferred_days = self.teacher_preferences.get(lesson.teacher_id, set())
            if lesson.day not in teacher_preferred_days:
                penalty += PENALTY_TEACHER_PREFERENCE

        return penalty

def generate_random_schedule() -> Schedule:
    schedule = Schedule()
    
    # Список всех возможных предметов
    all_subjects = [
        "Математика", "Физика", "Информатика", "Английский язык",
        "История", "Литература", "Химия", "Биология",
        "География", "Обществознание", "Физкультура", "ОБЖ",
        "Алгебра", "Геометрия", "Программирование", "Базы данных",
        "Сети", "Операционные системы", "Архитектура компьютеров",
        "Теория вероятностей", "Статистика", "Экономика",
        "Право", "Философия", "Психология", "Иностранный язык"
    ]
    
    # Распределяем предметы между преподавателями
    for teacher_id in range(NUM_TEACHERS):
        # Каждый преподаватель ведет 5-7 предметов
        num_subjects = random.randint(5, 7)
        schedule.teacher_subjects[teacher_id] = random.sample(all_subjects, num_subjects)
        # Предпочтительные дни для каждого преподавателя
        schedule.teacher_preferences[teacher_id] = set(random.sample(range(NUM_DAYS), 3))

    # Распределяем предметы между группами
    for group_id in range(NUM_GROUPS):
        # Каждая группа изучает 10-12 предметов
        num_subjects = random.randint(10, 12)
        schedule.group_subjects[group_id] = random.sample(all_subjects, num_subjects)

    # Генерация расписания
    max_attempts = 100  # Максимальное количество попыток размещения занятия
    
    for group_id in range(NUM_GROUPS):
        for subject in schedule.group_subjects[group_id]:
            # Находим преподавателей, которые могут вести этот предмет
            possible_teachers = [
                t_id for t_id, subjects in schedule.teacher_subjects.items()
                if subject in subjects
            ]
            
            if not possible_teachers:
                continue

            # Пытаемся разместить занятие
            for _ in range(max_attempts):
                teacher_id = random.choice(possible_teachers)
                day = random.randint(0, NUM_DAYS - 1)
                slot = random.randint(0, NUM_SLOTS - 1)
                room_id = random.randint(0, NUM_ROOMS - 1)

                lesson = Lesson(teacher_id, group_id, subject, room_id, day, slot)
                if not schedule.has_conflict(lesson):
                    schedule.add_lesson(lesson)
                    break

    return schedule 