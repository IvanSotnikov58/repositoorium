import tkinter as tk  
from tkinter import messagebox, simpledialog, ttk
import os # Импорт модуля os для работы с файловой системой
import math
import random

# Список доступных школ
SCHOOLS = ["Электронная Школа Эстонии", "Narva Eesti E-kool", "Онлайн школа 3"]

SCHOOL_SUBJECTS = { # Словарь с предметами, учителями и тестами для каждой школы
    "Электронная Школа Эстонии": { # Ключ: название школы
        "Математика": {
            "teacher": "Иванов",
            "tests": [
                {"question": "2 + 2", "options": ["3", "4", "5"], "answer": "4"},
                {"question": "5 * 3", "options": ["15", "10", "20"], "answer": "15"},
            ]
        },
        "История": {
            "teacher": "Петрова",
            "tests": [
                {"question": "Когда началась Вторая мировая?", "options": ["1914", "1939", "1945"], "answer": "1939"},
                {"question": "первый президент США", "options": ["Линкольн", "Вашингтон", "Байден"], "answer": "Вашингтон"},
            ]
        },
        "Биология": {
            "teacher": "Сидоренко",
            "tests": [
                {"question": "Сколько хромосом у человека?", "options": ["42", "44", "46"], "answer": "46"},
                {"question": "Какой орган отвечает за дыхание?", "options": ["Печень", "Лёгкие", "Тяжёлые"], "answer": "Лёгкие"},
            ]
        }
    },
    "Narva Eesti E-kool": {
        "Математика": {
            "teacher": "Кузнецов",
            "tests": [
                {"question": "Корень из 9", "options": ["2", "3", "4"], "answer": "3"},
                {"question": "10 / 2", "options": ["2", "5", "10"], "answer": "5"},
            ]
        },
        "История": {
            "teacher": "Громова",
            "tests": [
                {"question": "Когда распался СССР", "options": ["1991", "1985", "2000"], "answer": "1991"},
                {"question": "Год Крещения Руси", "options": ["988", "1066", "1240"], "answer": "988"},
            ]
        },
        "Биология": {
            "teacher": "Лебедева",
            "tests": [
                {"question": "Как называется кровь без клеток", "options": ["Плазма", "Гемоглобин", "Сыворотка"], "answer": "Плазма"},
                {"question": "Что делает печень", "options": ["Фильтрует", "дышит", "не помню"], "answer": "Фильтрует"},
            ]
        }
    },
    "Онлайн школа 3": {
        "Математика": {
            "teacher": "Васильев",
            "tests": [
                {"question": "7 - 3", "options": ["4", "3", "5"], "answer": "4"},
                {"question": "2 * 6", "options": ["10", "12", "14"], "answer": "12"},
            ]
        },
        "История": {
            "teacher": "Мартынова",
            "tests": [
                {"question": "Что произошло в японии в 1945", "options": ["Втрожение пришельцев", "Были скинуты ядерные бомбы", "не знаю"], "answer": "Были скинуты ядерные бомбы"},
                {"question": "Кто открыл Америку", "options": ["Колумб", "Трамп", "Я"], "answer": "Колумб"},
            ]
        },
        "Биология": {
            "teacher": "Чернышев",
            "tests": [
                {"question": "Как называется основа ДНК", "options": ["РНК", "Нуклеотид", "Клетка"], "answer": "Нуклеотид"},
                {"question": "Что производит инсулин", "options": ["Печень", "Почки", "Поджелудочная"], "answer": "Поджелудочная"},
            ]
        }
    }
}




'''
В этом классе реализованы методы для сдачи предметов,
отоброжения вопросов в тестах и получения ответа
'''
class Student:
    '''Класс для представления студента и его оценок'''
    def __init__(self, name, code):
        self.name = name
        self.code = code
        self.grades = {}  # Словарь с оценками: ключ - предмет, значение - список оценок за тесты


    def pass_subject(self, subject, subject_data):
        '''Метод сдачи предмета (проходит тесты по предмету и сохраняет оценки)'''
        scores = []# Список оценок за тесты предмета
        for test in subject_data["tests"]:
            answer = self.ask_question(test)
            if answer == test["answer"]:
                scores.append(5)
            else:
                scores.append(2)
        self.grades[subject] = scores
        return scores
    
    def ask_question(self, test):
        '''Метод отображения вопроса и получения ответа'''
        qwin = tk.Toplevel()
        qwin.title("Вопрос")


        var = tk.StringVar()# хранениe выбранного ответа
        result = []

        def submit():
            '''Функция отправки выбранного варианта и закрытия окна'''
            result.append(var.get())# Добавляем выбранный ответ в result
            qwin.destroy()

        tk.Label(qwin, text=test["question"]).pack(pady=10)# Выводим текст вопроса с отступом по вертикали
        for opt in test["options"]:
            tk.Radiobutton(qwin, text=opt, variable=var, value=opt).pack(anchor="w")

        tk.Button(qwin, text="Ответить", command=submit).pack(pady=10)
        qwin.grab_set()
        qwin.wait_window()
        return result[0] if result else ""# Возвращаем выбранный ответ или пустую строку


   

