'''
This is the warframe prime part farming guide. This is inteneded to help players of all skill levels help find ways to farm for prime parts.
Press the run button and follow the text instructions to get started.

Update log is posted at the bottom

Verion 1.2 1/10/18:
  This is less of an update about the content of the program and more an update of where this program will be going.
  While repl.it has served me quite well, I find that a text terminal does not allow for a very user friendly experience. Because of this, I will be converting into a website usin github pages.
  The site will be available at https://AvisTonitrui.github.io/Warfarm (please note hat the site is case sensitive)
  With a website, I will hopefully be able to dliver an experience much more user friendly and make it even easier for you to optimize your prime farming.
  This will not be a short process, as I have to change programming languages and also make the whole program more web compatible. I will update this repl once I have gotten the site into a working state.
  In the meantime, this program will remain up and completely usable. However, all future updates will only be available via th site.
  
'''



'''
beginning with class, function, and variable definitions
'''

#These lists are used to create listings much easier
primes = []
frames = []
primaries = []
secondaries = []
melees = []
sentinels = []
archwings = []
planets = []

#shutdown_check checks input to see if it needs to shutdown
def shutdown_check(input):
  if input == "shutdown":
    print "Shutting down"
    return True

#function for checking if a given array has all of the parts requested 
def era_check(eras, request):
  #iterating through both to check if the parts are all there
  for part in request:
    #defaults broke to true in case there are no relics in a certain era
    if len(eras) == 0:
      broke = True
      
    else:
      #runs through the check if there are elements to check
      for piece in eras:
        if part[0].name == piece[0].name and part[1].name == piece[1].name:
          broke = True
          break
        
        else:
          broke = False
      
    if broke:
      return False
  
  return True

#function for marking indecies for deletion based on an era keyword
def delete(array, keyword):
  #starting an array for marking deletions as well as an index counter
  deletes = []
  index = 0
  
  for element in array:
    if element[2].era != keyword:
      deletes.insert(0, index)
  
  #returns the array of indecies marked for deletion
  return deletes

#checks if a node hasalready been appended to the list of current nodes
def check_node_match(locations, list):
  index = 0
  
  for location in list:
    if locations[4] == location:
      return index
    else:
      index += 1
  
  return -1

#checks if acombination hs all the requested parts
def check_requested(nodes, request):
  #iterate through the requests, as every element of it will be used
  for part in request:
    
    #runs through the list of nodes and checks it against the part
    for node in nodes:
      
      #running through the parts under each node
      for piece in node[1]:
        
        if part[1].name == piece[1].name:
          broke = True
          break
        
        broke = False
        
      if broke:
        break
      
      broke = False
      
    if not broke:
      found = False
      break
    
    found = True
  
  return found

def earliest_rotation(A, B, C, requested):
  deletes = []
  requests = requested
  
  #basic function to go through and delete all the parts already found
  for relic in A:
    parts_index = 0
    
    for part in requests:
      if relic[1] == part[1]:
        deletes.insert(0, parts_index)
        parts_index += 1
        break
      
      parts_index += 1
  
  for index in deletes:
    del requests[index]
  
  #checking if all requested parts are found, and returning this rotation if they are.
  if len(requests) == 0:
    return "A"
  
  #resetting and repeating for the other two rotations
  deletes = []
  
  for relic in B:
    parts_index = 0
    
    for part in requests:
      if relic[1] == part[1]:
        deletes.insert(0, parts_index)
        parts_index += 1
        break
      
      parts_index += 1
  
  for index in deletes:
    del requests[index]
  
  #checking if all requested parts are found, and returning this rotation if they are.
  if len(requests) == 0:
    return "B"
  
  #rotation C
  deletes = []
  
  for relic in C:
    parts_index = 0
    
    for part in requests:
      if relic[1] == part[1]:
        deletes.insert(0, parts_index)
        parts_index += 1
        break
      
      parts_index += 1
  
  for index in deletes:
    del requests[index]
  
  #checking if all requested parts are found, and returning this rotation if they are.
  if len(requests) == 0:
    return "C"
  
  else:
    return "Misc."

def check_duplicate_relics(relics):
  index1 = 0
  index2 = 0
  list = relics
  deletes = []
  
  while index1 < len(list) - 1:
    while index2 < len(list):
      if list[index1][2] == list[index2][2]:
        deletes.append(index2)
      
      index2 += 1
    index1 += 1
    index2 = index1 + 1
  
  #with deletes now populated, it is setted, then listed again in order to remove duplicates. we also sort and reverse.
  deletes_set = set(deletes)
  deletes = []
  
  for index in deletes_set:
    deletes.append(index)
  
  deletes.sort()
  deletes.reverse()
  
  #we now go through our deletes and remove elements from list at those indecies
  for index in deletes:
    del list[index]
  
  #finishing up by returning list
  return list

#compares the combinations, returning the index of the best one
def compare_possibles(possibles, requests):
  #condensing each combination of nodes and their relics into their rotation A chance, rotation B chance, and rotation C chance. The first element in the final array is what the earliest rotation that all parts are available in.
  modded_possibles = [] #the condensed version of the possible combinations for final comparison
  
  for combo in possibles:
    #resetting variables for the next combo
    relics_all = [] #all the uncondensed relics for this combination
    relics_A = [] #all the rotation A drops for the relics
    relics_B = [] #all the rotation B drops for the relics
    relics_C = [] #all the rotation C drops for the relics
    relics_misc = [] #all the relics that had their rotation wrongly initialized.
    node_index = 0 #index tracker
    combo_condensed = [] #the condensed version of the combo
    chance_A = 0 #combined chance for getting a selected relic at each respective rotation
    chance_B = 0
    chance_C = 0
    
    for node in combo:
      for relic in node[1]:
        relics_all.append(relic)
    
    #now that we have a massive list of all relics that are uncondensed, we will separate them into all of their rotations
    for relic in relics_all:
      if relic[4] == "A":
        relics_A.append(relic)
      
      elif relic[4] == "B":
        relics_B.append(relic)
      
      elif relic[4] == "C":
        relics_C.append(relic)
      
      else:
        relics_misc.append(relic)
    
    #debug to check if there was a wrong intialization of relic rotations
    #print len(relics_misc)
    
    #with each of the relics sorted into their proper rotations, we can now check which rotation is the earliest that all parts are available.
    combo_condensed.append(earliest_rotation(relics_A, relics_B, relics_C, requests))
    
    #now that everything is checked for rotations and parts, we can condense everything to only the relics and their chances.
    relics_A = check_duplicate_relics(relics_A)
    relics_B = check_duplicate_relics(relics_B)
    relics_C = check_duplicate_relics(relics_C)
    relics_misc = check_duplicate_relics(relics_misc)
    
    #go through each rotations list and combine the chances for each rotation
    for relic in relics_A:
      chance_A += relic[3]
    combo_condensed.append(chance_A)
    
    for relic in relics_B:
      chance_B += relic[3]
    combo_condensed.append((chance_B * 1/3) + (chance_A * 2/3))
    
    for relic in relics_C:
      chance_C += relic[3]
    combo_condensed.append((chance_C * 1/4) + (chance_B * 1/4) + (chance_A * 1/2))
    
    
    
    #taking the current condensed format, we can now delete the rotations that don't have all the parts
    if combo_condensed[0] == "C":
      #just takes the C rotation, as that is the only rotation with all parts for this combination
      combo_condensed = ["C", combo_condensed[3]]
    
    elif combo_condensed[0] == "B":
      #compares rotations B and C and the highest is what is decided on, recommends the earlier rotation in case of tie
      if combo_condensed[2] < combo_condensed[3]:
        combo_condensed = ["C", combo_condensed[3]]
      
      else:
        combo_condensed = ["B", combo_condensed[2]]
    
    else:
      #first, compares A to B, lower is deleted. A wins in tie.
      if combo_condensed[1] < combo_condensed[2]:
        del combo_condensed[1]
        combo_condensed[0] = "B"
      
      else:
        del combo_condensed[2]
      
      #now, compares winner to C, lower deleted, ealier wins tie.
      if combo_condensed[1] < combo_condensed[2]:
        del combo_condensed[1]
        combo_condensed[0] = "C"
      
      else:
        del combo_condensed[2]
    
    #we now have the combination condensed in [suggested rotation, chance for going to suggested rotation]
    #adding this combo to the modded possibilities list for further use.
    modded_possibles.append(combo_condensed)
    
    #now, comparing each of the combinations
    
  
  #now with all of the ocmbinations condensed, we compare them, deferring to the earliest in the list
  index1 = 0 #the index of the highest so far
  index2 = 1 #the index of the combo being compared
  
  while index2 < len(modded_possibles):
    if modded_possibles[index1][1] < modded_possibles[index2][1]:
      index1 = index2
    
    index2 += 1
  
  #now returns the index of the highest chance, along with the suggested rotation and chance
  return [index1, modded_possibles[index1][0], modded_possibles[index1][1]]

#Defining all the classes that we'll need
class Planet:
    def __init__(self, name, unlock_number):
        self.unlock_number = unlock_number
        self.name = name
        
        #adding planets to an array with an insertion sort
        #automatically adding planet to list if list is empty
        if len(planets) == 0:
          planets.append(self)
        
        #inserting planet into array
        else:
          index = 0
          for planet in planets:
            if self.unlock_number < planet.unlock_number:
              planets.insert(index, self)
              break
            
            else:
              index += 1
            
            if index == len(planets):
              planets.append(self)
              break

class Node:
    def __init__(self, name, planet, level_min, level_max):
        self.name = name
        self.planet = planet
        self.min_level = level_min
        self.max_level = level_max

