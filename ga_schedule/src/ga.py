import random
from copy import deepcopy
from typing import List, Tuple

from config import (
    POPULATION_SIZE,
    NUM_GENERATIONS,
    CROSSOVER_PROB,
    MUTATION_PROB,
    TOURNAMENT_SIZE,
    ELITISM_COUNT,
    EPSILON,
    NUM_DAYS,
    NUM_SLOTS,
)
from schedule import Schedule, Lesson, generate_random_schedule

def create_initial_population() -> List[Schedule]:
    return [generate_random_schedule() for _ in range(POPULATION_SIZE)]

def fitness_of(schedule: Schedule) -> float:
    penalty = schedule.calculate_penalty()
    return 1.0 / (penalty + EPSILON)

def tournament_selection(population: List[Schedule], fitnesses: List[float]) -> Schedule:
    chosen = random.sample(range(len(population)), TOURNAMENT_SIZE)
    best = chosen[0]
    for idx in chosen[1:]:
        if fitnesses[idx] > fitnesses[best]:
            best = idx
    return deepcopy(population[best])

def crossover(parent1: Schedule, parent2: Schedule) -> Tuple[Schedule, Schedule]:
    child1 = Schedule()
    child2 = Schedule()

    # Копируем предпочтения и предметы
    child1.teacher_preferences = deepcopy(parent1.teacher_preferences)
    child1.teacher_subjects = deepcopy(parent1.teacher_subjects)
    child1.group_subjects = deepcopy(parent1.group_subjects)
    
    child2.teacher_preferences = deepcopy(parent2.teacher_preferences)
    child2.teacher_subjects = deepcopy(parent2.teacher_subjects)
    child2.group_subjects = deepcopy(parent2.group_subjects)

    # Скрещиваем занятия
    all_lessons = parent1.lessons + parent2.lessons
    random.shuffle(all_lessons)
    
    mid = len(all_lessons) // 2
    child1.lessons = all_lessons[:mid]
    child2.lessons = all_lessons[mid:]

    return child1, child2

def mutation(schedule: Schedule):
    if not schedule.lessons:
        return

    # Выбираем случайное занятие
    lesson = random.choice(schedule.lessons)
    
    # Случайно меняем день или временной слот
    if random.random() < 0.5:
        lesson.day = random.randint(0, NUM_DAYS - 1)
    else:
        lesson.slot = random.randint(0, NUM_SLOTS - 1)

def evolve_population(population: List[Schedule]) -> Tuple[List[Schedule], List[float]]:
    fitnesses = [fitness_of(schedule) for schedule in population]
    
    # Сортируем по приспособленности
    sorted_indices = sorted(range(len(population)), key=lambda i: fitnesses[i], reverse=True)
    new_population = []

    # Элитизм
    for idx in sorted_indices[:ELITISM_COUNT]:
        new_population.append(deepcopy(population[idx]))

    # Создаем новое поколение
    while len(new_population) < POPULATION_SIZE:
        parent1 = tournament_selection(population, fitnesses)
        parent2 = tournament_selection(population, fitnesses)

        if random.random() < CROSSOVER_PROB:
            child1, child2 = crossover(parent1, parent2)
        else:
            child1, child2 = deepcopy(parent1), deepcopy(parent2)

        if random.random() < MUTATION_PROB:
            mutation(child1)
        if random.random() < MUTATION_PROB:
            mutation(child2)

        new_population.append(child1)
        if len(new_population) < POPULATION_SIZE:
            new_population.append(child2)

    fitnesses_new = [fitness_of(schedule) for schedule in new_population]
    return new_population, fitnesses_new

def run_ga() -> Tuple[Schedule, float]:
    population = create_initial_population()
    best_overall = None
    best_fitness = -1.0

    for gen in range(NUM_GENERATIONS):
        population, fitnesses = evolve_population(population)

        gen_best_idx = max(range(len(population)), key=lambda i: fitnesses[i])
        gen_best_fit = fitnesses[gen_best_idx]

        if gen_best_fit > best_fitness:
            best_fitness = gen_best_fit
            best_overall = deepcopy(population[gen_best_idx])

        if gen % 50 == 0 or gen == NUM_GENERATIONS - 1:
            best_penalty = 1.0 / (best_fitness + EPSILON)
            print(f"Поколение {gen:4d} | Лучший штраф ≈ {best_penalty:.3f}")

    return best_overall, 1.0 / (best_fitness + EPSILON) 