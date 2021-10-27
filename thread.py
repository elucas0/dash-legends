import threading

"""
Sert à la programmation dite "asynchrone" ou "parallele"
Les joueurs de notre jeu s'actualiseront en parallele (en meme temps)
leur fonction sera lancer en meme temps (plus besoin d'attendre l'actualisation du joueur preceddent)
"""


class MyThread(threading.Thread):
    def __init__(self, fonction):
        threading.Thread.__init__(self)
        self.fonction = fonction

    def run(self):
        """
        Lancer la fonction en mettant les parenthèses
        """
        self.fonction()