class Location:
    def __init__(self, nodes, type, tier):
        self.nodes = []
        self.type = type
        self.tier = tier
        self.sort  = nodes
        
        #print "intializing " + self.type + str(self.tier)
        index = 0
        
        #sorting the given nodes to be in level order
        for node in self.sort:
          #print "sorting " + node.name
          
          if len(self.nodes) == 0:
            #print node.name + " is the first node to be sorted"
            self.nodes.insert(0, node)
            
          else:
            index = 0
            
            for sorted in self.nodes:
              #print "resetting index value"
              
              if node.min_level < sorted.min_level:
                #print node.name + "'s minimum level is less than " + sorted.name + "'s minimum level"
                self.nodes.insert(index, node)
                break
              
              elif node.min_level > sorted.min_level:
                #print node.name + "'s minimum level is greater than " + sorted.name + "'s minimum level"
                index += 1
                
              else:
                #print node.name + "'s minimum level is equal to " + sorted.name + "'s minimum level"
                
                if node.max_level < sorted.max_level:
                  #print node.name + "'s maximum level is less than " + sorted.name + "'s maximum level"
                  self.nodes.insert(index, node)
                  break
                
                elif node.max_level > sorted.max_level:
                  #print node.name + "'s maximum level is greater than " + sorted.name + "'s maximum level"
                  index += 1
                  
                else:
                  #print node.name + "'s maximum level is equal to " + sorted.name + "'s maximum level"
                  
                  if node.planet.unlock_number < sorted.planet.unlock_number:
                    #print node.name + "'s unlock number is less than " + sorted.name + "'s unlock number"
                    self.nodes.insert(index, node)
                    break
                  
                  elif node.planet.unlock_number > sorted.planet.unlock_number:
                    #print node.name + "'s unlock number is greater than " + sorted.name + "'s unlock number"
                    index += 1
                    
                  else:
                    #print node.name + "'s unlock number is equal to " + sorted.name + "'s unlock number"
                    index += 1
                    
            if index == len(self.nodes):
              #print "we checked everything, appending " + node.name
              self.nodes.append(node)
        
        #print "printing the nodes in this location"
        #for node in self.nodes:
          #print node.name

class Relic:
    def __init__(self, locations, era):
        self.locations = locations
        self.era = era

class Prime_part:
    def __init__(self, relics, name):
        self.relics = relics
        self.name = name
        self.built = False

class Prime:
    def __init__(self, parts, name, type):
        self.parts = parts
        self.name = name
        self.type = type
        self.built = True
        primes.append(self)
        
        if self.type == "frame":
          frames.append(self)
          
        elif self.type == "primary":
          primaries.append(self)
          
        elif self.type == "secondary":
          secondaries.append(self)
          
        elif self.type == "melee":
          melees.append(self)
          
        elif self.type == "sentinel":
          sentinels.append(self)
          
        elif self.type == "archwing":
          archwings.append(self)
          
        else:
          print self.name + " isn't getting put into a specific type"

'''
This is the end of the class, function, and variable definition section, the following is all of the data entry
'''

#defining the planets in their unlock order. Orokin derelict is placed with saturn due to getting ready access to the nano spores needed to make derelict keys.
earth = Planet("earth", 0)
venus = Planet("venus", 1)
mercury = Planet("mercury", 2)
mars = Planet("mars", 3)
void1 = Planet("void1", 4)
phobos = Planet("phobos", 5)
ceres = Planet("ceres", 6)
jupiter = Planet("jupiter", 7)
void2 = Planet("void2", 8)
europa = Planet("europa", 9)
derelict = Planet("orokin derelict", 10)
saturn = Planet("saturn", 11)
uranus = Planet("uranus", 12)
void3 = Planet("void3", 13)
neptune = Planet("neptune", 14)
lua = Planet("lua", 15)
pluto = Planet("pluto", 16)
kuva_fortress = Planet("kuva fortress", 17)
void4 = Planet("void4", 18)
sedna = Planet("sedna", 19)
eris = Planet("eris", 20)


#defining nearly every node in the game with its planet and level range.  Some are commented out because their mission type does not drop relics. Trials and the index aren't listed.

#Earth nodes
cambria = Node("Cambria", earth, 2, 4)
#cervantes = Node("Cervantes", earth, 4, 6)
#e_prime = Node("E Prime", earth, 1, 3)
#erpo = Node("Erpo", earth, 1, 6)
#eurasia = Node("Eurasia", earth, 3 , 5)
everest = Node("Everest", earth, 1, 6)
gaia = Node("Gaia", earth, 1, 6)
lith = Node("Lith", earth, 1, 6)
mantle = Node("Mantle", earth, 2, 4)
#mariana = Node("Mariana", earth, 1, 3)
#pacific = Node("Pacific", earth, 3, 6)
coba = Node("Coba", earth, 6, 16)
tikal = Node("Tikal", earth, 6, 16)
#oro = Node("Oro", earth, 20, 25)

#Venus nodes
#aphrodite = Node("Aphrodite", venus, 6, 8)
cytherean = Node("Cytherean", venus, 3, 8)
#e_gate = Node("E Gate", venus, 3, 5)
#ishtar = Node("Ishtar", venus, 6, 8)
kiliken = Node("Kiliken", venus, 3, 8)
#linea = Node("Linea", venus, 5, 7)
malva = Node("Malva", venus, 8, 18)
#montes = Node("Montes", venus, 3, 8)
romula = Node("Romula", venus, 6, 8)
tessera = Node("Tessera", venus, 3, 8)
unda = Node("Unda", venus, 4, 6)
venera = Node("Venera", venus, 5, 7)
v_prime = Node("V Prime", venus, 3, 8)
#fossa = Node("Fossa", venus, 6, 8)

#Mercury nodes
apollodorus = Node("Apollodorus", mercury, 6, 11)
#boethius = Node("Boethius", mercury, 8, 10)
#caloris = Node("Caloris", mercury, 6, 8)
elion = Node("Elion", mercury, 7, 9)
lares = Node("Lares", mercury, 6, 11)
#m_prime = Node("M Prime", mercury, 7, 9)
odin = Node("Odin", mercury, 6, 11)
#pantheon = Node("Pantheon", mercury, 6, 8)
suisei = Node("Suisei", mercury, 8, 10)
#terminus = Node("Terminus", mercury, 8, 10)
#tolstoj = Node("Tolstoj", mercury, 9, 11)

#Mars nodes
alator = Node("Alator", mars, 8, 13)
ara = Node("Ara", mars, 10, 12)
#ares = Node("Ares", mars, 9, 11)
arval = Node("Arval", mars, 9, 11)
augustus = Node("Augustus", mars, 9, 14)
#gradivus = Node("Gradivus", mars, 9, 11)
#hellas = Node("Hellas", mars, 8, 10)
kadesh = Node("Kadesh", mars, 10, 20)
#martialis = Node("Martialis", mars, 10, 12)
#olympus = Node("Olympus", mars, 11, 13)
spear = Node("Spear", mars, 8, 13)
#syrtis = Node("Syrtis", mars, 8, 13)
#tharsis = Node("Tharsis", mars, 8, 10)
#ultor = Node("Ultor", mars, 11, 13)
#vallis = Node("Vallis", mars, 11, 13)
wahiba = Node("Wahiba", mars, 10, 20)
#war = Node("War", mars, 11, 13)

#Phobos nodes
#roche = Node("Roche", phobos, 10, 12)
#sharpless = Node("Sharpless", phobos, 11, 13)
gulliver = Node("Gulliver", phobos, 10, 15)
kepler = Node("Kepler", phobos, 12, 14)
memphis = Node("Memphis", phobos, 15, 25)
#monolith = Node("Monolith", phobos, 13, 15)
shklovsky = Node("Shklovsky", phobos, 11, 13)
skyresh = Node("Skyresh", phobos, 12, 14)
stickney = Node("Stickney", phobos, 10, 15)
zeuguma = Node("Zeuguma", phobos, 15, 25)
#iliad = Node("Iliad", phobos, 13, 15)

#Ceres nodes
bode = Node("Bode", ceres, 12, 14)
casta = Node("Casta", ceres, 12, 17)
cinxia = Node("Cinxia", ceres, 12, 17)
draco = Node("Draco", ceres, 12, 17)
gabii = Node("Gabii", ceres, 15, 25)
#ker= Node("Ker", ceres, 14, 16)
#kiste = Node("Kiste", ceres, 13, 15)
lex = Node("Lex", ceres, 14, 16)
#ludi = Node("Ludi", ceres, 15, 17)
#nuovo = Node("Nuovo", ceres, 13, 15)
#pallas = Node("Pallas", ceres, 12, 14)
seimeni = Node("Seimeni", ceres, 15, 25)
#thon = Node("Thon", ceres, 15, 17)
#exta = Node("Exta", ceres, 14, 16)

#Jupiter nodes
#adrastea = Node("Adrastea", jupiter, 18, 20)
amalthea = Node("Amalthea", jupiter, 17, 19)
ananke = Node("Ananke", jupiter, 16, 18)
callisto = Node("Callisto", jupiter, 15, 20)
#carme = Node("Carme", jupiter, 16, 18)
#carpo = Node("Carpo", jupiter, 17, 19)
elara = Node("Elara", jupiter, 15, 20)
#galilea = Node("Galilea", jupiter, 15, 20)
io = Node("Io", jupiter, 15, 20)
#metis = Node("Metis", jupiter, 20, 22)
#thebe = Node("Thebe", jupiter, 18, 20)
cameria = Node("Cameria", jupiter, 20, 30)
sinai = Node("Sinai", jupiter, 20, 30)
#themisto = Node("Themisto", jupiter, 18, 20)

