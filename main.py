import pygame,time,random,cmath,math

#
#Game Parameters Setup#
#
import gameset
pygame.mixer.pre_init(22050,-16,2,256) 
pygame.init()
pygame.mixer.set_num_channels(32)

display_w = 1280
display_h = 720
Display = pygame.display.set_mode((display_w,display_h))
pygame.display.set_caption('ZombieRun V1.0')
icon = pygame.image.load('bin/icon/zombierun.ico')
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
FPS = 60

#Colors
white,grey,brown,black = (255,255,255),(127,127,127),(136,0,21),(0,0,0)
red,light_red= (200,0,0),(255,0,0)
yellow,light_yellow= (230,220,0),(255,255,0)
green,light_green,dark_green = (34,177,76),(0,255,0),(134,122,77)
orange = (255,175,15)
blue,light_blue = (0,0,200),(0,0,255)
c1,c2,c3,c4,c5 = (187,124,79),(216,86,86),(16,82,36),(17,255,255),(255,72,255)
ground_color = (184,168,170)

#Dict Key Setup
hp,ift,dd = 'hp','ift','dd'
wp,wpbag,wpN = 'wp','wpbag','wpN'
c,l,w,ctl,thrwp = 'c','l','w','ctl','thrwp'
z,dz1,dz2,dzt,pos,dpos,dpx,dpy = 'z','dz1','dz2','dzt','pos','dpos','dpx','dpy'
erg,spd,dmg = 'erg','spd','dmg'
f,ft,r,rt = 'f','ft','r','rt'
az,alert = 'az','alert'

#Sound Effect
def SD(filename,filepath='bin/sounds/',fileformat='.wav'):
    return pygame.mixer.Sound(filepath+filename+fileformat)

minigun_hot = SD('minigun_hot')
lightsaber_in,lightsaber_buzz = SD('lightsaber_in'),SD('lightsaber_buzz')
chainsaw_in,chainsaw_hot,chainsaw_fire = SD('chainsaw_in'),SD('chainsaw_hot'),SD('chainsaw_fire')

out_of_ammo = SD('out_of_ammo')
gun_pickup = SD('gun_pickup')

bloodhit1 = SD('bloodhit1')
bloodhit2 = SD('bloodhit2')

zombie_eat_human_scream1 = SD('zombie_eat_human_scream1')
zombie_eat_human_scream2 = SD('zombie_eat_human_scream2')

#Music
def music_play(filename,t=0):
    pygame.mixer.music.stop()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play(t)
def music_stop():
    pygame.mixer.music.stop()

#weapon = [name,automation,power,deviation,reloadtime,round/mag,ammo,max r.g,max ammo,(..sounds),Length,weight]
bare_hand = ('bare_hand',-20,None,None,0.5,1,0,1,0,SD('hand_punch'),SD('hit_punch'),10,0)
glock = ('glock',-12,4,math.pi/60,2.5,15,30,15,90,SD('glock_fire'),SD('glock_reload'),10,0.1)
uzi = ('uzi',5,4,math.pi/60,2,30,60,30,120,SD('uzi_fire'),SD('uzi_reload'),20,0.15)
shotgun = ('shotgun',-100,3.6,math.pi/24,0.5,8,16,8,64,SD('shotgun_fire'),SD('shotgun_reload'),30,0.3)
ak47 = ('ak47',7,6.5,math.pi/30,2.5,30,60,30,120,SD('ak47_fire'),SD('ak47_reload'),30,0.3)
scar = ('scar',6,5.5,math.pi/48,2.5,30,60,30,120,SD('scar_fire'),SD('ak47_reload'),30,0.3)
svd = ('svd',-130,20,math.pi/360,3.5,10,10,10,30,SD('svd_fire'),SD('svd_reload'),50,0.5)
minigun = ('minigun',1,4.5,math.pi/24,4.5,600,1200,600,2400,SD('minigun_fire'),SD('minigun_out'),70,1.0)
chainsaw = ('chainsaw',1,0.5,None,0,200,0,200,0,SD('chainsaw_cut'),SD('chainsaw_out'),60,0.5)
lightsaber = ('lightsaber',1,10,None,0,1,0,1,0,SD('lightsaber_cut'),SD('lightsaber_out'),60,0)
lasersniper = ('lasersniper',-40,1000,0,0,35,0,35,0,SD('lasersniper_fire'),SD('uzi_reload'),5,0.4)

game_weapons = (bare_hand,glock,uzi,shotgun,ak47,scar,svd,minigun,chainsaw,lightsaber,lasersniper)
gameset.load_weapon(game_weapons)

#
#Game Module#
#
def gameLoop():
    gameOver = False     
    press_ctl,press_w = False,False
    
    gamemap = 'bin/maps/gamemap0'
   
    spos1,spos2,Barriers,Zombies,HACs,WeaponsOG,ZombieZones = gameset.set_map(gamemap,display_w,display_h)
    p1 = gameset.set_p1(spos1)
    p2 = gameset.set_p2(spos2)

    game_time = 0
    mouse_pos = complex(display_w/2+50, display_h/2+50)
    Bullets = []    

    music_play('bin/music/bgm1_start.mid')

