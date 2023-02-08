import os,pygame
from button import *
from network import *
from random import randint

def createAccount(pygame,screen,name,password):
    n = Network()

    screen_size = pygame.display.Info()
    widht = screen_size.current_w
    height = screen_size.current_h

    pygame.mixer.music.load("songs/Motivated.mp3")
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(0.1)

    splashs = ["Eliott", "BricoBricard", "Un homme de Dieu", "J'ai menti !","Barbossa","std::cout<<\"Pire language\"<<std::endl;","Ya moyen.. dans.. 2.. semaines..","Minecraft reference !", "ALED !", "Python !", "Base maink :O",
               "Le rasoir d'Ockham", "Sub 30 pain italien svp", "pile(), depile()", "for i in range(n):","Time to Slay !", "Splash text", "SpeedyBoi", "JESUSS!!!","RespectMyQiyana",
               "Atchoummm", "JustAlternate.pw", "La Bro Lounge", "Pingu", "Hey !", "Welcome Back", "Crewmate again","Impostor ?", "Dattebayo", "Jiraya :')", "Hokage !", "Ultra vomit !",
               "Skyyart 257.5 IQ !", "Pouah !", "Sardoche notre prophete", "Crazy Frog", "Bonjour","open mid ff15", "J'ai buy une AWP!", "RASENGAN!!!", "KAKAROTO", "Goku super sayan divin+++","Kammisam",
               "je suis content", "MAIS C'ETAIT SUR ENFAIT!!!", "G2 18 minutes", "MAIS NAN!", "MP2I !","Doscord !","https://discord.gg/xE8At9SgkE", "Canals", "CHECK MATE !", "Technique de la derivée 2nd",
               "La blague du mec au bec de cannard","Bah Yes","Chipie1007","Dédale BETA !","Le dormeur","Descend dans le bowl","H@ck3rman",
               "Groovy le boss","Minkavi devient ingénieur","Boss lvl 25","Récursivité","Itératif","La blague est valide","Le paradoxe du barbier de Séville",
               "Centos 7 > Unbuntu","Made with Pygame !","Compiled with auto-py-to-exe","Alexthunder a gagné les 20 €","Wolololo","Age of empire 2","JustAlternate sur osu!","Osu!",
               "Sharingan","le méchant minotaure","Rien du tout","Easter egg sur l'écran d'acceuil","http://JustAlternate.pw/alexandre_le_boss.mp4","Expert du Franglais !"," <3 Gwendal et Isak <3 "]
    splash = splashs[randint(0, len(splashs) - 1)]

    boutons = []

    images = ["img/Enter.png", "img/imageSettingMaze.png", "img/adventureMaze.png", "img/mazeTitle.png"]

    bg = pygame.image.load("img/bgtest.png").convert()
    screen.blit(bg, (0, 0))

    img = pygame.image.load("img/cross.png").convert()
    img.set_colorkey((127,127,127))
    x, y = img.get_rect(center=(widht / 1.1, height / 10))[0], img.get_rect(center=(widht / 1.2, height / 10))[1]
    boutons.append(Button("exit", x, y, 100, 107))
    screen.blit(img, (x, y))

    img=pygame.image.load("img/mazeTitle.png").convert()
    img.set_colorkey((127,127,127))
    w, h = img.get_width(), img.get_height()
    new_w, new_h = (w * widht) // 1920, (h * height) // 1080
    title = pygame.transform.scale(img, (new_w, new_h))
    screen.blit(title, title.get_rect(center=(widht / 2, height / 6)))

    text = pygame.font.Font('divers/Minecraftia.ttf', int(60 - len(splash))).render(splash, False, (249, 248, 80))
    text = pygame.transform.rotate(text, 20)
    screen.blit(text, title.get_rect(center=(widht / 2 + (title.get_width() / 1.5), height / 6 + (title.get_height() / 1.5))))

    font_size = (20 * widht) // 1920
    authors = pygame.font.Font('Estelle.ttf', font_size).render("Crée par : Lavoillotte Ethan et Weber Loïc",True, (0, 255, 0))
    rect = pygame.Rect(authors.get_rect(center=(widht / 1.2, height / 1.2))[0],
                       authors.get_rect(center=(widht / 1.3, height / 1.1))[1],
                       authors.get_width(), authors.get_height())
    pygame.draw.rect(screen, (0, 0, 0), rect)
    screen.blit(authors, authors.get_rect(center=(widht / 1.2, height / 1.1)))

    clock = pygame.time.Clock()
    font_size = (80 * widht) // 1920
    base_font = pygame.font.Font('Estelle.ttf', font_size)  # Text font and size
    user_text = ''

    input_rect = pygame.Rect(widht / 2 -400, height / 1.5, 800, 100) # x, y ,width , height
    color_active = pygame.Color('gray50')
    color_passive = pygame.Color('gray15')  # des couleurs pour savoir si on est entrain de taper dans le champ ou non
    color = color_passive
    launched=True

    if name!=None and password==None and n.send(("isindatabase", name)):
        name = None
        text = pygame.font.Font('Estelle.ttf', (30 * widht) // 1920).render("Ce pseudo est déjà dans la base de donnée, essayer en un autre.", False, (255, 0, 0))
        rect = pygame.Rect(text.get_rect(center=(widht / 2, height / 1.6))[0],text.get_rect(center=(widht / 2, height / 1.6))[1],text.get_width(), text.get_height())
        pygame.draw.rect(screen, (0, 0, 0), rect)
        screen.blit(text, rect)

    if name==None:
        text = pygame.font.Font('Estelle.ttf', (40 * widht) // 1920).render("Pour créer votre compte entrer votre pseudo :", False, (0, 255, 0))
        rect = pygame.Rect(text.get_rect(center=(widht / 2, height / 2))[0],text.get_rect(center=(widht / 2, height / 2))[1],text.get_width(), text.get_height())
        pygame.draw.rect(screen, (0, 0, 0), rect)
        screen.blit(text, rect)

    elif password==None:
        text = pygame.font.Font('Estelle.ttf',(40 * widht) // 1920).render("Entrer un mot de passe :", False, (0, 255, 0))
        rect = pygame.Rect(text.get_rect(center=(widht / 2, height / 2))[0],text.get_rect(center=(widht / 2, height / 2))[1],text.get_width(), text.get_height())
        pygame.draw.rect(screen, (0, 0, 0), rect)
        screen.blit(text, text.get_rect(center=(widht / 2, height / 2)))  

        text = pygame.font.Font('Estelle.ttf',(30 * widht) // 1920).render("(vous n'aurez pas besoin de le retenir)", False, (0, 255, 0))
        rect = pygame.Rect(text.get_rect(center=(widht / 2, height / 1.6))[0],text.get_rect(center=(widht / 2, height / 1.6))[1],text.get_width(), text.get_height())
        pygame.draw.rect(screen, (0, 0, 0), rect)
        screen.blit(text, text.get_rect(center=(widht / 2, height / 1.6)))

    boxActive = True

    while password==None:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                launched = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for bouton in boutons:

                    if bouton.isOver(pos):
                        pygame.mixer.music.stop()

                        if bouton.name == "exit":
                            exit()

                if input_rect.collidepoint(event.pos):  # la souris est elle sur le rectangle ?
                    boxActive = True  # on "active" le champ de saisie

            if event.type == pygame.KEYDOWN:  # utilise t-on le clavier ?
                if boxActive == True:

                    if event.key == pygame.K_RETURN:  # valider avec la touche Entrée
                        if name==None:
                            name = user_text
                            createAccount(pygame,screen,name,None)
                        else:
                            password = user_text
                            createAccount(pygame,screen,name,password)

                    elif event.key == pygame.K_BACKSPACE:  # enlever un caractere
                        user_text = user_text[:-1]


                    elif len(user_text) < 20:  # mettre une taille limite de caractère
                        user_text+=event.unicode


            if boxActive: color = color_active

            pygame.draw.rect(screen, color, input_rect, 2)  # 2 = l'épaisseur du bord

            if name!=None:text_surface = base_font.render(len(user_text)*'*', True, (255, 255, 255))  # 255 255 255 = couleur du text
            else:text_surface = base_font.render(user_text, True, (255, 255, 255))  # 255 255 255 = couleur du text
            screen.fill(color, input_rect)
            screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))  # le cadre

            pygame.display.flip()
            clock.tick(60)  # les fps (delay de rafraichissement de la fenetre)

    if password!=None and launched:
        try:
            if len(password)>=1 and len(name)>=3 and not n.send(("isindatabase",name)):

                f = open("infos.txt", "w+")
                f.write(str(name)+"\n")
                f.write(str(password))
                f.close()

                text = pygame.font.Font('Estelle.ttf', (50 * widht) // 1920).render("Compte Enregistré !", False, (0, 255, 0))
                rect = pygame.Rect(text.get_rect(center=(widht / 2, height / 2))[0], text.get_rect(center=(widht / 2, height / 2))[1], text.get_width(), text.get_height())
                pygame.draw.rect(screen, (0, 0, 0), rect)
                screen.blit(text, rect)

                text = pygame.font.Font('Estelle.ttf', (50 * widht) // 1920).render("Relancer le jeu !", False, (255, 255, 0))
                rect = pygame.Rect(text.get_rect(center=(widht / 2, height / 1.6))[0], text.get_rect(center=(widht / 2, height / 1.6))[1], text.get_width(), text.get_height())
                pygame.draw.rect(screen, (0, 0, 0), rect)
                screen.blit(text, rect)


                pygame.display.flip()

                while launched:
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            pos = pygame.mouse.get_pos()
                            for bouton in boutons:

                                if bouton.isOver(pos):
                                    pygame.mixer.music.stop()

                                    if bouton.name == "exit":
                                        pygame.quit()
        except:pass