from tkinter import font
import pygame,os,time,sys,threading
from button import *
from settingMaze import *
from maze_interface import *
from network import *

pygame.init()
screen_size=pygame.display.Info()

def Entrainement_choix(pygame,screen,algo_maze,color_mode,bg,n):

    boutons = []

    widht=screen.get_width()
    height=screen.get_height()
    level_cap = 1

    try:
        board = n.send("board?")
        print(board)
        f = open("infos.txt", "r")
        pseudo = f.readline()
        pseudo = pseudo[:-1]
        for player in board:
            if player[0]==pseudo:
                level_cap=player[1]
    except:pass

    img_button = pygame.image.load("img/maze_button.png").convert()

    w,h=img_button.get_width(),img_button.get_height()
    new_w,new_h=(w*widht)//1920,(h*height)//1080
    img_button=pygame.transform.scale(img_button,(new_w,new_h))
    img_button.set_colorkey((127,127,127))

    text=[]
    pos_buttons=[]

    index=0

    nbr_elements_on_screen_horizontal=8
    nbr_elements_on_screen_vertical=4

    decalage_vertical=height/(nbr_elements_on_screen_vertical+1)
    decalage_horizontal=widht/(nbr_elements_on_screen_horizontal+1)
    
    font_size = (55 * widht) // 1920

    for i in range(nbr_elements_on_screen_vertical):
        for j in range(nbr_elements_on_screen_horizontal):
            index+=1
            x,y = decalage_horizontal//2+decalage_horizontal*j,decalage_vertical//2+decalage_vertical* i
            text.append(pygame.font.Font('Estelle.ttf', font_size).render(str(index), True, (127, 0, 127)))
            pos_buttons.append([x,y])
            if index<=level_cap:
                boutons.append(Button(index, x, y, img_button.get_width(), img_button.get_height()))
            else:
                index-=1

    cross = pygame.image.load("img/cross.png").convert()
    cross.set_colorkey((127,127,127))
    x, y = cross.get_rect(center=(widht / 1.1, height / 10))[0], cross.get_rect(center=(widht / 1.1, height / 10))[1]
    boutons.append(Button("exit", x, y, 100, 107))

    launched = True

    bgX = -1
    bgX2 = bg.get_width()
    bgY = -1
    bgY2 = bg.get_height()
    clock = pygame.time.Clock()
    speed=60

    def redrawWindow(pos,img_button,cross,level_cap,text,pos_button,font_size):

        screen.blit(bg,(bgX,bgY))
        screen.blit(bg,(bgX2,bgY2))

        x, y = cross.get_rect(center=(widht/1.1, height/10))[0],cross.get_rect(center=(widht/1.1, height/10))[1]
        screen.blit(cross,(x,y))

    
        for i in range(index):
            x,y=pos_button[i]
            screen.blit(text[i], (x+img_button.get_width()//2 - font_size//2, y+img_button.get_height()))
            screen.blit(img_button, (x, y))

        font_size = (20 * widht) // 1920
        authors = pygame.font.Font('Estelle.ttf', font_size).render("Crée par : LAVOILLOTTE Ethan et WEBER Loïc", True, (0, 255, 0))
        rect = pygame.Rect(authors.get_rect(center=(widht / 1.2, height / 1.2))[0],
                           authors.get_rect(center=(widht / 1.3, height / 1.1))[1],
                           authors.get_width(), authors.get_height())
        pygame.draw.rect(screen, (0, 0, 0), rect)
        screen.blit(authors, authors.get_rect(center=(widht / 1.2, height / 1.1)))

        pygame.display.update()

    while launched:

        pos = pygame.mouse.get_pos()
        redrawWindow(pos,img_button,cross,level_cap,text,pos_buttons,font_size)
        clock.tick(speed)

        bgX -= 1.75
        bgX2 -= 1.75
        bgY -= 1.25
        bgY2 -= 1.25
        if bgX < bg.get_width() * -1:
            bgX = bg.get_width()
        if bgX2 < bg.get_width() * -1:
            bgX = bg.get_width()
        if bgY < bg.get_height() * -1:
            bgY = bg.get_height()
        if bgY2 < bg.get_height() * -1:
            bgY = bg.get_height()

        if bgX >= 7000 and bgX2 < -7000 and bgY >= 5000 and bgY2 <= -5000:
            bgX = -217
            bgX2 = bg.get_width()
            bgY = -217
            bgY2 = bg.get_height()

        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for bouton in boutons:
                    if bouton.isOver(pos) :
                        if bouton.name=="exit":launched=False

                        if type(bouton.name)==int:
                            k=bouton.name
                            maze_interface=new_window("Adventure_entrainement",screen_size,4+(k-1)*3,3+(k-1)*2,-1+(k-1),-2+(k-1),-5+(k-1),k,algo_maze,color_mode,n)
                            maze_interface.launch_loop()

            if event.type == pygame.QUIT:
                launched = False

        pygame.display.flip()

def niv_custom(pygame,screen,algo_maze,color_mode,bg,n):

    boutons = []

    widht=screen.get_width()
    height=screen.get_height()

    pygame.mixer.music.load("songs/Motivated.mp3")
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(0.1)

    boutons = []

    cross = pygame.image.load("img/cross.png").convert()
    cross.set_colorkey((127,127,127))
    play_img = pygame.image.load("img/playMaze.png").convert()
    play_img.set_colorkey((127,127,127))

    boutons.append(Button("Play", play_img.get_rect(center=(widht / 2, height / 1.2))[0], play_img.get_rect(center=(widht / 2, height / 1.2))[1], 280, 160))

    x, y = cross.get_rect(center=(widht / 1.1, height / 10))[0], cross.get_rect(center=(widht / 1.2, height / 10))[1]
    boutons.append(Button("exit", x, y, 100, 107))

    arrowU = pygame.image.load("img/arrow_up.png").convert()
    arrowD = pygame.image.load("img/arrow_down.png").convert()

    LarrowD=[]
    LarrowU=[]
    texts_data=[[2],[2],[1],[1],[1],[False]]

    nbr_elements_on_screen=6
    decalage=widht/(nbr_elements_on_screen+1)

    for i in range(nbr_elements_on_screen):
        x, y = arrowU.get_rect(center=(decalage+decalage*i, height // 2))[0], arrowU.get_rect(center=(decalage+decalage*i, height // 2))[1]
        LarrowD.append([x,height//1.5])
        LarrowU.append([x, height // 3])
        boutons.append(Button([i,"arrowD"], x-(arrowU.get_width()//2), height//1.5 - (arrowU.get_height()//2), 150, 75))
        boutons.append(Button([i, "arrowU"], x-(arrowU.get_width()//2), height // 3 - (arrowU.get_height()//2), 150, 75))
        x,y=[decalage+decalage*i -100, height // 2]
        texts_data[i].append([x,y])


    launched = True

    bg = pygame.image.load("img/bgtest.png").convert()
    bgX = -1
    bgX2 = bg.get_width()
    bgY= -1
    bgY2 = bg.get_height()
    clock = pygame.time.Clock()

    dico={0:"largeur",1:"hauteur",2:"minotaures",3:"boucliers",4:"teleporteurs",5:"Boss level"}

    txt=[]
    txt2=[]
    for i in range(6):
        txt.append(pygame.font.Font('Estelle.ttf', int((widht / height) * 50)).render(str(texts_data[i][0]), True, (255,0,0)))
        txt2.append(pygame.font.Font('Estelle.ttf', int((widht / height) * 25)).render(str(dico[i]), True, (255, 0, 0)))

    def redrawWindow(pos,play_img,arrowU,arrowD,cross,LarrowD,LarrowU,texts_data):

        screen.blit(bg,(bgX,bgY))
        screen.blit(bg,(bgX2,bgY2))

        screen.blit(play_img,play_img.get_rect(center=(widht//2,height//1.2)))

        for i in range(len(texts_data)):
            screen.blit(arrowU,arrowU.get_rect(center=(LarrowU[i][0],LarrowU[i][1])))
            screen.blit(arrowD,arrowD.get_rect(center=(LarrowD[i][0],LarrowD[i][1])))

            rect = pygame.Rect(txt[i].get_rect(center=(texts_data[i][1][0],texts_data[i][1][1]))[0], txt[i].get_rect(center=(texts_data[i][1][0]+50,texts_data[i][1][1]))[1], txt[i].get_width(), txt[i].get_height())
            pygame.draw.rect(screen, (255, 255, 255), rect)

            text=pygame.font.Font('Estelle.ttf', (40 * widht) // 1920).render(str(texts_data[i][0]), True, (255,0,0))
            screen.blit(text, text.get_rect(center=(texts_data[i][1][0],texts_data[i][1][1])))

            rect = pygame.Rect(txt2[i].get_rect(center=(texts_data[i][1][0],height//5))[0], txt2[i].get_rect(center=(texts_data[i][1][0]+50,height//5))[1], txt2[i].get_width(), txt2[i].get_height())
            pygame.draw.rect(screen, (255, 255, 255), rect)
            screen.blit(txt2[i], txt2[i].get_rect(center=(texts_data[i][1][0],height//5)))

        x, y = cross.get_rect(center=(widht/1.1, height/10))[0],cross.get_rect(center=(widht/1.1, height/10))[1]
        screen.blit(cross,(x,y))

        font_size = (20 * widht) // 1920
        authors = pygame.font.Font('Estelle.ttf', font_size).render("Crée par : LAVOILLOTTE Ethan et WEBER Loïc", True, (0, 255, 0))
        rect = pygame.Rect(authors.get_rect(center=(widht / 1.2, height / 1.2))[0],
                           authors.get_rect(center=(widht / 1.3, height / 1.1))[1],
                           authors.get_width(), authors.get_height())
        pygame.draw.rect(screen, (0, 0, 0), rect)
        screen.blit(authors, authors.get_rect(center=(widht / 1.2, height / 1.1)))

        pygame.display.update()

    speed=60

    while launched:
        pos = pygame.mouse.get_pos()
        redrawWindow(pos,play_img,arrowU,arrowD,cross,LarrowD,LarrowU,texts_data)
        clock.tick(speed)
        bgX-=1.75
        bgX2-=1.75
        bgY-=1.25
        bgY2-=1.25
        if bgX<bg.get_width()*-1:
            bgX=bg.get_width()
        if bgX2<bg.get_width()*-1:
            bgX=bg.get_width()
        if bgY<bg.get_height()*-1:
            bgY=bg.get_height()
        if bgY2<bg.get_height()*-1:
            bgY=bg.get_height()

        if bgX>=7000 and bgX2<-7000 and bgY>=5000 and bgY2<=-5000:
            bgX=-217
            bgX2=bg.get_width()
            bgY=-217
            bgY2=bg.get_height()

        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for bouton in boutons:
                    if bouton.isOver(pos) :
                        if bouton.name=="exit":launched=False
                        elif bouton.name=="Play":
                            if texts_data[5][0]!=False:
                                k=texts_data[5][0]
                                maze_interface = maze_interface=new_window("Adventure_entrainement",screen_size,4+(k-1)*3,3+(k-1)*2,-2+(k-1),-3+(k-1),-5+(k-1),k,algo_maze,color_mode,n)
                            else:
                                maze_interface = new_window("Adventure_entrainement", screen_size, texts_data[0][0], texts_data[1][0], texts_data[2][0], texts_data[3][0], texts_data[4][0], 1,algo_maze,color_mode,n)
                            maze_interface.launch_loop()
                        else:
                            if bouton.name[0]==0:
                                if bouton.name[1]=="arrowU":texts_data[0][0]+=1
                                if bouton.name[1] == "arrowD" and texts_data[0][0]>2:texts_data[0][0] -= 1

                            if bouton.name[0]==1:
                                if bouton.name[1]=="arrowU":texts_data[1][0]+=1
                                if bouton.name[1] == "arrowD" and texts_data[1][0]>2: texts_data[1][0] -= 1

                            if bouton.name[0]==2:
                                if bouton.name[1]=="arrowU":texts_data[2][0]+=1
                                if bouton.name[1] == "arrowD" and texts_data[2][0]>0: texts_data[2][0] -= 1

                            if bouton.name[0]==3:
                                if bouton.name[1]=="arrowU":texts_data[3][0]+=1
                                if bouton.name[1] == "arrowD" and texts_data[3][0]>0: texts_data[3][0] -= 1

                            if bouton.name[0]==4:
                                if bouton.name[1]=="arrowU":texts_data[4][0]+=1
                                if bouton.name[1] == "arrowD" and texts_data[4][0]>0: texts_data[4][0] -= 1

                            if bouton.name[0]==5:
                                if texts_data[5][0]==False:texts_data[5][0]=0
                                if bouton.name[1]=="arrowU":texts_data[5][0]+=5
                                if bouton.name[1] == "arrowD" and texts_data[5][0]>0: texts_data[5][0]-=5
                                if texts_data[5][0]==0:texts_data[5][0]=False

            if event.type == pygame.QUIT:
                launched = False

        pygame.display.flip()

def skin(pygame,screen,bg,n):

    widht=screen.get_width()
    height=screen.get_height()

    pygame.mixer.music.load("songs/Motivated.mp3")
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(0.1)

    boutons = []

    cross = pygame.image.load("img/cross.png").convert()
    cross.set_colorkey((127,127,127))

    x, y = cross.get_rect(center=(widht / 1.1, height / 10))[0], cross.get_rect(center=(widht / 1.2, height / 10))[1]
    boutons.append(Button("exit", x, y, 100, 107))

    arrowU = pygame.image.load("img/arrow_up.png").convert()
    arrowL = pygame.transform.rotate(arrowU,90)
    arrowR = pygame.transform.rotate(arrowU, -90)

    nbr_elements_on_screen=3
    decalage=widht/(nbr_elements_on_screen+1)

    arrowLx, arrowLy = arrowL.get_rect(center=(decalage + decalage * 0, height // 2))[0], arrowL.get_rect(center=(decalage + decalage * 0, height // 2))[1]
    boutons.append(Button("arrowL", arrowLx - (arrowL.get_width() // 2), height // 2 - (arrowL.get_height() // 2), 150, 150))
    arrowRx, arrowRy = arrowR.get_rect(center=(decalage + decalage * 2, height // 2))[0], arrowR.get_rect(center=(decalage + decalage * 2, height // 2))[1]
    boutons.append(Button("arrowR", arrowRx - (arrowR.get_width() // 2), height // 2 - (arrowR.get_height() // 2), 150, 150))

    skin_location=[widht//2,height//2]

    skin_index=0

    crowned=False
    levelcap=1

    try:
        board = n.send("board?")
        f = open("infos.txt", "r")
        pseudo = f.readline()
        pseudo = pseudo[:-1]
        if board[0][0]==pseudo:
            crowned=True
        for player in board:
            if player[0]==pseudo:
                levelcap=player[1]
    except:pass

    skins_dico={0:{"name":"Original","color":(0,0,255)},
                1:{"name":"Mango","color":(247,184,1)},
                2:{"name": "Light Pink", "color": (255, 165, 171)},
                3:{"name": "Slimy Green", "color": (55, 150, 52)},
                4:{"name": "Spanish Blue", "color": (1, 111, 185)},
                5:{"name": "Forest Green", "color": (10, 50, 0)},
                6:{"name": "Turquoise Blue", "color": (129, 247, 229)},
                7:{"name": "Dark Purple", "color": (40, 17, 43)},
                8:{"name": "Purple Munsell", "color": (177, 24, 200)},
                9:{"name": "Smoky Black", "color": (9, 12, 2)},
                10:{"name": "Sinopia", "color": (200, 76, 9)},
                11:{"name": "Xiketic", "color": (3, 5, 52)},
                12:{"name": "Yellowish Green", "color": (166, 207, 6)},
                13:{"name": "Red Orange Wheel", "color": (255, 64, 0)},
                14:{"name": "Ghost White", "color": (237, 237, 244)},
                15:{"name": "Russian Violet", "color": (21, 7, 74)},
                16:{"name": "Claret", "color": (133, 32, 60)},
                17:{"name": "Fluorescent Blue", "color": (18, 234, 234)},
                18:{"name": "Celadon Blue", "color": (8, 124, 167)},
                19:{"name": "Ultramarine", "color": (68, 22, 250)}}

    launched = True

    bg = pygame.image.load("img/bgtest.png").convert()
    bgX = -1
    bgX2 = bg.get_width()
    bgY= -1
    bgY2 = bg.get_height()
    clock = pygame.time.Clock()

    def redrawWindow(pos,skin_index):

        screen.blit(bg,(bgX,bgY))
        screen.blit(bg,(bgX2,bgY2))

        pygame.draw.circle(screen,(255,255,255),(widht//2,height//2),(decalage),0)

        circle_radius=100
        pygame.draw.circle(screen,skins_dico[skin_index]['color'],skin_location,circle_radius,0)

        if crowned:
            k=1.5
            offset=[widht//2-((45*k)//2),height//2 -circle_radius - (25*k)]
            poly_pos=[(0+offset[0],0+offset[1]),(0+offset[0],30*k+offset[1]),(40*k+offset[0],30*k+offset[1]),(40*k+offset[0],0+offset[1]),(30*k+offset[0],24*k+offset[1]),(20*k+offset[0],0+offset[1]),(14*k+offset[0],24*k+offset[1])]
            pygame.draw.polygon(screen,(255,255,0),poly_pos)

        screen.blit(arrowL,[arrowLx,arrowLy])
        screen.blit(arrowR,[arrowRx,arrowRy])

        text=pygame.font.Font('Estelle.ttf', int((widht / height) * 40)).render(str(skins_dico[skin_index]['name']), True, skins_dico[skin_index]['color'])
        screen.blit(text, text.get_rect(center=(widht / 2, height / 3.3)))

        x, y = cross.get_rect(center=(widht/1.1, height/10))[0],cross.get_rect(center=(widht/1.1, height/10))[1]
        screen.blit(cross,(x,y))

        font_size = (20 * widht) // 1920
        authors = pygame.font.Font('Estelle.ttf', font_size).render("Crée par : LAVOILLOTTE Ethan et WEBER Loïc", True, (0, 255, 0))
        rect = pygame.Rect(authors.get_rect(center=(widht / 1.2, height / 1.2))[0],
                           authors.get_rect(center=(widht / 1.3, height / 1.1))[1],
                           authors.get_width(), authors.get_height())
        pygame.draw.rect(screen, (0, 0, 0), rect)
        screen.blit(authors, authors.get_rect(center=(widht / 1.2, height / 1.1)))

        font_size = (40 * widht) // 1920
        if levelcap>len(skins_dico):nbr_skins=len(skins_dico)
        else:nbr_skins=levelcap
        text = pygame.font.Font('Estelle.ttf', font_size).render("Vous avez débloqué "+str(nbr_skins)+" / "+str(len(skins_dico))+" skins !", True, (0, 160, 0))
        rect = pygame.Rect(text.get_rect(center=(widht / 2, height / 1.5))[0],
                           text.get_rect(center=(widht / 2, height / 1.5))[1],
                           text.get_width(), text.get_height())
        screen.blit(text, text.get_rect(center=(widht / 2, height / 1.5)))


        pygame.display.update()

    speed=60

    f=open('infos.txt','r')
    pseudo=f.readline()
    password=f.readline()
    skin=f.readline()
    f.close()
    if password[-1]!='\n':
        password+=('\n')

    if skin!=None:
        for skini in skins_dico:
            if skin==skins_dico[skini]['name']:
                skin_index=skini

    while launched:
        pos = pygame.mouse.get_pos()
        redrawWindow(pos,skin_index)
        clock.tick(speed)
        bgX-=1.75
        bgX2-=1.75
        bgY-=1.25
        bgY2-=1.25
        if bgX<bg.get_width()*-1:
            bgX=bg.get_width()
        if bgX2<bg.get_width()*-1:
            bgX=bg.get_width()
        if bgY<bg.get_height()*-1:
            bgY=bg.get_height()
        if bgY2<bg.get_height()*-1:
            bgY=bg.get_height()

        if bgX>=7000 and bgX2<-7000 and bgY>=5000 and bgY2<=-5000:
            bgX=-217
            bgX2=bg.get_width()
            bgY=-217
            bgY2=bg.get_height()

        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for bouton in boutons:
                    if bouton.isOver(pos) :
                        if bouton.name=="exit":
                            f=open('infos.txt','w')                            
                            f.write(str(pseudo)+str(password)+str(skins_dico[skin_index]['name']))
                            f.close()
                            launched=False
                        elif bouton.name=="arrowL" and skin_index>0:
                            skin_index-=1
                        elif bouton.name=="arrowR" and len(skins_dico)-1 > skin_index and levelcap-1 > skin_index:
                            skin_index+=1

            if event.type == pygame.QUIT:
                launched = False

        pygame.display.flip()

def leaderboard(pygame,screen,bg,n):

    boutons = []

    widht=screen.get_width()
    height=screen.get_height()

    img = pygame.image.load("img/cross.png").convert()
    img.set_colorkey((127,127,127))
    x, y = img.get_rect(center=(widht / 1.1, height / 10))[0], img.get_rect(center=(widht / 1.1, height / 10))[1]
    boutons.append(Button("exit", x, y, 100, 107))

    launched = True

    bgX = -1
    bgX2 = bg.get_width()
    bgY = -1
    bgY2 = bg.get_height()
    clock = pygame.time.Clock()

    scores = []

    size = (35 * widht) // 1920

    try:
        board = n.send("board?")
        f = open("infos.txt", "r")
        pseudo = f.readline()
        pseudo = pseudo[:-1]

        index = 0
        while height - size * 1.5 > int(height / 10 + size * 1.5 * index):
            index += 1

        if len(board) > index:
            k = index
        else:
            k = len(board)

        color = (108, 0, 255)

        rank = "#" + ". "
        txtpos = (int(widht / 10), int(height / 10 - size * 1.5))
        text = pygame.font.Font('Estelle.ttf', size).render(rank, False, color)
        scores.append([text, txtpos])

        name = "Name"
        txtpos = (int(widht / 10) + (widht // 2) // 10, int(height / 10 - size * 1.5))
        text = pygame.font.Font('Estelle.ttf', size).render(name, False, color)
        scores.append([text, txtpos])

        level = "Level"
        txtpos = (int(widht / 10) + (widht // 2) // 3, int(height / 10 - size * 1.5))
        text = pygame.font.Font('Estelle.ttf', size).render(level, False, color)
        scores.append([text, txtpos])

        w = "widht"
        txtpos = (int(widht /10) + (widht // 2) // 2.1, int(height / 10 - size * 1.5))
        text = pygame.font.Font('Estelle.ttf', size).render(w, False, color)
        scores.append([text, txtpos])

        h = "height"
        txtpos = (int(widht / 10) + (widht // 2) // 1.7, int(height / 10 - size * 1.5))
        text = pygame.font.Font('Estelle.ttf', size).render(h, False, color)
        scores.append([text, txtpos])

        nbr_move = "Déplacements"
        txtpos = (int(widht / 10) + (widht // 2) // 1.40, int(height / 10 - size * 1.5))
        text = pygame.font.Font('Estelle.ttf', size).render(nbr_move, False, color)
        scores.append([text, txtpos])

        timer = "Timer"
        txtpos = (int(widht / 10) + (widht // 2.1), int(height / 10 - size * 1.5))
        text = pygame.font.Font('Estelle.ttf', size).render(timer, False, color)
        scores.append([text, txtpos])

        heure = "[Time]"
        txtpos = (int(widht / 10) + (widht // 1.8), int(height / 10 - size * 1.5))
        text = pygame.font.Font('Estelle.ttf', size).render(str(heure), False, color)
        scores.append([text, txtpos])

        date = "[Date]"
        txtpos = (int(widht / 10) + (widht // 1.55), int(height / 10 - size * 1.5))
        text = pygame.font.Font('Estelle.ttf', size).render(str(date), False, color)
        scores.append([text, txtpos])

        for i in range(k):

            color = (255, 0, 128)
            if i == 0:color = (255, 255, 0)
            
            if str(board[i][0]) == pseudo: color = (0, 255, 0)

            rank = str(i + 1) + ". "
            txtpos = (int(widht / 10), int(height / 10 + size * 1.5 * i))
            text = pygame.font.Font('Estelle.ttf', size).render(rank, False, color)
            scores.append([text, txtpos])

            name = str(board[i][0])
            txtpos = (int(widht / 10) + (widht // 2) // 10, int(height / 10 + size * 1.5 * i))
            text = pygame.font.Font('Estelle.ttf', size).render(name, False, color)
            scores.append([text, txtpos])

            level = str(board[i][1])
            txtpos = (int(widht / 10) + (widht // 2) // 3, int(height / 10 + size * 1.5 * i))
            text = pygame.font.Font('Estelle.ttf', size).render(level, False, color)
            scores.append([text, txtpos])

            w = str(board[i][3])
            txtpos = (int(widht / 10) + (widht // 2) // 2.1, int(height / 10 + size * 1.5 * i))
            text = pygame.font.Font('Estelle.ttf', size).render(w, False, color)
            scores.append([text, txtpos])

            h = str(board[i][4])
            txtpos = (int(widht / 10) + (widht // 2) // 1.7, int(height / 10 + size * 1.5 * i))
            text = pygame.font.Font('Estelle.ttf', size).render(h, False, color)
            scores.append([text, txtpos])

            nbr_move = str(board[i][5])
            txtpos = (int(widht / 10) + (widht // 2) // 1.4, int(height / 10 + size * 1.5 * i))
            text = pygame.font.Font('Estelle.ttf', size).render(nbr_move, False, color)
            scores.append([text, txtpos])

            timer = str(board[i][6])
            txtpos = (int(widht / 10) + (widht // 2.1), int(height / 10 + size * 1.5 *i))
            text = pygame.font.Font('Estelle.ttf', size).render(timer, False, color)
            scores.append([text, txtpos])

            heure = " [" + str(board[i][2].hour) + ":" + str(board[i][2].minute) + "]"
            txtpos = (int(widht / 10) + (widht // 1.85), int(height / 10 + size * 1.5 * i))
            text = pygame.font.Font('Estelle.ttf', size).render(str(heure), False, color)
            scores.append([text, txtpos])

            date = "[" + str(board[i][2].day) + "/" + str(board[i][2].month) + "/" + str(board[i][2].year) + "]"
            txtpos = (int(widht / 10) + (widht // 1.6), int(height / 10 + size * 1.5 * i))
            text = pygame.font.Font('Estelle.ttf', size).render(str(date), False, color)
            scores.append([text, txtpos])

    except:
        Error="Connectez vous a internet."
        txtpos = (int(widht / 3), int(height / 2))
        text = pygame.font.Font('Estelle.ttf', size*2).render(Error, False, (255,0,0))
        scores.append([text, txtpos])

    speed = 60

    def redrawWindow(pos,scores):

        screen.blit(bg, (bgX, bgY))
        screen.blit(bg, (bgX2, bgY2))

        img = pygame.image.load("img/cross.png").convert()
        img.set_colorkey((127,127,127))
        x, y = img.get_rect(center=(widht / 1.1, height / 10))[0], img.get_rect(center=(widht / 1.1, height / 10))[1]
        screen.blit(img, (x, y))

        pygame.draw.rect(screen,(0,0,0),(scores[0][1][0]-40,height//25,widht//1.3,scores[-1][1][1]+20),0)

        for score in scores:
            screen.blit(score[0],score[1])

        font_size = (20 * widht) // 1920
        authors = pygame.font.Font('Estelle.ttf', font_size).render("Crée par : LAVOILLOTTE Ethan et WEBER Loïc", True, (0, 255, 0))
        rect = pygame.Rect(authors.get_rect(center=(widht / 1.2, height / 1.2))[0],
                           authors.get_rect(center=(widht / 1.3, height / 1.1))[1],
                           authors.get_width(), authors.get_height())
        pygame.draw.rect(screen, (0, 0, 0), rect)
        screen.blit(authors, authors.get_rect(center=(widht / 1.2, height / 1.1)))

        k=0.5
        offset=[(scores[0][1][0]+scores[1][1][0])//2,scores[10][1][1]+font_size//2]
        poly_pos=[(0+offset[0],0+offset[1]),(0+offset[0],30*k+offset[1]),(40*k+offset[0],30*k+offset[1]),(40*k+offset[0],0+offset[1]),(30*k+offset[0],24*k+offset[1]),(20*k+offset[0],0+offset[1]),(14*k+offset[0],24*k+offset[1])]
        pygame.draw.polygon(screen,(255,255,0),poly_pos)

        pygame.display.update()

    while launched:
        pos = pygame.mouse.get_pos()
        redrawWindow(pos,scores)
        clock.tick(speed)
        bgX -= 1.75
        bgX2 -= 1.75
        bgY -= 1.25
        bgY2 -= 1.25
        if bgX < bg.get_width() * -1:
            bgX = bg.get_width()
        if bgX2 < bg.get_width() * -1:
            bgX = bg.get_width()
        if bgY < bg.get_height() * -1:
            bgY = bg.get_height()
        if bgY2 < bg.get_height() * -1:
            bgY = bg.get_height()

        if bgX >= 7000 and bgX2 < -7000 and bgY >= 5000 and bgY2 <= -5000:
            bgX = -217
            bgX2 = bg.get_width()
            bgY = -217
            bgY2 = bg.get_height()

        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for bouton in boutons:
                    if bouton.isOver(pos):
                        if bouton.name == "exit":
                            launched = False

            if event.type == pygame.QUIT:
                launched = False
        pygame.display.flip()

def message_au_dev(pygame,screen,bg,n):

    import mysql.connector
    import datetime

    def connexion():
        # Connexion à la base de donnée
        connexion_mysql = mysql.connector.connect(host="152.89.237.254", port="3306", user="message",password="password", database="dedale")
        return connexion_mysql


    boutons = []

    widht=screen.get_width()
    height=screen.get_height()

    cross = pygame.image.load("img/cross.png").convert()
    cross.set_colorkey((127,127,127))
    x, y = cross.get_rect(center=(widht / 1.1, height / 10))[0], cross.get_rect(center=(widht / 1.1, height / 10))[1]
    boutons.append(Button("exit", x, y, 100, 107))

    launched = True

    bgX = -1
    bgX2 = bg.get_width()
    bgY = -1
    bgY2 = bg.get_height()
    clock = pygame.time.Clock()

    scores = []

    size = (35 * widht) // 1920

    try:
        board = n.send("board?")
        f = open("infos.txt", "r")
        pseudo = f.readline()
        pseudo = pseudo[:-1]
    except:
        Error="Connectez vous a internet."
        txtpos = (int(widht / 3), int(height / 2))
        text = pygame.font.Font('Estelle.ttf', size*2).render(Error, False, (255,0,0))
        scores.append([text, txtpos])

    speed = 60
    color_active = pygame.Color('gray50')
    color_passive = pygame.Color('gray15')  # des couleurs pour savoir si on est entrain de taper dans le champ ou non
    color = color_passive
    boxActive = True
    user_text=""
    k=80

    font_size = (20 * widht) // 1920
    authors = pygame.font.Font('Estelle.ttf', font_size).render("Crée par : LAVOILLOTTE Ethan et WEBER Loïc", True, (0, 255, 0))
    rect_authors = pygame.Rect(authors.get_rect(center=(widht / 1.2, height / 1.2))[0],
                        authors.get_rect(center=(widht / 1.3, height / 1.1))[1],
                        authors.get_width(), authors.get_height())

    font_size = (40 * widht) // 1920
    text2 = pygame.font.Font('Estelle.ttf', font_size).render("Que ce soit un signalement de bug, un problème avec Dédale, une question sur le jeu,", False, (0, 255, 0))
    rect2 = pygame.Rect(text2.get_rect(center=(widht / 2, height / 2.9))[0],text2.get_rect(center=(widht / 2, height / 2.9 ))[1],text2.get_width(), text2.get_height())

    text3 = pygame.font.Font('Estelle.ttf', font_size).render("un mot gentil, une blague drole, une théorie phylosophique, NIMPORTE QUOI !", False, (0, 255, 0))
    rect3 = pygame.Rect(text3.get_rect(center=(widht / 2, height / 2.5))[0],text3.get_rect(center=(widht / 2, height / 2.5))[1],text3.get_width(), text3.get_height())

    i=0
    message_sent=None
    def redrawWindow(pos,i):
        
        font_size = (80 * widht) // 1920

        if message_sent==True:
            text1 = pygame.font.Font('Estelle.ttf', int(font_size*1.5)).render("MESSAGE BIEN ENVOYE", False, (0, 255, 0))
            rect1 = pygame.Rect(text1.get_rect(center=(widht / 2, height / 4))[0],text1.get_rect(center=(widht / 2, height / 4))[1],text1.get_width(), text1.get_height())
        elif message_sent==False:
            text1 = pygame.font.Font('Estelle.ttf', int(font_size*0.4)).render("IL Y A UN PROBLEME, ESSAYER DE RELANCER TON JEU, SINON CONTACT MOI PAR DISCORD : JustAlternate#8683 ", False, (255, 0, 0))
            rect1 = pygame.Rect(text1.get_rect(center=(widht / 2, height / 4))[0],text1.get_rect(center=(widht / 2, height / 4))[1],text1.get_width(), text1.get_height())
        else:
            text1 = pygame.font.Font('Estelle.ttf', font_size).render("Envoie moi un message !", False, (255, 255, 0))
            rect1 = pygame.Rect(text1.get_rect(center=(widht / 2, height / 4))[0],text1.get_rect(center=(widht / 2, height / 4))[1],text1.get_width(), text1.get_height())


        screen.blit(bg, (bgX, bgY))
        screen.blit(bg, (bgX2, bgY2))

        x, y = cross.get_rect(center=(widht / 1.1, height / 10))[0], cross.get_rect(center=(widht / 1.1, height / 10))[1]
        screen.blit(cross, (x, y))

        pygame.draw.rect(screen, (0, 0, 0), rect_authors)
        screen.blit(authors, authors.get_rect(center=(widht / 1.2, height / 1.1)))
        
        pygame.draw.rect(screen, (0, 0, 0), rect1)
        screen.blit(text1, text1.get_rect(center=(widht / 2, height / 4)))

        pygame.draw.rect(screen, (0, 0, 0), rect2)
        screen.blit(text2, text2.get_rect(center=(widht / 2, height / 2.9)))
            
        pygame.draw.rect(screen, (0, 0, 0), rect3)
        screen.blit(text3, text3.get_rect(center=(widht / 2, height / 2.5)))

        if boxActive: color = color_active

        font_size = ((100-i) * widht) // 1920
        if (len(user_text)+1)*(font_size//2) > widht*0.8 :
            i+=1

        w,h=widht,font_size*2
        input_rect = pygame.Rect(font_size*2 , height /2 , (len(user_text)+1)*(font_size//2), h) # x, y ,width , height
        pygame.draw.rect(screen, color, input_rect, 2)  # 2 = l'épaisseur du bord
        screen.fill(color, input_rect)
        text_surface = pygame.font.Font('Estelle.ttf', font_size).render(user_text, True, (255, 255, 255))  # 255 255 255 = couleur du text
        screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))  # le cadre
 
        pygame.display.update()

        return input_rect,i

    while launched:
        pos = pygame.mouse.get_pos()
        input_rect,i=redrawWindow(pos,i)
        clock.tick(speed)
        bgX -= 1.75
        bgX2 -= 1.75
        bgY -= 1.25
        bgY2 -= 1.25
        if bgX < bg.get_width() * -1:
            bgX = bg.get_width()
        if bgX2 < bg.get_width() * -1:
            bgX = bg.get_width()
        if bgY < bg.get_height() * -1:
            bgY = bg.get_height()
        if bgY2 < bg.get_height() * -1:
            bgY = bg.get_height()

        if bgX >= 7000 and bgX2 < -7000 and bgY >= 5000 and bgY2 <= -5000:
            bgX = -217
            bgX2 = bg.get_width()
            bgY = -217
            bgY2 = bg.get_height()

        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for bouton in boutons:

                    if bouton.isOver(pos):
                        pygame.mixer.music.stop()

                        if bouton.name == "exit":
                            launched=False

                if input_rect.collidepoint(event.pos):  # la souris est elle sur le rectangle ?
                    boxActive = True  # on "active" le champ de saisie

            if event.type == pygame.KEYDOWN:  # utilise t-on le clavier ?
                if boxActive == True:

                    if event.key == pygame.K_RETURN:  # valider avec la touche Entrée
                        message=user_text
                        try:
                            req="INSERT INTO messages_au_dev VALUES ('"+str(pseudo)+"','"+str(message)+"',CURRENT_TIMESTAMP());"
                            connexion_mysql = connexion()
                            cur_BD = connexion_mysql.cursor()
                            cur_BD.execute(req)
                            connexion_mysql.commit()
                            connexion_mysql.close()
                            user_text=""
                            message_sent=True
                        except:
                            message_sent=False

                    elif event.key == pygame.K_BACKSPACE:  # enlever un caractere
                        user_text = user_text[:-1]


                    elif len(user_text) < 300:  # mettre une taille limite de caractère
                        user_text+=event.unicode


def bonus_Maze(algo_maze,color_mode,screen,pygame,bg,n):
    widht = screen_size.current_w
    height = screen_size.current_h

    pygame.mixer.music.load("songs/Motivated.mp3")
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(0.1)

    boutons = []

    images=[pygame.image.load("img/Entrainement_Aventure.png").convert(),pygame.image.load("img/Leaderboard.png").convert(),
            pygame.image.load("img/CustomLevel.png").convert(),pygame.image.load("img/message_dev.png"),pygame.image.load("img/Skins-Cosmetiques.png").convert(),pygame.image.load("img/cross.png").convert()]

    levelcap=1

    try:
        board = n.send("board?")
        f = open("infos.txt", "r")
        pseudo = f.readline()
        pseudo = pseudo[:-1]
        for player in board:
            if player[0]==pseudo:
                levelcap=player[1]
    except:pass

    if levelcap<25:images[2]=pygame.image.load("img/CustomLevelDISABLE.png").convert()

    scale_imgs=[]
    for i in range(len(images)):
        w, h = images[i].get_width(), images[i].get_height()
        new_w, new_h = (w * widht) // 1920, (h * height) // 1080
        images[i]=pygame.transform.scale(images[i], (new_w, new_h))
        images[i].set_colorkey((127,127,127))

        img2=pygame.transform.scale(images[i], (320, 182))
        w, h = img2.get_width(), img2.get_height()
        new_w, new_h = (w * widht) // 1920, (h * height) // 1080
        img2=pygame.transform.scale(img2, (new_w, new_h))
        img2.set_colorkey((127,127,127))
        scale_imgs.append(img2)

    img=images[0]
    x, y = img.get_rect(center=(widht / 2, height / 2.3))[0],img.get_rect(center=(widht / 2, height / 2.3))[1]
    boutons.append(Button("Entrainement_Aventure", x, y, img.get_width(), img.get_height()))

    img=images[1]
    x, y = img.get_rect(center=(widht / 5, height / 2.3))[0],img.get_rect(center=(widht / 5, height / 2.3))[1]
    boutons.append(Button("Leaderboard", x, y, img.get_width(), img.get_height()))

    img=images[2]
    x, y = img.get_rect(center=(widht / 1.25, height / 2.3))[0],img.get_rect(center=(widht / 1.25, height / 2.3))[1]
    boutons.append(Button("Custom", x, y, img.get_width(), img.get_height()))

    img=images[3]
    x, y = img.get_rect(center=(widht / 2, height / 1.3))[0],img.get_rect(center=(widht / 2, height / 1.3))[1]
    boutons.append(Button("Cosmetique", x, y, img.get_width(), img.get_height()))

    img=images[4]
    x, y = img.get_rect(center=(widht/1.25, height / 1.3))[0],img.get_rect(center=(widht / 1.25, height / 1.3))[1]
    boutons.append(Button("message_au_dev", x, y, img.get_width(), img.get_height()))

    img = images[5]
    x, y = img.get_rect(center=(widht / 1.1, height / 10))[0], img.get_rect(center=(widht / 1.1, height / 10))[1]
    boutons.append(Button("exit", x, y, img.get_width(), img.get_height()))



    launched = True

    bgX = -1
    bgX2 = bg.get_width()
    bgY= -1
    bgY2 = bg.get_height()
    clock = pygame.time.Clock()

    def redrawWindow(pos,images,scale_imgs,bg):

        screen.blit(bg,(bgX,bgY))
        screen.blit(bg,(bgX2,bgY2))

        img = images[0]
        rect=img.get_rect(center=(widht / 2, height / 2.3))
        if rect.collidepoint(pos):
            img = scale_imgs[0]
        screen.blit(img,img.get_rect(center=(widht / 2, height / 2.3)))

        img = images[1]
        rect=img.get_rect(center=(widht / 5, height / 2.3))
        if rect.collidepoint(pos):
            img = scale_imgs[1]
        screen.blit(img,img.get_rect(center=(widht / 5, height / 2.3)))

        img = images[2]
        rect=img.get_rect(center=(widht / 1.25, height / 2.3))
        if rect.collidepoint(pos):
            img = scale_imgs[2]
        screen.blit(img,img.get_rect(center=(widht / 1.25, height / 2.3)))

        img = images[4]
        rect=img.get_rect(center=(widht / 2, height / 1.3))
        if rect.collidepoint(pos):
            img = scale_imgs[4]
        screen.blit(img,img.get_rect(center=(widht / 2, height / 1.3)))

        img = images[3]
        rect=img.get_rect(center=(widht / 1.25, height / 1.3))
        if rect.collidepoint(pos):
            img = scale_imgs[3]
        screen.blit(img,img.get_rect(center=(widht / 1.25, height / 1.3)))


        img = images[5]
        x, y = img.get_rect(center=(widht/1.1, height/10))[0],img.get_rect(center=(widht/1.1, height/10))[1]
        screen.blit(img,(x,y))

        font_size = (20 * widht) // 1920
        authors = pygame.font.Font('Estelle.ttf', font_size).render("Crée par : LAVOILLOTTE Ethan et WEBER Loïc", True, (0, 255, 0))
        rect = pygame.Rect(authors.get_rect(center=(widht / 1.2, height / 1.2))[0],
                           authors.get_rect(center=(widht / 1.3, height / 1.1))[1],
                           authors.get_width(), authors.get_height())
        pygame.draw.rect(screen, (0, 0, 0), rect)
        screen.blit(authors, authors.get_rect(center=(widht / 1.2, height / 1.1)))

        pygame.display.update()

    speed=60

    while launched:
        try:
            pos = pygame.mouse.get_pos()
            redrawWindow(pos,images,scale_imgs,bg)
            clock.tick(speed)
            bgX-=1.75
            bgX2-=1.75
            bgY-=1.25
            bgY2-=1.25
            if bgX<bg.get_width()*-1:
                bgX=bg.get_width()
            if bgX2<bg.get_width()*-1:
                bgX=bg.get_width()
            if bgY<bg.get_height()*-1:
                bgY=bg.get_height()
            if bgY2<bg.get_height()*-1:
                bgY=bg.get_height()

            if bgX>=7000 and bgX2<-7000 and bgY>=5000 and bgY2<=-5000:
                bgX=-217
                bgX2=bg.get_width()
                bgY=-217
                bgY2=bg.get_height()
        except:pass

        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for bouton in boutons:
                    if bouton.isOver(pos) :
                        if bouton.name=="exit":launched=False
                        elif bouton.name == "Leaderboard":
                            leaderboard(pygame,screen,bg,n)
                        elif bouton.name == "Entrainement_Aventure":
                            Entrainement_choix(pygame,screen,algo_maze,color_mode,bg,n)
                        elif bouton.name == "Cosmetique":
                            skin(pygame, screen, bg,n)
                        elif bouton.name == "Custom" and levelcap>=25:
                            niv_custom(pygame, screen, algo_maze, color_mode, bg,n)
                        elif bouton.name == "message_au_dev":
                            message_au_dev(pygame,screen,bg,n)

            if event.type == pygame.QUIT:
                launched = False

        pygame.display.flip()



