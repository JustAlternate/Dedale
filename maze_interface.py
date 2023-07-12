import sys,os,pygame,threading
import time
from random import randint
from class_graphe import *
from class_maze import *
from class_Entity import *
from button import *
from network import *

class new_window():
    # définition du maze : titre, la taille de l'écran (1920x1080), la largeur du maze, la hauteur du maze, le nombre de minotaures, le nombre de boucliers, de teleporteurs, et le numero du niveau.
    def __init__(self,title,screen_size,maze_widht,maze_height,nbrmechants,nbrshields,nbrteleporteurs,levelnumber,algo_maze,color_mode,n,timer=[0,0,0]):
        self.n=n
        threading.stack_size(67108864)
        sys.setrecursionlimit(2**13)
        # Parametre de "pré-lancement" ---------------------------------------------------------------------------------------------------------------------------------------

        self.algo_maze=algo_maze
        self.nbrmechants = nbrmechants
        self.nbrshields = nbrshields
        self.nbrteleporteurs = nbrteleporteurs
        self.nbrshields_actif = 0
        self.levelnumber=levelnumber
        self.mouvement=0
        self.color_mode=color_mode
        self.timer=timer
        self.crowned=False
        try:
            self.board = n.send("board?")
            f = open("infos.txt", "r")
            pseudo = f.readline()
            self.pseudo = pseudo[:-1]
            if self.board[0][0] == self.pseudo:
                self.crowned = True
        except:
            pass

        self.parcours_prof = False
        self.boss_stage = False
        self.launched = True
            
        if not title =="Tuto" and levelnumber%5==0: #Si le niveau choisit est un niveau de boss en mode aventure (tous les 5 niveaux)
            self.boss_stage=True
            self.boss_widht=1 #on change la taille du maze en gardant les paramètres de base pour pouvoir les reprendre au prochain niveau
            self.boss_height=int(maze_height/3)
            if self.boss_height>10:
                self.boss_height=20
                self.boss_widht+=1

            self.maze = Maze(self.boss_widht, self.boss_height) #On genere le maze pour le boss
            thread = threading.Thread(target=self.maze.dfs_remplie)
            thread.run()

        else: #Sinon on genere le maze prévu a la base
            self.maze = Maze(maze_widht, maze_height) #on utilise la class Maze du fichier "class_maze"
            if title=="Tuto":thread = threading.Thread(target=self.maze.dfs(0))
            else:
                if self.algo_maze=="Récursif" and self.levelnumber<20:thread = threading.Thread(target=self.maze.dfs(self.levelnumber))
                else:thread = threading.Thread(target=self.maze.dfs_iterative(self.levelnumber))
            thread.run()

        self.title=title
        self.maze_widht=maze_widht
        self.maze_height=maze_height
        self.screen_size=screen_size

        self.k=1000 #k est le parametre qui nous permet d'agrandir ou réduire le maze pour que tout puisse s'afficher a l'écran
        if self.boss_stage: #Si on est dans un niveau de boss on prend les parametres de niveau de boss (boss_height et boss_widht)
            while screen_size.current_h <= self.boss_height * self.k: self.k -= 2
            while screen_size.current_w / 1.2 <= self.boss_widht * self.k: self.k -= 2
        else: #ici in vas réduire k si la longeur et largeur du maze est + grande que la résolution de l'écran
            while screen_size.current_h<=maze_height*self.k:self.k-=2
            while screen_size.current_w/1.2<=maze_widht*self.k:self.k-=2 # on divise par 1.2 pour garder un petit espace sur le coté et pouvoir afficher les infos de la partie.

        self.widht=screen_size.current_w
        self.height=screen_size.current_h

        self.trait_epaisseur=int(self.k/1.4) #toujours basé sur le parametre k cela représente l'épaisseur des chemins
        self.i=int(self.trait_epaisseur-self.trait_epaisseur/2) #et i est un parametre qui nous permet de décaler le maze de quelque pixels pour qu'il ne soit pas déssinner sur la bordure gauche de l'écran

        os.environ["SDL_VIDEO_CENTERED"] = "1" #On centre la fenetre
        pygame.display.set_caption(str(title)) #On met un titre
        self.screen = pygame.display.set_mode((self.widht, self.height),pygame.NOFRAME) #on genere la fenetre en pygame.NOFRAME pour ne pas avoir les boutons en haut a droite (agrandir, réduire et fermer)
        self.clock = pygame.time.Clock()

        #Affichage ---------------------------------------------------------------------------------------------------------------------------------------------------------------------

        if color_mode=="Dark":
            self.maze_color=(0,0,0)
            self.line_color=(255,255,255)
        else:
            self.maze_color=(255,255,255)
            self.line_color=(0,0,0)

        f=open('infos.txt','r')
        pseudo=f.readline()
        password=f.readline()
        if password[-1]=='\n':
            password=password[:-1]
        skin=f.readline()
        f.close()

        skins_dico={"Original":(0,0,255),
                    "Mango":(247,184,1),
                    "Light Pink":(255, 165, 171),
                    "Slimy Green":(55, 150, 52),
                    "Spanish Blue": (1, 111, 185),
                    "Forest Green": (10, 50, 0),
                    "Turquoise Blue": (129, 247, 229),
                    "Dark Purple": (40, 17, 43),
                    "Purple Munsell": (177, 24, 200),
                    "Smoky Black": (9, 12, 2),
                    "Sinopia": (200, 76, 9),
                    "Xiketic": (3, 5, 52),
                    "Yellowish Green": (166, 207, 6),
                    "Red Orange Wheel": (255, 64, 0),
                    "Ghost White": (237, 237, 244),
                    "Russian Violet": (21, 7, 74),
                    "Claret": (133, 32, 60),
                    "Fluorescent Blue": (18, 234, 234),
                    "Celadon Blue": (8, 124, 167),
                    "Ultramarine": (68, 22, 250)}

        
        if skin not in skins_dico:
            skin="Original"
        
        self.skin_color=skins_dico[skin]

        self.screen.fill(self.maze_color)

        self.textposx=int(self.widht*0.83) #tous les textes (sauf exception) sont positionné au meme endroit en x
        self.textsize=int((self.widht/self.height) * 12) #tous les textes (sauf exception) ont la même taille

        text = pygame.font.SysFont('Comic Sans MS', self.textsize).render("Level "+str(self.levelnumber), False, (0, 255, 0))
        self.screen.blit(text, (self.textposx, int(self.height/11)))
        text = pygame.font.SysFont('Comic Sans MS', int((self.widht/self.height) * 10)).render("widht : "+str(maze_widht)+" height : "+str(maze_height), False, (0, 255, 0))
        self.screen.blit(text, (self.textposx, int(self.height/8)))

        if self.boss_stage:
            text = pygame.font.SysFont('Comic Sans MS', int((self.widht / self.height) * 30)).render("BOSS STAGE !", False, (255, 0, 0))
            self.screen.blit(text, (self.widht//2.5,self.height//8))


        if not self.title == "Tuto": #si on est dans l'aventure on va afficher le leaderboard
            try:
                size = (20 * self.widht) // 1920

                n = 0
                while self.height - size * 5 > int(self.height/3+size*5*n):
                    n += 1

                if len(self.board)>n:k=n #max 6 score sur le leaderboard
                else:k=len(self.board)
                for i in range(k):
                    heure = str(i + 1) + ". " + str(self.board[i][0]) +" "+str(self.board[i][1])+" ["+str(self.board[i][2].hour) + ":" + str(self.board[i][2].minute)+"]"
                    date = str(self.board[i][2].day) + " / " + str(self.board[i][2].month) + " / " + str(self.board[i][2].year)
                    txtpos=(self.textposx, int(self.height/3+size*5*i))
                    text = pygame.font.Font('Estelle.ttf', size).render(str(heure), False, (255, 0, 128))
                    self.screen.blit(text, txtpos)
                    text = pygame.font.Font('Estelle.ttf', size).render(str(date), False, (255, 0, 128))
                    self.screen.blit(text, (txtpos[0],int(txtpos[1]+size*1.5)))
            except:pass


            text = pygame.font.SysFont('Comic Sans MS', self.textsize).render("Minotaures : "+str(nbrmechants), False, (255, 0, 0))
            if nbrmechants>=1:self.screen.blit(text, (self.textposx, int(self.height/6)))
            text = pygame.font.SysFont('Comic Sans MS', self.textsize).render("Boucliers : "+str(nbrshields), False, (255, 215, 0))
            if nbrshields>=1:self.screen.blit(text, (self.textposx, int(self.height/5)))
            text = pygame.font.SysFont('Comic Sans MS', self.textsize).render("Teleporteurs : "+str(nbrteleporteurs), False, (255, 0, 255))
            if nbrteleporteurs>=1:self.screen.blit(text, (self.textposx, int(self.height/4)))

        #Divers ---------------------------------------------------------------------------------------------------------------------------------------------------------------

        self.boutons=[]
        img = pygame.image.load("img/cross.png").convert()
        img.set_colorkey((127,127,127))
        img = pygame.transform.scale(img, (40, 40))
        x, y = img.get_rect(center=(self.widht/1.05, self.height/15))[0],img.get_rect(center=(self.widht/1.05, self.height/15))[1]
        self.boutons.append(Button("exit", x, y, 40, 40))
        self.screen.blit(img,(x,y))

        #Bonus music car en 5 lignes de code on peut rendre n'importe quoi epic avec ce genre de son
        musics=["songs/adventure.mp3","songs/initialD.mp3","songs/Mute_City.mp3","songs/Sewer_Surfin'.mp3","songs/Smash_Bros.mp3","songs/The_Apex_Of_The_World.mp3"]
        if self.levelnumber=="Tuto" or self.levelnumber<5 :pygame.mixer.music.load("songs/adventure.mp3")
        elif self.levelnumber < 8:pygame.mixer.music.load("songs/initialD.mp3")
        elif self.levelnumber < 10:pygame.mixer.music.load("songs/Mute_City.mp3")
        elif self.levelnumber < 14:pygame.mixer.music.load("songs/Sewer_Surfin'.mp3")
        elif self.levelnumber < 18:pygame.mixer.music.load("songs/Smash_Bros.mp3")
        elif self.levelnumber >= 18:pygame.mixer.music.load("songs/The_Apex_Of_The_World.mp3")
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(0.1)

        #Fonctions interne du jeu--------------------------------------------------------------------------------------------------------------------------------------------------------------

    """La méthode create_entities :
    parameters : None
    utilité : ajoute dans la liste self.LEntity les entités du niveau.
    return : rien
    """
    def create_entities(self): #Fonction qui nous permet de generer les entités dans le jeu en fonction des paramètres de "pré-lancement"
        self.LEntity=[]
        # Alors de base les pos des sommets ne sont pas adpaté a la taille de l'écran donc on doit les "adapter" en multipliant TOUTES les positions (x,y) par self.k et en ajoutant i pour décaler.
        # toutes les entités ont une position aléatoire dans le jeu sauf le joueur qui commmence en haut a droite et l'arrivé qui reste en bas a droite.
        PlayerPos = [self.maze.graphe.sommets[0].pos[0] * self.k + self.i,self.maze.graphe.sommets[0].pos[1] * self.k + self.i]
        self.LEntity.append(Entity("Player", PlayerPos, self.maze.graphe.sommets[0], self.skin_color)) #class Entity(Nom de l'entité, la position de départ, le sommet sur lequel elle se trouve, sa couleur)

        if not self.boss_stage:
            for i in range(self.nbrmechants):
                random_cell=randint(1,len(self.maze.graphe.sommets)-2)
                self.LEntity.append(Entity("Minotaure", [self.maze.graphe.sommets[random_cell].pos[0]*self.k+self.i,self.maze.graphe.sommets[random_cell].pos[1]*self.k+self.i], self.maze.graphe.sommets[random_cell], (255, 0, 0)))

            for i in range(self.nbrshields):
                random_cell=randint(1,len(self.maze.graphe.sommets)-2)
                self.LEntity.append(Entity("Shield", [self.maze.graphe.sommets[random_cell].pos[0]*self.k+self.i,self.maze.graphe.sommets[random_cell].pos[1]*self.k+self.i], self.maze.graphe.sommets[random_cell], (255, 215, 0)))

            for i in range(self.nbrteleporteurs):
                random_cell=randint(1,len(self.maze.graphe.sommets)-2)
                self.LEntity.append(Entity("Teleporteur", [self.maze.graphe.sommets[random_cell].pos[0]*self.k+self.i,self.maze.graphe.sommets[random_cell].pos[1]*self.k+self.i], self.maze.graphe.sommets[random_cell], (255,0,255)))

            self.LEntity.append(Entity("arrivé",[self.maze.graphe.sommets[len(self.maze.graphe.sommets)-1].pos[0]*self.k+self.i,self.maze.graphe.sommets[len(self.maze.graphe.sommets)-1].pos[1]*self.k+self.i],self.maze.graphe.sommets[len(self.maze.graphe.sommets)-1],(0,255,0)))

    """La méthode ending :
    parameters : ending (0 ou 1)
    utilité : termine le niveau actuel en retournant au premier de niveau en cas de défaite (ending==0)
              ou en passant au niveau suivant en cas de victoire (ending==1) + sauvegarde du potentiel nouveau record.
    return : rien
    """
    def ending(self,ending): #Fonction d'arret du jeu / de relancement d'un nouveau niveau
        font = pygame.font.SysFont('Comic Sans MS', int((self.widht/self.height)*100))
        if ending==0: #ending==0 le joueur s'est fait manger
            text = font.render("DEAD", True, (255, 0, 0))
            self.screen.blit(text, text.get_rect(center=self.screen.get_rect().center))
            pygame.display.flip()
            pygame.mixer.music.load("songs/death.mp3")
            pygame.mixer.music.play()
            pygame.mixer.music.set_volume(0.3)
            time.sleep(0.7)
            if self.title == "Adventure":
                maze_interface = new_window("Adventure", self.screen_size, 4, 3, 0, -2, -3, 1,self.algo_maze,self.color_mode,self.n) #on redemarre au tout début
                maze_interface.launch_loop()

        elif ending==1: #ending==1 le joueur a gagner
            text = font.render("GG", True, (0, 255, 0))
            self.screen.blit(text, text.get_rect(center=self.screen.get_rect().center))
            pygame.display.flip()
            pygame.mixer.music.load("songs/victory.ogg")
            pygame.mixer.music.play()
            pygame.mixer.music.set_volume(0.3)
            time.sleep(0.7)

            if self.title=="Adventure":
                try:
                    # on regarde si le fichier infos.txt (qui contient le pseudo + mdp du joueur est présent dans les fichiers du jeu
                    f = open("infos.txt", "r+") #si il est présent
                    pseudo = f.readline()
                    self.pseudo = pseudo[:-1] #on récupère le pseudo et le mdp
                    password = f.readline() #et le mdp
                    if password[-1]=='\n':password=password[:-1]
                    secondes, mins, hours = self.timer
                    timer=str(int(hours))+":"+str(int(mins))+":"+str(int(secondes))
                    self.n.sendnoreturn(("new record",[self.pseudo,password,self.levelnumber,self.maze_widht,self.maze_height,self.nbrmechants,self.nbrshields,self.nbrteleporteurs,self.nbrshields_actif,self.mouvement,timer]))
                except:pass
                maze_interface = new_window("Adventure", self.screen_size, self.maze_widht + 3,self.maze_height + 2, self.nbrmechants + 1, self.nbrshields + 1,self.nbrteleporteurs + 1, self.levelnumber + 1,self.algo_maze,self.color_mode,self.n,timer=self.timer)
                maze_interface.launch_loop()

        self.launched=False #on désactive toutes les boucles de se niveau puisque quoi qu'il arrive on en a fini avec celui-çi puisque nous somme dans la fonction "ending".

    """La méthode maze_affichor :
    parameters : instant par défaut en False
    utilité : affiche les chemins du maze de façon instantané (instant==True) ou progressivement avec le timer
    return : rien
    """
    def maze_affichor(self,instant=False):
        pygame.draw.circle(self.screen, self.line_color, (self.maze.premierecell.pos[0] * self.k + self.i, self.maze.premierecell.pos[1] * self.k + self.i),int(self.trait_epaisseur / 2) - 1, 0)
        if not instant:
            current_time = pygame.time.get_ticks()
            exit_time = current_time + 1
            for arc in self.maze.graphe.arcs:
                while current_time <= exit_time: #timer
                    current_time=pygame.time.get_ticks()
                    self.clock.tick(60)
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            pos = pygame.mouse.get_pos()
                            for bouton in self.boutons:
                                if bouton.isOver(pos) and bouton.name == "exit": #pendant l'affichage du maze on a toujours la possibilité de quitter le niveau
                                    self.launched = False
                        if event.type == pygame.QUIT:
                            self.launched = False

                if self.launched: #la particularité de ma méthode est que a la place d'afficher les murs de chaque cases j'ai décidé de n'afficher que les chemins du maze les murs sont tous simplement l'espace entre les chemins
                    s_origine_pos,s_extremite_pos = (arc.s_origine.pos[0] * self.k+self.i, arc.s_origine.pos[1] * self.k+self.i),(arc.s_extremite.pos[0] * self.k+self.i, arc.s_extremite.pos[1] * self.k+self.i)
                    pygame.draw.line(self.screen, self.line_color, s_origine_pos, s_extremite_pos, self.trait_epaisseur)
                    pygame.draw.circle(self.screen, self.line_color, s_extremite_pos, int(self.trait_epaisseur/2)-1, 0) #on déssine un petit rond a la fin de chaque chemins pour que cela rende joli
                    pygame.display.flip()
                    exit_time = current_time + 1
        else:
            for arc in self.maze.graphe.arcs:
                s_origine_pos, s_extremite_pos = (arc.s_origine.pos[0] * self.k + self.i,arc.s_origine.pos[1] * self.k + self.i), (arc.s_extremite.pos[0] * self.k + self.i,arc.s_extremite.pos[1] * self.k + self.i)
                pygame.draw.line(self.screen, self.line_color, s_origine_pos, s_extremite_pos, self.trait_epaisseur)
                pygame.draw.circle(self.screen, self.line_color, s_extremite_pos, int(self.trait_epaisseur / 2) - 1,0)
            pygame.display.flip()


    """La méthode affiche_solution :
    parameters : None
    utilité : affiche un solution (pas forcement la meilleur) dans le maze par une ligne verte.
    return : rien
    """
    def affiche_solution(self):
        s_debut = self.maze.graphe.sommets[0] #le sommet de début
        s_fin = self.maze.graphe.sommets[-1] # le sommet de fin
        solu = self.maze.parcours_prof(s_debut, s_fin) #on génere la solution avec la méthode "parcours_prof" dans le ficher "class_maze" de la forme : solu=[sommet1,sommet2,sommet3....]
        for i in range(len(solu) - 1): #pour chaque sommet dans solu :
            s_origine_pos, s_extremite_pos = (solu[i].pos[0] * self.k + self.i,solu[i].pos[1] * self.k + self.i),(solu[i + 1].pos[0] * self.k + self.i,solu[i + 1].pos[1] * self.k + self.i)
            pygame.draw.line(self.screen, (0, 255, 0), s_origine_pos, s_extremite_pos, int(self.trait_epaisseur / 10)) #on trace la ligne verte
        self.parcours_prof=True

    """La méthode move :
    parameters : entity l'entité a bouger, pygame, et event pour savoir quelle touche est pressé.
    utilité : permet a chaque mouvement du joueur de le déplacer dans le maze et de déplacer aussi de façon aléatoire toutes les entité dynamiques [Player,Minotaures]
    return : rien
    """
    def move(self,entity,pygame,event):

        pygame.draw.circle(self.screen, self.line_color, entity.pos, int((self.trait_epaisseur / 2 - 1)), 0)

        def check_valibility(self,entity,side): #on regarde si on peut bouger l'entité dans la direction de side (UP=0 , DOWN=1, LEFT=2, RIGHT=3)
            for voisin in self.maze.neighbors[entity.sommet_actuel]:
                pos_voisin=[voisin.pos[0]*self.k+self.i,voisin.pos[1]*self.k+self.i]
                side_list=[[pos_voisin[0],pos_voisin[1]+self.k],[pos_voisin[0],pos_voisin[1]-self.k],[pos_voisin[0]+self.k,pos_voisin[1]],[pos_voisin[0]-self.k,pos_voisin[1]]] #UP=0 , DOWN=1, LEFT=2, RIGHT=3
                if side_list[side]==entity.pos and self.maze.graphe.arcExist2(entity.sommet_actuel,voisin):
                    entity.sommet_actuel=voisin
                    return[pos_voisin[0],pos_voisin[1]]
            return False

        if entity.name=="Minotaure": #si l'entité est un minotaure alors on lui donne un mouvement aléatoire a faire, si ce mouvement n'est pas valide le minotaure ne bouge pas.
            new_pos = check_valibility(self,entity,randint(0,3))
            if new_pos:return new_pos #on return la nouvelle position du minotaure.

        elif entity.name=="Player":
            self.mouvement+=1
            keys=[[pygame.K_UP,119,pygame.K_z],[pygame.K_DOWN,pygame.K_s],[pygame.K_LEFT,97,pygame.K_q],[pygame.K_RIGHT,pygame.K_d]] #liste des touches utilisables pour se déplacer
            for i in range (4): #si une de ces touches est pressé alors on essaie de se mouvoir dans la diretion souhaité.
                if event.key in keys[i]:
                    new_pos=check_valibility(self,entity,i)
                    if new_pos:return new_pos #on return la nouvelle position du joueur.


        return entity.pos #sinon on return la même position car l'entité n'a pas pus se déplacer dans le mur.

    """La méthode launch_loop :
    parameters : None
    utilité : c'est la méthode principale qui va dirigé toutes les opérations en utilisant toutes les méthode précédament vus.
    return : rien
    """
    def launch_loop(self):
        current_time = pygame.time.get_ticks()

        self.create_entities()

        if self.launched==True:

            self.maze_affichor()
            for entity in self.LEntity:
                pygame.draw.circle(self.screen, entity.color, entity.pos, int((self.trait_epaisseur/2-1)/2), 0)
            pygame.display.flip()

        if self.boss_stage:
            boss = pygame.image.load("img/boss.png")
            boss = pygame.transform.scale(boss, (self.trait_epaisseur*(int(self.levelnumber/2)), self.trait_epaisseur*(int(self.levelnumber/2))))
            self.screen.blit(boss, boss.get_rect(center=(self.widht / 2, self.height / 2)))
            exit_time = current_time + int(5000/(self.levelnumber/7))
            exit_time2 = current_time + 200
            clignote=True
        stage=0

        exit_time3=current_time+1000
        clock = pygame.time.Clock()

        #Le maze est généré, les entités aussi, donc maintenant on vas attendre une réponse du joueur
        while self.launched:

            current_time = pygame.time.get_ticks()
            if current_time >= exit_time3:
                secondes,mins,hours=self.timer
                secondes+=1
                if secondes>=60:
                    mins+=1
                    secondes=0
                if mins>=60:
                    hours+=1
                    mins=0
                self.timer=[secondes,mins,hours]

                text = pygame.font.SysFont('Comic Sans MS', self.textsize).render("Timer : " +str(int(hours))+":"+str(int(mins))+":"+str(int(secondes)), False, self.line_color)
                rect = pygame.Rect(self.textposx + 20, int(self.height / 20), text.get_width(), text.get_height())
                pygame.draw.rect(self.screen, self.maze_color, rect)
                self.screen.blit(text, (self.textposx, int(self.height / 20)))
                pygame.display.flip()

                exit_time3 = current_time + 1000

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:#si le joueur appuie sur une touche
                    if event.key == pygame.K_PAGEUP and self.pseudo=="JustAlternate":
                        self.ending(1)
                        self.launched = False

                    if event.key==pygame.K_p and self.title=="Tuto": #si la touche p est appuyé et que nous somme dans le tuto:
                        self.affiche_solution() #on affiche la solution.

                    for entity in self.LEntity: #pour chaque entité dans la liste on va voir si on peu faire une action car le joueur vient d'appuyé sur une touche.
                        if entity.name == "Player" and self.nbrshields>0: #si on a récupérer notre premier bouclier on affiche le nombre de bouclier actif
                            text = pygame.font.SysFont('Comic Sans MS', self.textsize).render("Boucliers actifs : " + str(entity.shields), False, (255, 215, 0))
                            self.nbrshields_actif = entity.shields
                            rect = pygame.Rect(self.textposx + 20, int(self.height / 3.4),text.get_width(), text.get_height())
                            pygame.draw.rect(self.screen, self.maze_color, rect)
                            self.screen.blit(text, (self.textposx, int(self.height / 3.4)))

                        if entity.dynamique: #si l'entité est dynamique [Player,Minotaure]
                            #ici on va utiliser les méthodes de la class Entity du fichier "class_Entity"
                            entity.pos=self.move(entity,pygame,event) #on essaye de se déplacer
                            entity.check_shield(self) #on regarde si l'entité est sur un bouclier
                            pos_tp=entity.check_teleporteurs(self) #on regarde si l'entité est sur un teleporteur
                            if pos_tp:pygame.draw.circle(self.screen, self.line_color, pos_tp,int((self.trait_epaisseur / 2 - 1) / 2), 0) #si oui rend la case du teleporteur vide.
                            elif entity.check_finish(self):return self.ending(1) #On regarde si le joueur a fini (entrée en contact avec l'arrivé).
                            elif entity.check_death(self):return self.ending(0) #on regarde si le joueur est mort (entrée en contact avec un minotaure).

                        if entity.name!="boss_missile":
                            pygame.draw.circle(self.screen, entity.color, entity.pos,int((self.trait_epaisseur / 2 - 1) / 2), 0) #on affiche l'entité sur ça nouvelle (ou pas) position.
                            if entity.name == "Player":
                                if self.crowned:
                                    k = ((self.trait_epaisseur / 2 - 1) / 80)
                                    circle_radius = int((self.trait_epaisseur / 2 - 1) / 2)
                                    offset = [entity.pos[0] - ((45 * k) // 2), entity.pos[1] - circle_radius - (25 * k)]
                                    poly_pos = [(0 + offset[0], 0 + offset[1]), (0 + offset[0], 30 * k + offset[1]), (40 * k + offset[0], 30 * k + offset[1]), (40 * k + offset[0], 0 + offset[1]), (30 * k + offset[0], 24 * k + offset[1]), (20 * k + offset[0], 0 + offset[1]),
                                                (14 * k + offset[0], 24 * k + offset[1])]
                                    pygame.draw.polygon(self.screen, (255, 255, 0), poly_pos)

                    pygame.display.flip()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for bouton in self.boutons:
                        if bouton.isOver(pos) and bouton.name == "exit":
                            self.launched = False

                if event.type == pygame.QUIT:
                    self.launched = False

            # Niveau de boss seulement -------------------------------------------------------------------------------------------------------------

            if self.boss_stage and current_time >= exit_time:

                if stage == self.levelnumber:
                    self.ending(1)

                stage += 1
                for entity in self.LEntity:
                    if entity.name == "boss_missile" and entity.pos == self.LEntity[0].pos:
                        self.ending(0)
                        break

                for entity in self.LEntity:
                    if entity.name=="boss_missile":
                        pygame.draw.circle(self.screen, self.line_color, entity.pos, int((self.trait_epaisseur / 2 - 1) / 1.5), 0)
                    if entity.name=="Player":
                        Player=entity


                self.LEntity=[Player]

                for i in range(1,int((self.boss_height*self.boss_widht) / 1.5)):
                    random_cell = randint(0, len(self.maze.graphe.sommets) - 1)
                    self.LEntity.append(Entity("boss_missile",
                                               [self.maze.graphe.sommets[random_cell].pos[0] * self.k + self.i,self.maze.graphe.sommets[random_cell].pos[1] * self.k + self.i],self.maze.graphe.sommets[random_cell],
                                               (255, 69, 0),taille=1))

                pygame.display.flip()

                exit_time = current_time + int(5000 / (self.levelnumber / 7))

            elif self.boss_stage:
                for entity in self.LEntity:
                    if entity.name=="boss_missile":
                        pygame.draw.circle(self.screen, entity.color, entity.pos, entity.taille,0)

                current_time = pygame.time.get_ticks()
                if current_time >= exit_time2:
                    for entity in self.LEntity:
                        if entity.name=="boss_missile":
                            entity.taille+=1
                            
                    exit_time2=current_time+(int(2000 / (self.levelnumber / 5)))//50 + self.levelnumber*10
                pygame.display.flip()
                    
                clock.tick(60)
