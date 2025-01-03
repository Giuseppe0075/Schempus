import threading
import tkinter as tk
from tkinter import ttk, messagebox
from Env import Professor, Subjects, Course, Classroom, Timetable
import pickle
import random
import GA
import os

DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri"]
HOURS = [f"{h}" for h in range(8)]  # 0..7 to match your zero-based hour indexing
HOURS_PER_DAY = 8

# Make a dictionary to map numeric values to string names (for combobox display)
SUBJECT_NAMES = {
    Subjects.COMPUTER_SCIENCE: "COMPUTER_SCIENCE",
    Subjects.PHYSICS: "PHYSICS",
    Subjects.MATH: "MATH",
    Subjects.CHEMISTRY: "CHEMISTRY",
    Subjects.BIOLOGY: "BIOLOGY",
    Subjects.HISTORY: "HISTORY",
    Subjects.GEOGRAPHY: "GEOGRAPHY",
    Subjects.ART: "ART",
    Subjects.MUSIC: "MUSIC",
    Subjects.PHILOSOPHY: "PHILOSOPHY",
    Subjects.ECONOMICS: "ECONOMICS",
    Subjects.LITERATURE: "LITERATURE",
    Subjects.SOCIOLOGY: "SOCIOLOGY",
    Subjects.PSYCHOLOGY: "PSYCHOLOGY",
    Subjects.ANTHROPOLOGY: "ANTHROPOLOGY",
    Subjects.POLITICAL_SCIENCE: "POLITICAL_SCIENCE",
    Subjects.LINGUISTICS: "LINGUISTICS",
    Subjects.ASTRONOMY: "ASTRONOMY",
    Subjects.STATISTICS: "STATISTICS",
}

professors = [
    Professor("di nucci"),
    Professor("smith"),
    Professor("johnson"),
    Professor("lee"),
    Professor("kim"),
]

# Define courses and classrooms
courses = [
Course("ETC", professors[0], 200, 8, Subjects.COMPUTER_SCIENCE),
Course("Math", professors[1], 190, 7, Subjects.MATH, 3),
Course("Physics", professors[2], 75, 8, Subjects.PHYSICS),
Course("Programming", professors[3], 75, 9, Subjects.COMPUTER_SCIENCE, 3),
Course("Chemistry", professors[4], 100, 6, Subjects.CHEMISTRY),
Course("Biology", professors[0], 120, 6, Subjects.BIOLOGY),
Course("History", professors[1], 80, 6, Subjects.HISTORY),
Course("Geography", professors[2], 90, 4, Subjects.GEOGRAPHY),
Course("Art", professors[3], 60, 4, Subjects.ART),
Course("Music", professors[4], 50, 2, Subjects.MUSIC),
Course("Philosophy", professors[0], 60, 4, Subjects.PHILOSOPHY),
Course("Economics", professors[1], 80, 6, Subjects.ECONOMICS),
Course("Literature", professors[2], 70, 6, Subjects.LITERATURE),
Course("Sociology", professors[3], 85, 6, Subjects.SOCIOLOGY),
Course("Psychology", professors[4], 90, 8, Subjects.PSYCHOLOGY),
Course("Anthropology", professors[0], 65, 4, Subjects.ANTHROPOLOGY),
Course("Political Science", professors[1], 75, 7, Subjects.POLITICAL_SCIENCE, 3),
Course("Linguistics", professors[2], 55, 4, Subjects.LINGUISTICS),
Course("Astronomy", professors[3], 85, 6, Subjects.ASTRONOMY),
Course("Statistics", professors[4], 95, 9, Subjects.STATISTICS, 3),
Course("Programming 1", professors[0], 100, 9, Subjects.COMPUTER_SCIENCE, 3),
]

classrooms = [
    Classroom("p1", 200),
    Classroom("p2", 75),
    Classroom("p3", 100),
    Classroom("p4", 150),
    Classroom("p5", 90),
    Classroom("labCS", 200, True, Subjects.COMPUTER_SCIENCE),
    Classroom("labS", 95, True, Subjects.STATISTICS),
    Classroom("labPS", 90, True, Subjects.POLITICAL_SCIENCE),
    Classroom("labM", 200, True, Subjects.MATH),
]