#Europa nodes
abaddon = Node("Abaddon", europa, 21, 23)
#armaros = Node("Armaros", europa, 18, 20)
#baal = Node("Baal", europa, 21, 23)
#kokabiel = Node("Kokabiel", europa, 20, 22)
#morax = Node("Morax", europa, 18, 20)
#orias = Node("Orias", europa, 20, 22)
ose = Node("Ose", europa, 18, 23)
paimon = Node("Paimon", europa, 18, 23)
#sorath = Node("Sorath", europa, 19, 21)
valac = Node("Valac", europa, 18, 20)
valefor = Node("Valefor", europa, 18, 23)
cholistan = Node("Cholistan", europa, 23, 33)
larzac = Node("Larzac", europa, 23, 33)
#naamah = Node("Naamah", europa, 21, 23)

#Saturn nodes
#anthe = Node("Anthe", saturn, 22, 24)
#calypso = Node("Calypso", saturn, 24, 26)
caracol = Node("Caracol", saturn, 26, 36)
cassini = Node("Cassini", saturn, 21, 23)
dione = Node("Dione", saturn, 21, 23)
#encleadus = Node("Encleadus", saturn, 23, 25)
helene = Node("Helene", saturn, 21, 26)
#keeler = Node("Keeler", saturn, 23, 25)
numa = Node("Numa", saturn, 22, 24)
pandora = Node("Pandora", saturn, 21, 23)
piscinas = Node("Piscinas", saturn, 26, 36)
rhea = Node("Rhea", saturn, 21, 26)
#telesto = Node("Telesto", saturn, 22, 24)
titan = Node("Titan", saturn, 21, 26)
#tethys = Node("Tethys", saturn, 24, 26)

#Uranus nodes
ariel = Node("Ariel", uranus, 25, 27)
assur = Node("Assur", uranus, 25, 35)
caelus = Node("Caelus", uranus, 24, 29)
#caliban = Node("Caliban", uranus, 25, 27)
#cressida = Node("Cressida", uranus, 25, 27)
#desdemona = Node("Desdemona", uranus, 26, 28)
ophelia = Node("Ophelia", uranus, 24, 29)
#puck = Node("Puck", uranus, 27, 29)
rosalind = Node("Roaslind", uranus, 27, 29)
stephano = Node("Stephano", uranus, 25, 27)
#sycorax = Node("Sycorax", uranus, 24, 26)
umbriel = Node("Umbriel", uranus, 24, 29)
ur = Node("Ur", uranus, 27, 37)
#titania = Node("Titania", uranus, 27, 29)

#Neptune nodes
despina = Node("Despina", neptune, 27, 32)
galatea = Node("Galatea", neptune, 27, 29)
kelashin = Node("Kelashin", neptune, 30, 40)
laomedeia = Node("Laomedeia", neptune, 30, 32)
#larissa = Node("Larissa", neptune, 29, 31)
#nereid = Node("Nereid", neptune, 30, 32)
#neso = Node("Neso", neptune, 29, 31)
proteus = Node("Proteus", neptune, 30, 32)
#salacia = Node("Salacia", neptune, 27, 32)
#sao = Node("Sao", neptune, 29, 31)
#triton = Node("Triton", neptune, 28, 30)
yursa = Node("Yursa", neptune, 30, 40)
#psamanthe = Node("Psamanthe", neptune, 30, 32)

#Lua nodes
copernicus = Node("Copernicus", lua, 25, 30)
#grimaldi = Node("Grimaldi", lua, 25, 30)
pavlov = Node("Pavlov", lua, 25, 30)
#plato = Node("Plato", lua, 25, 30)
stofler = Node("Stofler", lua, 25, 30)
tycho = Node("Tycho", lua, 25, 30)
#zeipel = Node("Zeipal", lua, 25, 30)

#Pluto nodes
#acheron = Node("Acheron", pluto, 34, 38)
cerberus = Node("Cerberus", pluto, 30, 40)
#cypress = Node("Cypress", pluto, 34, 38)
hydra = Node("Hydra", pluto, 30, 34)
#minthe = Node("Minthe", pluto, 30, 34)
#narcissus = Node("Narcissus", pluto, 32, 36)
oceanum = Node("Oceanum", pluto, 32, 36)
outer_terminus = Node("Outer Terminus", pluto, 30, 40)
palus = Node("Palus", pluto, 30, 40)
#regna = Node("Regna", pluto, 34, 38)
hieracon = Node("Hieracon", pluto, 35, 45)
sechura = Node("Sechura", pluto, 32, 36)
#hades = Node("Hades", pluto, 35, 45)

#Kuva Fortress nodes
#dakata = Node("Dakata", kuva_fortress, 28, 30)
#garus = Node("Garus", kuva_fortress, 31, 33)
#koro = Node("Koro", kuva_fortress, 29, 31)
nabuk = Node("Nabuk", kuva_fortress, 30, 32)
pago = Node("Pago", kuva_fortress, 31, 33)
#rotuma = Node("Rotuma", kuva_fortress, 30, 32)
tamu = Node("Tamu", kuva_fortress, 32, 34)
taveuni = Node("Taveuni", kuva_fortress, 32, 34)

#Sedna nodes
#naga = Node("Naga", sedna, 30, 34)
berehynia = Node("Berehynia", sedna, 30, 40)
hydron = Node("Hydron", sedna, 30, 40)
selkie = Node("Selkie", sedna, 30, 40)
#adaro = Node("Adaro", sedna, 32, 36)
rusalka = Node("Rusalka", sedna, 32, 36)
kappa = Node("Kappa", sedna, 34, 38)
#marid = Node("Marid", sedna, 34, 38)
#charybdis = Node("Charybdis", sedna, 34, 38)
amarna = Node("Amarna", sedna, 35, 45)
sangeru = Node("Sangeru", sedna, 35, 45)
#kelpie = Node("Kelpie", sedna, 36, 40)
#nakki = Node("Nakki", sedna, 40, 40)
#yam = Node("Yam", sedna, 60, 60)
#vodyanoi = Node("Vodyanoi", sedna, 85, 85)
#merrow = Node("Merrow", sedna, 35, 40)

#Eris nodes
#brugia = Node("Brugia", eris, 32, 36)
isos = Node("Isos", eris, 32, 36)
kala_azar = Node("Kala-azar", eris, 30, 40)
#naeglar = Node("Naeglar", eris, 30, 34)
nimus = Node("Nimus", eris, 30, 40)
oestrus = Node("Oestrus", eris, 34, 38)
#saxis = Node("Saxis", eris, 34, 38)
#solium = Node("Solium", eris, 34, 38)
xini = Node("Xini", eris, 30, 40)
akkad = Node("Akkad", eris, 35, 45)
zabala = Node("Zabala", eris, 35, 45)
#jordas_golem_assassinate = Node("Jordas Golem Assassinate", eris, 32, 34)

#Void nodes
#teshub = Node("Teshub", void1, 10, 15)
hepit = Node("Hepit", void1, 10, 15)
taranis = Node("Taranis", void1, 10, 15)
#tiwaz = Node("Tiwaz", void2, 20, 25)
#stribog = Node("Stribog", void2, 20, 25)
ani = Node("Ani", void2, 20, 25)
ukko = Node("Ukko", void3, 30, 35)
#oxomoco = Node("Oxomoco", void3, 30, 35)
belenus = Node("Belenus", void3, 30, 35)
#aten = Node("Aten", void4, 40, 45)
#marduk = Node("Marduk", void4, 40, 45)
mithra = Node("Mithra", void4, 40, 45)
mot = Node("Mot", void4, 40, 45)

#Orokin Derelict nodes
#derelict_assassinate = Node("Orokin Derelict Assassinate", derelict, 25, 35)
derelict_defense = Node("Orokin Derelict Defense", derelict, 25, 35)
#derelict_exterminate = Node("Orokin Derelict Exterminate", derelict, 25, 35)
#derelict_mobile_defense = Node("Orokin Derelict Mobile Defense", derelict, 25, 35)
#derelict_sabotage = Node("Orokin Derelict Sabotage", derelict, 25, 35)
derelict_survival = Node("Orokin Derelict Survival", derelict, 25, 35)

#Defining locations which are the mission type and tier combination. tier 0 indicates shared rewards across all tiers, 5 indicates general dark sector, 6 indicates derelict, 7 indicates archwing, 8 for kuva fortress, 9 for Lua, 10 for dark sector 1, 11 for dark sector 2, 12 for dark sector 3, and 13 for dark sector 4.
capture = Location([mantle, venera, elion, ara, skyresh, lex, ananke, cassini, ariel, galatea, rusalka, isos, hydra, copernicus, hepit, ukko, nabuk], "Capture", 0)
defection1 = Location([memphis], "Defection", 1)
defection2 = Location([caracol], "Defection", 2)
defection3 = Location([yursa], "Defection", 3)
defense1 = Location([lith, tessera, lares, spear, gulliver, casta, taranis], "Defense", 1)
defense2 = Location([io, paimon, helene], "Defense", 2)
defense3 = Location([stephano, proteus, hydron, kala_azar, outer_terminus, stofler, belenus, tamu], "Defense", 3)
defense_dark = Location([akkad, coba, kadesh, larzac, romula, sangeru, sechura, seimeni, sinai, ur], "Defense", 5)
defense_derelict = Location([derelict_defense], "Defense", 6)
excavation1 = Location([everest, kiliken, augustus], "Excavation", 1)
excavation2 = Location([valefor], "Excavation", 2)
excavation3 = Location([despina], "Excavation", 3)
salvage = Location([oestrus], "Salvage", 0)
interception1 = Location([gaia, cytherean, odin, alator, cinxia], "Interception", 1)
interception2 = Location([callisto, ose, rhea, umbriel], "Interception", 2)
interception3 = Location([berehynia, xini, cerberus, mithra], "Interception", 3)
interception_arch = Location([caelus], "Interception", 7)
pursuit = Location([pandora], "Pursuit", 7)
rush = Location([kepler], "Rush", 7)
spy1 = Location([cambria, unda, suisei, arval, shklovsky], "Spy", 1)
spy2 = Location([bode, amalthea, valac, dione], "Spy", 2)
spy3 = Location([rosalind, laomedeia, kappa, oceanum], "Spy", 3)
spy_kuva = Location([pago], "Spy", 8)
spy_lua = Location([pavlov], "Spy", 9)
survival1 = Location([v_prime, apollodorus, stickney], "Survival", 1)
survival2 = Location([draco, elara, titan, ani], "Survival", 2)
survival3 = Location([ophelia, selkie, nimus, palus, tycho, taveuni], "Survival", 3)
survival4 = Location([mot], "Survival", 4)
survival_derelict = Location([derelict_survival], "Survival", 6)
survival_dark1 = Location([gabii, malva], "Survival", 10)
survival_dark2 = Location([cameria, piscinas, wahiba, zeuguma], "Survival", 11)
survival_dark3 = Location([amarna, assur, kelashin], "Survival", 12)
survival_dark4 = Location([zabala], "Survival", 13)