#Begin of gameLoop
    while not gameOver:
        if game_time == 60*39:
            music_play('bin/music/glyzb.mid',-1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type  == pygame.MOUSEMOTION:                
                mouse_pos = complex(event.pos[0],event.pos[1])
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if not p1[r]:
                        if p1[wp][5] > 0:
                            if game_time - p1[ft] >= abs(p1[wp][1]):
                                p1[f] = True
                                p1[ft] = game_time - abs(p1[wp][1])
                        elif p1[wp][0] != 'bare_hand':
                            pygame.mixer.Sound.play(out_of_ammo)
                elif event.button == 3:
                    if (not p1[r]) and p1[wp][6] > 0 and p1[wp][5] < p1[wp][7]:
                        p1[r] = True
                        p1[rt] = game_time
                        pygame.mixer.Sound.play(p1[wp][10])
                elif event.button == 4:
                    p1[wpN] -= 1
                    p1[r] = False
                    pygame.mixer.Sound.stop(p1[wp][10])
                    if p1[wp][0] == 'lightsaber':
                        pygame.mixer.Sound.play(p1[wp][10])
                elif event.button == 5:
                    p1[wpN] += 1
                    p1[r] = False
                    pygame.mixer.Sound.stop(p1[wp][10])
                    if p1[wp][0] == 'lightsaber':
                        pygame.mixer.Sound.play(p1[wp][10])                        
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:                  
                    p1[f] = False
                    if p1[wp][0] == 'minigun' or p1[wp][0] == 'lightsaber' or p1[wp][0] == 'chainsaw':
                        pygame.mixer.Sound.play(p1[wp][10])
                        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    p1[dpos][2] = 1
                elif event.key == pygame.K_d:
                    p1[dpos][3] = 1
                elif event.key == pygame.K_w:
                    p1[dpos][0] = 1
                    press_w = True
                elif event.key == pygame.K_s:
                    p1[dpos][1] = 1
                elif event.key == pygame.K_g:
                    p1[thrwp] = True

                elif event.key == pygame.K_LEFT:
                    p2[dpos][2] = 1
                elif event.key == pygame.K_RIGHT:
                    p2[dpos][3] = 1
                elif event.key == pygame.K_UP:
                    p2[dpos][0] = 1
                elif event.key == pygame.K_DOWN:
                    p2[dpos][1] = 1
                elif event.key == pygame.K_KP4:
                    if game_time - p2[dzt] > 12:
                        p2[dzt] = game_time
                        p2[dz1] = (0-1j)**(0.75/FPS)
                    else:
                        p2[dz1] = (0-1j)**(3/FPS)
                elif event.key == pygame.K_KP6:
                    if game_time - p2[dzt] > 12:
                        p2[dzt] = game_time
                        p2[dz2] = (0+1j)**(0.75/FPS)
                    else:
                        p2[dz2] = (0+1j)**(3/FPS)
                elif event.key == pygame.K_KP5:
                    if not p2[r]:
                        if p2[wp][5] > 0:
                            if game_time - p2[ft] >= abs(p2[wp][1]):
                                p2[f] = True
                                p2[ft] = game_time - abs(p2[wp][1])
                        elif p2[wp][0] != 'bare_hand':
                            pygame.mixer.Sound.play(out_of_ammo)
                elif event.key == pygame.K_KP8:
                    if (not p2[r]) and p2[wp][6] > 0 and p2[wp][5] < p2[wp][7]:
                        p2[r] = True
                        p2[rt] = game_time
                        pygame.mixer.Sound.play(p2[wp][10])
                elif event.key == pygame.K_KP7:
                    p2[wpN] -= 1
                    p2[r] = False
                    pygame.mixer.Sound.stop(p2[wp][10])
                    if p2[wp][0] == 'lightsaber':
                        pygame.mixer.Sound.play(p1[wp][10])
                elif event.key == pygame.K_KP9:
                    p2[wpN] += 1
                    p2[r] = False
                    pygame.mixer.Sound.stop(p2[wp][10])
                    if p2[wp][0] == 'lightsaber':
                        pygame.mixer.Sound.play(p1[wp][10])
                elif event.key == pygame.K_KP_PERIOD:
                    p2[thrwp] = True
                                    
                elif event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                    press_ctl = True
                elif event.key == pygame.K_F2:
                    p2[ctl] = bool(1-p2[ctl])
                elif event.key == pygame.K_ESCAPE:
                    game_Pause(game_state)
                    
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    p1[dpos][2] = 0
                elif event.key == pygame.K_d:
                    p1[dpos][3] = 0
                elif event.key == pygame.K_w:
                    p1[dpos][0] = 0
                    press_w = False
                elif event.key == pygame.K_s:                
                    p1[dpos][1] = 0
                elif event.key == pygame.K_LEFT:
                    p2[dpos][2] = 0
                elif event.key == pygame.K_RIGHT:
                    p2[dpos][3] = 0
                elif event.key == pygame.K_UP:
                    p2[dpos][0] = 0
                elif event.key == pygame.K_DOWN:             
                    p2[dpos][1] = 0
                elif event.key == pygame.K_KP4:
                    p2[dz1] = 1
                elif event.key == pygame.K_KP6:
                    p2[dz2] = 1
                elif event.key == pygame.K_KP5:
                    p2[f] = False
                    if p2[wp][0] == 'minigun' or p2[wp][0] == 'lightsaber' or p2[wp][0] == 'chainsaw':
                        pygame.mixer.Sound.play(p2[wp][10])
                elif event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                    press_ctl = False


#Game State Control

        game_state = [game_time,p1,p2,WeaponsOG,Zombies,ZombieZones,HACs,Barriers]
        if press_ctl and press_w:
            game_state = gameset.command_window(game_state)
            time.sleep(0.5)
            game_time = game_state[0]
            p1 = game_state[1]
            p2 = game_state[2] 
            WeaponsOG = game_state[3]
            Zombies = game_state[4]
            ZombieZones = game_state[5]
            HACs = game_state[6]
            Barriers = game_state[7]

#Vision Core
        Display.fill(ground_color)

        if mouse_pos.real <= display_w * 0.1:
            dmapX = 4
        elif mouse_pos.real < display_w * 0.9:
            dmapX = 0
        else:
            dmapX = -4

        if mouse_pos.imag <= display_h * 0.1:
            dmapY = 4
        elif mouse_pos.imag < display_h * 0.9:
            dmapY = 0
        else:
            dmapY = -4

        if p1[pos].real+dmapX <= display_w * 0.2:
            dmapX = 0
        elif p1[pos].real+dmapX >= display_w * 0.8:
            dmapX = 0

        if p1[pos].imag+dmapY <= display_h * 0.2:
            dmapY = 0
        elif p1[pos].imag+dmapY >= display_h * 0.8:
            dmapY = 0

        dp1_pos = complex(p1[dpos][3] - p1[dpos][2],p1[dpos][1] - p1[dpos][0])*p1[spd]
        dmapZ = complex(dmapX, dmapY) - dp1_pos     

#Player Mobility Core
        
        
        if p2[ctl]:
            dp2_pos = complex(p2[dpos][3] - p2[dpos][2],p2[dpos][1] - p2[dpos][0])*p2[spd]
        else:
            p2[f],p2[r] = False,False
            p2[dz1],p2[dz2] = 1,1
            p1back_pos = p1[pos]-p1[z]*60
            p2_p1 = p1back_pos-p2[pos]        
            if 500 > abs(p2_p1) > 5:
                p2[z] = p2_p1/abs(p2_p1)
                dp2_pos = p2[z] * p2[spd]
            else:
                dp2_pos = complex(0,0)

        for ba in Barriers:
            ba[0][0] += dmapZ.real
            ba[0][1] += dmapZ.imag
            pygame.draw.rect(Display,ba[1],ba[0])
            dp1_pos = RectBoundOut(p1[pos].real-20,p1[pos].imag-20,40,40 ,dp1_pos.real,dp1_pos.imag, ba[0])
            if p2[hp] > 0:
                dp2_pos = RectBoundOut(p2[pos].real-20,p2[pos].imag-20,40,40 ,dp2_pos.real,dp2_pos.imag, ba[0])
            for b in Bullets:
                b_left = min(b[pos].real,b[pos].real+b[spd]*b[z].real)
                b_top = min(b[pos].imag,b[pos].imag+b[spd]*b[z].imag)
                if RectOverlap(b_left,b_top,abs(b[spd]*b[z].real),abs(b[spd]*b[z].imag), ba[0][0], ba[0][1], ba[0][2], ba[0][3]):
                    damage = min(ba[-1],b[dmg])
                    ba[-1] -= damage
                    b[dmg] -= damage
                    if b[dmg] <= 0:
                        Bullets.remove(b)
                    else:
                        Barriers.remove(ba)                                           
        p1[pos] += dp1_pos + dmapZ                    
        p1[z] = mouse_pos-p1[pos]
        if abs(p1[z]) == 0:
            p1_z = 1 + 1j
        p1[z] = p1[z]/abs(p1[z])
        

#P1 core
        if p1[thrwp]:
            pygame.mixer.Sound.stop(p1[wp][9])
            if p1[wp][0] != 'bare_hand':
                WeaponsOG.append([p1[wp],p1[pos]+p1[z]*90])
                p1[f], p1[r] = False,False          
                p1[wpbag].remove(p1[wp])
            p1[thrwp] = False
        p1[wpN] = p1[wpN] % len(p1[wpbag])
        p1[wp] = p1[wpbag][p1[wpN]]                     
        p1_wpbag_weight = 0
        for weapon in p1[wpbag]:
            p1_wpbag_weight += weapon[-1]           
        p1[spd] = 2/(1+p1[wp][-1]) * p1[hp]/(3+p1[hp]) - p1_wpbag_weight/7
                 
#P2 Core
        if p2[hp] > 0:
            if p2[ctl]:
                if p2[thrwp]:
                    pygame.mixer.Sound.stop(p2[wp][9])
                    if p2[wp][0] != 'bare_hand':
                        WeaponsOG.append([p2[wp],p2[pos]+p2[z]*90])
                        p2[f], p2[r] = False,False
                        p2[wpbag].remove(p2[wp])
                    p2[thrwp] = False           
                p2[wpN] = p2[wpN] % len(p2[wpbag])
                p2[wp] = p2[wpbag][p2[wpN]]                                  
            p2_wpbag_weight = 0
            for weapon in p2[wpbag]:
                p2_wpbag_weight += weapon[-1]      
            p2[spd] = 2/(1+p2[wp][-1]) * p2[hp]/(3+p2[hp]) - p2_wpbag_weight/7
            p2[z] = p2[z]*p2[dz1]*p2[dz2]
            p2[pos] += dp2_pos + dmapZ
            

#WeaponsOG:        
        for WP in WeaponsOG:
            WP[1] += dmapZ
            draw_WeaponsOG(WP[0][0],WP[1],WP[0][11])
            if RectOverlap(p1[pos].real-20,p1[pos].imag-20,40,40,WP[1].real-WP[0][11]/2,WP[1].imag-WP[0][11]/2,WP[0][11],WP[0][11]):        
                p1[f],p1[r] = False,False
                p1[wpbag].append(WP[0])           
                if WP[0][5] > 0:
                    p1[wpN] = len(p1[wpbag])-1
                    pygame.mixer.Sound.stop(p1[wp][10])
                WeaponsOG.remove(WP)
                pygame.mixer.Sound.play(gun_pickup)
            if p2[hp] > 0 and p2[ctl]:
                if RectOverlap(p2[pos].real-20,p2[pos].imag-20,40,40,WP[1].real-WP[0][11]/2,WP[1].imag-WP[0][11]/2,WP[0][11],WP[0][11]):                
                    p2[f],p2[r] = False,False
                    p2[wpbag].append(WP[0])           
                    if WP[0][5] > 0:
                        p2[wpN] = len(p2[wpbag])-1
                        pygame.mixer.Sound.stop(p2[wp][10])
                    WeaponsOG.remove(WP)                
                    pygame.mixer.Sound.play(gun_pickup)
            
        
#P1 weapon core
        if p1[wp][0] == 'minigun' and (not p1[r]):
            if not game_time % 10:
                pygame.mixer.Sound.play(minigun_hot)
        elif p1[wp][0] == 'chainsaw':
            if not game_time % 6:
                if p1[f]:
                    pygame.mixer.Sound.play(chainsaw_fire)
                    p1[wp][5] -= 1
                else:
                    pygame.mixer.Sound.play(chainsaw_hot)
        elif p1[wp][0] == 'lightsaber' and p1[f]:
            if game_time - p1[ft] == 1:
                pygame.mixer.Sound.play(lightsaber_in)
            if not game_time % 10:
                pygame.mixer.Sound.play(lightsaber_buzz)
                
        if p1[r]:
            if p1[wp][5] < p1[wp][7]:
                if p1[wp][0] == 'shotgun':
                    d = 1                    
                else:
                    d = min(p1[wp][6], p1[wp][7] - p1[wp][5])
                if game_time - p1[rt] > p1[wp][4] * FPS:
                    p1[r] = False
                    p1[wp][6] -= d
                    p1[wp][5] += d        
        if p1[f]:
            if p1[wp][0] == 'lightsaber' or p1[wp][0] == 'chainsaw':
                if p1[wp][5] > 0:
                    for zob in Zombies:
                        if L_C_intersect(p1[pos].real,p1[pos].imag,p1[z],zob[pos].real,zob[pos].imag,20,90):
                            zob[hp] -= p1[wp][2]
                            pygame.mixer.Sound.stop(chainsaw_fire)
                            pygame.mixer.Sound.play(p1[wp][9])
                else:
                    p1[f] = False
                    pygame.mixer.Sound.play(p1[wp][10])
            elif p1[wp][0] == 'bare_hand':
                if game_time - p1[ft] > abs(p1[wp][1]):
                    pygame.mixer.Sound.play(p1[wp][9])
                    p1[f] = False
                    p1[ft] = game_time 
            else:
                if game_time - p1[ft] >= abs(p1[wp][1]):
                    p1[wp][5] -= 1
                    p1[ft] = game_time
                    pygame.mixer.Sound.play(p1[wp][9])
                    if p1[wp][0] == 'shotgun':
                        for _ in range(0,6):
                            bullet = set_bullet(p1[pos],p1[z],p1[wp][2],p1[wp][3],p1[wp][11])
                            Bullets.append(bullet)
                    elif p1[wp][0] == 'lasersniper':
                        bullet = set_bullet(p1[pos],p1[z],p1[wp][2],p1[wp][3],p1[wp][11],1000,6,c5)
                        Bullets.append(bullet)
                    else:
                        bullet = set_bullet(p1[pos],p1[z],p1[wp][2],p1[wp][3],p1[wp][11])                        
                        Bullets.append(bullet)                     
                    if p1[wp][1] < 0 or p1[wp][5] <= 0:
                        p1[f] = False
        
                        

#P2 weapon core
        if p2[hp] > 0:
            if p2[wp][0] == 'minigun' and (not p2[r]):
                if not game_time % 10:
                    pygame.mixer.Sound.play(minigun_hot)
            elif p2[wp][0] == 'chainsaw':
                if not game_time % 6:
                    if p2[f]:
                        pygame.mixer.Sound.play(chainsaw_fire)
                    else:
                        pygame.mixer.Sound.play(chainsaw_hot)
            elif p2[wp][0] == 'lightsaber' and p2[f]:
                if game_time - p2[ft] == 1:
                    pygame.mixer.Sound.play(lightsaber_in)
                if not game_time % 10:
                    pygame.mixer.Sound.play(lightsaber_buzz)
                    
            if p2[r]:
                if p2[wp][5] < p2[wp][7]:
                    if p2[wp][0] == 'shotgun':
                        d = 1                    
                    else:
                        d = min(p2[wp][6], p2[wp][7] - p2[wp][5])
                    if game_time - p2[rt] > p2[wp][4] * FPS:
                        p2[r] = False
                        p2[wp][6] -= d
                        p2[wp][5] += d        
            if p2[f]:
                if p2[wp][0] == 'lightsaber' or p2[wp][0] == 'chainsaw':
                    if p2[wp][5] > 0:
                        for zob in Zombies:
                            if L_C_intersect(p2[pos].real,p2[pos].imag,p2[z],zob[pos].real,zob[pos].imag,20,90):
                                zob[hp] -= p2[wp][2]
                                pygame.mixer.Sound.stop(chainsaw_fire)
                                pygame.mixer.Sound.play(p2[wp][9])
                    else:
                        p2[f] = False
                        pygame.mixer.Sound.play(p2[wp][10])
                elif p2[wp][0] == 'bare_hand':
                    if game_time - p2[ft] > abs(p2[wp][1]):
                        pygame.mixer.Sound.play(p2[wp][9])
                        p2[f] = False
                        p2[ft] = game_time 
                else:
                    if game_time - p2[ft] >= abs(p2[wp][1]):
                        p2[wp][5] -= 1
                        p2[ft] = game_time
                        pygame.mixer.Sound.play(p2[wp][9])
                        if p2[wp][0] == 'shotgun':
                            for _ in range(0,6):
                                bullet = set_bullet(p2[pos],p2[z],p2[wp][2],p2[wp][3],p2[wp][11])
                                Bullets.append(bullet)
                        elif p2[wp][0] == 'lasersniper':
                            bullet = set_bullet(p2[pos],p2[z],p2[wp][2],p2[wp][3],p2[wp][11],1000,6,c5)
                            Bullets.append(bullet)
                        else:
                            bullet = set_bullet(p2[pos],p2[z],p2[wp][2],p2[wp][3],p2[wp][11])                        
                            Bullets.append(bullet)                     
                        if p2[wp][1] < 0 or p2[wp][5] <= 0:
                            p2[f] = False
            
         
#HAC Core#
        for hac in HACs:
            if hac[hp] <= 0:
                WeaponsOG.append([hac[wp],hac[pos]])
                HACs.remove(hac)
                break
            draw_HAC(hac[pos])
            draw_weapon(hac[wp][0],hac[wp][11],hac[z],hac[pos],hac[f])       
            hac_p1 = p1[pos]-hac[pos]
            d_hac_p1 = abs(hac_p1)
            if d_hac_p1 < 700:
                laserscope(hac[z],hac[pos],hac[wp][11])
            else:
                hac[erg] = False
            hac[z] = hac_p1/d_hac_p1                  
                       
            if d_hac_p1 < 240:
                hac[erg] = True
            elif d_hac_p1 < 700:
                if p1[wp][0] != 'bare_hand':
                    if abs(cmath.phase(-p1[z]/hac_p1)) < 0.6:
                        hac[erg] = True
               
            if p2[hp] > 0:
                hac_p2 = p2[pos]-hac[pos]
                d_hac_p2 = abs(hac_p2)
                if d_hac_p2 < d_hac_p1 and (game_time != p1[ft]):
                    hac[z] = hac_p2/d_hac_p2
                if d_hac_p2 < 240:
                    hac[erg] = True
                    hac[z] = hac_p2/d_hac_p2
                elif d_hac_p2 < 700:
                    if p2[wp][0] != 'bare_hand':
                        if abs(cmath.phase(-p2[z]/hac_p2)) < 0.6:
                            hac[erg] = True
                        
            if hac[erg]:
                if (not hac[r]) and hac[wp][5] > 0:
                    if game_time - hac[ft] >= abs(hac[wp][1]):
                        hac[f] = True
                        hac[ft] = game_time - abs(hac[wp][1])
                
            if hac[f]:                                                
                if game_time - hac[ft] >= abs(hac[wp][1]):
                    hac[wp][5] -= 1
                    hac[ft] = game_time
                    pygame.mixer.Sound.play(hac[wp][9])
                    b = set_bullet(hac[pos],hac[z],hac[wp][2],hac[wp][3],hac[wp][11])                  
                    Bullets.append(b)
                    if hac[wp][1] < 0:
                        hac[f] = False
                    if hac[wp][5] == 0:
                        hac[f] = False
                        hac[r] = True
                        
            if hac[r]:
                if game_time - hac[ft] >= (hac[wp][4]+1) * FPS:
                    hac[r] = False
                    hac[wp][5] = hac[wp][7]
            hac[az][0] += dmapZ.real
            hac[az][1] += dmapZ.imag
            hac[pos] += dmapZ + hac[z] * hac[hp]/10
            hac[pos] = RectBoundIn(hac[pos].real,hac[pos].imag,hac[az][0],hac[az][1],hac[az][2],hac[az][3])
            for b in Bullets:
                if L_C_intersect(b[pos].real,b[pos].imag,b[z],hac[pos].real,hac[pos].imag,20,b[spd]):
                    pygame.mixer.Sound.play(bloodhit1)
                    damage = random.uniform(0.8,1.2) * b[dmg]
                    b[dmg] -= min(zob[hp],b[dmg])
                    hac[hp] -= damage
                    hac[pos] += b[z] * (damage/2)**2
                    if b[dmg] <= 0:
                        Bullets.remove(b)


#Zombie Core#
        for zob in Zombies:
            zob[pos] += dmapZ
            draw_zombie(zob[pos])
            zob[alert] = False
            zob_p1 = p1[pos]-zob[pos]
            d_zob_p1 = abs(zob_p1)        
            if d_zob_p1 < 40:
                if not p1[ift]:
                    pygame.mixer.Sound.play(zombie_eat_human_scream1)
                p1[ift]= True
                p1[hp] -= 0.25
            elif d_zob_p1 < 50:
                if p1[wp][0] == 'bare_hand':
                    if p1[f]:
                        if abs(cmath.phase(-p1[z]/zob_p1)) < 0.3:
                            damage = 1.5 * random.random()
                            zob[hp] -= damage
                            zob[pos] += p1[z] * 10
                            pygame.mixer.Sound.play(p1[wp][10])
            elif d_zob_p1 < 500:
                zob[alert] = True
            elif d_zob_p1 < 1500:
                if p1[wp][0] != 'bare_hand':
                    if game_time - p1[ft] < 600:
                        zob[alert] = True

            if p2[hp] > 0:
                zob_p2 = p2[pos]-zob[pos]
                d_zob_p2 = abs(zob_p2)
                if d_zob_p2 < 40:
                    if not p2[ift]:
                        pygame.mixer.Sound.play(zombie_eat_human_scream2)
                    p2[ift]= True
                    p2[hp] -= 0.25
                elif d_zob_p2 < 50:
                    if p2[wp][0] == 'bare_hand':
                        if p2[f]:
                            if abs(cmath.phase(-p2[z]/zob_p2)) < 0.3:
                                damage = 1.5 * random.random()
                                zob[hp] -= damage
                                zob[pos] += p2[z] * 10
                                pygame.mixer.Sound.play(p2[wp][10])
                elif d_zob_p2 < 500:
                    zob[alert] = True
                elif d_zob_p2 < 1500:
                    if p2[wp][0] != 'bare_hand':
                        if game_time - p2[ft] < 600:
                            zob[alert] = True
                         
            if zob[alert]:
                zob[z] = zob_p1/d_zob_p1
                if p2[hp] > 0:
                    if d_zob_p1 > d_zob_p2:
                        zob[z] = zob_p2/d_zob_p2       
            zob[dpos] = zob[z] * zob[hp]/10
            for ba in Barriers:
                zob[dpos] = RectBoundOut(zob[pos].real-20,zob[pos].imag-20,40,40, zob[dpos].real,zob[dpos].imag, ba[0])

            for m in range(Zombies.index(zob),len(Zombies)):
                azob= Zombies[m]
                if abs(zob[pos].real - azob[pos].real) < 40 and abs(zob[pos].imag - azob[pos].imag) < 40:
                    if zob[hp] < azob[hp]:
                        if abs(zob[pos]+zob[dpos]-azob[pos])<abs(zob[pos]-azob[pos]):                            
                            zob[dpos] = 0+0j
                            break                                                          
            zob[pos] += zob[dpos]        
            for b in Bullets:
                if L_C_intersect(b[pos].real,b[pos].imag,b[z],zob[pos].real,zob[pos].imag,20,b[spd]):
                    pygame.mixer.Sound.play(bloodhit2)
                    damage = random.uniform(0.8,1.2) * b[dmg]
                    b[dmg] -= min(zob[hp],b[dmg])
                    zob[hp] -= damage
                    zob[pos] += b[z] * (damage/2)**2
                    if b[dmg] <= 0:
                        Bullets.remove(b)                              
            if zob[hp] <= 0:
                Zombies.remove(zob)

#Bullet Core#
        for b in Bullets:
            pygame.draw.line(Display,b[c],(b[pos].real,b[pos].imag),(b[pos].real+b[l]*b[z].real,b[pos].imag+b[l]*b[z].imag), b[w])
            if L_C_intersect(b[pos].real,b[pos].imag,b[z],p1[pos].real,p1[pos].imag,20,b[spd]):
                pygame.mixer.Sound.play(bloodhit2)
                damage = random.uniform(0.8,0.9) * b[dmg]
                p1[hp] -= damage
                p1[pos] += b[z] * (damage/2)**2
                b[dmg] = 0             
            if p2[hp] > 0:               
                if L_C_intersect(b[pos].real,b[pos].imag,b[z],p2[pos].real,p2[pos].imag,20,b[spd]):
                    pygame.mixer.Sound.play(bloodhit2)
                    damage = random.uniform(0.8,0.9) * b[dmg]
                    p2[hp] -= damage
                    p2[pos] += b[z] * (damage/2)**2
                    b[dmg] = 0
            if b[dmg] <= 0:
                    Bullets.remove(b)
            b[pos] += b[z] * b[spd]

#ZombieZones

        for zone in ZombieZones:
            zone[0] += dmapZ.real
            zone[1] += dmapZ.imag
            if not game_time % (zone[4] * FPS):
                zob = gameset.set_default_zob()
                x = random.uniform(zone[0],zone[0]+zone[2])
                y = random.uniform(zone[1],zone[1]+zone[3])
                zob[pos] = complex(x,y)
                zob[hp] = zone[5]*random.uniform(0.9,1.1)
                Zombies.append(zob)

       

#Drawing Player
        draw_p1(p1[pos])
        draw_weapon(p1[wp][0],p1[wp][11],p1[z],p1[pos],p1[f])
        if p2[hp] > 0:
            draw_p2(p2[pos])
            draw_weapon(p2[wp][0],p2[wp][11],p2[z],p2[pos],p2[f])
            if p2[wp][0] != 'bare_hand' and p2[wp][0] != 'lightsaber':
                laserscope(p2[z],p2[pos],p2[wp][11])



#Message Display#
        if p1[ift]:
            message_to_screen('INFECTED',red, -330, -300, 22)
            message_to_screen("Find the antibody!",black, -285, -330, 22)
            p1[hp] -= 0.0002
        if abs(mouse_pos-p1[pos]) < 20:
            player_info(mouse_pos,p1)
            
        message_to_screen(p1[wp][0],black, -500, -330, 22)
        message_to_screen(str(p1[wp][5])+' / '+str(p1[wp][6]),black, -500, -300, 50)
        if p1[r]:
            message_to_screen('Reloading...',black, -500, -260, 22)

        if p2[hp] > 0:
            if p2[ift]:
                message_to_screen('INFECTED',red, 225, -300, 22)
                message_to_screen("Find the antibody!",black, 185, -330, 22)
                p2[hp] -= 0.0002
            if abs(mouse_pos-p2[pos]) < 20:
                player_info(mouse_pos,p2)
                
            message_to_screen(p2[wp][0],black, 500, -330, 22)
            message_to_screen(str(p2[wp][5])+' / '+str(p2[wp][6]),black, 500, -300, 50)
            if p2[r]:
                message_to_screen('Reloading...',black, 500, -260, 22)


        if p1[hp] <= 0:
            gameOver = True
                                               
        if p2[hp] < 0:
            if not p2[dd]:
                p2[f], p2[r] = False,False
                for weapon in p2[wpbag]:
                    if weapon[0] != 'bare_hand':
                        WeaponsOG.append([weapon,p2[pos]])
                        p2[wpbag].remove(weapon)           
                p2[dd] = True


                
        game_time += 1
        pygame.display.update()
        clock.tick(FPS)

    if gameOver:
        return game_Over(game_time)
#End of GameLoop
    

def game_Pause(gamesate):
    pygame.mixer.stop()
    paused = True
    while paused:
        message_to_screen("Pause", red, 0,-200, 100)
        if button("Resume",display_w/2-100,300,200,50,green,light_green):
            paused = False      
        elif button("Save Game",display_w/2-100,380,200,50,yellow,light_yellow):
            print("Save")
        elif button("Load Game",display_w/2-100,460,200,50,yellow,light_yellow):
            print("Load")
        elif button("Replay",display_w/2-100,540,200,50,red,light_red):
            return gameLoop()
               
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False
        clock.tick(FPS)
        

def game_Over(g_time):
    time.sleep(1.5)
    gameOver = True
    while gameOver:
        Display.fill(c1)
        message_to_screen("Game over", red, 0,-200,80)
        message_to_screen("Score: "+str(g_time), light_blue, 0,0,80)
        if button("Replay",display_w/2-100,600,200,50,green,light_green):
            pygame.mixer.stop()
            return gameLoop()
        
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        clock.tick(FPS)
    

#
#Game Function#
#
def RectOverlap(x1,y1,w1,h1,x2,y2,w2,h2):
    if x1+w1>x2 and x1<x2+w2 and y1+h1>y2 and y1<y2+h2:
        return True
    
def RectBoundOut(x1,y1,w1,h1,dx1,dy1,xywh2):
    if RectOverlap(x1+dx1,y1,w1,h1,xywh2[0],xywh2[1],xywh2[2],xywh2[3]):
        dx = 0
    else:
        dx = dx1
    if RectOverlap(x1,y1+dy1,w1,h1,xywh2[0],xywh2[1],xywh2[2],xywh2[3]):
        dy = 0
    else:
        dy = dy1
    return complex(dx,dy)

def RectBoundIn (x,y,left,top,w,h):    
    if x < left:
        x0 = left
    elif x > left + w:
        x0 = left + w
    else:
        x0 = x
    if y < top:
        y0 = top
    elif y > top + h:
        y0 = top + h
    else:
        y0 = y
    return complex(x0,y0)

def L_C_intersect(x,y,z,x0,y0,R,L):
    z1 = complex(x0-x,y0-y)
    th1 = abs(cmath.phase(z1/z))
    if th1 >= 1.5 :
        return False
    elif abs(z1) * math.sin(th1) <= R:
        z2 = complex(x0-x-z.real*L,y0-y-z.imag*L)
        if abs(cmath.phase(z2/z)) > 0.765:
            return True

def set_bullet(ppos,pz,dmg,dev,wpl,l=0,w=2,color=black):
    bpos = ppos + pz * (20+wpl)
    th = random.uniform(-dev,dev)
    z0 = complex(math.cos(th),math.sin(th))
    z = pz * z0
    if l == 0:
        l = dmg * 5
    bullet = {'pos':bpos,'z':z,'dmg':dmg,'l':l,'spd':60+l,'w':w,'c':color}
    return bullet

def player_info(Pos,player):
    pygame.draw.rect(Display,black,(Pos.real-100,Pos.imag-30,100,30),5)
    pygame.draw.rect(Display,white,(Pos.real-100,Pos.imag-30,100,30))
    playerhp = round(player[hp],2)
    message_to_screen('HP:'+str(playerhp),red,Pos.real-690, Pos.imag-375, 22)
            

def draw_p1(Z):
    x, y = round(Z.real), round(Z.imag)
    pygame.draw.circle(Display,black,(x,y),20)
    pygame.draw.circle(Display,light_blue,(x,y),15)

def draw_p2(Z):
    x, y = round(Z.real), round(Z.imag)
    pygame.draw.circle(Display,black,(x,y),20)
    pygame.draw.circle(Display,orange,(x,y),15)

def draw_zombie(Z):
    x, y = round(Z.real), round(Z.imag)
    pygame.draw.circle(Display,red,(x,y),20)
    pygame.draw.circle(Display,c1,(x,y),15)

def draw_HAC(Z):
    x, y = round(Z.real), round(Z.imag)
    pygame.draw.circle(Display,black,(x,y),20)
    pygame.draw.circle(Display,grey,(x,y),15)


def laserscope(z,posZ,wpl,color=red):
    d = max(20,wpl)
    x1,y1 = posZ.real+z.real*d,posZ.imag+z.imag*d
    x2,y2 = posZ.real+z.real*1600,posZ.imag+z.imag*1600
    pygame.draw.line(Display,color,(x1,y1),(x2,y2),1)

def draw_weapon(weapon_name,length,z,posZ,fire):
    x,y = posZ.real,posZ.imag
    X,Y = round(x+z.real*(20+length)),round(y+z.imag*(20+length))
    if weapon_name == 'bare_hand':
        z0 = complex(0.707,0.707)
        z1,z2 = z * z0, z * z0.conjugate()
        x1,y1 = x+z1.real*25,y+z1.imag*25
        x2,y2 = x+z2.real*25,y+z2.imag*25
        if fire:
            pygame.draw.line(Display,black,(x+z.real*20,y+z.imag*20),(x+z.real*30,y+z.imag*30),4)
        else:
            pygame.draw.line(Display,black,(x+z1.real*20,y+z1.imag*20),(x1,y1),3)
        pygame.draw.line(Display,black,(x+z2.real*20,y+z2.imag*20),(x2,y2),3)
    elif weapon_name == 'glock':
        pygame.draw.line(Display,black,(x+z.real*20,y+z.imag*20),(X,Y),5)    
        if fire:
            pygame.draw.circle(Display,light_yellow,(X,Y),4)
    elif weapon_name == 'uzi':
        pygame.draw.line(Display,black,(x+z.real*20,y+z.imag*20),(X,Y),5)
        pygame.draw.line(Display,grey,(x+z.real*20,y+z.imag*20),(x+z.real*35,y+z.imag*35),8)
        if fire:
            pygame.draw.circle(Display,light_yellow,(X,Y),4)
    elif weapon_name == 'shotgun':
        pygame.draw.line(Display,grey,(x+z.real*20,y+z.imag*20),(X,Y),6)
        pygame.draw.line(Display,brown,(x+z.real*20,y+z.imag*20),(x+z.real*30,y+z.imag*30),8)
        if fire:
            pygame.draw.circle(Display,light_yellow,(X,Y),6)
    elif weapon_name == 'ak47':  
        pygame.draw.line(Display,black,(x+z.real*20,y+z.imag*20),(X,Y),5)
        pygame.draw.line(Display,red,(x+z.real*20,y+z.imag*20),(x+z.real*35,y+z.imag*35),8)
        if fire:
            pygame.draw.circle(Display,light_yellow,(X,Y),7)
    elif weapon_name == 'scar':  
        pygame.draw.line(Display,black,(x+z.real*20,y+z.imag*20),(X,Y),5)
        pygame.draw.line(Display,dark_green,(x+z.real*20,y+z.imag*20),(x+z.real*35,y+z.imag*35),8)
        if fire:
            pygame.draw.circle(Display,light_yellow,(X,Y),7)
    elif weapon_name == 'svd':
        pygame.draw.line(Display,c3,(x+z.real*20,y+z.imag*20),(X,Y),5)
        pygame.draw.line(Display,grey,(x+z.real*25,y+z.imag*25),(x+z.real*45,y+z.imag*45),7)
        if fire:
            pygame.draw.circle(Display,light_yellow,(X,Y),9)
    elif weapon_name == 'minigun':
        z1 = z/abs(z)*(0+1j)
        z2 = z/abs(z)*(0-1j)
        x1,y1 = x+z1.real*4,y+z1.imag*4
        x2,y2 = x+z2.real*4,y+z2.imag*4
        pygame.draw.line(Display,grey,(x+z.real*20,y+z.imag*20),(x+z.real*100,y+z.imag*100),3)
        pygame.draw.line(Display,grey,(x1+z.real*20,y1+z.imag*20),(x1+z.real*100,y1+z.imag*100),3)
        pygame.draw.line(Display,grey,(x2+z.real*20,y2+z.imag*20),(x2+z.real*100,y2+z.imag*100),3)
        pygame.draw.line(Display,black,(x+z.real*20,y+z.imag*20),(x+z.real*40,y+z.imag*40),5)
        pygame.draw.line(Display,black,(x1+z.real*20,y1+z.imag*20),(x1+z.real*40,y1+z.imag*40),7)
        pygame.draw.line(Display,black,(x2+z.real*20,y2+z.imag*20),(x2+z.real*40,y2+z.imag*40),7)
        if fire:
            X,Y = round(x+z.real*100),round(y+z.imag*100)
            pygame.draw.circle(Display,light_yellow,(X,Y),8)
    elif weapon_name == 'chainsaw':
        pygame.draw.line(Display,grey,(x+z.real*20,y+z.imag*20),(X,Y),8)
        pygame.draw.line(Display,black,(x+z.real*20,y+z.imag*20),(X,Y),3)
        pygame.draw.line(Display,red,(x+z.real*20,y+z.imag*20),(x+z.real*35,y+z.imag*35),13)
    elif weapon_name == 'lasersniper':
        pygame.draw.line(Display,light_blue,(x+z.real*50,y+z.imag*50),(X,Y),7)
        pygame.draw.line(Display,c4,(x+z.real*20,y+z.imag*20),(x+z.real*63,y+z.imag*63),6)
        pygame.draw.line(Display,grey,(x+z.real*20,y+z.imag*20),(x+z.real*40,y+z.imag*40),12)
        if fire:
            pygame.draw.circle(Display,light_green,(X,Y),4)
    elif weapon_name == 'lightsaber':
        if fire:
            pygame.draw.line(Display,c5,(x+z.real*20,y+z.imag*20),(X,Y),6)
        pygame.draw.line(Display,grey,(x+z.real*20,y+z.imag*20),(x+z.real*30,y+z.imag*30),8)
                
def draw_WeaponsOG(weapon_name,z,length):
    x,y = z.real-length/2,z.imag-length/2
    if weapon_name == 'glock':
        pygame.draw.rect(Display,grey,(x,y,5,15))
        pygame.draw.rect(Display,black,(x,y,25,5))
        pygame.draw.rect(Display,black,(x+5,y+5,3,3))
    elif weapon_name == 'uzi':
        pygame.draw.rect(Display,black,(x+4,y,7,30))
        pygame.draw.rect(Display,grey,(x,y,30,10))   
        pygame.draw.rect(Display,black,(x+30,y,5,5))
        pygame.draw.line(Display,black,(x+11,y+13),(x+14,y+13))
        pygame.draw.line(Display,black,(x+14,y+10),(x+14,y+13))
    elif weapon_name == 'shotgun':
        pygame.draw.rect(Display,grey,(x,y+20,60,8))
        pygame.draw.rect(Display,brown,(x,y+20,17,10))
        pygame.draw.rect(Display,brown,(x,y+20,10,18))
        pygame.draw.line(Display,black,(x+10,y+33),(x+13,y+33))
        pygame.draw.line(Display,black,(x+13,y+30),(x+13,y+33))
    elif weapon_name == 'ak47' or weapon_name == 'scar':
        pygame.draw.rect(Display,black,(x,y+22,60,6))
        pygame.draw.rect(Display,black,(x+8,y+22,7,20))
        if weapon_name == 'ak47':
            pygame.draw.rect(Display,red,(x+8,y+19,22,11))
        else:
            pygame.draw.rect(Display,dark_green,(x+8,y+19,22,11))
        pygame.draw.rect(Display,black,(x+8,y+30,22,3))
        pygame.draw.line(Display,black,(x+15,y+34),(x+19,y+34))
        pygame.draw.line(Display,black,(x+19,y+30),(x+19,y+34))
        pygame.draw.polygon(Display,grey,((x+22,y+33),(x+31,y+51),(x+37,y+43),(x+30,y+33)))
        pygame.draw.polygon(Display,brown,((x+8,y+22),(x-15,y+22),(x-15,y+33),(x+8,y+30)))
    elif weapon_name == 'svd':
        pygame.draw.rect(Display,c3,(x,y+25,85,6))
        pygame.draw.rect(Display,grey,(x+5,y+20,30,5))
        pygame.draw.polygon(Display,black,((x,y+30),(x-7,y+47),(x,y+47),(x+7,y+30)))
        pygame.draw.line(Display,black,(x+5,y+36),(x+13,y+36))
        pygame.draw.line(Display,black,(x+16,y+30),(x+13,y+36))
        pygame.draw.polygon(Display,brown,((x,y+25),(x-30,y+25),(x-30,y+35),(x,y+30)))
    elif weapon_name == 'minigun':
        pygame.draw.rect(Display,grey,(x,y+36,92,4))
        pygame.draw.rect(Display,grey,(x,y+41,92,4))
        pygame.draw.rect(Display,black,(x,y+33,28,14))
        pygame.draw.rect(Display,grey,(x,y+30,20,3))
        pygame.draw.rect(Display,black,(x-5,y+35,5,10))
        pygame.draw.rect(Display,brown,(x+12,y+47,12,36))
    elif weapon_name == 'chainsaw':
        pygame.draw.rect(Display,red,(x,y+30,25,20))
        pygame.draw.rect(Display,black,(x+25,y+30,60,15))
        pygame.draw.rect(Display,grey,(x+28,y+33,54,9))
    elif weapon_name == 'lasersniper':
        pygame.draw.rect(Display,c4,(x,y+22,60,8))
        pygame.draw.rect(Display,c4,(x-10,y+27,45,8))
        pygame.draw.rect(Display,light_blue,(x+40,y+25,35,5))
        pygame.draw.rect(Display,c5,(x+8,y+30,4,15))
        pygame.draw.rect(Display,c5,(x+23,y+30,30,7))
        pygame.draw.rect(Display,c5,(x+23,y+30,6,23))
        pygame.draw.rect(Display,grey,(x+8,y+22,17,8))
        pygame.draw.rect(Display,black,(x+12,y+30,11,4))
    elif weapon_name == 'lightsaber':
        pygame.draw.rect(Display,grey,(x+16,y+36,35,6))
        pygame.draw.rect(Display,black,(x+13,y+37,3,4))
        pygame.draw.rect(Display,black,(x+42,y+32,4,16))
    
def text_objects(text, color, size):
    gamefont = pygame.font.Font('bin/fonts/LSANS.TTF', size)
    textSurface = gamefont.render(text, True, color)           
    return textSurface, textSurface.get_rect()
def message_to_screen(msg,color, x_displace=0, y_displace=0, size=22):
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = (display_w/2)+x_displace, (display_h/2)+y_displace
    Display.blit(textSurf, textRect)
def button(text,x,y,w,h,inactive_color,active_color,fontsize=22):    
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > cur[0] > x and y + h > cur[1] > y:            
        pygame.draw.rect(Display, active_color, (x,y,w,h))
        if click[0] == 1: return True
    else: pygame.draw.rect(Display, inactive_color, (x,y,w,h))
    text_to_button(text,black,x,y,w,h,fontsize)
def text_to_button(msg,color,btnx,btny,btnw,btnh,size):
    textSurf, textRect = text_objects(msg,color,size)
    textRect.center = (btnx+btnw/2, btny+btnh/2)
    Display.blit(textSurf, textRect)



gameLoop()
