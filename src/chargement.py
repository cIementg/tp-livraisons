from tri import tri_fusion


def gain_valeur(c):
    return c.valeur


def gain_priorite(c):
    return c.valeur * (1 + c.priorite / 5)


def sac_a_dos(colis, capacite, gain=gain_valeur):
    candidats = [c for c in colis if c.poids <= capacite]
    meilleur = [0] * (capacite + 1)
    pris = []

    for c_obj in candidats:
        p, g = c_obj.poids, gain(c_obj)
        ligne = bytearray(capacite + 1)
        for cap in range(capacite, p - 1, -1):
            avec = meilleur[cap - p] + g
            if avec > meilleur[cap]:
                meilleur[cap] = avec
                ligne[cap] = 1
        pris.append(ligne)

    choisis = []
    cap = capacite
    for i in range(len(candidats) - 1, -1, -1):
        if pris[i][cap]:
            choisis.append(candidats[i])
            cap -= candidats[i].poids
    choisis.reverse()
    return choisis, meilleur[capacite]


def glouton(colis, capacite, gain=gain_valeur):
    tries = tri_fusion(colis, cle=lambda c: gain(c) / c.poids, decroissant=True)
    choisis, poids, total = [], 0, 0
    for c in tries:
        if poids + c.poids <= capacite:
            choisis.append(c)
            poids += c.poids
            total += gain(c)
    return choisis, total