#Defining every currently unvaulted relic with their locations
#Each location is an array consisting of the location class instance, chance at that instance (expressed as a percent), and the rotation it is rewarded on. A rotaion of 'A' is used in the instance that the mission type doesn't use rotations.
#relics will be removed from the code when vaulted
#bounties not included

#Lith relics
lithA2 = Relic([[capture, 0.2, "A"], [defection1, 9.68, "B"], [defection1, 9.68, "C"], [defense_derelict, 10, "A"], [defense1, 7.69, "A"], [defense_dark, 9.48, "A"], [excavation1, 7.14, "B"], [excavation1, 9.68, "C"], [interception1, 8.33, "A"], [rush, 8.6, "C"], [spy1, 12.5, "B"], [survival_derelict, 10, "A"], [survival1, 7.14, "B"], [survival1, 9.68, "C"], [survival_dark1, 7.14, "B"], [survival_dark1, 9.68, "C"]], "Lith")
lithB2 = Relic([[defection1, 9.68, "B"], [defection1, 9.68, "C"], [defense_derelict, 10, "A"], [defense1, 7.69, "A"], [defense_dark, 3.16, "A"], [excavation1, 7.14, "B"], [excavation1, 9.68, "C"], [interception1, 8.33, "A"], [rush, 8.6, "C"], [spy1, 12.5, "B"], [survival_derelict, 10, "A"], [survival1, 7.14, "B"], [survival1, 9.68, "C"], [survival_dark1, 7.14, "B"], [survival_dark1, 9.68, "C"]], "Lith")
lithC2 = Relic([[defection1, 9.68, "B"], [defection1, 9.68, "C"], [defense_derelict, 10, "A"], [defense1, 7.69, "A"], [defense_dark, 9.48, "A"], [excavation1, 7.14, "B"], [excavation1, 9.68, "C"], [interception1, 8.33, "A"], [rush, 8.6, "C"], [spy1, 12.5, "B"], [survival_derelict, 10, "A"], [survival1, 7.14, "B"], [survival1, 9.68, "C"], [survival_dark1, 7.14, "B"], [survival_dark1, 9.68, "C"]], "Lith")
lithN3 = Relic([[capture, 0.2, "A"], [defection1, 9.68, "B"], [defection1, 9.68, "C"], [defense_derelict, 10, "A"], [defense1, 7.69, "A"], [defense_dark, 3.16, "A"], [excavation1, 7.14, "B"], [excavation1, 9.68, "C"], [interception1, 8.33, "A"], [rush, 8.6, "C"], [spy1, 12.5, "B"], [survival_derelict, 10, "A"], [survival1, 7.14, "B"], [survival1, 9.68, "C"], [survival_dark1, 7.14, "B"], [survival_dark1, 9.68, "C"]], "Lith")
lithS7 = Relic([[defection1, 9.68, "B"], [defection1, 9.68, "C"], [defense_derelict, 10, "A"], [defense1, 7.69, "A"], [defense_dark, 9.48, "A"], [excavation1, 7.14, "B"], [excavation1, 9.68, "C"], [interception1, 8.33, "A"], [rush, 8.6, "C"], [spy1, 12.5, "B"], [survival_derelict, 10, "A"], [survival1, 7.14, "B"], [survival1, 9.68, "C"], [survival_dark1, 7.14, "B"], [survival_dark1, 9.68, "C"]], "Lith")
lithT1 = Relic([[defection1, 9.68, "B"], [defection1, 9.68, "C"], [defense_derelict, 10, "A"], [defense1, 7.69, "A"], [defense_dark, 3.16, "A"], [excavation1, 7.14, "B"], [excavation1, 9.68, "C"], [interception1, 8.33, "A"], [rush, 8.6, "C"], [spy1, 12.5, "B"], [survival_derelict, 10, "A"], [survival1, 7.14, "B"], [survival1, 9.68, "C"], [survival_dark1, 7.14, "B"], [survival_dark1, 9.68, "C"]], "Lith")
lithV2 = Relic([[defection1, 9.68, "B"], [defection1, 9.68, "C"], [defense_derelict, 10, "A"], [defense1, 7.69, "A"], [defense_dark, 3.16, "A"], [excavation1, 7.14, "B"], [excavation1, 9.68, "C"], [interception1, 8.33, "A"], [rush, 8.6, "C"], [spy1, 12.5, "B"], [survival_derelict, 10, "A"], [survival1, 7.14, "B"], [survival1, 9.68, "C"], [survival_dark1, 7.14, "B"], [survival_dark1, 9.68, "C"]], "Lith")
lithV3 = Relic([[defection1, 9.68, "B"], [defection1, 9.68, "C"], [defense_derelict, 10, "A"], [defense1, 7.69, "A"], [excavation1, 7.14, "B"], [excavation1, 9.68, "C"], [interception1, 8.33, "A"], [rush, 8.6, "C"], [spy1, 12.5, "B"], [survival_derelict, 10, "A"], [survival1, 7.14, "B"], [survival1, 9.68, "C"], [survival_dark1, 7.14, "B"], [survival_dark1, 9.68, "C"]], "Lith")

#meso relics
mesoG1 = Relic([[defection2, 15.49, "B"], [defense_derelict, 15.49, "C"], [defense1, 10, "B"], [defense1, 10, "C"], [defense_dark, 1.84, "B"], [defense_dark, 9.48, "C"], [defense2, 16.67, "A"], [excavation2, 8.33, "B"], [interception1, 6.67, "B"], [interception1, 19.48, "C"], [interception2, 11.11, "A"], [pursuit, 16.67, "C"], [spy3, 12.91, "B"], [spy_kuva, 12.91, "B"], [spy2, 12.91, "C"], [survival2, 8.33, "B"], [excavation2, 8.33, "B"], [survival_dark2, 8.33, "B"]], "Meso")
mesoH1 = Relic([[defection2, 15.49, "B"], [defense_derelict, 15.49, "C"], [defense1, 10, "B"], [defense1, 10, "C"], [defense_dark, 1.84, "B"], [defense_dark, 9.48, "C"], [defense2, 16.67, "A"], [excavation2, 8.33, "B"], [interception1, 6.67, "B"], [interception1, 19.48, "C"], [interception2, 11.11, "A"], [pursuit, 16.67, "C"], [spy3, 12.91, "B"], [spy_kuva, 12.91, "B"], [spy2, 12.91, "C"], [survival2, 8.33, "B"], [excavation2, 8.33, "B"], [survival_dark2, 8.33, "B"]], "Meso")
mesoK1 = Relic([[defection2, 15.49, "B"], [defense_derelict, 15.49, "C"], [defense1, 10, "B"], [defense1, 10, "C"], [defense_dark, 1.84, "B"], [defense_dark, 9.48, "C"], [defense2, 16.67, "A"], [excavation2, 8.33, "B"], [interception1, 6.67, "B"], [interception1, 19.48, "C"], [interception2, 11.11, "A"], [pursuit, 16.67, "C"], [spy3, 12.91, "B"], [spy_kuva, 12.91, "B"], [spy2, 12.91, "C"], [survival2, 8.33, "B"], [excavation2, 8.33, "B"], [survival_dark2, 8.33, "B"]], "Meso")
mesoN5 = Relic([[defection2, 15.49, "B"], [defense_derelict, 15.49, "C"], [defense1, 10, "B"], [defense1, 10, "C"], [defense_dark, 1.84, "B"], [defense_dark, 9.48, "C"], [defense2, 16.67, "A"], [excavation2, 8.33, "B"], [interception1, 6.67, "B"], [interception1, 19.48, "C"], [interception2, 11.11, "A"], [pursuit, 16.67, "C"], [spy3, 12.91, "B"], [spy_kuva, 12.91, "B"], [spy2, 12.91, "C"], [survival2, 8.33, "B"], [excavation2, 8.33, "B"], [survival_dark2, 8.33, "B"]], "Meso")
mesoO1 = Relic([[capture, 0.2, "A"], [defection2, 15.49, "B"], [defense_derelict, 15.49, "C"], [defense1, 10, "B"], [defense1, 10, "C"], [defense_dark, 1.84, "B"], [defense_dark, 9.48, "C"], [defense2, 16.67, "A"], [excavation2, 8.33, "B"], [interception1, 6.67, "B"], [interception1, 19.48, "C"], [interception2, 11.11, "A"], [pursuit, 16.67, "C"], [spy3, 12.91, "B"], [spy_kuva, 12.91, "B"], [spy2, 12.91, "C"], [survival2, 8.33, "B"], [excavation2, 8.33, "B"], [survival_dark2, 8.33, "B"]], "Meso")

