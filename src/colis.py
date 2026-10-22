import random


class Colis:
    __slots__ = ("id", "poids", "valeur", "priorite", "destination")

    def __init__(self, id, poids, valeur, priorite, destination):
        self.id = id
        self.poids = poids
        self.valeur = valeur
        self.priorite = priorite
        self.destination = destination

    def __str__(self):
        return (f"{self.id:>7} | {self.poids:>5} kg | {self.valeur:>6} € | "
                f"prio {self.priorite} | {self.destination}")


class Entrepot:
    def __init__(self):
        self.colis = []
        self.index = {}

    def ajouter(self, c):
        if c.id in self.index:
            return False
        self.colis.append(c)
        self.index[c.id] = c
        return True

    def rechercher(self, id):
        return self.index.get(id)

    def rechercher_lineaire(self, id):
        for c in self.colis:
            if c.id == id:
                return c
        return None

    def __len__(self):
        return len(self.colis)

    def statistiques(self):
        n = len(self.colis)
        if n == 0:
            return None
        poids_total = valeur_totale = 0
        par_prio = [0] * 6
        for c in self.colis:
            poids_total += c.poids
            valeur_totale += c.valeur
            par_prio[c.priorite] += 1
        return {
            "nombre": n,
            "poids_total": poids_total,
            "valeur_totale": valeur_totale,
            "poids_moyen": poids_total / n,
            "valeur_moyenne": valeur_totale / n,
            "par_priorite": par_prio[1:],
        }


VILLES = ["Paris", "Lille", "Lyon", "Marseille", "Bordeaux", "Nantes", "Toulouse"]


def generer_colis(entrepot, n, graine=None):
    rng = random.Random(graine)
    depart = max(entrepot.index, default=100) + 1
    for i in range(n):
        entrepot.ajouter(Colis(
            depart + i,
            rng.randint(1, 30),
            rng.randint(5, 100),
            rng.randint(1, 5),
            rng.choice(VILLES),
        ))


def charger_exemple(entrepot):
    for data in [(101, 8, 20, 2, "Paris"), (102, 3, 10, 5, "Lille"),
                 (103, 12, 40, 1, "Lyon"), (104, 5, 25, 4, "Paris"),
                 (105, 2, 15, 3, "Lille")]:
        entrepot.ajouter(Colis(*data))
