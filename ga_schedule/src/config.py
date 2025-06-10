# Параметры генетического алгоритма
POPULATION_SIZE = 200
NUM_GENERATIONS = 50
CROSSOVER_PROB = 0.8
MUTATION_PROB = 0.1
TOURNAMENT_SIZE = 3
ELITISM_COUNT = 2
EPSILON = 1e-10

# Параметры расписания
NUM_DAYS = 5  # Количество учебных дней
NUM_SLOTS = 6  # Количество временных слотов в день
NUM_ROOMS = 10  # Количество аудиторий
NUM_TEACHERS = 15  # Количество преподавателей
NUM_GROUPS = 12  # Количество групп студентов

# Штрафы за нарушения ограничений
PENALTY_TEACHER_CONFLICT = 1000  # Штраф за конфликт у преподавателя
PENALTY_GROUP_CONFLICT = 1000    # Штраф за конфликт у группы
PENALTY_ROOM_CONFLICT = 1000     # Штраф за конфликт в аудитории
PENALTY_TEACHER_PREFERENCE = 100 # Штраф за нарушение предпочтений преподавателя 