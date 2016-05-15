
## Player Set up##


def set_p1(pos=complex(0,0)):

    p1 = {'hp':10.0,
          'ift':False,
          'pos':pos,
          'dpos':[0,0,0,0],
          'z':complex(0.1+0.1j),
          'spd':1.6,
          'wp':list(bare_hand),          
          'wpbag':[list(bare_hand)],'wpN':0,
          'thrwp':False,
          'f':False,'ft':0,
          'r':False,'rt':0}

    return p1



def set_p2(pos=complex(0,0)):

    p2 = {'hp':10.0,
          'ift':False,
          'pos':pos,
          'dpos':[0,0,0,0],
          'z':complex(0.6+0.8j),
          'dz1':complex(1,0),'dz2':complex(1,0),'dzt':0,
          'spd':1.6,
          'wp':list(bare_hand),          
          'wpbag':[list(bare_hand)],'wpN':0,
          'thrwp':False,
          'f':False,'ft':0,
          'r':False,'rt':0,
          'ctl':False,'dd':False}

    return p2 


## Entities set up##

def set_default_zob():

    zombie = {'hp':10,
          'pos':complex(0,0),
          'dpx':0,'dpy':0,
          'z':complex(0,0),
          'alert':False}
    
    return zombie

def set_default_HAC():

    HAC = {'hp':8,
           'pos':complex(1000,300),
           'z':1+0j,
           'az':[900,100,200,200],
           'wp':list(scar),
           'ft':0,'f':False,'r':False}
    
    return HAC

##Weapons Set up##


def load_weapon(weapons):
    global allweapons,bare_hand,glock,uzi,shotgun,ak47,scar,svd,minigun,chainsaw,lightsaber,lasersniper
    bare_hand = weapons[0]
    glock = weapons[1]
    uzi = weapons[2]
    shotgun = weapons[3]
    ak47 = weapons[4]
    scar = weapons[5]
    svd = weapons[6]
    minigun = weapons[7]
    chainsaw = weapons[8]
    lightsaber = weapons[9]
    lasersniper = weapons[10]

    allweapons = weapons




##Loading Mapfile and Set Map##
b_c1 = [90,90,90]
b_c2 = [216,123,97]


def set_map(filename,dpW,dpH):
    global display_w,display_h
    display_w,display_h = dpW,dpH
    Barriers,Zombies,HACs,WeaponsOnGround,ZombieZones = [],[],[],[],[]

    mapfile = open(filename,'r')

    lines = mapfile.readlines()
    for line in lines:
        line = line.strip().split('\t')
        
        if line[0] == 'sp1':
            StartPos1 = complex(int(line[1]),int(line[2]))
        elif line[0] == 'sp2':
            StartPos2 = complex(int(line[1]),int(line[2]))
            
        elif line[0] == 'ba':
            ba = []
            ba.append([int(line[1]),int(line[2]),int(line[3]),int(line[4])])
            if line[5] == 'c1':
                ba.append((90,90,90))
            else:
                ba.append((90,90,90))
            ba.append(int(line[3])*int(line[4])/10)
            Barriers.append(ba)
            
        elif line[0] == 'zob':
            zob = {'hp':int(line[1]),
                   'pos':complex(int(line[2]),int(line[3])),
                   'dpos':0+0j,
                   'z':0+0j,
                   'alert':bool(int(line[4]))}
            Zombies.append(zob)

        elif line[0] == 'zobzone':
            zobzone = [int(line[1]),int(line[2]),int(line[3]),int(line[4]),float(line[5]),float(line[6])]
            ZombieZones.append(zobzone)
            
        elif line[0] == 'hac':
            for wp in allweapons:
                if wp[0] == line[8]:
                    weapon = list(wp)
            hac = {'hp':int(line[1]),
                   'pos':complex(int(line[2]),int(line[3])),
                   'z':1+0j,
                   'az':[int(line[4]),int(line[5]),int(line[6]),int(line[7])],
                   'erg':False,
                   'wp':weapon,
                   'ft':0,
                   'f':False,
                   'r':False}
        
            HACs.append(hac)

        elif line[0] == 'wp':
            posZ = complex(int(line[2]),int(line[3]))        
            for wp in allweapons:
                if wp[0] == line[1]:
                    weapon = list(wp)
            WeaponsOnGround.append([weapon,posZ])

    mapfile.close()


    dmapZ = complex(dpW/2,dpH/2)-StartPos1
    StartPos1 += dmapZ
    StartPos2 += dmapZ

    for ba in Barriers:
        ba[0][0] += dmapZ.real
        ba[0][1] += dmapZ.imag
    for zob in Zombies:
        zob['pos'] += dmapZ
    for zone in ZombieZones:
        zone[0] += dmapZ.real
        zone[1] += dmapZ.imag
    for hac in HACs:
        hac['pos'] += dmapZ
        hac['az'][0] += dmapZ.real
        hac['az'][1] += dmapZ.imag
    for weapon in WeaponsOnGround:
        weapon[1] += dmapZ


    return StartPos1,StartPos2,Barriers,Zombies,HACs,WeaponsOnGround,ZombieZones





## Command Window ##

