from colis import Colis, Entrepot, generer_colis, charger_exemple
from tri import tri_fusion
from chargement import sac_a_dos, glouton, gain_valeur, gain_priorite

MAX_AFFICHAGE = 30


def afficher_liste(liste, titre="Colis"):
    print(f"\n--- {titre} ({len(liste)}) ---")
    print("     ID |  Poids  |  Valeur  | Prio  | Destination")
    for c in liste[:MAX_AFFICHAGE]:
        print(c)
    if len(liste) > MAX_AFFICHAGE:
        print(f"... ({len(liste) - MAX_AFFICHAGE} autres non affichés)")


def lire_entier(message, mini=None, maxi=None):
    while True:
        try:
            v = int(input(message))
            if (mini is None or v >= mini) and (maxi is None or v <= maxi):
                return v
        except ValueError:
            pass
        print("Valeur invalide.")


def ajouter_colis(ent):
    id = lire_entier("ID : ")
    if ent.rechercher(id):
        print("Cet ID existe déjà.")
        return
    poids = lire_entier("Poids (kg) : ", 1)
    valeur = lire_entier("Valeur (€) : ", 0)
    prio = lire_entier("Priorité (1 faible -> 5 urgent) : ", 1, 5)
    dest = input("Destination : ").strip() or "Inconnue"
    ent.ajouter(Colis(id, poids, valeur, prio, dest))
    print("Colis ajouté.")


def organiser(ent):
    print("1. Par poids   2. Par valeur   3. Par priorité")
    choix = lire_entier("Critère : ", 1, 3)
    if choix == 1:
        afficher_liste(tri_fusion(ent.colis, lambda c: c.poids), "Par poids croissant")
    elif choix == 2:
        afficher_liste(tri_fusion(ent.colis, lambda c: c.valeur, True), "Par valeur décroissante")
    else:
        afficher_liste(tri_fusion(ent.colis, lambda c: c.priorite, True), "Par priorité décroissante")


def preparer_camion(ent):
    if len(ent) == 0:
        print("Aucun colis.")
        return None
    capacite = lire_entier("Capacité du camion (kg) : ", 1)
    print("1. Maximiser la valeur (optimal)\n"
          "2. Maximiser la valeur en tenant compte de la priorité (optimal)\n"
          "3. Glouton rapide (non optimal, pour comparaison)")
    mode = lire_entier("Mode : ", 1, 3)
    if mode == 1:
        choisis, _ = sac_a_dos(ent.colis, capacite, gain_valeur)
    elif mode == 2:
        choisis, _ = sac_a_dos(ent.colis, capacite, gain_priorite)
    else:
        choisis, _ = glouton(ent.colis, capacite, gain_valeur)
    chargement = {"capacite": capacite, "colis": choisis}
    afficher_chargement(chargement)
    return chargement


def afficher_chargement(ch):
    if not ch:
        print("Aucun camion préparé.")
        return
    poids = sum(c.poids for c in ch["colis"])
    valeur = sum(c.valeur for c in ch["colis"])
    afficher_liste(ch["colis"], "Chargement")
    print(f"Poids : {poids}/{ch['capacite']} kg | Valeur transportée : {valeur} €")


def afficher_stats(ent):
    s = ent.statistiques()
    if not s:
        print("Aucun colis.")
        return
    print(f"\nNombre de colis : {s['nombre']}")
    print(f"Poids total : {s['poids_total']} kg (moyenne {s['poids_moyen']:.1f})")
    print(f"Valeur totale : {s['valeur_totale']} € (moyenne {s['valeur_moyenne']:.1f})")
    print("Répartition par priorité (1 -> 5) :", s["par_priorite"])


def main():
    ent = Entrepot()
    charger_exemple(ent)
    chargement = None
    while True:
        print("\n===== GESTION DES LIVRAISONS =====")
        print("1. Afficher les colis\n2. Ajouter un colis\n3. Rechercher un colis\n"
              "4. Organiser les colis\n5. Préparer un camion\n6. Afficher le chargement\n"
              "7. Afficher les statistiques\n8. Générer des colis aléatoires\n0. Quitter")
        choix = lire_entier("Choix : ", 0, 8)
        if choix == 0:
            break
        elif choix == 1:
            afficher_liste(ent.colis)
        elif choix == 2:
            ajouter_colis(ent)
        elif choix == 3:
            c = ent.rechercher(lire_entier("ID : "))
            print(c if c else "Colis introuvable.")
        elif choix == 4:
            organiser(ent)
        elif choix == 5:
            chargement = preparer_camion(ent)
        elif choix == 6:
            afficher_chargement(chargement)
        elif choix == 7:
            afficher_stats(ent)
        elif choix == 8:
            n = lire_entier("Combien ? (ex. 100, 1000, 10000, 100000) : ", 1)
            generer_colis(ent, n)
            print(f"{n} colis générés. Total : {len(ent)}")


if __name__ == "__main__":
    main()
