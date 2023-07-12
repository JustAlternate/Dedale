"""
 Implémentations des opérations élémentaires du graphe 6 orienté et pondéré sous forme d'objet
"""
# Rappel et compléments des classes Sommet(), Arc() et Graphe()
# =============================================================

class Sommet():
    def __init__(self,nom,pos,visited=False):
        self.nom = nom
        self.pos = pos
        self.visited=visited
    def __str__(self):
        return f"Sommet : {self.nom} , {self.pos} , {self.visited}"

class Arc():
    def __init__(self,s_origine,s_extremite):
        self.s_origine=s_origine
        self.s_extremite=s_extremite

    def __str__(self):
        return f"Arc {self.nom} de {self.s_origine.nom} à {self.s_extremite.nom}"

    def origine_fin(self):
        return (self.s_origine.nom,self.s_extremite.nom)

class Graphe():
    def __init__(self,nom):
        self.nom=nom
        self.sommets=[]
        self.arcs=[]

    def __str__(self):
        aff = f"Graphe {self.nom} : \n"
        aff += "\t Liste des sommets : \n"
        for s in self.sommets:
            aff += "\t\t"+str(s)+"\n"
        aff += "\t Liste des arcs : \n"
        for a in self.arcs:
            aff += "\t\t"+str(a)+"\n"
        return aff

    def ajouterSommet(self,s):
        if not self.sommetExist(s):
            self.sommets.append(s)

    def ajouterArc(self,a):
        if self.sommetExist(a.s_origine) and self.sommetExist(a.s_extremite) and not self.arcExist(a):
            self.arcs.append(a)

    def supprimerArc(self,a):
        if self.arcExist(a):
            self.arcs.remove(a)

    def supprimerSommet(self,s):
        if self.sommetExist(s):
            nArc=len(self.arcs)-1
            while nArc>=0:
                a=self.arcs[nArc]
                if a.s_origine==s or a.s_extremite==s:
                    self.supprimerArc(a)
                nArc-=1
            self.sommets.remove(s)

    def sommetExist(self,s):
        return s in self.sommets

    def arcExist(self,a):
        return a in self.arcs

    def arcExist2(self,a,b):
        for arc in self.arcs:
            if arc.s_origine==a and arc.s_extremite==b or arc.s_origine==b and arc.s_extremite==a:
                return True
        return False