#neo relics
neoB2 = Relic([[capture, 9.48, "A"], [defection3, 11.06, "B"], [defection2, 11.06, "C"], [defense_dark, 1.84, "C"], [defense3, 10, "A"], [defense2, 6.25, "B"], [defense2, 11.06, "C"], [excavation3, 6.67, "B"], [excavation2, 11.06, "C"], [interception3, 10, "A"], [interception2, 6.67, "B"], [interception2, 14.29, "C"], [salvage, 10, "A"], [spy3, 3.76, "B"], [spy_kuva, 3.76, "B"], [survival_derelict, 12.5, "B"], [survival_dark4, 14.29, "B"], [survival3, 6.67, "B"], [excavation3, 6.67, "B"], [survival_dark3, 6.67, "B"], [survival2, 11.06, "C"], [excavation2, 11.06, "C"], [survival_dark2, 11.06, "C"], [survival4, 14.29, "B"]], "Neo")
neoH1 = Relic([[defection3, 11.06, "B"], [defection2, 11.06, "C"], [defense_dark, 1.84, "C"], [defense3, 10, "A"], [defense2, 6.25, "B"], [defense2, 11.06, "C"], [excavation3, 6.67, "B"], [excavation2, 11.06, "C"], [interception3, 10, "A"], [interception2, 6.67, "B"], [interception2, 14.29, "C"], [salvage, 10, "A"], [spy3, 12.91, "B"], [spy_kuva, 12.91, "B"], [survival_derelict, 12.5, "B"], [survival_dark4, 14.29, "B"], [survival3, 6.67, "B"], [excavation3, 6.67, "B"], [survival_dark3, 6.67, "B"], [survival2, 11.06, "C"], [excavation2, 11.06, "C"], [survival_dark2, 11.06, "C"], [survival4, 14.29, "B"]], "Neo")
neoM1 = Relic([[defection3, 11.06, "B"], [defection2, 11.06, "C"], [defense_dark, 1.84, "C"], [defense3, 10, "A"], [defense2, 6.25, "B"], [defense2, 11.06, "C"], [excavation3, 6.67, "B"], [excavation2, 11.06, "C"], [interception3, 10, "A"], [interception2, 6.67, "B"], [interception2, 14.29, "C"], [salvage, 10, "A"], [spy3, 3.76, "B"], [spy_kuva, 3.76, "B"], [survival_derelict, 12.5, "B"], [survival_dark4, 14.29, "B"], [survival3, 6.67, "B"], [excavation3, 6.67, "B"], [survival_dark3, 6.67, "B"], [survival2, 11.06, "C"], [excavation2, 11.06, "C"], [survival_dark2, 11.06, "C"], [survival4, 14.29, "B"]], "Neo")
neoS7 = Relic([[defection3, 11.06, "B"], [defection2, 11.06, "C"], [defense_dark, 1.84, "C"], [defense3, 10, "A"], [defense2, 6.25, "B"], [defense2, 11.06, "C"], [excavation3, 6.67, "B"], [excavation2, 11.06, "C"], [interception3, 10, "A"], [interception2, 6.67, "B"], [interception2, 14.29, "C"], [salvage, 10, "A"], [spy3, 3.76, "B"], [spy_kuva, 3.76, "B"], [survival_derelict, 12.5, "B"], [survival_dark4, 14.29, "B"], [survival3, 6.67, "B"], [excavation3, 6.67, "B"], [survival_dark3, 6.67, "B"], [survival2, 11.06, "C"], [excavation2, 11.06, "C"], [survival_dark2, 11.06, "C"], [survival4, 14.29, "B"]], "Neo")
neoV2 = Relic([[defection3, 11.06, "B"], [defection2, 11.06, "C"], [defense_dark, 1.84, "C"], [defense3, 10, "A"], [defense2, 6.25, "B"], [defense2, 11.06, "C"], [excavation3, 6.67, "B"], [excavation2, 11.06, "C"], [interception3, 10, "A"], [interception2, 6.67, "B"], [interception2, 14.29, "C"], [salvage, 10, "A"], [spy3, 3.76, "B"], [spy_kuva, 3.76, "B"], [survival_derelict, 12.5, "B"], [survival_dark4, 14.29, "B"], [survival3, 6.67, "B"], [excavation3, 6.67, "B"], [survival_dark3, 6.67, "B"], [survival2, 11.06, "C"], [excavation2, 11.06, "C"], [survival_dark2, 11.06, "C"], [survival4, 14.29, "B"]], "Neo")
neoV5 = Relic([[capture, 0.2, "A"], [defection3, 11.06, "B"], [defection2, 11.06, "C"], [defense_dark, 1.84, "C"], [defense3, 10, "A"], [defense2, 6.25, "B"], [defense2, 11.06, "C"], [excavation3, 6.67, "B"], [excavation2, 11.06, "C"], [interception3, 10, "A"], [interception2, 6.67, "B"], [interception2, 14.29, "C"], [salvage, 10, "A"], [spy3, 3.76, "B"], [spy_kuva, 3.76, "B"], [survival_derelict, 12.5, "B"], [survival_dark4, 14.29, "B"], [survival3, 6.67, "B"], [excavation3, 6.67, "B"], [survival_dark3, 6.67, "B"], [survival2, 11.06, "C"], [excavation2, 11.06, "C"], [survival_dark2, 11.06, "C"], [survival4, 14.29, "B"]], "Neo")
neoV6 = Relic([[defection3, 11.06, "B"], [defection2, 11.06, "C"], [defense_dark, 1.84, "C"], [defense3, 10, "A"], [defense2, 6.25, "B"], [defense2, 11.06, "C"], [excavation3, 6.67, "B"], [excavation2, 11.06, "C"], [interception3, 10, "A"], [interception2, 6.67, "B"], [interception2, 14.29, "C"], [salvage, 10, "A"], [spy3, 3.76, "B"], [spy_kuva, 3.76, "B"], [survival_derelict, 12.5, "B"], [survival_dark4, 14.29, "B"], [survival3, 6.67, "B"], [excavation3, 6.67, "B"], [survival_dark3, 6.67, "B"], [survival2, 11.06, "C"], [excavation2, 11.06, "C"], [survival_dark2, 11.06, "C"], [survival4, 14.29, "B"]], "Neo")

#axi relics
axiA3 = Relic([[defection3, 12.91, "C"], [defense3, 6.67, "B"], [defense3, 11.06, "C"], [excavation3, 11.06, "C"], [interception_arch, 9.68, "C"], [interception3, 14.29, "B"], [interception3, 14.29, "C"], [salvage, 6.67, "B"], [survival_derelict, 11.06, "C"], [survival_dark4, 12.5, "C"], [survival3, 11.06, "C"], [excavation3, 11.06, "C"], [survival_dark3, 11.06, "C"], [survival4, 14.29, "C"]], "Axi")
axiB2 = Relic([[defense3, 6.67, "B"], [defense3, 11.06, "C"], [excavation3, 11.06, "C"], [interception_arch, 9.68, "C"], [interception3, 14.29, "B"], [interception3, 14.29, "C"], [salvage, 6.67, "B"], [survival_derelict, 11.06, "C"], [survival_dark4, 12.5, "C"], [survival3, 11.06, "C"], [excavation3, 11.06, "C"], [survival_dark3, 11.06, "C"], [survival4, 14.29, "C"]], "Axi")
axiE2 = Relic([[defection3, 12.91, "C"], [defense3, 6.67, "B"], [defense3, 11.06, "C"], [excavation3, 11.06, "C"], [interception_arch, 9.68, "C"], [interception3, 14.29, "B"], [interception3, 14.29, "C"], [salvage, 6.67, "B"], [survival_derelict, 11.06, "C"], [survival_dark4, 12.5, "C"], [survival3, 11.06, "C"], [excavation3, 11.06, "C"], [survival_dark3, 11.06, "C"], [survival4, 14.29, "C"]], "Axi")
axiN5 = Relic([[defection3, 12.91, "C"], [defense3, 6.67, "B"], [defense3, 11.06, "C"], [excavation3, 11.06, "C"], [interception_arch, 9.68, "C"], [interception3, 14.29, "B"], [interception3, 14.29, "C"], [salvage, 6.67, "B"], [survival_derelict, 11.06, "C"], [survival_dark4, 12.5, "C"], [survival3, 11.06, "C"], [excavation3, 11.06, "C"], [survival_dark3, 11.06, "C"], [survival4, 14.29, "C"]], "Axi")
axiO1 = Relic([[defection3, 12.91, "C"], [defense3, 6.67, "B"], [defense3, 11.06, "C"], [excavation3, 11.06, "C"], [interception_arch, 9.68, "C"], [interception3, 14.29, "B"], [interception3, 14.29, "C"], [salvage, 6.67, "B"], [survival_derelict, 11.06, "C"], [survival_dark4, 12.5, "C"], [survival3, 11.06, "C"], [excavation3, 11.06, "C"], [survival_dark3, 11.06, "C"], [survival4, 14.29, "C"]], "Axi")
axiV6 = Relic([[defection3, 12.91, "C"], [defense3, 6.67, "B"], [defense3, 11.06, "C"], [excavation3, 11.06, "C"], [interception_arch, 9.68, "C"], [interception3, 14.29, "B"], [interception3, 14.29, "C"], [salvage, 6.67, "B"], [survival_derelict, 11.06, "C"], [survival_dark4, 12.5, "C"], [survival3, 11.06, "C"], [excavation3, 11.06, "C"], [survival_dark3, 11.06, "C"], [survival4, 14.29, "C"]], "Axi")
axiV7 = Relic([[defection3, 12.91, "C"], [defense3, 6.67, "B"], [defense3, 11.06, "C"], [excavation3, 11.06, "C"], [interception_arch, 9.68, "C"], [interception3, 14.29, "B"], [interception3, 14.29, "C"], [salvage, 6.67, "B"], [survival_derelict, 11.06, "C"], [survival_dark4, 12.5, "C"], [survival3, 11.06, "C"], [excavation3, 11.06, "C"], [survival_dark3, 11.06, "C"], [survival4, 14.29, "C"]], "Axi")

