import sys,threading
from class_graphe import *
import random

#Class maze, initialisation du maze.

class Maze:
    def __init__(self,widht,height):
        """parameters :
        widht (int) -> largeur du maze en nombre de cases
        height (int) -> hauteur du maze en nombre de cases
        """
        self.widht=widht
        self.height=height

    def __str__(self):
        return(self.widht,self.height,self.nbrsommets,self.len_chemin_res)

    def gen_graphe_vide(self):
        self.graphe=Graphe("maze")
        k=0
        for i in range (self.widht):
            for j in range (self.height):
                sommet=Sommet(k,(i,j))
                k+=1
                self.graphe.ajouterSommet(sommet)

    def find_neighbors(self,s):
        sommets_voisins = []
        pos_possibles=[(s.pos[0] + 1, s.pos[1]),(s.pos[0], s.pos[1] + 1),(s.pos[0] - 1, s.pos[1]),(s.pos[0], s.pos[1] - 1)]
        for sommet in self.graphe.sommets:
            if sommet.pos in pos_possibles:
                sommets_voisins.append(sommet)
        return sommets_voisins

    def ajouter_des_arcs(self,levelnumber):
        # On ajoute quelques arc en + pour créer des passages alternatifs dans le maze.
        for i in range(levelnumber):
            arc_exist = True
            while arc_exist:
                cell = random.choice(self.graphe.sommets)
                neighbor = random.choice(self.neighbors[cell])
                if not self.graphe.arcExist2(cell, neighbor):
                    arc_exist = False
                    self.graphe.ajouterArc(Arc(cell, neighbor))

    def dfs(self,levelnumber): #depth first search
        self.gen_graphe_vide()
        cell = self.graphe.sommets[-1]
        self.premierecell=cell
        self.neighbors={}
        for s in self.graphe.sommets:
            self.neighbors[s]=self.find_neighbors(s)

        def dfs_recu(self,cell):
            random.shuffle(self.neighbors[cell])
            for neighbor in self.neighbors[cell]:
                if neighbor.visited==False:
                    self.graphe.ajouterArc(Arc(cell,neighbor))
                    neighbor.visited=True
                    dfs_recu(self,neighbor)

        dfs_recu(self,cell)
        self.ajouter_des_arcs(levelnumber)

    def dfs_remplie(self):
        self.gen_graphe_vide()
        self.neighbors={}
        self.premierecell = self.graphe.sommets[0]
        for s in self.graphe.sommets:
            self.neighbors[s]=self.find_neighbors(s)
        for s in self.graphe.sommets:
            for neighbor in self.neighbors[s]:
                if not self.graphe.arcExist2(s,neighbor):
                    self.graphe.ajouterArc(Arc(s, neighbor))
                s.visited=True

    def dfs_iterative(self,levelnumber):
        self.gen_graphe_vide()
        self.neighbors = {}
        for s in self.graphe.sommets:
            self.neighbors[s]=self.find_neighbors(s)
        stack=[]
        cell = self.graphe.sommets[-1]
        self.premierecell=cell
        cell.visited=True
        stack.append(cell)

        while(len(stack)):
            cell=stack[-1]
            stack.pop()
            random.shuffle(self.neighbors[cell])
            for neighbor in self.neighbors[cell]:
                if not neighbor.visited:
                    stack.append(cell)
                    random.shuffle(self.neighbors[cell])
                    for neighbor in self.neighbors[cell]:
                        if not neighbor.visited:
                            self.graphe.ajouterArc(Arc(cell,neighbor))
                            neighbor.visited=True
                            stack.append(neighbor)
                            break
                    break
        self.ajouter_des_arcs(levelnumber//2)


    def sommmet_voisin_non_visite(self,sommet,s_deja_vu):
        svnv=''
        index=0
        while svnv=='' and index<len(self.neighbors[sommet]):
            sCandidate=self.neighbors[sommet][index]
            if self.graphe.arcExist2(sommet,sCandidate) and sCandidate not in s_deja_vu:
                svnv=sCandidate
            index+=1
        return svnv

    def parcours_prof(self, s_debut, s_fin):
        visites=[]
        pile=[]
        visites.append(s_debut)
        salle=s_debut
        fin=False
        while not fin:
            sSuivante=self.sommmet_voisin_non_visite(salle,visites)
            if sSuivante!='':
                pile.append(salle)
                salle = sSuivante
                visites.append(salle)
                if salle == s_fin:
                    pile.append(salle)
                    fin = True
            else:
                if len(pile) > 0:
                    salle = pile.pop()
                else:
                    fin = True
        return pile
