import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import json
import csv


FICHIER_JSON = "evenements.json"

# Dictionnaire de traductions
traductions = {
    "fr": {
        "title": "FASO SPORT & CULTURE EVENTS",
        "creer_evenement": "Créer un événement",
        "ajouter_inscrit": "Ajouter un inscrit",
        "rechercher_evenement": "Rechercher un événement",
        "exporter_inscrits": "Exporter les inscrits",
        "rafraichir": "Rafraîchir",
        "type_evenement": "Type d'événement (sportif/culturel) :",
        "date_evenement": "Date (AAAA-MM-JJ) :",
        "lieu_evenement": "Lieu de l’événement :",
        "nom_inscrit": "Nom de l’inscrit :",
        "aucun_evenement": "Sélectionnez un événement.",
        "succes_creation": "Événement créé.",
        "succes_inscrit": "Inscrit ajouté.",
        "incomplet": "Tous les champs sont obligatoires.",
        "aucun_trouve": "Aucun événement trouvé.",
        "rechercher_critere": "Rechercher par 'type' ou 'date' :",
        "rechercher_valeur": "Valeur à rechercher :",
        "export_succes": "Inscrits exportés avec succès.",
        "aucun_selection": "Aucun événement sélectionné.",
        "langue_label": "Langue / Language:"
    },
    "en": {
        "title": "FASO SPORT & CULTURE EVENTS",
        "creer_evenement": "Create Event",
        "ajouter_inscrit": "Add Participant",
        "rechercher_evenement": "Search Event",
        "exporter_inscrits": "Export Participants",
        "rafraichir": "Refresh",
        "type_evenement": "Event type (sport/cultural):",
        "date_evenement": "Date (YYYY-MM-DD):",
        "lieu_evenement": "Event location:",
        "nom_inscrit": "Participant name:",
        "aucun_evenement": "Please select an event.",
        "succes_creation": "Event created.",
        "succes_inscrit": "Participant added.",
        "incomplet": "All fields are required.",
        "aucun_trouve": "No event found.",
        "rechercher_critere": "Search by 'type' or 'date':",
        "rechercher_valeur": "Value to search:",
        "export_succes": "Participants exported successfully.",
        "aucun_selection": "No event selected.",
        "langue_label": "Langue / Language:"
    }
}