#defining prime parts and their primes together. they'll be done in order: frames, primaries, secondaries, melee, companions, sentinel weapons, and archwings.
#primes will be removed from the code when they are vaulted
#the word prime is dropped from the variable names because they are implied to be prime.
#prime parts are defined with an array of arrays, the child array holding both the relic instance and commonality within that relic
#primes get appended to arrays during intialization


#Warframes
banshee_blueprint = Prime_part([neoH1], "blueprint")
banshee_neuroptics = Prime_part([neoS7], "neuroptics")
banshee_chassis = Prime_part([neoB2], "chassis")
banshee_systems = Prime_part([axiB2], "systems")
banshee = Prime([banshee_blueprint, banshee_neuroptics, banshee_chassis, banshee_systems], "banshee", "frame")

hydroid_blueprint = Prime_part([mesoN5], "blueprint")
hydroid_neuroptics = Prime_part([axiA3], "neuroptics")
hydroid_chassis = Prime_part([mesoH1], "chassis")
hydroid_systems = Prime_part([neoH1], "systems")
hydroid = Prime([hydroid_blueprint, hydroid_neuroptics, hydroid_chassis, hydroid_systems], "hydroid", "frame")

mirage_blueprint = Prime_part([neoM1], "blueprint")
mirage_neuroptics = Prime_part([mesoH1], "neuroptics")
mirage_chassis = Prime_part([lithS7], "chassis")
mirage_systems = Prime_part([neoV6], "systems")
mirage = Prime([mirage_blueprint, mirage_neuroptics, mirage_chassis, mirage_systems], "mirage", "frame")

nekros_blueprint = Prime_part([lithN3], "blueprint")
nekros_neuroptics = Prime_part([axiN5], "neuroptics")
nekros_chassis = Prime_part([mesoK1], "chassis")
nekros_systems = Prime_part([mesoN5], "systems")
nekros = Prime([nekros_blueprint, nekros_neuroptics, nekros_chassis, nekros_systems], "nekros", "frame")

oberon_blueprint = Prime_part([mesoH1], "blueprint")
oberon_neuroptics = Prime_part([mesoO1], "neuroptics")
oberon_chassis = Prime_part([axiN5], "chassis")
oberon_systems = Prime_part([axiO1], "systems")
oberon = Prime([oberon_blueprint, oberon_neuroptics, oberon_chassis, oberon_systems], "oberon", "frame")

valkyr_blueprint = Prime_part([lithA2, lithN3, axiV7], "blueprint")
valkyr_neuroptics = Prime_part([lithT1], "neuroptics")
valkyr_chassis = Prime_part([axiV6], "chassis")
valkyr_systems = Prime_part([lithV3], "systems")
valkyr = Prime([valkyr_blueprint, valkyr_neuroptics, valkyr_chassis, valkyr_systems], "valkyr", "frame")

vauban_blueprint = Prime_part([neoV2], "blueprint")
vauban_neuroptics = Prime_part([neoV5], "neuroptics")
vauban_chassis = Prime_part([neoV6], "chassis")
vauban_systems = Prime_part([lithV2], "systems")
vauban = Prime([vauban_blueprint, vauban_neuroptics, vauban_chassis, vauban_systems], "vauban", "frame")


#Primary weapons
braton_blueprint = Prime_part([lithN3, lithV3, axiV6], "blueprint")
braton_barrel = Prime_part([mesoG1, axiA3], "barrel")
braton_receiver = Prime_part([lithB2], "receiver")
braton_stock = Prime_part([mesoN5, neoB2, neoV2, axiE2], "stock")
braton = Prime([braton_blueprint, braton_barrel, braton_receiver, braton_stock], "braton", "primary")

burston_blueprint = Prime_part([lithT1], "blueprint")
burston_barrel = Prime_part([neoV5], "barrel")
burston_receiver = Prime_part([lithN3, neoH1], "receiver")
burston_stock = Prime_part([neoV6], "stock")
burston = Prime([burston_blueprint, burston_barrel, burston_receiver, burston_stock], "burston", "primary")

cernos_blueprint = Prime_part([lithA2], "blueprint")
cernos_lower = Prime_part([lithC2], "lower limb")
cernos_upper = Prime_part([lithV3, mesoK1], "upper limb")
cernos_grip = Prime_part([neoV6], "grip")
cernos_string = Prime_part([mesoO1, axiA3], "string")
cernos = Prime([cernos_blueprint, cernos_lower, cernos_upper, cernos_grip, cernos_string], "cernos", "primary")

paris_blueprint = Prime_part([axiE2, axiO1, mesoH1], "blueprint")
paris_lower = Prime_part([lithB2, lithV2, lithV3, mesoO1], "lower limb")
paris_upper = Prime_part([lithV2, lithC2], "upper limb")
paris_grip = Prime_part([lithS7], "grip")
paris_string = Prime_part([neoV5, neoM1], "string")
paris = Prime([paris_blueprint, paris_lower, paris_upper, paris_grip, paris_string], "paris", "primary")

sybaris_blueprint = Prime_part([axiB2], "blueprint")
sybaris_barrel = Prime_part([lithS7], "barrel")
sybaris_receiver = Prime_part([neoS7], "receiver")
sybaris_stock = Prime_part([lithN3], "stock")
sybaris = Prime([sybaris_blueprint, sybaris_barrel, sybaris_receiver, sybaris_stock], "sybaris", "primary")

tigris_blueprint = Prime_part([lithT1], "blueprint")
tigris_barrel = Prime_part([lithV3, neoH1], "barrel")
tigris_receiver = Prime_part([mesoN5, mesoK1], "receiver")
tigris_stock = Prime_part([lithB2, neoB2], "stock")
tigris = Prime([tigris_blueprint, tigris_barrel, tigris_receiver, tigris_stock], "tigris", "primary")


#Secondary weapons (akbronco is defined right after its singular counterparts instead of in alphabetical order)
akbolto_blueprint = Prime_part([neoM1], "blueprint")
akbolto_barrel = Prime_part([lithC2], "barrel")
akbolto_receiver = Prime_part([axiA3], "receiver")
akbolto_link = Prime_part([lithS7], "link")
akboloto = Prime([akbolto_blueprint, akbolto_barrel, akbolto_receiver, akbolto_link], "akbolto", "secondary")


akstiletto_blueprint = Prime_part([lithA2], "blueprint")
akstiletto_barrel = Prime_part([mesoK1], "barrel")
akstiletto_receiver = Prime_part([axiO1], "receiver")
akstiletto_link = Prime_part([mesoO1], "link")
akstiletto = Prime([akstiletto_blueprint, akstiletto_barrel, akstiletto_receiver, akstiletto_link], "akstiletto", "secondary")

ballistica_blueprint = Prime_part([lithB2], "blueprint")
ballistica_lower = Prime_part([axiV6], "lower limb")
ballistica_upper = Prime_part([lithT1], "upper limb")
ballistica_string = Prime_part([mesoG1], "string")
ballistica_receiver = Prime_part([neoS7], "receiver")
ballistica = Prime([ballistica_blueprint, ballistica_lower, ballistica_upper, ballistica_string, ballistica_receiver], "ballistica", "secondary")

bronco_blueprint = Prime_part([neoM1], "blueprint")
bronco_barrel = Prime_part([axiE2], "barrel")
bronco_receiver = Prime_part([lithC2], "receiver")
bronco = Prime([bronco_blueprint, bronco_barrel, bronco_receiver], "bronco", "secondary")

akbronco_blueprint = Prime_part([lithT1, mesoO1], "blueprint")
akbronco_link = Prime_part([lithA2], "link")
akbronco = Prime([bronco, akbronco_blueprint, akbronco_link], "akbronco", "secondary")

euphona_blueprint = Prime_part([axiN5, axiO1], "blueprint")
euphona_barrel = Prime_part([neoM1], "barrel")
euphona_receiver = Prime_part([axiE2], "receiver")
euphona = Prime([euphona_blueprint, euphona_barrel, euphona_receiver], "euphona", "secondary")

lex_blueprint = Prime_part([lithS7], "blueprint")
lex_barrel = Prime_part([lithA2, lithV2, axiN5, axiV7], "barrel")
lex_receiver = Prime_part([mesoN5, axiE2], "receiver")
lex = Prime([lex_blueprint, lex_barrel, lex_receiver], "lex", "secondary")


#Melee weapons
fang_blueprint = Prime_part([lithV2, neoB2], "blueprint")
fang_blade = Prime_part([neoS7, axiB2], "blade")
fang_handle = Prime_part([neoV2, axiV6], "handle")
fang = Prime([fang_blueprint, fang_blade, fang_handle], "fang", "melee")

fragor_blueprint = Prime_part([mesoH1], "blueprint")
fragor_head = Prime_part([neoH1, axiB2], "head")
fragor_handle = Prime_part([neoV6], "handle")
fragor = Prime([fragor_blueprint, fragor_head, fragor_handle], "fragor", "melee")

galatine_blueprint = Prime_part([mesoG1], "blueprint")
galatine_blade = Prime_part([neoV2, lithS7], "blade")
galatine_handle = Prime_part([neoV2, neoV2, axiV6], "handle")
galatine = Prime([galatine_blueprint, galatine_blade, galatine_handle], "galatine", "melee")

kogake_blueprint = Prime_part([axiV7], "blueprint")
kogake_gauntlet = Prime_part([mesoK1], "gauntlet")
kogake_boot = Prime_part([axiA3], "boot")
kogake = Prime([kogake_blueprint, kogake_gauntlet, kogake_boot], "kogake", "melee")

