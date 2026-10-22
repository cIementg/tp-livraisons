def tri_fusion(elements, cle, decroissant=False):
    if len(elements) <= 1:
        return list(elements)
    milieu = len(elements) // 2
    gauche = tri_fusion(elements[:milieu], cle, decroissant)
    droite = tri_fusion(elements[milieu:], cle, decroissant)
    return _fusion(gauche, droite, cle, decroissant)


def _fusion(gauche, droite, cle, decroissant):
    resultat = []
    i = j = 0
    while i < len(gauche) and j < len(droite):
        a, b = cle(gauche[i]), cle(droite[j])
        if (a >= b) if decroissant else (a <= b):
            resultat.append(gauche[i])
            i += 1
        else:
            resultat.append(droite[j])
            j += 1
    resultat.extend(gauche[i:])
    resultat.extend(droite[j:])
    return resultat


def tri_insertion(elements, cle):
    res = list(elements)
    for i in range(1, len(res)):
        x = res[i]
        k = cle(x)
        j = i - 1
        while j >= 0 and cle(res[j]) > k:
            res[j + 1] = res[j]
            j -= 1
        res[j + 1] = x
    return res