# Fonctions de gestion des données
def charger_evenements():
    try:
        with open(FICHIER_JSON, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def sauvegarder_evenements(evenements):
    with open(FICHIER_JSON, "w") as f:
        json.dump(evenements, f, indent=2)

# Interface
class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.langue = "fr"  # Langue par défaut
        self.title(traductions[self.langue]["title"])
        self.geometry("1080x720")
        self.configure(bg="#2c3e50")  # Fond sombre élégant
        self.evenements = charger_evenements()

        # Style des polices
        self.font_title = ("Helvetica", 24, "bold")
        self.font_btn = ("Helvetica", 12)
        self.font_list = ("Consolas", 12)

        # Menu de sélection de la langue
        frame_langue = tk.Frame(self, bg="#2c3e50")
        frame_langue.pack(pady=5)

        label_langue = tk.Label(frame_langue, text=traductions[self.langue]["langue_label"], fg="white", bg="#2c3e50")
        label_langue.pack(side=tk.LEFT)

        self.option_langue = tk.StringVar(value=self.langue)
        menu_langue = tk.OptionMenu(frame_langue, self.option_langue, "fr", "en", command=self.changer_langue)
        menu_langue.pack(side=tk.LEFT)

        # Titre
        self.label_title = tk.Label(self, text=traductions[self.langue]["title"], font=self.font_title, fg="white", bg="#2c3e50")
        self.label_title.pack(pady=20)

        # Liste des événements avec scrollbar
        frame_list = tk.Frame(self, bg="#34495e")
        frame_list.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(frame_list)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listebox = tk.Listbox(frame_list, width=80, height=20, font=self.font_list, yscrollcommand=scrollbar.set,
                                  bg="#ecf0f1", fg="#2c3e50", selectbackground="#2980b9", selectforeground="white", bd=0)
        self.listebox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.listebox.yview)

        # Boutons dans un cadre horizontal
        frame_btn = tk.Frame(self, bg="#2c3e50")
        frame_btn.pack(pady=15)

        self.boutons = []
        btns = [
            (traductions[self.langue]["creer_evenement"], self.creer_evenement),
            (traductions[self.langue]["ajouter_inscrit"], self.ajouter_inscrit),
            (traductions[self.langue]["rechercher_evenement"], self.rechercher_evenement),
            (traductions[self.langue]["exporter_inscrits"], self.exporter_inscrits),
            (traductions[self.langue]["rafraichir"], self.afficher_evenements)
        ]

        for texte, commande in btns:
            btn = tk.Button(frame_btn, text=texte, command=commande, font=self.font_btn,
                            bg="#2980b9", fg="white", activebackground="#3498db", activeforeground="white",
                            relief=tk.FLAT, padx=15, pady=8)
            btn.pack(side=tk.LEFT, padx=10)
            self.boutons.append(btn)

        self.afficher_evenements()
        self.mettre_a_jour_textes()

    def changer_langue(self, valeur):
        self.langue = valeur
        self.mettre_a_jour_textes()

    def mettre_a_jour_textes(self):
        self.title(traductions[self.langue]["title"])
        self.label_title.config(text=traductions[self.langue]["title"])

        textes = [
            traductions[self.langue]["creer_evenement"],
            traductions[self.langue]["ajouter_inscrit"],
            traductions[self.langue]["rechercher_evenement"],
            traductions[self.langue]["exporter_inscrits"],
            traductions[self.langue]["rafraichir"]
        ]
        for btn, texte in zip(self.boutons, textes):
            btn.config(text=texte)

        self.afficher_evenements()

    def afficher_evenements(self):
        self.listebox.delete(0, tk.END)
        for i, event in enumerate(self.evenements):
            ligne = f"{i}. {event['type'].capitalize()} - {event['date']} à {event['lieu']} ({len(event['inscrits'])} inscrit(s))"
            self.listebox.insert(tk.END, ligne)

    def creer_evenement(self):
        type_event = simpledialog.askstring(traductions[self.langue]["type_evenement"], traductions[self.langue]["type_evenement"], parent=self)
        date = simpledialog.askstring(traductions[self.langue]["date_evenement"], traductions[self.langue]["date_evenement"], parent=self)
        lieu = simpledialog.askstring(traductions[self.langue]["lieu_evenement"], traductions[self.langue]["lieu_evenement"], parent=self)
        if type_event and date and lieu:
            self.evenements.append({"type": type_event, "date": date, "lieu": lieu, "inscrits": []})
            sauvegarder_evenements(self.evenements)
            self.afficher_evenements()
            messagebox.showinfo(traductions[self.langue]["succes_creation"], traductions[self.langue]["succes_creation"], parent=self)
        else:
            messagebox.showwarning(traductions[self.langue]["incomplet"], traductions[self.langue]["incomplet"], parent=self)

    def ajouter_inscrit(self):
        selection = self.listebox.curselection()
        if not selection:
            messagebox.showwarning(traductions[self.langue]["aucun_selection"], traductions[self.langue]["aucun_selection"], parent=self)
            return
        index = selection[0]
        nom = simpledialog.askstring(traductions[self.langue]["nom_inscrit"], traductions[self.langue]["nom_inscrit"], parent=self)
        if nom:
            self.evenements[index]["inscrits"].append(nom)
            sauvegarder_evenements(self.evenements)
            self.afficher_evenements()
            messagebox.showinfo(traductions[self.langue]["succes_inscrit"], traductions[self.langue]["succes_inscrit"], parent=self)

    def rechercher_evenement(self):
        critere = simpledialog.askstring(traductions[self.langue]["rechercher_critere"], traductions[self.langue]["rechercher_critere"], parent=self)
        valeur = simpledialog.askstring(traductions[self.langue]["rechercher_valeur"], traductions[self.langue]["rechercher_valeur"], parent=self)
        if critere and valeur:
            resultats = [e for e in self.evenements if e.get(critere) == valeur]
            self.listebox.delete(0, tk.END)
            if resultats:
                for i, event in enumerate(resultats):
                    ligne = f"{event['type'].capitalize()} - {event['date']} à {event['lieu']} ({len(event['inscrits'])} inscrit(s))"
                    self.listebox.insert(tk.END, ligne)
            else:
                self.listebox.insert(tk.END, traductions[self.langue]["aucun_trouve"])

    def exporter_inscrits(self):
        selection = self.listebox.curselection()
        if not selection:
            messagebox.showwarning(traductions[self.langue]["aucun_selection"], traductions[self.langue]["aucun_selection"], parent=self)
            return
        index = selection[0]
        nom_fichier = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if nom_fichier:
            with open(nom_fichier, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Nom des inscrits"])
                for nom in self.evenements[index]["inscrits"]:
                    writer.writerow([nom])
            messagebox.showinfo(traductions[self.langue]["export_succes"], traductions[self.langue]["export_succes"], parent=self)

# Lancer l'application
if __name__ == "__main__":
    app = Application()
    app.mainloop()
