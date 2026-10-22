import random
import time

from colis import Entrepot, generer_colis
from tri import tri_fusion, tri_insertion
from chargement import sac_a_dos, glouton

TAILLES = [100, 1_000, 10_000, 100_000]
CAPACITE = 50


def chrono(f, *args, repet=1):
    debut = time.perf_counter()
    for _ in range(repet):
        f(*args)
    return (time.perf_counter() - debut) / repet * 1000


def main():
    print(f"{'n':>8} | {'rech. dict':>10} | {'rech. lin.':>10} | {'tri fusion':>10} | "
          f"{'tri insert.':>11} | {'sac DP':>9} | {'glouton':>9}")
    print("-" * 85)
    for n in TAILLES:
        ent = Entrepot()
        generer_colis(ent, n, graine=42)
        ids = [random.choice(ent.colis).id for _ in range(1000)]

        t_dict = chrono(lambda: [ent.rechercher(i) for i in ids]) / 1000
        t_lin = chrono(lambda: [ent.rechercher_lineaire(i) for i in ids[:50]]) / 50
        t_fus = chrono(tri_fusion, ent.colis, lambda c: c.poids)
        t_ins = (chrono(tri_insertion, ent.colis, lambda c: c.poids)
                 if n <= 10_000 else float("nan"))
        t_dp = chrono(sac_a_dos, ent.colis, CAPACITE)
        t_glo = chrono(glouton, ent.colis, CAPACITE)

        print(f"{n:>8} | {t_dict:>8.4f}ms | {t_lin:>8.4f}ms | {t_fus:>8.1f}ms | "
              f"{t_ins:>9.1f}ms | {t_dp:>7.1f}ms | {t_glo:>7.1f}ms")
    print("\n(tri par insertion non mesuré à 100 000 : trop long, O(n²))")
    print(f"(capacité du camion : {CAPACITE} kg)")


if __name__ == "__main__":
    main()
