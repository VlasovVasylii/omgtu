import tkinter as tk
from tkinter import ttk
from math import sqrt, pow

# Исходные данные
critics = {
    'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
                  'Just My Luck': 3.0, 'Superman Returns': 3.5,
                  'You, Me and Dupree': 2.5, 'The Night Listener': 3.0},
    'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
                     'Just My Luck': 1.5, 'Superman Returns': 5.0,
                     'The Night Listener': 3.0, 'You, Me and Dupree': 3.5},
    'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
                         'Superman Returns': 3.5, 'The Night Listener': 4.0},
    'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
                     'The Night Listener': 4.5, 'Superman Returns': 4.0,
                     'You, Me and Dupree': 2.5},
    'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
                     'Just My Luck': 2.0, 'Superman Returns': 3.0,
                     'The Night Listener': 3.0, 'You, Me and Dupree': 2.0},
    'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
                      'The Night Listener': 3.0, 'Superman Returns': 5.0,
                      'You, Me and Dupree': 3.5},
    'Toby': {'Snakes on a Plane': 4.5, 'You, Me and Dupree': 1.0,
             'Superman Returns': 4.0}
}


# Функции коллаборативной фильтрации
def sim_distance(prefs, person1, person2):
    si = {item: 1 for item in prefs[person1] if item in prefs[person2]}
    if len(si) == 0: return 0
    sum_of_squares = sum(pow(prefs[person1][item] - prefs[person2][item], 2)
                         for item in si)
    return 1 / (1 + sum_of_squares)


def sim_pearson(prefs, p1, p2):
    si = {item: 1 for item in prefs[p1] if item in prefs[p2]}
    n = len(si)
    if n == 0: return 0
    sum1 = sum(prefs[p1][it] for it in si)
    sum2 = sum(prefs[p2][it] for it in si)
    sum1Sq = sum(pow(prefs[p1][it], 2) for it in si)
    sum2Sq = sum(pow(prefs[p2][it], 2) for it in si)
    pSum = sum(prefs[p1][it] * prefs[p2][it] for it in si)
    num = pSum - (sum1 * sum2 / n)
    den = sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n))
    return num / den if den != 0 else 0


def get_recommendations(prefs, person, similarity=sim_pearson):
    totals = {}
    simSums = {}
    for other in prefs:
        if other == person:
            continue
        sim = similarity(prefs, person, other)
        if sim <= 0:
            continue
        for item in prefs[other]:
            if item not in prefs[person] or prefs[person][item] == 0:
                totals[item] = totals.get(item, 0) + prefs[other][item] * sim
                simSums[item] = simSums.get(item, 0) + sim

    rankings = [(totals[item] / simSums[item], item) for item in totals]
    rankings.sort(reverse=True)
    return rankings


def top_matches(prefs, person, n=5, similarity=sim_pearson):
    scores = [(similarity(prefs, person, other), other)
              for other in prefs if other != person]
    scores.sort(reverse=True)
    return scores[:n]


# GUI приложение
class MovieRecommenderApp:
    def __init__(self, master):
        self.master = master
        master.title("Movie Recommender System")
        master.geometry("600x400")

        # Стиль
        self.style = ttk.Style()
        self.style.configure('TButton', font=('Arial', 10))
        self.style.configure('TLabel', font=('Arial', 11))

        # Основные элементы
        self.create_widgets()

    def create_widgets(self):
        # Выбор пользователя
        self.user_frame = ttk.Frame(self.master)
        self.user_frame.pack(pady=10)

        self.user_label = ttk.Label(self.user_frame, text="Select User:")
        self.user_label.pack(side=tk.LEFT, padx=5)

        self.user_var = tk.StringVar()
        self.user_combobox = ttk.Combobox(
            self.user_frame,
            textvariable=self.user_var,
            values=list(critics.keys()),
            state="readonly",
            width=25
        )
        self.user_combobox.pack(side=tk.LEFT)
        self.user_combobox.current(0)

        # Выбор метрики
        self.metric_frame = ttk.Frame(self.master)
        self.metric_frame.pack(pady=10)

        self.metric_var = tk.StringVar(value="pearson")
        self.pearson_btn = ttk.Radiobutton(
            self.metric_frame,
            text="Pearson Correlation",
            variable=self.metric_var,
            value="pearson"
        )
        self.euclid_btn = ttk.Radiobutton(
            self.metric_frame,
            text="Euclidean Distance",
            variable=self.metric_var,
            value="euclid"
        )
        self.pearson_btn.pack(side=tk.LEFT, padx=10)
        self.euclid_btn.pack(side=tk.LEFT, padx=10)

        # Кнопка запуска
        self.run_btn = ttk.Button(
            self.master,
            text="Get Recommendations",
            command=self.update_results
        )
        self.run_btn.pack(pady=10)

        # Результаты
        self.result_text = tk.Text(self.master, height=12, width=70)
        self.result_text.pack(padx=10, pady=5)
        self.result_text.insert(tk.END, "Results will be shown here...")
        self.result_text.config(state=tk.DISABLED)

    def update_results(self):
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)

        user = self.user_var.get()
        metric = self.metric_var.get()

        if not user:
            self.result_text.insert(tk.END, "Error: Please select a user!")
            self.result_text.config(state=tk.DISABLED)
            return

        # Вычисление результатов
        similarity = sim_pearson if metric == "pearson" else sim_distance
        recommendations = get_recommendations(critics, user, similarity)
        matches = top_matches(critics, user, similarity=similarity)

        # Форматирование вывода
        self.result_text.insert(tk.END, f"Top matches for {user}:\n")
        for score, name in matches:
            self.result_text.insert(tk.END, f" - {name}: {score:.2f}\n")

        self.result_text.insert(tk.END, "\nRecommended movies:\n")
        for score, movie in recommendations:
            self.result_text.insert(tk.END, f" - {movie}: {score:.2f}\n")

        self.result_text.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    app = MovieRecommenderApp(root)
    root.mainloop()