def command_window(game_state):
    game_time = game_state[0]
    p1 = game_state[1]
    p2 = game_state[2]
    WeaponsOG = game_state[3]
    Zombies = game_state[4]
    ZombieZones = game_state[5]
    HACs = game_state[6]
    Barriers = game_state[7]

    print("Escape from ZombieRun ----Command Window v2.0")    
    print("Enter 'exit' to resume game\n\n")
    incommand = True
    commands = []
    
    while incommand:
        command,player,entity = [],None,None
        
        if commands:
            command = commands.pop(0)
        else:
            Uin = input('> ').split('\t')
            while len(Uin) < 3:
                Uin.append('')
            actions,subjects,results = Uin[0].split(';'),Uin[1].split(';'),Uin[2].split(';')
            for act in actions:
                for subj in subjects:
                    for res in results:
                        commands.append([act.strip(),subj.strip(),res.strip()])
                            

        if len(command) == 3:
            action,subject,result = command[0],command[1],command[2]
            
            if subject == 'p1':
                player = p1
            elif subject == 'p2':
                player = p2
            elif subject == 'zob':
                entity = Zombies
            elif subject == 'zobzone':
                entity = ZombieZones
            elif subject == 'hac':
                entity = HACs
            elif subject == 'ba':
                entity = Barriers
            elif subject == 'wp':
                entity = WeaponsOG
                    
            if action == 'set':
                if player:           
                    keyNvalue = result.split('=')       
                    if len(keyNvalue) == 2:
                        key,value = keyNvalue[0].strip(),keyNvalue[1].strip()
                        if key == 'wp':
                            if value == 'reload':
                                print("Command Confirmed.")
                                for weapon in player['wpbag']:
                                    weapon [5],weapon[6] = weapon [7],weapon [8]                           
                                print(subject,'all weapons fully reloaded.')
                            for weapon in allweapons:
                                if weapon[0] == value:
                                    player['wpbag'][player['wpN']] = list(weapon)
                                    print("Command Confirmed.\n"+subject,key,':',value)
                        elif key in player:
                            value = value.split(',')
                            if len(value) == 1:
                                if type(player[key]) is int:
                                    try: value = int(value[0].strip())
                                    except ValueError: value = player[key]
                                elif type(player[key]) is float:
                                    try: value = float(value[0].strip())
                                    except ValueError: value = player[key]
                                elif type(player[key]) is bool:
                                    value = bool(value[0])
                            elif len(value) == 2:
                                if type(player[key]) is complex:
                                    try: value[0] = float(value[0].strip())
                                    except ValueError: value[0] = player[key].real
                                    try: value[1] = float(value[1].strip())
                                    except ValueError: value[1] = player[key].imag
                                    value = complex(value[0],value[1])
                            else:
                                value = player[key]
                                       
                            player[key] = value
                            print("Command Confirmed.\n"+subject,key,':',value) 

                                                     
            elif action == 'print':
                key = result
                if player:                    
                    if key in player:
                        print(subject,key,':',player[key])
                    elif key == 'all':
                        print(subject,'info:')
                        for m,n in player.items():
                            print(m,':',n)
                elif entity != None:
                    if key == 'all':
                        print("Command Confirmed.\n"+subject,'info:')
                        for i in entity:
                            print(i)
                    else:                       
                        try: key = int(key)
                        except ValueError: key = None
                        if type(key) is int and -len(entity) <=key < len(entity):
                            print("Command Confirmed.\n"+entity[key])
                        

            elif action == 'spawn':
                if player:
                    item = result
                    if item == 'all':
                        for weapon in allweapons:
                            if weapon[0] != 'bare_hand':
                                commands.append(['spawn',subject,weapon[0]])
                        commands.append(['set',subject,'wp=reload'])
                    else:
                        for weapon in allweapons:
                            if weapon[0] == item:
                                player['wpbag'].append(list(weapon))
                                print("Command Confirmed\n"+item.capitalize(),"spawned.")
                                

            elif action == 'del':
                if entity != None:
                    key = result
                    if key == 'all':
                        print("Command Confirmed.")
                        while len(entity) > 0:
                            entity.pop()
                    elif key == 'nearby':
                        if len(entity)>0 and 'pos' in entity[0]:
                            for obj in entity:
                                if abs(obj['pos']-p1['pos'])<500:
                                    del obj          
                    else:                       
                        try: key = int(key)
                        except ValueError: key = None
                        if type(key) is int and -len(entity) <=key < len(entity):
                            print("Command Confirmed.")
                            del entity[key]

                            
            elif action == 'focus':
                dmapZ = None
                if subject == 'p1':
                    dmapZ = complex(display_w/2,display_h/2) - p1['pos']
                elif subject == 'p2':
                    dmapZ = complex(display_w/2,display_h/2) - p2['pos']
                if dmapZ:                        
                    print("Command Confirmed.\nAdjusting coordinates...\n")
                    p1['pos'] += dmapZ
                    p2['pos'] += dmapZ
                    for weapon in WeaponsOG:
                        weapon[1] += dmapZ
                        print(weapon[1])
                    for zob in Zombies:
                        zob['pos'] += dmapZ
                        print(zob['pos'])
                    for zobzone in ZombieZones:
                        zobzone[0] += dmapZ.real
                        zobzone[1] += dmapZ.imag
                        print(zobzone[0],zobzone[1])
                    for hac in HACs:
                        hac['pos'] += dmapZ
                        hac['az'][0] += dmapZ.real
                        hac['az'][1] += dmapZ.imag
                        print(hac['pos'],hac['az'])
                    for ba in Barriers:
                        ba[0][0] += dmapZ.real
                        ba[0][1] += dmapZ.imag
                        print(ba)
                    print("\nAdjusting completed.")
 

            elif action == 'exit':
                incommand = False


           
    game_state = [game_time,p1,p2,WeaponsOG,Zombies,ZombieZones,HACs,Barriers]
    return game_state