nami_skyla_blueprint = Prime_part([axiV7], "blueprint")
nami_skyla_blade = Prime_part([axiN5], "blade")
nami_skyla_handle = Prime_part([lithC2], "handle")
nami_skyla = Prime([nami_skyla_blueprint, nami_skyla_blade, nami_skyla_handle], "nami skyla", "melee")

orthos_blueprint = Prime_part([axiB2], "blueprint")
orthos_blade = Prime_part([lithB2], "blade")
orthos_handle = Prime_part([neoH1, mesoK1], "handle")
orthos = Prime([orthos_blueprint, orthos_blade, orthos_handle], "orthos", "melee")

silva_aegis_blueprint = Prime_part([axiV7], "blueprint")
silva_aegis_blade = Prime_part([mesoG1], "blade")
silva_aegis_guard = Prime_part([neoS7], "guard")
silva_aegis_hilt = Prime_part([neoV5], "hilt")
silva_aegis = Prime([silva_aegis_blueprint, silva_aegis_blade, silva_aegis_guard, silva_aegis_hilt], "silva and aegis", "melee")

venka_blueprint = Prime_part([neoB2], "blueprint")
venka_blade = Prime_part([lithC2, mesoG1], "blade")
venka_gauntlet = Prime_part([axiV7], "gauntlet")
venka = Prime([venka_blueprint, venka_blade, venka_gauntlet], "venka", "melee")


#Companions
#primed sentinel weapons come automatically with primed sentinels
helios_blueprint = Prime_part([neoM1], "blueprint")
helios_cerebrum = Prime_part([mesoH1], "cerebrum")
helios_carapace = Prime_part([neoS7, neoV5, axiA3], "carapace")
helios_systems = Prime_part([lithV3, axiN5], "systems")
helios = Prime([helios_blueprint, helios_cerebrum, helios_carapace, helios_systems], "helios", "sentinel")

#Archwings
#there are currently no unvaulted archwings


'''
This is the end of data entry, the code following this is what actually executes the program
'''

#welcoming statement
blank = raw_input("Welcome to the Warframe prime farming program, created by AvisTonitrui.  Here you'll be able to choose what primes you'd like to farm for, what parts you need for those primes, and what planets you have unlocked.  Once chosen you'll receive an optimized selection of nodes for you to go to to get the relics you'll need in as short a time as possible. (Press enter to continue)")
print ""

#shutdown begins as false so an error doesn't occur trying to call a non-existent variable
shutdown = False


#Menuing begins here, if shutdown is ever typed, program will immediately break through all loops and finish.
while True:
  print "Please select the number of the choice that you would like."
  print "1. Start prime finder"
  print "2. Look at list of currently unvaulted primes (not yet working)"
  print "3. Read FAQ"
  print "4. Read credits"
  print "5. Exit program"
  choice = raw_input("--->")
  print ""
  
  if choice == "1":#prime finder
    #intializing various variables for later use. these are the lists that are used for organization throughout the enitre process.
    requested = [] #the requested primes
    parts = [] #the requested prime parts in the form [Prime, Prime_Part]
    unlocked = [] #planets unlocked
    relics = [] #list by relic in the form of [Prime, Part, Relic]
    locations = [] # list by relic in the form of [Prime, Part, Relic, [type, chance, rotation]
    deletes = [] #array used for keeping track of indicies to delete
    missing = [] #any parts that are missing
    lith = [] #list for the lith relics
    meso = [] #list for the meso relics
    neo = [] #list for the neo relics
    axi = [] #list for the axi relics
    nodes = [] #list of the nodes where relics can be found
    location_nodes = [] #list by nodes with each nodes list of parts in the form [node, [prime, part, relic, chance, rotation], [prime, part, relic, chance, rotation], ...]
    size = 1 #starting size of combinations
    possible = [] #list of combinations that have all requested parts
    
    
    #looping continuosly until a blank input is given to get all the primes that person wants
    while True:
      
      #setting a few variables back to defaults for each iteration
      found = False
      included = False
      
      #taking in the request for the prime
      request = raw_input("What prime would you like to farm for (press enter when done): ")
      print ""
      
      #a blank input results in the continuation to the next step
      if request == "":
        print "Continuing on"
        print ""
        break
      
      #shutdown check
      if shutdown_check(request):
        shutdown = True
        break
      
      #looking to see if a prime has already been added to the list
      for prime in requested:
        if prime.name == request:
          included = True
          break
        else:
          included = False
      
      #if no repeat, then look to see if the input is valid
      if included == False:
        for prime in primes:
          
          
          #print "checking against " + prime.name
          if prime.name == request:
            found = True
            requested.append(prime)
            break
      
      #adding prime to list if it was found
      if found == True:
        print "Added " + request + " to your list."
        print ""
      
      #looping if prime is already on the list
      elif included == True:
        print request + " is already on your list."
        print ""
      
      #telling false input
      else:
        print "I couldn't find " + request + ".  Please try again."
        print ""
    
    #if no primes are added, breaks
    if len(requested) == 0:
      print "You didn't add any primes, returning you to the main menu."
      print ""
    
    else:
      #continuing on to asking for exactly what parts are needed
      for prime in requested:
        #looping through this continuosly until all parts needed are selected
        while True:
          #resetting certain values to defaults for the iteration
          broke = False
          found = False
          
          print "What parts do you need for " + prime.name + "(press enter when done)?"
          print ""
          print "Possible parts:"
          
          #resetting index value
          index = 0
          
          #listing off the parts for that prime
          for part in prime.parts:
            index += 1
            if index == len(prime.parts):
              print  part.name
            
            else:
              print part.name + ", ",
          
          print ""
          
          choice = raw_input("-->")
          print ""
          
          #checking for empty input, which will break the loop
          if choice == "":
            break
          
          #shutdown check
          if shutdown_check(choice):
            shutdown = True
            break
          
          #checking if input is a valid part
          for part in prime.parts:
            if choice == part.name:
              found = True
              
              #if the part is a prime itself, it will add the prime to requested list if it isn't already on there
              if part.built:
                append = True
                print "That part is a fully built prime, ",
                
                #checking if prime is already on the list
                for prime in requested:
                  if prime.name == choice:
                    included = True
                    break
                  
                  else:
                    included = False
                
                if included:
                  print "but that prime is already on your reqested list."
                  print ""
                
                else:
                  print "I'm adding that prime to your requested list.  You'll be able to choose the parts you need for that prime later."
                  print ""
                  requested.append(part)
              
              #checking if the part isn't already on the list, and appending if it isn't
              else:
                  #checks for repeats
                  for requested in parts:
                    
                    if requested[0].name == prime.name and part.name == requested[1].name:
                      print prime.name + " " + part.name + " is already in your requested list"
                      print ""
                      broke = True
                      break
                  
                  #appends if there wasn't a repeat
                  if broke:
                    pass
                  else:
                    print "Adding " + prime.name + " " + part.name + " to your list."
                    print ""
                    parts.append([prime, part])
              
              break
          
          #if input wasn't valid, tells user and loops
          if found:
            pass
          else:
            print prime.name + " " + choice + " is not a valid part"
            print ""
        
        #breaking for shutdown
        if shutdown:
          break
      
      #breaking for shutdown
      if shutdown:
        break
      
      #checks to make sure at least one part is requested, and then prints out all the requested parts to the user
      if len(parts) == 0:
        print "You didn't add any parts, returning you to the main menu."
        print ""
      
      else:
        
        #prints out all the parts requested
        print "These are the parts that you requested:",
        for part in parts:
          print part[0].name + " " + part[1].name + ", ",
        print ""
        print ""
        
        #asks for the planet, looping in case of an invalid input
        while True:
          #resetting values to defaults for this iteration
          index = 0
          found = False
          
          #asking for the planet
          unlock = raw_input("What is the furthest planet that you have unlocked: ")
          print ""
          
          #shutdown check
          if shutdown_check(unlock):
            shutdown = True
            break
          
          #checking for valid input, appending to the list of unlocked planets along the way
          for planet in planets:
            if planet.name == unlock:
              found = True
              unlocked.append(planet)
              break
            
            else:
              unlocked.append(planet)
          
          #prints the list of unlocked planets if input is valid, otherwise reloops
          if found:
            print "These are the planets you can get to their nodes: ",
            for planet in unlocked:
              print planet.name + ", ",
            print ""
            print ""
            break
          
          else:
            print unlock + " is not a valid input"
            print ""
            unlocked = []
        
        #breaking for shutdown
        if shutdown:
          break
        
        #now that we have the planets unlocked, we create an array of all the relics and their corresponding parts
        #iteration of requested parts
        for part in parts:
          #iteration of each parts relics, appending the relic to the relics array
          for relic in part[1].relics:
            relics.append([part[0], part[1], relic])
        
        #takes the relics array and breaks all of those relics down into their locations
        #iteration of all the relics and their corresponding parts
        for relic in relics:
          #iteration of the relics locations
          for location in relic[2].locations:
            locations.append([relic[0], relic[1], relic[2], location])
        
        #We now check through the locations to get the best node for each of them.  If one isn't found then it will store that locations index which will be deleted later
        #iterating through the locations array
        index = 0
        for location in locations:
          #iterating through the nodes, which are presorted by level
          for node in location[3][0].nodes:
            
            #checks if that node's planet is in the unlocked array
            if node.planet in unlocked:
              location.append(node)
              valid = True
              break
            else:
              valid = False
          
          if valid:
            pass
          else:
            deletes.insert(0, index)
          
          index += 1
        
        #goes through the deletions, which are in reverse index order, and removes those locations from the array
        for delete in deletes:
          del locations[delete]
        
        #goes through the parts array, making sure that everything is present in the locations array.  puts the parts missing into a missing array
        for part in parts:
          for location in locations:
            if location[0] == part[0] and location[1] == part[1]:
              found = True
              break
            else:
              found = False
            
          if not found:
            missing.append(part)
        
        #checks to see if parts are missing, and tells user result.
        if len(missing) == 0:
          print "You can access at least one relic for each part you requested."
          print ""
          choice = "y"
        
        else:
          print "You cannot access a relic for these parts: ",
          
          for part in missing:
            print part[0].name + " " + part[1].name + ", ",
          print ""
          
          #asks if user would like to continue without the parts
          choice = raw_input("Would you like to continue without these parts (y/n): ")
          print ""
        
        #defaults to no, also accepts a shutdown input
        if choice == 'y':
          #if they're continuing, continues on with the process.
          #first, organize the relics into different lists baqsed on era.
          for relic in locations:
            
            #multi-conditional statment for each relic era
            if relic[2].era == "Lith":
              lith.append(relic)
            
            elif relic[2].era == "Meso":
              meso.append(relic)
              
            elif relic[2].era == "Neo":
              neo.append(relic)
              
            elif relic[2].era == "Axi":
              axi.append(relic)
            
            else:
              print "Relic does not belong to an era, it's era is listed as " + relic[2].name
              print ""
          
          #once all relics have been added to the appropriate list, checks to see if a single era contains all relics.
          if era_check(lith, parts):
            #all parts are in lith relics
            deletes = delete(locations, "Lith")
            
            #goes through the deletions, which are in reverse index order, and removes those locations from the array
            for delete in deletes:
              del locations[delete]
          
          elif era_check(meso, parts):
            #all parts are in meso relics
            deletes = delete(locations, "Meso")
            
            #goes through the deletions, which are in reverse index order, and removes those locations from the array
            for delete in deletes:
              del locations[delete]
          
          elif era_check(neo, parts):
            #all parts are in neo relics
            deletes = delete(locations, "Neo")
            
            #goes through the deletions, which are in reverse index order, and removes those locations from the array
            for delete in deletes:
              del locations[delete]
            
          elif era_check(axi, parts):
            #all parts are in axi relics
            deletes = delete(locations, "Axi")
            
            #goes through the deletions, which are in reverse index order, and removes those locations from the array
            for delete in deletes:
              del locations[delete]
          
          #we can now take the current locations list and optimize it.
          #reorganizing the list so that it is by node and not by relic
          for location in locations:
            if check_node_match(location, nodes) == -1:
              nodes.append(location[4])
              location_nodes.append([location[4], [[location[0], location[1], location[2], location[3][1], location[3][2]]]])
            else:
              location_nodes[check_node_match(location, nodes)][1].append([location[0], location[1], location[2], location[3][1], location[3][2]])
          
          #now we begin to go through and assemble the list of posible node combinations to go to. size is capped at three and prioritizes less nodes.
          #variables needed for this step
          
          
          while size <= 4:
            index1 = 0
            index2 = 1
            index3 = 2
            found = False
            
            if size == 1:
              for node in location_nodes:
                if check_requested([node], parts):
                  found = True
                  possible.append([node])
            
            elif size == 2:
              for node in location_nodes:
                while index2 < len(nodes):
                  if check_requested([node, location_nodes[index2]], parts):
                    found = True
                    possible.append([node, location_nodes[index2]])
                  
                  index2 += 1
                
                index1 += 1
                index2 = index1 + 1
            
            elif size == 3:
              for node in location_nodes:
                while index2 < len(nodes):
                  while index3 < len(nodes):
                    if check_requested([node, location_nodes[index2], location_nodes[index3]], parts):
                      found= True
                      possible.append([node, location_nodes[index2], location_nodes[index3]])
                    
                    index3 += 1
                  
                  index2 += 1
                  index3 = index2 + 1
                
                index1 += 1
                index2 = index1 + 1
                index3 = index2 + 1
                
            else:
              print "The parts you have requsted require more than three nodes to reach all of them. Please refine your requested parts and try again."
              suggested = []
              break
            
            if found:
              #comparing the combinations to find the best one
              suggested = compare_possibles(possible, parts)
              break
            else:
              #increasing size to find a combination
              size += 1
          
          #with the suggested combination now given, we print out the information for the user to have
          print "Your suggested node(s): ",
          for node in possible[suggested[0]]:
            print node[0].name,
          
          print ""
          print "Go to rotation " + suggested[1]
          print ""
          blank =  raw_input("Press enter to return to the main menu")
          
          if shutdown_check(blank):
            shutdown = True
            break
          
          print ""
          print "Returning to main menu"
          print ""
          
          
        
        elif shutdown_check(choice):
          shutdown = True
          break
        
        else:
          print "returning to main menu"
          print ""
        
    
  elif choice == "2":#list unvaulted primes
    pass
    
  elif choice == "3":#FAQ
    blank =  raw_input("There are currently no frequently asked questions as this program is new. Please press enter to return to the main menu.")
    
  elif choice == "4":#credits
    blank = raw_input ("This program was made entirely by AvisTonitrui. Please Press enter to return to the main menu.")
  
  elif choice == "5":#shutdown
    print "Thank you for using the prime farming guide by AvisTonitrui"
    break
  
  elif shutdown_check(choice):
    break
  
  else:
    print "I'm sorry, I didn't recognize that input."
  
  if shutdown:
    break


