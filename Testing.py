import multiprocessing
import matplotlib.pyplot as plt
from Env import Timetable, Course, Classroom, Professor
import GA

professors = [
    Professor("di nucci", [[1, 2], [1, 3]]),
    Professor("smith", [[2, 3], [3, 4]]),
    Professor("johnson", [[2, 3], [3, 4]]),
    Professor("lee", [[1, 2], [1, 3]]),
    Professor("kim", [[2, 3], [3, 4]]),
]

# Define courses and classrooms
courses = [
    Course("ETC", professors[0], 200, 8),
    Course("Math", professors[1], 190, 7, 3),
    Course("Physics", professors[2], 75, 8),
    Course("Programming", professors[3], 75, 9, 3),
    Course("Chemistry", professors[4], 100, 6),
    Course("Biology", professors[0], 120, 6),
    Course("History", professors[1], 80, 6),
    Course("Geography", professors[2], 90, 4),
    Course("Art", professors[3], 60, 4),
    Course("Music", professors[4], 50, 2),
    Course("Philosophy", professors[0], 60, 4),
    Course("Economics", professors[1], 80, 6),
    Course("Literature", professors[2], 70, 6),
    Course("Sociology", professors[3], 85, 6),
    Course("Psychology", professors[4], 90, 8),
    Course("Anthropology", professors[0], 65, 4),
    Course("Political Science", professors[1], 75, 7, 3),
    Course("Linguistics", professors[2], 55, 4),
    Course("Astronomy", professors[3], 85, 6),
    Course("Statistics", professors[4], 95, 9, 3),
    Course("Computer Science", professors[0], 100, 9, 3),
]

classrooms = [
    Classroom("p1", 200),
    Classroom("p2", 75),
    Classroom("p3", 100),
    Classroom("p4", 150),
    Classroom("p5", 90)
]

STRING = "k-m"

def run_ga_test(_generations, mutation_rate, k, m):
    agents = [Timetable(classrooms, courses) for _ in range(50)]
    result, fitness, statistics = GA.run(agents, generations=_generations,
                                         mutation_rate=mutation_rate,
                                         k=k, m=m)
    # Restituisco i due valori: fitness e l'array delle statistiche
    return fitness, statistics

if __name__ == '__main__':
    # Numero di test
    num_tests = 25
    # Numero di processi TOT da lanciare per ogni test
    num_processes = 25
    # Numero di processi massimi in parallelo
    max_workers = 10  # ad esempio 10

    # Pulisco il file dei risultati
    with open('results.txt', 'w'):
        pass

    # Creo la pool con concurrency limitata a max_workers
    pool = multiprocessing.Pool(processes=max_workers)

    for j in range(11, num_tests + 1):
        generations = 500

        # Invio i job alla pool e mi salvo i riferimenti
        async_results = []
        for i in range(num_processes):
            async_results.append(
                pool.apply_async(
                    run_ga_test,
                    args=(generations, 0.9, 20, 20)
                )
            )

        # Ora aspetto che tutti i job finiscano
        # e raccolgo i risultati (fitness e statistics)
        results = []
        statistics_list = []
        for ar in async_results:
            fit, stats = ar.get()  # blocca finché non è pronto
            results.append(fit)
            statistics_list.append(stats)

        print(f"{STRING} ({j})")

        # Plotto le statistiche di tutti i processi
        for stats in statistics_list:
            if stats is not None:
                plt.plot(stats)

        plt.xlabel('Generation')
        plt.ylabel('Normalized Best Fitness')
        plt.title(f'{STRING} k=m={j*2}')
        plt.grid(True)
        plt.xlim(0, generations-1)
        plt.ylim(0, 1)
        plt.savefig(f'plots/{STRING}_{j*2}.png')
        plt.close()

        # Calcolo e salvo la media dei fitness
        valid_results = [r for r in results if r is not None]
        if valid_results:
            mean_value = sum(valid_results) / len(valid_results)
            with open('results.txt', 'a') as f:
                f.write(f"Mean {STRING} {j} generations: {mean_value}\n")

    # Chiudo la pool
    pool.close()
    pool.join()
