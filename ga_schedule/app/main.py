from ga import run_ga
from utils import print_schedule, print_conflicts

def main():
    print("Запуск генетического алгоритма для составления расписания...")
    best_schedule, best_penalty = run_ga()
    
    print("\nРезультаты:")
    print(f"Лучший найденный штраф: {best_penalty:.3f}")
    
    print_schedule(best_schedule)
    print_conflicts(best_schedule)

if __name__ == "__main__":
    main() 