'''
Update log:
Version 1.1 1/5/18:
  fixed neptuine nodes being initialized as uranus nodes.

Version 1.0 1/3/18:
  Updated database for mirage prime access
  noted not yet working listing of unvaulted primes
  woot! released.
  hotfix: wrongly input akbolto prime initialization.
  hotfix: fixed issue with inaccessible mission types not being deleted correctly.

Version 0.16 1/2/18:
  Time to see if I can finish this quickly, at least get it working anyways.
  Finished getting everything written, onto debugging
  Things appear to be working at the moment. The nodes will give all the relics needed, not 100% sure if the math is being done correctly. I will have to test for that after release.
  Beginning work on database update for mirage prime access and then this will be ready for release.

Version 0.15 1/1/18:
  A new year has come, and while I don't often make resolutions, the completion of this is going to be one.
  Nearly have the comparison function finished, just need a few final touches before this is ready to work, though drop tables are now out of date.

Version 0.14 12/31/17:
  Happy New Years Eve! Would love this to be a new years gift, but that probably won't happen at this rate, We'll see though.
  Got rid of the part explaining the process for now as it is difficult to easily explain in a non-graphical format.
  Fixed up the menuing a little bit and added the credits.

Version 0.13 12/19/17:
  program can now find any combination of nodes that has all requested parts, up to three in size.
  modified the matching node check function to be usable in more areas
  nevermind, won't work in a modified way anyways.

Version 0.12 12/18/17:
  Wow!, it has been quite a long time since I was last here. I am so sorry to all of you.  In the time that I was gone, it appears that repl.it has changed their format, so I can no longer give links to older versions.
  I know that mirage prime access has messed with my data. I will not fix the database though until I am done with the program.  Anyone who wants to come test, please use relics as of hydroid prime access until fixed.
  When I update the database, I will also be moving it to a separate file and make this a project instead of a file.
  Got the list reassembled to be by node now instead of by relic
  More commenting so I don't forget how things are formatted later down the road
  Made a function to check if a node combination has all the parts requested
  began work on the final optimizations, only a couple steps left.

Version 0.11 10/2/2017:
  As badly as I hoped to get this done soon, I'm am likely going to be a little while now, seeing as I can only get in about 20 lines of code a day.
  While there is no actual programming in this update, I'm putting this here because I need to figure out the math first, then I'll psuedo-code it and finally put it into this program.  Because I have a little bit more regular access to pen and paper than a PC, I should be able to work a little bit faster during this part. No promises though.

Version 0.10 9/29/17:
  I am so behind schedule right now.  Again, I apologize, but when you're a lead in a musical you don't get much free time.
  Now checks to see if all relics are in a single era to simplify optimization process

Version 0.9 9/26/17:
  Yes, I know I'm behind schedule.  Trying to work but school is keeping me busy.  I am working on this as much as I can, though.
  got to the point in the process where we check to make sure all parts are accessible based on planet.

Version 0.8 9/24/17:
  began work on the process itself
  reworked shutdown process to be more streamlined
  made it so primes were added to arrays so that they are accessed easier
  added planets to a list, and then sort said list by unlock number
  got the process to the point where all the valid locations are chosen, still need to go through optimizations.

Version 0.7 9/23/17:
  haven't been able to work much, had a crash losing me progress and life is keeping me busy.  Progress will still come, but at a little slower of a pace.
  added names to primes and their parts
  had relics pre-sort their nodes for easier use later down the road

Version 0.6 9/20/17:
  continued to work on the proces

Version 0.5 9/19/2017:
  Added eras to relics to simplify optimization process, as eras share very similar drop tables
  continued work on the process

Version 0.4: 9/18/2017:
  removed the rarities from prime part relic drops, seeing as so few would have differences across the rarities they occur.  It may get added in for better optimization later, but it is not worth the effort while trying to get the program to work.
  FAQ is left as empty until people stat asking questions about the program
  began work on spelling out the tire process for the program

Version 0.3 9/17/2017:
  began work on menu:
    nothing currently put into the FAQ
    started work on writing out the entire process both for others to know and for my own reference

Version 0.2 9/16/2017:
  finished commenting out the nodes that don't have relic drops
  defined all of the locations
  defined all relics
  defined all primes and their respective parts
  intial data entry complete, though it is possible I'll need to do another round if I need more information

Version 0.1 9/15/2017:
  set up classes for the primes and their requirements
  defined all the planets
  defined all nodes
  began to comment out nodes for mission types that don't drop relics
'''
