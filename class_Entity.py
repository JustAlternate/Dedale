#Class Entity
from random import randint

class Entity:
    def __init__(self,name,pos,sommet_actuel,color,shields=0,taille=0):
        self.name=name

        Liste_entity_name_dynamique=["Player","Minotaure"]

        if self.name in Liste_entity_name_dynamique:self.dynamique=True
        else:self.dynamique=False

        self.pos=pos
        self.sommet_actuel=sommet_actuel
        self.color=color
        self.shields=shields
        self.taille=taille

    def __str__(self):
        return self.name

    def check_finish(self,maze_interface):
        for entity in maze_interface.LEntity:
            if entity.name=="arrivé" and self.name=="Player" and self.pos==entity.pos:
                return True
        return False

    def check_death(self,maze_interface):
        for entity in maze_interface.LEntity:
            if (entity.name=="Minotaure" and self.name=="Player"):
                if self.pos==entity.pos:
                    if self.shields==0:
                        return True
                    else:
                        self.shields-=1
                        maze_interface.LEntity.remove(entity)

                        return False
            elif (self.name=="Minotaure" and entity.name=="Player"):
                if self.pos==entity.pos:
                    if entity.shields==0:
                        return True
                    else:
                        entity.shields-=1
                        maze_interface.LEntity.remove(self)
                        return False
        return False

    def check_shield(self,maze_interface):
        for entity in maze_interface.LEntity:
            if entity.name=="Shield" and self.name=="Player" and self.pos==entity.pos:
                self.shields+=1
                maze_interface.LEntity.remove(entity)

    def check_teleporteurs(self,maze_interface):
        for entity in maze_interface.LEntity:
            if entity.name=="Teleporteur" and self.name=="Player" and self.pos==entity.pos:
                random_cell = randint(0, len(maze_interface.maze.graphe.sommets) - 2)
                self.pos=[maze_interface.maze.graphe.sommets[random_cell].pos[0]*maze_interface.k+maze_interface.i,maze_interface.maze.graphe.sommets[random_cell].pos[1]*maze_interface.k+maze_interface.i]
                self.sommet_actuel=maze_interface.maze.graphe.sommets[random_cell]
                pos_tp=entity.pos
                maze_interface.LEntity.remove(entity)
                return pos_tp
        return False
