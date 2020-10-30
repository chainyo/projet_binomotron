import mysql.connector
import tkinter as tk
from tkinter import ttk, Label, Entry, Frame, Button, YES, FLAT
from tkinter.ttk import Treeview
import random
import time

'''
Définition des fonctions du programme
'''
# Fonction pour se connecter à la base de données
def connect_bdd () :
    config = {
      'user': 'thomas',
      'password': 'lolmysql',
      'host': 'localhost',
      'port': '8081',
      'database': 'projet_binomotron',
      'raise_on_warnings': True,
    }
    return config

# Récupération de la liste des apprenants 
def recuplist (dic, cur) :   
    # Récupération des de la table des apprenants
    cur.execute("SELECT * FROM students")
    rows = cur.fetchall()
    # Création du dictionnaire avec les apprenants {"id" : "prénom nom"}
    for row in rows :
        dic[row[0]] = dic.get(row[0], '') + f'{row[2]} {row[1]}'

# Fonction pour créer les équipes
def make_teams(dic, num) :
    # Récupération du dictionnaire des apprenants et création d'une liste qui mélange les ids
    keys = list(dic.items())
    random.shuffle(keys)
    # Définition de deux dictionnaires, un sera utilisé pour la BDD, et l'autre pour l'affichage
    ids_teams, names_teams = {}, {}
    # Définition du nombre d'équipes à créer
    nb_teams = len(dic)//num
    # Remplissage des dictionnaires avec les différentes ids et noms
    for i in range(nb_teams):
        ids_teams[i+1] = ', '.join(str(item[0]) for item in keys[i*num:(i+1)*num])
        names_teams[i+1] = ', '.join(str(item[1]) for item in keys[i*num:(i+1)*num])
    # Exception si il reste des membres sans équipe
    if len(ids_teams) < len(dic)/num:
        ids_teams[nb_teams+1] = ', '.join(str(item[0]) for item in keys[nb_teams*num:])
        names_teams[nb_teams+1] = ', '.join(str(item[1]) for item in keys[nb_teams*num:])
    return ids_teams, names_teams

# Envoi du résultat dans la table "projects" de la BDD
def wr_project(cur, bdd, name, time) :
    reference = (name, time)
    cur.execute("""INSERT INTO projects (label, date) VALUES (%s, %s)""", reference)
    bdd.commit()

# Envoi du résultat dans la table "students_grp" de la BDD
def wr_grp(cur, bdd, proj_id, dic) :
    # Iteration pour chaque clefs et chaque valeurs dans le dictionnaire final
    for key, value in dic.items() :
        members_value = value.split(', ')
        for m in members_value :
            ref = (m, key, proj_id)
            cur.execute("""INSERT INTO students_grp (id_student, id_grp, id_project) VALUES (%s, %s, %s)""", ref)
    bdd.commit()

# Création et affichage de la fenêtre des résultats du tirage aléatoire des équipes
def show_res_window(name, dic, window, frame):
    # Fenêtre des équipes
    appframe.destroy()
    window.config(bg=bg_simplon)
    # Titre du tableau
    res_title = Label(window, text=f"{name.upper()}", font=("Helvetica", 30), bg=bg_simplon, fg='white')
    res_title.pack(expand=YES)
    # Création du tableau
    res_tab = Treeview(window, style='mystyle.Treeview', columns=("equip_num", "members"))
    style = ttk.Style()
    style.configure("mystyle.Treeview", font=('Helvetica', 11))
    res_tab.column("equip_num", width=80, anchor='center')
    res_tab.heading("equip_num", text="Equipes")
    res_tab.column("members", width=620, anchor='center')
    res_tab.heading("members", text="Membres")
    res_tab["show"] = "headings"
    res_tab.pack(pady=10)
    for key in dic:
        res_tab.insert('', "end", values=((f"n° {key}"), (f"{dic[key]}")))
    # Bouton retour menu
    reset_btn = Button(window, text='BACK', bg='#212121', fg='white', command=restore_home)
    reset_btn.configure(width=15, relief=FLAT)
    reset_btn.pack(pady=10)
    window.mainloop()

# Retourner au menu principal via bouton "BACK"
def restore_home () :
    root_window.destroy()
    init_prog()

# Monter le pop-up d'alerte si la "taille de l'équipe" n'est pas un entier
def show_popup(frame, txt):
    txt.pack(expand=YES)
    frame.pack(side='left', padx=0, pady=0, anchor='center', expand=1, fill=tk.X)