'''
В этом классе реализованы методы загрузки студентов из файла,
регистрации нового студента, сохранения всех студентов в файл, 
и аутентификации студента
'''
class SchoolManager:
    '''Класс для управления школой (учениками и предметами)'''
    def __init__(self, school_name):
        self.school_name = school_name
        self.filename = f"students_{school_name.replace(' ', '_').lower()}.txt"
        self.subjects = SCHOOL_SUBJECTS[school_name]  
        self.students = self.load_students()          

    
    def load_students(self):
        '''Метод загрузки студентов из файла'''
        students = {}
        # Если файл не существует, то создаётся новый с рандомно сгенерированными учениками.
        if not os.path.exists(self.filename):
            
            first_names_male   = ["Алексей", "Дмитрий", "Иван", "Егор", "Кирилл", "Максим", "Роман", "Павел", "Сергей", "Никита", "Кирило", "Артём", "Сава", "Андрей", "Егор", "Матвей", "Тимур", "Павел", "Георгий", "Виктор", "Фёдор", "Юрий", "Лев", "Владимир"]
            first_names_female = ["Виктория", "Анна", "Мария", "Полина", "Екатерина", "Ольга", "Елена", "Светлана", "Юлия", "Алина", "Аня"]
            last_names_male    = ["Смирнов", "Кузнецов", "Лебедев", "Козлов", "Попович", "Морозов", "Павлов", "Волков", "Соколов", "Гагаринко", "Бутов", "Агартов", "Васильев", "Зайцев", "Павлов"]
            last_names_female  = ["Антонова", "Белова", "Воронова", "Громова", "Давыдова", "Егорова", "Жукова", "Зиновьева", "Исаева", "Кириллова", "Ларина", "Малышева", "Николаева", "Орлова", "Рябова"]

            
            male_combos   = [f"{fn} {ln}" for fn in first_names_male   for ln in last_names_male]
            female_combos = [f"{fn} {ln}" for fn in first_names_female for ln in last_names_female]

            
            selected = random.sample(male_combos, 5) + random.sample(female_combos, 5)
            random.shuffle(selected)
            # Добавляем сгенерированные имена в файл для школы
            with open(self.filename, "w", encoding="utf-8") as f: 
                for full_name in selected:
                    code = str(random.randint(10000000, 99999999))  

                    grades_parts = []# Временный список для хранения строк с оценками для записи в файл
                    grades_dict  = {}# Сgrades_dictловарь для оценок. Используется далее
                    for subject in self.subjects:
                        t1  = random.randint(2, 5)
                        t2  = random.randint(2, 5)
                        avg = (t1 + t2) // 2
                        grades_parts.append(f"{subject}:{t1},{t2},{avg}")
                        grades_dict[subject] = [t1, t2]
                    
                    grades_str = "|".join(grades_parts)
                    f.write(f"{full_name};{code};{grades_str}\n")
                    students[full_name] = {"code": code, "grades": grades_dict}

        else:# Если файл с данными студентов существует загружаем его
            with open(self.filename, "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().split(";")
                    name, code = parts[0], parts[1]
                    grades = {}
                    if len(parts) > 2:# Если есть оценки (больше двух частей)
                        subjects_data = parts[2].split("|")
                        for subj_entry in subjects_data:
                            if ":" in subj_entry:
                                subj_name, marks = subj_entry.split(":")
                                t1, t2, avg = map(int, marks.split(","))
                                grades[subj_name] = [t1, t2]
                    students[name] = {
                        "code": code,
                        "grades": grades
                    }

        return students



    
    def register_student(self, name, code):
        '''Метод регистрации нового студента'''
        if name in self.students:# Проверяем, что имя студента ещё не занято
            return False
        self.students[name] = {"code": code, "grades": {}}
        self.save_students()
        return True

    
    def save_students(self):
        '''Метод сохранения всех студентов в файл'''
        with open(self.filename, "w", encoding="utf-8") as f:
            for name, data in self.students.items():
                line = f"{name};{data['code']}"
                grades_part = []
                for subj, marks in data.get("grades", {}).items():
                    if len(marks) == 2:
                        avg = (marks[0] + marks[1]) // 2
                        grades_part.append(f"{subj}:{marks[0]},{marks[1]},{avg}")
                if grades_part:
                    line += ";" + "|".join(grades_part)
                f.write(line + "\n")

    
    def authenticate(self, name, code):
        '''Метод аутентификации студента (проверка имени и кода)'''
        student = self.students.get(name)
        return student and student["code"] == code


'''
В этом классе реализованы методы для построения интерфейса,
регистрации, входа, открытие главного "портала",
и методы для детального просмотра информации о учениках 
'''
class MainApp:
    '''Главный класс приложения'''
    def __init__(self, root):
        self.root = root # Сохраняем ссылку на главное окно Tkinter
        self.root.title("Электронная школа")
        self.root.geometry("400x300") 
        self.root.minsize(400, 300) 
        self.selected_school = tk.StringVar()# Создаем Tkinter-переменную для хранения выбранной школы
        self.school_manager = None
        self.student = None
        self.build_ui()

    def build_ui(self):
        '''Метод для построения интерфейса'''
        school_frame = tk.LabelFrame(self.root, text="Выбор школы")
        school_frame.pack(fill="x", padx=10, pady=10)

        for school in SCHOOLS: # Создаем радиокнопки для каждой школы из списка SCHOOLS
            tk.Radiobutton(
                school_frame,
                text=school, 
                variable=self.selected_school,
                value=school # Значение, которое будет присвоено переменной при выборе
            ).pack(anchor="w", padx=5, pady=2)

        # Создаем окнo для входа/регистрации
        login_frame = tk.LabelFrame(self.root, text="Вход / Регистрация")
        login_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(login_frame, text="Имя:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        tk.Label(login_frame, text="Код:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        # поле вводa
        self.entry_name = tk.Entry(login_frame, width=30)
        self.entry_code = tk.Entry(login_frame, width=30)
        
        self.entry_name.grid(row=0, column=1, padx=5, pady=5)
        self.entry_code.grid(row=1, column=1, padx=5, pady=5)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(fill="x", padx=10, pady=10)

        tk.Button(btn_frame, text="Зарегистрироваться", command=self.register).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Войти", command=self.login).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Выход", command=self.root.destroy).pack(side="right", padx=5)


    def register(self):
        school = self.selected_school.get() # Получаем выбранную школу из радиокнопок
        if not school:
            messagebox.showwarning("Ошибка", "Сначала выберите школу.")
            return

        # Получаем имя и код из полей ввода
        name = self.entry_name.get().strip()
        code = self.entry_code.get().strip()
        if not name or not code:
            messagebox.showwarning("Ошибка", "Введите имя и код.")
            return

        # Проверяем все остальные школы
        for other in SCHOOLS:
            if other == school: continue # Пропускаем текущую выбранную школу
            fn = f"students_{other.replace(' ', '_').lower()}.txt" 
            if os.path.exists(fn): # Если файл существует, проверяем наличие имени в нем
                with open(fn, "r", encoding="utf-8") as f:
                    for line in f:# Если имя найдено в файле другой школы
                        if line.startswith(name + ";"):
                            messagebox.showerror("Ошибка", 
                                f"Пользователь {name} уже зарегистрирован в школе «{other}».")
                            return

        
        self.school_manager = SchoolManager(school)
        if self.school_manager.register_student(name, code):
            self.student = Student(name, code)
            messagebox.showinfo("Успех", "Вы зарегистрированы!")
            self.root.withdraw()#Закрывается окно с регистрацией/входом и открывается главное окно 
            self.open_portal() 
        else:
            messagebox.showerror("Ошибка", "Имя уже занято.")

    def login(self):
        school = self.selected_school.get()# Получаем выбранную школу
        if not school:
            messagebox.showwarning("Ошибка", "Сначала выберите школу.")
            return

        name = self.entry_name.get().strip()
        code = self.entry_code.get().strip()
        
        self.school_manager = SchoolManager(school)# Создаем менеджер для выбранной школы и получаем данные студента по имени
        student_data = self.school_manager.students.get(name) 
        
        if student_data and student_data["code"] == code: # проверяем что студент существует и код
            self.student = Student(name, code)
            self.student.grades = student_data.get("grades", {})
            messagebox.showinfo("Успех", "Вход выполнен.")
            self.root.withdraw()#Закрывается окно с регистрацией/входом и открывается главное окно 
            self.open_portal()
        else:
            messagebox.showerror("Ошибка", "Неверные имя или код.")


    
    def open_portal(self):
        '''Открытие важной части с оценками, предметами и всем таким'''


        # Открываем новое окно портала
        self.portal = tk.Toplevel(self.root)
        self.portal.title(f"{self.student.name} — {self.selected_school.get()}")
        self.portal.protocol("WM_DELETE_WINDOW", self._on_portal_close)


        tk.Label(self.portal, text=f"Добро пожаловать, {self.student.name}").pack(pady=5)

        columns = ("subject", "teacher", "test1", "test2", "avg")
        self.tree = ttk.Treeview(self.portal, columns=columns, show="headings")
        for col, title in zip(columns, ["Предмет", "Учитель", "Тест 1", "Тест 2", "Средняя"]):
            self.tree.heading(col, text=title)

        self.tree.pack(pady=5)
        self.update_subject_table()

        btn_frame = tk.Frame(self.portal)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Сдать предмет", command=self.pass_subject).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Посмотреть учеников", command=self.open_students_list).pack(side="left", padx=5)

        exit_btn = tk.Button(self.portal, text="Выход", command=self._on_portal_close)
        exit_btn.pack(anchor="se", padx=10, pady=10)  # south-east: правый нижний угол (для тех кто не знает английского)

    def _on_portal_close(self):
        self.portal.destroy()       # Закрываем окно портала и показываем окно входа заново
        self.root.deiconify()       
        
    def open_students_list(self):
        '''Метод для открытия окна со списком всех учеников школы'''
        
        self.students_win = tk.Toplevel(self.root)
        self.students_win.title(f"Ученики — {self.selected_school.get()}")

        columns = ("name", "code")
        tree = ttk.Treeview(self.students_win, columns=columns, show="headings")
        tree.heading("name", text="Имя ученика")
        tree.heading("code", text="Код")

        tree.pack(fill="both", expand=True)

        # Заполняем таблицу данными об учениках
        for name, data in self.school_manager.students.items():
            tree.insert("", "end", values=(name, data["code"]))# Добавляем строку с именем и кодом каждого ученика

        
        def on_student_double_click(event):
            '''Привязываем двойной клик по строке к функции открытия деталей ученика'''
            selected = tree.focus()# Получаем выбранную строку
            if not selected:
                return
            values = tree.item(selected, "values")# Получаем данные из выбранной строки
            self.open_student_details(values[0])  # Открываем детальную информацию об ученике (передаем имя)

        tree.bind("<Double-1>", on_student_double_click) 


    def open_student_details(self, student_name):
        '''Метод для открытия детальной информации об ученике'''
        student_data = self.school_manager.students.get(student_name)
        # Получаем данные ученика по имени из school_manager
        if not student_data:
            messagebox.showerror("Ошибка", "Ученик не найден.")
            return

        #Настройка окна
        details_win = tk.Toplevel(self.root)
        details_win.title(f"Данные ученика — {student_name}")

        tk.Label(details_win, text=f"Имя: {student_name}").pack(anchor="w", padx=10, pady=5)
        tk.Label(details_win, text=f"Код: {student_data['code']}").pack(anchor="w", padx=10, pady=5)

        tk.Label(details_win, text="Оценки:").pack(anchor="w", padx=10, pady=(10, 0))

        columns = ("subject", "test1", "test2", "avg")
        grades_tree = ttk.Treeview(details_win, columns=columns, show="headings")
        for col, title in zip(columns, ["Предмет", "Тест 1", "Тест 2", "Средняя"]):
            grades_tree.heading(col, text=title)
        grades_tree.pack(fill="both", expand=True, padx=10, pady=5)

        grades = student_data.get("grades", {})# Получаем словарь с оценками ученика
        for subject, marks in grades.items():
            if len(marks) == 2:
                avg = (marks[0] + marks[1]) // 2
                grades_tree.insert("", "end", values=(subject, marks[0], marks[1], avg))
            else:
                grades_tree.insert("", "end", values=(subject, "—", "—", "—"))

    def update_subject_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)# Удаляем все строки из таблицы

        for subject, data in self.school_manager.subjects.items():
            teacher = data["teacher"]
            if subject in self.student.grades:
                t1, t2 = self.student.grades[subject]
                avg = math.floor((t1 + t2) / 2) 
            else:
                t1 = t2 = avg = "МА"# Если нет оценок, пишем "МА"
            self.tree.insert("", "end", values=(subject, teacher, t1, t2, avg))  


    def pass_subject(self):
        selected = self.tree.focus()# Получаем выбранную строку в таблице
        if not selected:
            messagebox.showwarning("Ошибка", "Выберите предмет.")
            return

        values = self.tree.item(selected, "values") # Получаем значения выбранной строки
        subject = values[0] 
        result = self.student.pass_subject(subject, self.school_manager.subjects[subject])
        if result:# Запускаем тесты по предмету
            status = "СДАН" if sum(result)/2 > 2 else "НЕ СДАН" 
            messagebox.showinfo("Результат", f"{subject}: {result[0]}, {result[1]} → {math.floor(sum(result)/2)} ({status})")  
            self.update_subject_table()
            self.school_manager.students[self.student.name]["grades"] = self.student.grades
            self.school_manager.save_students()


# === Запуск ===
if __name__ == "__main__":
    root = tk.Tk()# Создаем главное окно приложения
    app = MainApp(root)# Создаем экземпляр приложения
    root.mainloop()# Запускаем цикл обработки событий tkinter
