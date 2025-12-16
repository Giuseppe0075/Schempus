# Schempus

Schempus is an application that uses an adaptive genetic algorithm to generate optimized timetables for universities. It provides a graphical user interface to input data, run the optimization process, and visualize the resulting schedule in real-time.

## Key Features

- **Automated Timetable Scheduling**: Generates schedules for multiple courses, classrooms, and laboratories.
- **Genetic Algorithm Optimization**: Finds optimal solutions based on a comprehensive fitness function that considers:
    - **Collision Avoidance**: Prevents multiple classes from being scheduled in the same room at the same time.
    - **Professor Conflict Avoidance**: Ensures a professor is not scheduled to teach more than one class simultaneously.
    - **Classroom Capacity**: Assigns courses to rooms that can accommodate the number of students, penalizing over-capacity and rewarding efficient use of space.
    - **Lab Allocation**: Correctly assigns lab sessions to dedicated laboratory rooms and theory classes to standard classrooms.
    - **Weekly & Daily Distribution**: Optimizes for consecutive lesson hours and minimizes classroom changes for the same course within a day.
- **Visual Application**: A Tkinter-based GUI for managing data and visualizing the timetable as it's being calculated.
- **Example Dataset**: Includes a pre-configured dataset based on the UNISA 2024/25 first semester computer science schedule.

## How It Works

The core of Schempus is a genetic algorithm implemented in `GA.py`. Each potential timetable is an "agent" or "individual" in a population. The algorithm evolves the population over generations to find a timetable with the lowest penalty score (i.e., highest fitness).

1.  **Representation**: A timetable is represented as a list of courses, where each course has a list of its scheduled lessons. A lesson is defined by `[day, classroom_index, hour, is_lab]`.
2.  **Fitness Evaluation**: Each agent is evaluated by a fitness function (`GA.fitness`) which calculates a penalty score based on the weighted sum of constraint violations (collisions, professor conflicts, capacity issues, etc.). A lower score is better.
3.  **Selection**: The algorithm uses **k-way tournament selection** to choose the best-performing agents from the current generation to create the next one.
4.  **Crossover**: Parent agents are combined by swapping course schedules to create offspring, inheriting traits from both.
5.  **Adaptive Mutation**: To explore the solution space and avoid local minima, lessons within an agent's timetable are randomly mutated. The mutation range (for day, classroom, and hour) decreases over generations, an approach similar to simulated annealing, allowing for large changes early on and fine-tuning in later stages.
6.  **Live Updates**: The application saves the best-performing agent to `best_agent.pkl` after each generation where an improvement is found. The GUI polls this file and updates the visual timetable, allowing the user to see the optimization process in real-time.

## The Application

The main entry point is `Application.py`, which launches a GUI with the following functionalities:

- **Data Management**: Add, view, and manage professors, courses, and classrooms.
- **Use Example Data**: Quickly load a sample dataset for a demonstration.
- **Calculate Timetable**: Starts the genetic algorithm. A progress bar shows the current generation, and the best fitness score is updated live. The process can be stopped at any time.
- **Timetable Visualization**: A grid displays the schedule, organized by classroom and day. Each cell shows the scheduled course and professor. Collisions are highlighted for easy identification.

## Project Structure

```
├── Application.py      # Main entry point with the Tkinter GUI.
├── GA.py               # Implements the Genetic Algorithm (fitness, selection, crossover, mutation).
├── Env.py              # Defines the core data structures (Professor, Course, Classroom, Timetable).
├── Testing.py          # Script for running experiments and benchmarking GA parameters.
└── Statistics/         # Contains results from parameter tuning experiments.
```

## Requirements

- **Python 3.12**

## Installation and Usage

1.  Clone the repository:
    ```bash
    git clone https://github.com/Giuseppe0075/Schempus.git
    cd Schempus
    ```
2.  Run the application:
    ```bash
    python Application.py
    ```

## Contact

- **Author**: Giuseppe Sica
- **Email**: giuseppesica03@gmail.com
- **LinkedIn**: https://www.linkedin.com/in/03-giuseppe-sica/
- **GitHub**: @Giuseppe0075