# Cacher la pop-up d'alerte 
def hide_popup(frame, txt):
    txt.pack_forget()
    frame.pack_forget()

# Permet d'obtenir des placeholders sur la fenêtre principale du programme
class PlaceholderEntry(ttk.Entry):
    def __init__(self, container, placeholder, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.placeholder = placeholder
        self.field_style = kwargs.pop("style", "TEntry")
        self.placeholder_style = kwargs.pop("placeholder_style", self.field_style)
        self["style"] = self.placeholder_style
        self.insert("0", self.placeholder)
        self.bind("<FocusIn>", self._clear_placeholder)
        self.bind("<FocusOut>", self._add_placeholder)
    def _clear_placeholder(self, e):
        if self["style"] == self.placeholder_style:
            self.delete("0", "end")
            self["style"] = self.field_style
    def _add_placeholder(self, e):
        if not self.get():
            self.insert("0", self.placeholder)
            self["style"] = self.placeholder_style

# Commande liée au bouton générer de la fenêtre principale de l'app
# Appelle les autres fonctions pour exécuter la tâche principale
def do_magic():
    # Connexion à la bdd
    config = connect_bdd()
    n = inpnum.get()
    if n.isdigit():
        # Destruction de la popup si elle existe
        hide_popup(pop_infos, pop_txt)
        # Initialisation de variables : dict, string de l'imput et un timer
        dic_students, pname, ptime = {}, inpname.get(), time.strftime('%Y-%m-%d %H:%M:%S')
        n = int(n)
        # Création du curseur pour sélectionner des données de la bdd
        link = mysql.connector.connect(**config)
        cursor = link.cursor()
        # Récupération des données de la table "students"
        recuplist(dic_students, cursor)
        # Création d'un dictionnaire avec les différentes valeurs de la table "students" en fonction de n
        dic_team = make_teams(dic_students, n)
        # Ajout du projet dans la bdd
        wr_project(cursor, link, pname, ptime)
        project_id = cursor.lastrowid
        # Ajout des différents groupes dans la table "students_grp"
        wr_grp(cursor, link, project_id, dic_team[0])
        # Affichage de la fenêtre des résultats en remplaçant l'accueil de l'app
        show_res_window(pname, dic_team[1], root_window, appframe)
        # Fermeture de la BDD
        cursor.close()
        del cursor
    else :
        # Affichage d'une pop-up si la taille de l'équipe n'est pas un entier
        show_popup(pop_infos, pop_txt)

def init_prog () :
    global root_window, appframe, inpnum, inpname, pop_infos, pop_txt
    # Création de la fenêtre principale de l'app
    root_window = tk.Tk()
    style = ttk.Style(root_window)
    style.configure("Placeholder.TEntry", fg="#ECF0F1")
    # Personnalisation de la fenêtre
    root_window.title("Binomotron App")
    root_window.geometry("800x400")
    root_window.config(background=bg_simplon)
    # Différentes frames
    appframe = Frame(root_window, bg=bg_simplon)
    titframe = Frame(appframe, bg=bg_simplon)
    inpframe = Frame(appframe, bg=bg_simplon)
    btnframe = Frame(appframe, bg=bg_simplon)
    # Titres de l'app
    label_title = Label(titframe, text="TEAM GENERATOR", font=("Helvetica", 38), bg=bg_simplon, fg="white")
    label_title.pack()
    sub_title = Label(titframe, text="by Jérémy & Thomas", font=("Helvetica", 10), bg=bg_simplon, fg="white")
    sub_title.pack()
    # Inputs
    inpname = PlaceholderEntry(inpframe, "project name", font=("Helvetica", "8", "italic"))
    inpname.pack(pady=5)
    inpnum = PlaceholderEntry(inpframe, "team size", font=("Helvetica", "8", "italic"))
    inpnum.pack()
    # Config de la popup
    pop_infos = Frame(root_window, width=50, height=50, bg='#212121')
    pop_txt = Label(pop_infos, text='Warning: team size must be integer', bg="#212121", fg='white')
    # Bouton pour générer
    genbtn = Button(btnframe, text="GENERATE", bg="#212121", fg="white", command=do_magic)
    genbtn.configure(width=15, relief=FLAT) 
    genbtn.pack()
    # Affichage des frames
    appframe.pack(expand=YES)
    titframe.pack(expand=YES, pady=20)
    inpframe.pack(expand=YES, pady=40)
    btnframe.pack(expand=YES)
    # Affichage de la fenêtre
    root_window.mainloop()

# Variable de couleur pour tkinter
bg_simplon = '#CE0036'

# Start
init_prog()