def toggle_subject_field(subject_combobox, is_lab_var):
    """
    Enable the subject combobox if is_lab_var is True, else disable it.
    """
    if is_lab_var.get():
        subject_combobox.configure(state="readonly")  # or normal
    else:
        subject_combobox.set("")
        subject_combobox.configure(state="disabled")


def _generate_course_colors(num_courses):
    """
    Generate a color map for each course index (0..num_courses-1).
    Returns a dict: { index: "#RRGGBB", ... }
    """
    color_map = {}
    for i in range(num_courses):
        # Generate a random pastel color or any random color
        r = random.randint(100, 255)
        g = random.randint(100, 255)
        b = random.randint(100, 255)
        color_map[i] = f"#{r:02x}{g:02x}{b:02x}"
    return color_map

class TimetableApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.color_map = None
        self.title("University Timetable Generator")
        self.geometry("600x400")

        welcome_label = tk.Label(self, text="Welcome to the University Timetable Generator!")
        welcome_label.pack(pady=20)

        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        add_prof_button = tk.Button(button_frame, text="Add Professor", command=self.add_professor)
        add_prof_button.grid(row=0, column=0, padx=5)

        add_course_button = tk.Button(button_frame, text="Add Course", command=self.add_course)
        add_course_button.grid(row=0, column=1, padx=5)

        add_classroom_button = tk.Button(button_frame, text="Add Classroom", command=self.add_classroom)
        add_classroom_button.grid(row=0, column=2, padx=5)

        calculate_tt_button = tk.Button(button_frame, text="Calculate Timetable", command=self.calculate_timetable)
        calculate_tt_button.grid(row=0, column=3, padx=5)

        # Data placeholders
        self.professors = professors
        self.courses = courses
        self.classrooms = classrooms

        # This is your Timetable object, which has .timetable inside
        self.timetable = None

        # We track the last time we loaded best_agent.pkl
        self.last_best_agent_mtime = 0

        # Create a container for the timetable Canvas with scrollbars
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        xscrollbar = tk.Scrollbar(container, orient="horizontal")
        yscrollbar = tk.Scrollbar(container, orient="vertical")
        xscrollbar.pack(side="bottom", fill="x")
        yscrollbar.pack(side="right", fill="y")

        self.canvas = tk.Canvas(container,
                                bg="white",
                                xscrollcommand=xscrollbar.set,
                                yscrollcommand=yscrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)

        xscrollbar.config(command=self.canvas.xview)
        yscrollbar.config(command=self.canvas.yview)

        # Mouse wheel binding
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        def _on_shiftmousewheel(event):
            self.canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")

        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)
        self.canvas.bind_all("<Shift-MouseWheel>", _on_shiftmousewheel)

        # Start polling the file every 3 seconds
        self.after(3000, self.poll_best_agent_file)

    def poll_best_agent_file(self):
        """
        Checks if 'best_agent.pkl' has been updated. If so, load the new Timetable
        and update the display. Then schedule another check in 3s.
        """
        file_path = "best_agent.pkl"
        if os.path.isfile(file_path):
            mtime = os.path.getmtime(file_path)
            if mtime > self.last_best_agent_mtime:
                self.last_best_agent_mtime = mtime
                # Load the new best timetable
                try:
                    with open(file_path, "rb") as f:
                        new_best_timetable = pickle.load(f)
                    # Assign & redraw
                    self.timetable = new_best_timetable
                    self.redraw_timetable()
                except Exception as e:
                    print(f"Error loading timetable from {file_path}: {e}")

        # Schedule again in 3000 ms
        self.after(3000, self.poll_best_agent_file)

    def redraw_timetable(self):
        """
        Clears and re-draws the timetable in 'self.canvas' using 'self.timetable'.
        We reuse 'self.color_map' to keep colors consistent.
        """
        self.canvas.delete("all")  # Clear previous drawing

        if not self.timetable or not self.timetable.classrooms or not self.timetable.courses:
            # Nothing to draw
            return

        from collections import defaultdict

        # Build collisions dict
        lessons_by_slot = defaultdict(list)
        for course_index, lessons in enumerate(self.timetable.timetable):
            for (day, c_idx, hour, lab) in lessons:
                lessons_by_slot[(day, c_idx, hour)].append((course_index, lab))

        # Instead of regenerating a random map each time, we use self.color_map:
        # if you haven't set self.color_map yet, you can do a safety check:
        if not self.color_map:
            # If it doesn't exist yet, generate it once. But ideally,
            # you generate it right after you've finalized your courses.
            self.color_map = _generate_course_colors(len(self.timetable.courses))

        color_map = self.color_map  # Reuse the same map each time

        # Layout constants
        header_height = 30
        left_label_width = 60
        col_width = 150
        row_height = HOURS_PER_DAY * 30  # 8 hours * 30 px

        total_width = left_label_width + len(self.timetable.classrooms) * col_width
        total_height = header_height + 5 * row_height

        # Draw classroom headers
        for c_index, classroom in enumerate(self.timetable.classrooms):
            x0 = left_label_width + c_index * col_width
            x1 = x0 + col_width
            y0 = 0
            y1 = header_height
            self.canvas.create_rectangle(x0, y0, x1, y1, fill="#cccccc", outline="black")
            self.canvas.create_text(
                (x0 + x1) / 2, (y0 + y1) / 2,
                text=classroom.name, font=("Arial", 10, "bold")
            )

        # Day labels
        for day_index in range(5):
            x0 = 0
            x1 = left_label_width
            y0 = header_height + day_index * row_height
            y1 = y0 + row_height
            self.canvas.create_rectangle(x0, y0, x1, y1, fill="#dddddd", outline="black")
            self.canvas.create_text(
                (x0 + x1) / 2, (y0 + y1) / 2,
                text=DAYS[day_index], font=("Arial", 10, "bold")
            )

        # Grid lines
        for day_index in range(5):
            top_y = header_height + day_index * row_height
            for hour in range(HOURS_PER_DAY + 1):
                y = top_y + hour * (row_height / HOURS_PER_DAY)
                self.canvas.create_line(left_label_width, y, total_width, y, fill="black")

        for c_index in range(len(self.timetable.classrooms) + 1):
            x = left_label_width + c_index * col_width
            self.canvas.create_line(x, 0, x, total_height, fill="black")

        # Fill subcells
        cell_height = row_height / HOURS_PER_DAY
        for day_index in range(5):
            day_top_y = header_height + day_index * row_height
            for hour in range(HOURS_PER_DAY):
                subcell_y0 = day_top_y + hour * cell_height
                subcell_y1 = subcell_y0 + cell_height
                for c_idx in range(len(self.timetable.classrooms)):
                    subcell_x0 = left_label_width + c_idx * col_width
                    subcell_x1 = subcell_x0 + col_width

                    collisions = lessons_by_slot.get((day_index, c_idx, hour), [])
                    if not collisions:
                        # FREE
                        self.canvas.create_rectangle(
                            subcell_x0, subcell_y0, subcell_x1, subcell_y1,
                            fill="white", outline="black"
                        )
                        self.canvas.create_text(
                            (subcell_x0 + subcell_x1) / 2,
                            (subcell_y0 + subcell_y1) / 2,
                            text="FREE", font=("Arial", 9)
                        )
                    else:
                        distinct_courses = set(ci for (ci, _) in collisions)
                        if len(distinct_courses) == 1:
                            # One distinct course => color cell
                            (course_idx, lab_flag) = collisions[0]
                            fill_color = color_map[course_idx]  # <-- reusing the stable color map
                            self.canvas.create_rectangle(
                                subcell_x0, subcell_y0, subcell_x1, subcell_y1,
                                fill=fill_color, outline="black"
                            )

                            lines = []
                            for (ci, lb) in collisions:
                                crs_obj = self.timetable.courses[ci]
                                line_txt = f"{crs_obj.name} (ID: {ci})"
                                if lb:
                                    line_txt = "Lab: " + line_txt
                                lines.append(line_txt)

                            text_content = "\n".join(lines)
                            self.canvas.create_text(
                                (subcell_x0 + subcell_x1) / 2,
                                (subcell_y0 + subcell_y1) / 2,
                                text=text_content,
                                font=("Arial", 9),
                                width=col_width - 10
                            )
                        else:
                            # Collision => gray
                            self.canvas.create_rectangle(
                                subcell_x0, subcell_y0, subcell_x1, subcell_y1,
                                fill="gray", outline="black"
                            )
                            lines = []
                            for (ci, lb) in collisions:
                                crs_obj = self.timetable.courses[ci]
                                line_txt = f"{crs_obj.name} (ID: {ci})"
                                if lb:
                                    line_txt = "Lab: " + line_txt
                                lines.append(line_txt)

                            text_content = "\n".join(lines)
                            self.canvas.create_text(
                                subcell_x0 + 5, subcell_y0 + 5,
                                anchor="nw",
                                text=text_content,
                                font=("Arial", 9),
                                width=col_width - 10
                            )

        self.canvas.configure(scrollregion=(0, 0, total_width, total_height))

    def add_professor(self):
        """ Opens a popup window to input professor data (name + a 5×8 grid). """
        professor_window = tk.Toplevel(self)
        professor_window.title("Add Professor")
        professor_window.geometry("500x400")

        # --- Professor Name ---
        name_label = tk.Label(professor_window, text="Professor Name:")
        name_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")

        name_entry = tk.Entry(professor_window)
        name_entry.grid(row=0, column=1, padx=10, pady=5, columnspan=8, sticky="w")

        # --- Button to save ---
        add_button = tk.Button(
            professor_window,
            text="Add Professor",
            command=lambda: self.save_professor(name_entry.get(), professor_window)
        )
        add_button.grid(row=3 + len(DAYS), column=0, columnspan=9, pady=10)

    def save_professor(self, name, window):
        """Gathers [day, hour] for each checked cell and creates a Professor."""
        if not name.strip():
            messagebox.showerror("Error", "Professor name cannot be empty.")
            return
        new_prof = Professor(name)
        self.professors.append(new_prof)

        print(f"Added Professor: {new_prof.name}")

        # Close the popup
        window.destroy()

    def add_course(self):
        """
        Open a popup window to input the following course data:
          - name
          - professor (choose from existing self.professors)
          - number_of_students (integer)
          - hours_for_week (integer)
          - subject (choose from Subjects)
          - lab_hours (optional, integer)
        """
        if not self.professors:
            messagebox.showwarning("No Professors", "Please add at least one professor before adding a course.")
            return

        course_window = tk.Toplevel(self)
        course_window.title("Add Course")
        course_window.geometry("400x400")

        # Course Name
        tk.Label(course_window, text="Course Name:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        name_entry = tk.Entry(course_window)
        name_entry.grid(row=0, column=1, padx=10, pady=10)

        # Professor Selection
        tk.Label(course_window, text="Professor:").grid(row=1, column=0, padx=10, pady=10, sticky="e")

        # We'll create a Combobox with the names of the professors
        professor_names = [prof.name for prof in self.professors]
        prof_combobox = ttk.Combobox(course_window, values=professor_names, state="readonly")
        prof_combobox.grid(row=1, column=1, padx=10, pady=10)
        prof_combobox.set(professor_names[0])  # Set a default selection

        # Number of Students
        tk.Label(course_window, text="Number of Students:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        num_students_entry = tk.Entry(course_window)
        num_students_entry.grid(row=2, column=1, padx=10, pady=10)

        # Hours per Week
        tk.Label(course_window, text="Hours per Week:").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        hours_week_entry = tk.Entry(course_window)
        hours_week_entry.grid(row=3, column=1, padx=10, pady=10)

        # Subject Selection
        tk.Label(course_window, text="Subject:").grid(row=4, column=0, padx=10, pady=10, sticky="e")
        subject_values = list(SUBJECT_NAMES.values())  # e.g., ["COMPUTER_SCIENCE", "PHYSICS", ...]
        subject_combobox = ttk.Combobox(course_window, values=subject_values, state="readonly")
        subject_combobox.grid(row=4, column=1, padx=10, pady=10)
        subject_combobox.set(subject_values[0])  # default

        # Lab Hours (optional)
        tk.Label(course_window, text="Lab Hours (optional):").grid(row=5, column=0, padx=10, pady=10, sticky="e")
        lab_hours_entry = tk.Entry(course_window)
        lab_hours_entry.grid(row=5, column=1, padx=10, pady=10)

        # Save Button
        save_button = tk.Button(
            course_window,
            text="Add Course",
            command=lambda: self.save_course(
                name=name_entry.get(),
                professor_name=prof_combobox.get(),
                students_str=num_students_entry.get(),
                hours_str=hours_week_entry.get(),
                subject_str=subject_combobox.get(),
                lab_str=lab_hours_entry.get(),
                window=course_window
            )
        )
        save_button.grid(row=6, column=0, columnspan=2, pady=20)

    def save_course(self, name, professor_name, students_str, hours_str, subject_str, lab_str, window):
        """
        Validate inputs, create the Course object, and store in self.courses.
        """
        # Basic validation
        if not name.strip():
            messagebox.showerror("Error", "Course name cannot be empty.")
            return

        if not professor_name or professor_name not in [p.name for p in self.professors]:
            messagebox.showerror("Error", "Please select a valid professor.")
            return

        # Convert students to int
        try:
            number_of_students = int(students_str)
        except ValueError:
            messagebox.showerror("Error", "Number of students must be an integer.")
            return

        # Convert hours_for_week to int
        try:
            hours_for_week = int(hours_str)
        except ValueError:
            messagebox.showerror("Error", "Hours per week must be an integer.")
            return

        # Convert subject_str to the corresponding Subjects enum
        # We reverse the SUBJECT_NAMES dictionary to find the enum key
        subject_map = {v: k for k, v in SUBJECT_NAMES.items()}
        if subject_str not in subject_map:
            messagebox.showerror("Error", "Invalid subject selected.")
            return
        subject_enum_value = subject_map[subject_str]

        # Lab Hours (optional), default to 0 if empty
        lab_hours = 0
        if lab_str.strip():
            try:
                lab_hours = int(lab_str)
            except ValueError:
                messagebox.showerror("Error", "Lab hours must be an integer if provided.")
                return

        # Find the actual Professor object
        selected_professor = None
        for p in self.professors:
            if p.name == professor_name:
                selected_professor = p
                break

        if not selected_professor:
            messagebox.showerror("Error", "Selected professor not found.")
            return

        # Create the Course object
        new_course = Course(
            name=name,
            professor=selected_professor,
            number_of_students=number_of_students,
            hours_for_week=hours_for_week,
            subject=subject_enum_value,
            lab_hours=lab_hours
        )

        # Add the course to our list
        self.courses.append(new_course)
        print(f"Added Course: {new_course.name}, Professor: {new_course.professor}, "
              f"Students: {new_course.number_of_students}, Hours/Week: {new_course.hours_for_week}, "
              f"Subject: {subject_str}, Lab Hours: {new_course.lab_hours}")

        # Close the popup window
        window.destroy()

    def add_classroom(self):
        """
        Open a popup window to input classroom data:
          - name (string)
          - capacity (int)
          - is_lab (boolean)
          - subject (only if is_lab is True)
        """
        room_window = tk.Toplevel(self)
        room_window.title("Add Classroom")
        room_window.geometry("400x300")

        # Name
        tk.Label(room_window, text="Classroom Name:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        name_entry = tk.Entry(room_window)
        name_entry.grid(row=0, column=1, padx=10, pady=10)

        # Capacity
        tk.Label(room_window, text="Capacity:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        capacity_entry = tk.Entry(room_window)
        capacity_entry.grid(row=1, column=1, padx=10, pady=10)

        # Is Lab?
        is_lab_var = tk.BooleanVar(value=False)
        tk.Label(room_window, text="Is Lab?").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        is_lab_check = tk.Checkbutton(room_window, variable=is_lab_var,
                                      command=lambda: toggle_subject_field(subject_combobox, is_lab_var))
        is_lab_check.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        # Subject combobox (initially disabled if not lab)
        tk.Label(room_window, text="Subject (if lab):").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        subject_values = list(SUBJECT_NAMES.values())  # e.g. ["COMPUTER_SCIENCE", "PHYSICS", ...]
        subject_combobox = ttk.Combobox(room_window, values=subject_values, state="disabled")
        subject_combobox.grid(row=3, column=1, padx=10, pady=10)

        # Add button
        tk.Button(
            room_window,
            text="Add Classroom",
            command=lambda: self.save_classroom(
                name_entry.get(),
                capacity_entry.get(),
                is_lab_var.get(),
                subject_combobox.get(),
                room_window
            )
        ).grid(row=4, column=0, columnspan=2, pady=20)

    def save_classroom(self, name, capacity_str, is_lab, subject_str, window):
        """
        Validate the input and create a Classroom object. If 'is_lab' is True,
        we require a subject to be selected.
        """
        # Validate name
        if not name.strip():
            messagebox.showerror("Error", "Classroom name cannot be empty.")
            return

        # Validate capacity
        try:
            capacity = int(capacity_str)
        except ValueError:
            messagebox.showerror("Error", "Capacity must be an integer.")
            return

        # If is_lab is True, then subject_str must be valid
        if is_lab:
            if not subject_str or subject_str not in SUBJECT_NAMES.values():
                messagebox.showerror("Error", "Please select a valid subject for the laboratory.")
                return
            # Convert subject_str to enum
            inv_map = {v: k for k, v in SUBJECT_NAMES.items()}
            subject_enum_value = inv_map[subject_str]
            new_room = Classroom(name, capacity, True, subject_enum_value)
        else:
            new_room = Classroom(name, capacity, False, None)

        # Add to our list
        self.classrooms.append(new_room)
        print(f"Added Classroom: {new_room.name}, Capacity: {new_room.capacity}, "
              f"Is Lab? {new_room.is_lab}, Subject: {getattr(new_room, 'subject', None)}")

        # Close window
        window.destroy()

    def calculate_timetable(self):
        """
        Calculate the timetable using the current data.
        Now with a REAL progress bar that updates each generation,
        unclosable popup, and a 'Stop' button to cancel.
        """
        if not self.professors or not self.courses or not self.classrooms:
            messagebox.showinfo("Data Missing", "Please add Professors, Courses, and Classrooms first.")
            return
        self.color_map = _generate_course_colors(len(self.courses))
        
        # Create a popup for progress
        progress_window = tk.Toplevel(self)
        progress_window.title("Calculating Timetable")

        # Disable the close button (WM close) so user must use Stop or wait
        progress_window.protocol("WM_DELETE_WINDOW", lambda: None)

        label = tk.Label(progress_window, text="Calculating Timetable, please wait...")
        label.pack(pady=10, padx=10)

        progress_bar = ttk.Progressbar(progress_window, orient="horizontal", length=300, mode="determinate")
        progress_bar.pack(pady=10, padx=10)
        progress_bar["maximum"] = 100
        progress_bar["value"] = 0

        # A flag to indicate stop
        self._stop_ga = False

        # Stop button
        def on_stop():
            # Set the stop flag
            self._stop_ga = True
            # You might also want to close the popup immediately, or wait until
            # the thread sees _stop_ga and returns. If you want it immediate, do:
            # progress_window.destroy()
            # But typically, let's keep the popup open until the thread sees the flag.
            pass

        stop_button = tk.Button(progress_window, text="Stop", command=on_stop)
        stop_button.pack(pady=10)

        def update_progress(current_gen, total_gen):
            progress_percent = (current_gen / total_gen) * 100
            # Update the progress bar in the main thread
            self.after(0, lambda: progress_bar.config(value=progress_percent))

        def stop_check():
            return self._stop_ga  # True if user pressed Stop

        def worker():
            agents = [Timetable(self.classrooms, self.courses) for _ in range(50)]
            best_timetable, best_fitness = GA.run(
                agents,
                generations=5000,
                mutation_rate=0.9,
                k=20,
                m=20,
                update_callback=update_progress,
                stop_check=stop_check
            )
            self.timetable = best_timetable

            # Close the popup (in the main thread)
            self.after(0, progress_window.destroy)
            if self._stop_ga:
                messagebox.showwarning("Stopped", "Timetable calculation was canceled.")
            else:
                messagebox.showinfo("Done", "Timetable generated!")

        t = threading.Thread(target=worker, daemon=True)
        t.start()

if __name__ == "__main__":
    app = TimetableApp()
    app.mainloop()