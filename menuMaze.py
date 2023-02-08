from tkinter.tix import DECREASING
import pygame,os
from button import *
from network import *
from settingMaze import *
from bonusMaze import *
from maze_interface import *
from createAccount import *

def menu_Maze():
    pygame.init()
    screen_size = pygame.display.Info()
    widht = screen_size.current_w
    height = screen_size.current_h
    screen = pygame.display.set_mode((widht,height),pygame.NOFRAME)

    n=Network()

    def get_board(n):
        try:
            board = n.send("board?")
            f = open("infos.txt", "r")
            pseudo = f.readline()
            pseudo = pseudo[:-1]
            for player in board:
                if player[0]==pseudo:
                    levelcap=player[1]
            f.close()
            return levelcap,pseudo
        except:
            return 1,"Not connected to the server"

    try:
        f=open("infos.txt","r")
        if f.readline()==None:
            createAccount(pygame,screen,None,None)
        f.close()
    except:createAccount(pygame,screen,None,None)

    pygame.mixer.music.load("songs/Motivated.mp3")
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(0.1)

    f=open("divers/splashs.txt","r")
    splashs=f.read().split('\n')
    f.close()
    splash=splashs[randint(0,len(splashs)-1)]
    algo_maze="Itératif"
    color_mode="Dark"

    boutons=[]

    images=["img/playMaze.png","img/imageSettingMaze.png","img/adventureMaze.png",'img/Bonus.png',"img/mazeTitle.png"]


    pos=[2.3,1.5,1.1,1.1]
    imgs=[pygame.image.load(images[0]),pygame.image.load(images[1]),pygame.image.load(images[2]),pygame.image.load(images[3])]

    for i in range(len(images)-1):
        if i == 3:x, y = imgs[i].get_rect(center=(widht / 10, height / pos[i]))[0], imgs[i].get_rect(center=(widht / 10, height / pos[i]))[1]
        else:x,y=imgs[i].get_rect(center=(widht / 2, height / pos[i]))[0],imgs[i].get_rect(center=(widht / 2, height / pos[i]))[1]
        boutons.append(Button(i,x,y,imgs[i].get_width(),imgs[i].get_height()))

    levelcap,pseudo=get_board(n)
    if levelcap<5:images[3]="img/BonusDISABLE.png"

    images_loaded=[]
    for img in images:
        image=pygame.image.load(img).convert()
        image.set_colorkey((127,127,127))
        w, h = image.get_width(), image.get_height()
        new_w, new_h = (w * widht) // 1920, (h * height) // 1080
        image = pygame.transform.scale(image, (new_w, new_h))
        images_loaded.append(image)

    scale_imgs=[]

    for img in images_loaded:
        img=pygame.transform.scale(img, (320, 182))
        w, h = img.get_width(), img.get_height()
        new_w, new_h = (w * widht) // 1920, (h * height) // 1080
        scale_imgs.append(pygame.transform.scale(img, (new_w, new_h)))

    img_vrac_raw=['img/mazeTitle.png',"img/cross.png","img/Recursif.png","img/Iteratif.png","img/dark_mode.png","img/light_mode.png"]
    img_vrac=[]

    for img in img_vrac_raw:
        img=pygame.image.load(img).convert()
        img.set_colorkey((127, 127, 127))
        w, h = img.get_width(), img.get_height()
        new_w, new_h = (w * widht) // 1920, (h * height) // 1080
        img_vrac.append(pygame.transform.scale(img, (new_w, new_h)))

    img=img_vrac[1]
    x, y = img.get_rect(center=(widht / 1.1, height / 10))[0], img.get_rect(center=(widht / 1.2, height / 10))[1]
    boutons.append(Button("exit", x, y, img.get_width(), img.get_height()))

    img=img_vrac[3]
    x, y = img.get_rect(center=(widht / 10, height / 10))[0], img.get_rect(center=(widht / 10, height / 10))[1]
    boutons.append(Button("algo_maze", x, y, img.get_width(), img.get_height()))

    img=img_vrac[5]
    x, y = img.get_rect(center=(widht / 1.3, height / 15))[0], img.get_rect(center=(widht / 1.1, height / 10))[1]
    boutons.append(Button("color_mode", x, y, img.get_width(), img.get_height()))

    img_vrac_pos=[]
    img_vrac_pos.append((img.get_rect(center=(widht/1.1, height/10))[0],img.get_rect(center=(widht/1.2, height/10))[1]))
    img_vrac_pos.append((img.get_rect(center=(widht / 10, height / 10))[0], img.get_rect(center=(widht / 10, height / 10))[1]))
    img_vrac_pos.append((img.get_rect(center=(widht / 1.3, height / 15))[0], img.get_rect(center=(widht / 1.1, height / 10))[1]))


    pos_img = [2.3, 1.5, 1.1, 1.1]

    def make_rect(text,w1,h1,w2,h2):
        return pygame.Rect(text.get_rect(center=(widht / w1, height / h1))[0],
                       text.get_rect(center=(widht / w2, height / h2))[1],
                       text.get_width(), text.get_height())

    font_size_authors = (20 * widht) // 1920
    authors_of_game = pygame.font.Font('Estelle.ttf', font_size_authors).render("Crée par : LAVOILLOTTE Ethan et WEBER Loïc", True, (0, 255, 0))
    rect_autors_of_game = make_rect(authors_of_game,1.2,1.2,1.3,1.1)
    pos_authors_of_game = authors_of_game.get_rect(center=(widht / 1.2, height / 1.1))


    discord = pygame.font.Font('Estelle.ttf', font_size_authors).render("https://discord.gg/pwJ3SuFxA8", True, (0, 255, 0))
    discord_rect = make_rect(discord,1.2,1.1,1.3,1.05)
    pos_discord = discord.get_rect(center=(widht / 1.2, height / 1.05))

    splash_pos=(widht/2+(img_vrac[0].get_width()/1.5), height/8+(img_vrac[0].get_height()/1.5))


    def redrawWindow(pos,splash,algo_maze,images_loaded,scale_imgs,img_vrac,img_vrac_pos,bg,onit,splash_size,decreasing,ticks):

        screen.blit(bg,(bgX,bgY))
        screen.blit(bg,(bgX2,bgY2))

        for i in range(4):
            img = images_loaded[i]
            if i == 3:rect=img.get_rect(center=(widht / 10, height / pos_img[i]))
            else:rect=img.get_rect(center=(widht / 2, height / pos_img[i]))
            if rect.collidepoint(pos):
                img=scale_imgs[i]

            if i == 3:
                screen.blit(img, img.get_rect(center=(widht / 10, height / pos_img[i])))
            else:
                screen.blit(img,img.get_rect(center=(widht / 2, height / pos_img[i])))

        screen.blit(img_vrac[0], img_vrac[0].get_rect(center=(widht/2, height/6)))

        screen.blit(img_vrac[1],img_vrac_pos[0])

        if algo_maze == "Récursif":
            screen.blit(img_vrac[2],img_vrac_pos[1])
        else:
            screen.blit(img_vrac[3],img_vrac_pos[1])

        if color_mode == "Dark":
            img=img_vrac[4]
            x, y = img_vrac[4].get_rect(center=(widht / 1.3, height / 15))[0], img_vrac[4].get_rect(center=(widht / 10, height / 10))[1]
            screen.blit(img_vrac[4],img_vrac_pos[2])
        
        else:
            x, y = img_vrac[5].get_rect(center=(widht / 1.3, height / 15))[0], img_vrac[5].get_rect(center=(widht / 10, height / 10))[1]
            screen.blit(img_vrac[5],img_vrac_pos[2])
        
        max_splash_size = ((500//len(splash))*widht)//1920
        min_splash_size = ((400//len(splash))*widht)//1920

        if splash_size > max_splash_size:
            decreasing = True
        elif splash_size < min_splash_size:
            decreasing = False

        ticks+=1
        if ticks%6==0:
            if decreasing:
                splash_size-=1
            else:
                splash_size+=1

        text = pygame.font.Font('divers/Minecraftia.ttf', splash_size).render(splash, False, (249, 248, 80))
        text = pygame.transform.rotate(text, 20)

        screen.blit(text, img_vrac[0].get_rect(center=splash_pos))

        pygame.draw.rect(screen, (0, 0, 0), rect_autors_of_game)
        screen.blit(authors_of_game, pos_authors_of_game)

        pygame.draw.rect(screen, (0, 0, 0), discord_rect)
        screen.blit(discord,pos_discord)

        if pseudo=="Not connected to the server":
            color=(225,0,0)
        else:
            color=(225,155,0)

        authors = pygame.font.Font('Estelle.ttf', font_size_authors).render("Connecté en tant que : "+str(pseudo), True, color)
        rect = pygame.Rect(authors.get_rect(center=(widht / 8, font_size_authors*2))[0],
                        authors.get_rect(center=(widht / 8, font_size_authors*2))[1],
                        authors.get_width(), authors.get_height())
        pygame.draw.rect(screen, (0, 0, 0), rect)
        screen.blit(authors, authors.get_rect(center=(widht / 8, font_size_authors*2)))


        pygame.display.update()
        
        return splash,onit,decreasing,splash_size,ticks

    launched = True

    bg = pygame.image.load("img/bgtest.png").convert()
    bgX = -1
    bgX2 = bg.get_width()
    bgY= -1
    bgY2 = bg.get_height()
    clock = pygame.time.Clock()

    speed=60
    onit=False
    splash_size=((500//len(splash))*widht)//1920
    decreasing=False
    ticks=0

    while launched:

        pos = pygame.mouse.get_pos()
        splash,onit,decreasing,splash_size,ticks=redrawWindow(pos,splash,algo_maze,images_loaded,scale_imgs,img_vrac,img_vrac_pos,bg,onit,splash_size,decreasing,ticks)
        clock.tick(speed)
        bgX-=1.8
        bgX2-=1.8
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

        if bgX>=8500 and bgX2<-8500 and bgY>=5600 and bgY2<=-5600:
            bgX=-217
            bgX2=bg.get_width()
            bgY=-217
            bgY2=bg.get_height()

        for event in pygame.event.get():
            if event.type==pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for bouton in boutons:

                    if bouton.isOver(pos):

                        if bouton.name=="exit":
                            pygame.mixer.music.stop()
                            pygame.quit()
                            launched=False

                        elif bouton.name == 1:
                            pygame.mixer.music.stop()
                            settings_Maze(algo_maze,color_mode,n)

                        elif bouton.name == 0:
                            pygame.mixer.music.stop()
                            maze_interface = new_window("Tuto", screen_size, 10, 7, 0, 0, 0, "Tuto",algo_maze,color_mode,n)
                            maze_interface.launch_loop()
                            levelcap,pseudo=get_board(n)


                        elif bouton.name == 2:
                            pygame.mixer.music.stop()
                            maze_interface = new_window("Adventure", screen_size, 4, 3, -1, -2, -5, 1,algo_maze,color_mode,n)
                            maze_interface.launch_loop()
                            levelcap,pseudo=get_board(n)

                        elif bouton.name == 3 and levelcap>=5:
                            pygame.mixer.music.stop()
                            bonus_Maze(algo_maze,color_mode,screen,pygame,bg,n)


                        elif bouton.name == "algo_maze":
                            if algo_maze=="Itératif":algo_maze="Récursif"
                            else:algo_maze="Itératif"

                        elif bouton.name == "color_mode":
                            if color_mode=="Dark":color_mode="Light"
                            else:color_mode="Dark"

            if event.type == pygame.QUIT:
                launched = False

menu_Maze()
