# TO DO LIST:
# overlap of car and parking spot for more points
# make more complex with hidden layer

from graphics import *
import time
import math
import keyboard
import random
import csv

starttime = time.time()
bots = 30
rounds = 5 #
variety = 0.1
runs = 50
database = 3
for run in range (0, runs):
     if False:
          genre = "random"
     elif run % 3 == 0:
          genre = "redo"
     else:
          genre = "best"

     screenwidth = 600
     screenheight = 600
     canvas = GraphWin("canvas", screenwidth, screenheight, autoflush = False)
     canvas.setBackground (color_rgb(255, 255, 255))
     canvas.setCoords(-(screenwidth/2),-(screenheight/2),(screenwidth/2),(screenheight/2))

     def makename():
          namelist = open ("surnames.csv", "rt", newline = "")
          data = csv.reader (namelist, delimiter=',')
          for row in data:
               if random.randint(1,2) == 1:
                    prefix = "Mr"
               elif random.randint(1,2) == 1:
                    prefix = "Mrs"
               elif random.randint(1,3) == 1:
                    prefix = "Miss"
               elif random.randint(1,3) == 1:
                    prefix = "Sir"
               elif random.randint(1,3) == 1:
                    prefix = "Lady"
               elif random.randint(1,3) == 1:
                    prefix = "Master"
               else:
                    prefix = "Lord"
          return str(prefix+" "+ (row[random.randint(0,2154)]).title())

     def intersect(x1, x2, x3, x4, y1, y2, y3, y4):
          global px3
          global py3
          px1 = (((x1*y2) - (y1*x2)) * (x3-x4)) - ((x1-x2) * ((x3*y4) - (y3*x4)))
          px2 = ((x1-x2) * (y3-y4)) - ((y1-y2) * (x3-x4))
          if px2 == 0:
               px2 = 0.000001
          px3 = px1/px2

          py1 = (((x1*y2) - (y1*x2)) * (y3-y4)) - ((y1-y2) * ((x3*y4) - (y3*x4)))
          py2 = ((x1-x2) * (y3-y4)) - ((y1-y2) * (x3-x4))
          if py2 == 0:
               py2 = 0.000001
          py3 = py1/py2

     def sense(who):
          #(math.sqrt((hyp**2)/2))

          sensors[4] = math.sqrt((goalx-carx[who])**2 + (goaly-cary[who])**2)
          sensors[5] = (cara[who] - 45 - (math.degrees(math.atan2((goaly - cary[who]),(goalx - carx[who])))))%360
          if sensors[5] > 180:
               sensors[5] = sensors[5] - 360

          for e in range (0, 4):
               if e == 0:
                    owl = -90
                    red = -hyp
               if e == 1:
                    owl = -45
                    red = -(math.sqrt((hyp**2)/2))
               if e ==2:
                    owl = 0
                    red = -hyp
               if e == 3:
                    owl = 135
                    red = -(math.sqrt((hyp**2)/2))

               x1 = carx[who]
               x2 = carx[who] + math.cos(math.radians(cara[who]+owl)) * hyp
               y1 = cary[who]
               y2 = cary[who] + math.sin(math.radians(cara[who]+owl)) * hyp

               # top or bottom
               x3 = -1
               x4 = 1
               if ((cara[who]+owl)%360) < 180:
                    y3 = (screenheight/2)
                    y4 = (screenheight/2)
               else:
                    y3 = -(screenheight/2)
                    y4 = -(screenheight/2)
               intersect(x1, x2, x3, x4, y1, y2, y3, y4)
               distance = red + (math.sqrt(((carx[who]-px3)**2) + ((cary[who]-py3)**2)))
               if distance < 0:
                    distance = 0
               if distance < sensors[e]:
                    sensors[e] = distance

               # left or right
               y3 = -1
               y4 = 1
               if ((cara[who]+owl+90)%360) < 180:
                    x3 = (screenwidth/2)
                    x4 = (screenwidth/2)
               else:
                    x3 = -(screenwidth/2)
                    x4 = -(screenwidth/2)
               intersect(x1, x2, x3, x4, y1, y2, y3, y4)
               distance = red + (math.sqrt(((carx[who]-px3)**2) + ((cary[who]-py3)**2)))
               if distance < 0:
                    distance = 0
               if distance < sensors[e]:
                    sensors[e] = distance
                    
               # obstacles
               for o in range (0, obstacles):
                    for i in range (0, 4):
                         x3 = ox[(4*o)+(i%4)]
                         x4 = ox[(4*o)+((i+1)%4)]
                         y3 = oy[(4*o)+(i%4)]
                         y4 = oy[(4*o)+((i+1)%4)]
                         intersect(x1, x2, x3, x4, y1, y2, y3, y4)
                         # needs to check if the point is between the max possible xy and the min possible xy
                         # next needs to check that it isn't looking backwards
                         legit = False
                         if ((px3 <= x3 and px3 >= x4) or (px3 <= x4 and px3 >= x3)) and ((py3 <= y3 and py3 >= y4) or (py3 <= y4 and py3 >= y3)):
                              legit = True
                         if ((px3 - (carx[who] + math.cos(math.radians(cara[who]+owl+90))))*((cary[who] + math.sin(math.radians(cara[who]+owl-90))) - (cary[who] + math.sin(math.radians(cara[who]+owl+90))))) - ((py3 - (cary[who] + math.sin(math.radians(cara[who]+owl+90))))*((carx[who] + math.cos(math.radians(cara[who]+owl-90))) - (carx[who] + math.cos(math.radians(cara[who]+owl+90))))) > 0:
                              legit = False
                         distance = red + (math.sqrt(((carx[who]-px3)**2) + ((cary[who]-py3)**2)))
                         if distance < 0:
                              distance = 0
                         if distance < sensors[e] and legit == True:
                              sensors[e] = distance
          for i in range (0,5):
               sensors[i] = sensors[i] / 500
          sensors[5] = sensors[5]/100

     def crashed(crashs, who):
          global speed
          global crash
          global score

          speed[who] = crashs*-0.1
          carx[who] = carx[who] + math.cos(math.radians(cara[who]-45)) * -crashs
          cary[who] = cary[who] + math.sin(math.radians(cara[who]-45)) * -crashs

          if crash == 1:
               score[who] = score[who] - (crashs ** 2)*10
          if crash == 2:
               score[who] = score[who] - (crashs ** 2)*10
          if crash == 3:
               score[who] = score[who] - (crashs ** 2)*10

     def draw(genre):
          global timeleft
          global runs
          global obstacles
          global rounds
          global carx
          global cary
          global cara
          global goalx
          global goaly
          global goala
          global w
          global a
          global s
          global d
          global r
          
          for i in range (0, obstacles):
               obstacle = Polygon(Point(ox[(4*i)], oy[(4*i)]), Point(ox[(4*i)+1], oy[(4*i)+1]), Point(ox[(4*i)+2], oy[(4*i)+2]), Point(ox[(4*i)+3], oy[(4*i)+3]))
               obstacle.draw(canvas)
          for i in range (0, bots):
               car = Polygon (Point(carx[i]+(hyp*math.cos(math.radians(cara[i]))),(cary[i]+(hyp*math.sin(math.radians(cara[i]))))), Point(carx[i]+(hyp*math.cos(math.radians(cara[i]+90))),(cary[i]+(hyp*math.sin(math.radians(cara[i]+90))))), Point(carx[i]+(hyp*math.cos(math.radians(cara[i]+180))),(cary[i]+(hyp*math.sin(math.radians(cara[i]+180))))), Point(carx[i]+(hyp*(math.cos(math.radians(cara[i]+270)))),(cary[i]+(hyp*(math.sin(math.radians(cara[i]+270)))))))
               car.setFill(color_rgb(0,round(i*(250/bots)),0))
               car.draw(canvas)
          goal = Polygon (Point(goalx+(hyp*math.cos(math.radians(goala))),(goaly+(hyp*math.sin(math.radians(goala))))), Point(goalx+(hyp*math.cos(math.radians(goala+90))),(goaly+(hyp*math.sin(math.radians(goala+90))))), Point(goalx+(hyp*math.cos(math.radians(goala+180))),(goaly+(hyp*math.sin(math.radians(goala+180))))), Point(goalx+(hyp*(math.cos(math.radians(goala+270)))),(goaly+(hyp*(math.sin(math.radians(goala+270)))))))
          goal.setOutline(color_rgb(150,0, 0))
          goal.setWidth(3)
          goal.draw(canvas)
          timer = Text(Point(round(screenwidth/2)-30 , round(screenheight/2)-20), str(count))
          timer.draw(canvas)
          Round = Text(Point(round(screenwidth/2)-30 , round(screenheight/2)-40), (str(obstacles+1), "/", str(rounds)))
          Round.draw(canvas)
          Runs = Text(Point(round(screenwidth/2)-30 , round(screenheight/2)-60), (str(run+1), "/", (runs)))
          Runs.draw(canvas)
          points =  Text(Point(0 , round(screenheight/2)-20), str(round(sum(score) / len(score))))
          points.draw(canvas)
          Time = Text(Point(round(screenwidth/2)-40 , round(screenheight/-2)+20), timeleft)
          Time.draw(canvas)
          tYpe = Text(Point(round(screenwidth/-2)+40 , round(screenheight/-2)+20), genre)
          tYpe.draw(canvas)
          loc = Text(Point(round(screenwidth/-2)+50 , round(screenheight/-2)+40), ("database"+str(database)))
          loc.draw(canvas)
          keyw = Rectangle(Point ((round(screenwidth/-2)+40),(round(screenheight/2)-40)), Point((round(screenwidth/-2)+60), (round(screenheight/2)-20)))
          keys = Rectangle(Point ((round(screenwidth/-2)+40),(round(screenheight/2)-60)), Point((round(screenwidth/-2)+60), (round(screenheight/2)-40)))
          keyr = Rectangle(Point ((round(screenwidth/-2)+70),(round(screenheight/2)-30)), Point((round(screenwidth/-2)+90), (round(screenheight/2)-10)))
          keya = Rectangle(Point ((round(screenwidth/-2)+20),(round(screenheight/2)-60)), Point((round(screenwidth/-2)+40), (round(screenheight/2)-40)))
          keyd = Rectangle(Point ((round(screenwidth/-2)+60),(round(screenheight/2)-60)), Point((round(screenwidth/-2)+80), (round(screenheight/2)-40)))
          if w == True:
               keyw.setFill(color_rgb(0,0,0))
          if s == True:
               keys.setFill(color_rgb(0,0,0))
          if r == True:
               keyr.setFill(color_rgb(0,0,0))
          if a == True:
               keya.setFill(color_rgb(0,0,0))
          if d == True:
               keyd.setFill(color_rgb(0,0,0))
          keyw.draw(canvas)
          keys.draw(canvas)
          keyr.draw(canvas)
          keya.draw(canvas)
          keyd.draw(canvas)
          canvas.update()
          for item in canvas.items[:]:
               item.undraw()

     def makebots(genre, randomness):
          if genre == "best" or genre == "redo":
               file = open ("database"+str(database)+".csv", "rt", newline = "")
               data = [row for row in csv.reader(file)]
               List = []
               bestno = []
               for i in range (0, len(data)):
                    List.append(float(data[i][1]))
               for i in range (0, len(data)):
                    bestnos.append(List.index(max(List)))
                    List[List.index(max(List))] = 0
               file.close()
                    
          for o in range (0, bots):
               wone = []
               bone = []
               wtwo = []
               btwo = []
               wthree = []
               bthree = []
               
               if genre == "random":
                    for i in range (0, 60):
                         wone.append (random.uniform(-1,1))
                    for i in range (0,10):
                         bone.append (random.uniform(-1,1))
                    for i in range (0, 100):
                         wtwo.append (random.uniform(-1,1))
                    for i in range (0,10):
                         btwo.append (random.uniform(-1,1))
                    for i in range (0,50):
                         wthree.append (random.uniform(-1,1))
                    for i in range (0,5):
                         bthree.append (random.uniform(-1,1))
                    

               if genre == "best":
                    file = open ("database"+str(database)+".csv", "rt", newline = "")
                    data = [row for row in csv.reader(file)]
                    file.close()
                    how = random.randint (0, round(len(data) / 20))
                    for i in range (0, 60):
                         stored = (data[bestnos[how]][2])
                         stored = (stored.strip("][").split(", "))
                         wone.append (float(stored[i])+random.uniform(-randomness,randomness))
                    for i in range (0,10):
                         stored = (data[bestnos[how]][3])
                         stored = (stored.strip("][").split(", "))
                         bone.append (float(stored[i])+random.uniform(-randomness,randomness))
                    for i in range (0,100):
                         stored = (data[bestnos[how]][4])
                         stored = (stored.strip("][").split(", "))
                         wtwo.append (float(stored[i])+random.uniform(-randomness,randomness))
                    for i in range (0,10):
                         stored = (data[bestnos[how]][5])
                         stored = (stored.strip("][").split(", "))
                         btwo.append (float(stored[i])+random.uniform(-randomness,randomness))
                    for i in range (0,50):
                         stored = (data[bestnos[how]][6])
                         stored = (stored.strip("][").split(", "))
                         wthree.append (float(stored[i])+random.uniform(-randomness,randomness))
                    for i in range (0,5):
                         stored = (data[bestnos[how]][7])
                         stored = (stored.strip("][").split(", "))
                         bthree.append (float(stored[i])+random.uniform(-randomness,randomness))

               if genre == "redo":
                    file = open ("database"+str(database)+".csv", "rt", newline = "")
                    data = [row for row in csv.reader(file)]
                    file.close()
                    for i in range (0, 60):
                         stored = (data[bestnos[o]][2])
                         stored = (stored.strip("][").split(", "))
                         wone.append (float(stored[i])+random.uniform(-randomness,randomness))
                    for i in range (0,10):
                         stored = (data[bestnos[o]][3])
                         stored = (stored.strip("][").split(", "))
                         bone.append (float(stored[i])+random.uniform(-randomness,randomness))
                    for i in range (0,100):
                         stored = (data[bestnos[o]][4])
                         stored = (stored.strip("][").split(", "))
                         wtwo.append (float(stored[i])+random.uniform(-randomness,randomness))
                    for i in range (0,10):
                         stored = (data[bestnos[o]][5])
                         stored = (stored.strip("][").split(", "))
                         btwo.append (float(stored[i])+random.uniform(-randomness,randomness))
                    for i in range (0,50):
                         stored = (data[bestnos[o]][6])
                         stored = (stored.strip("][").split(", "))
                         wthree.append (float(stored[i])+random.uniform(-randomness,randomness))
                    for i in range (0,5):
                         stored = (data[bestnos[o]][7])
                         stored = (stored.strip("][").split(", "))
                         bthree.append (float(stored[i])+random.uniform(-randomness,randomness))

               wsone.append (wone)
               bsone.append (bone)
               wstwo.append (wtwo)
               bstwo.append (btwo)
               wsthree.append (wthree)
               bsthree.append (bthree)


     def sigmoid(value):
          e = 2.718
          return (1-(1 / (1 + e**(-value))))*2

     def botchoose(who):
          global w
          global a
          global s
          global d
          global r

          wone = wsone[who]
          bone = bsone[who]
          wtwo = wstwo[who]
          btwo = bstwo[who]
          wthree = wsthree[who]
          bthree = bsthree[who]
          hone = []
          htwo = []
          
          w = bthree[0]
          s = bthree[1]
          r = bthree[2]
          a = bthree[3]
          d = bthree[4]

          for i in range (0, 10):
              hone.append(bone[i])
              htwo.append(btwo[i])

          for i in range (0, 6):
               for o in range (0, 10):
                    hone[o] = hone[o] + (sensors[i] * wone[o+(i*10)])
          for i in range (0,10):
               hone[i] = sigmoid(hone[i])

          for i in range (0, 10):
               for o in range (0, 10):
                    htwo[o] = htwo[o] + (hone[i] * wtwo[o+(i*10)])
          for i in range (0,10):
               htwo[i] = sigmoid(htwo[i])
               
          for i in range (0, 10):
               w = w+ (htwo[i] * wthree[i])
               s = s+ (htwo[i] * wthree[i+5])
               r = r+ (htwo[i] * wthree[i+10])
               a = a+ (htwo[i] * wthree[i+15])
               d = d+ (htwo[i] * wthree[i+20])

          w = sigmoid(w)
          s = sigmoid(s)
          r = sigmoid(r)
          a = sigmoid(a)
          d = sigmoid(d)

          if w > 0.5:
               w = True
          if s > 0.5:
               s = True
          if r > 0.5:
               r =True
          if a > 0.5 and d < 0.5:
               a = True
          if d > 0.5 and a < 0.5:
               d = True
          

     def humanchoose():
          global w
          global a
          global s
          global d
          global r

          w = False
          s = False
          r = False
          a = False
          d = False
          if keyboard.is_pressed("w"):
               w = True
          if keyboard.is_pressed("s"):
               s = True
          if keyboard.is_pressed("r"):
               r = True
          if keyboard.is_pressed("a") and not keyboard.is_pressed("d"):
               a = True
          if keyboard.is_pressed("d") and not keyboard.is_pressed("a"):
               d = True

     def confirm(who):
          global w
          global a
          global s
          global d
          global r
          global accelleration
          global sensitivity
          
          if w == True:
               speed[who] = speed[who] + acceleration
          if s == True:
               speed[who] = speed[who]*(1-(2.5*acceleration))
          if r == True:
               speed[who] = speed[who] - acceleration*0.5
          if a == True:
               cara[who] = cara[who] + speed[who] * sensitivity
          if d == True:
               cara[who] = cara[who] - speed[who] * sensitivity
          speed[who] = speed[who] * (1-(acceleration/ 4))
          carx[who] = carx[who] + math.cos(math.radians(cara[who]-45)) * speed[who]
          cary[who] = cary[who] + math.sin(math.radians(cara[who]-45)) * speed[who]

     def check(who):
          global crash
          global crashspeed

          # if it touches screen edges
          x1 = (carx[who]+(hyp*math.cos(math.radians(cara[who]))))
          x2 = (carx[who]+(hyp*math.cos(math.radians(cara[who]+90))))
          x3 = (carx[who]+(hyp*math.cos(math.radians(cara[who]+180))))
          x4 = (carx[who]+(hyp*math.cos(math.radians(cara[who]+270))))
          y1 = (cary[who]+(hyp*math.sin(math.radians(cara[who]))))
          y2 = (cary[who]+(hyp*math.sin(math.radians(cara[who]+90))))
          y3 = (cary[who]+(hyp*math.sin(math.radians(cara[who]+180))))
          y4 = (cary[who]+(hyp*math.sin(math.radians(cara[who]+270))))
          
          if x1 < (screenwidth/-2) or x2 < (screenwidth/-2) or x3 < (screenwidth/-2) or x4 < (screenwidth/-2) or x1 > (screenwidth/2) or x2 > (screenwidth/2) or x3 > (screenwidth/2) or x4 > (screenwidth/2):
               crash = 3
               crashspeed = speed[who]
          elif y1 < (screenheight/-2) or y2 < (screenheight/-2) or y3 < (screenheight/-2) or y4 < (screenheight/-2) or y1 > (screenheight/2) or y2 > (screenheight/2) or y3 > (screenheight/2) or y4 > (screenheight/2):
               crash = 3
               crashspeed = speed[who]
          for o in range (0, len(ox)):
                    
               if (math.sqrt((ox[o]-carx[who])**2 + (oy[o]-cary[who])**2)) < hyp*1.5:
                     # if the detected corner is inside the car
                    x1 = (carx[who]+(hyp*math.cos(math.radians(cara[who]))))
                    x2 = (carx[who]+(hyp*math.cos(math.radians(cara[who]+90))))
                    x3 = (carx[who]+(hyp*math.cos(math.radians(cara[who]+180))))
                    x4 = (carx[who]+(hyp*math.cos(math.radians(cara[who]+270))))
                    y1 = (cary[who]+(hyp*math.sin(math.radians(cara[who]))))
                    y2 = (cary[who]+(hyp*math.sin(math.radians(cara[who]+90))))
                    y3 = (cary[who]+(hyp*math.sin(math.radians(cara[who]+180))))
                    y4 = (cary[who]+(hyp*math.sin(math.radians(cara[who]+270))))
                    
                    s1 = ((ox[o] - x1)*(y2 - y1)) - ((oy[o] - y1)*(x2 - x1)) # left side
                    s2 = ((ox[o] - x3)*(y4 - y3)) - ((oy[o] - y3)*(x4 - x3)) # right side
                    s3 = ((ox[o] - x2)*(y3 - y2)) - ((oy[o] - y2)*(x3 - x2)) # front side
                    s4 = ((ox[o] - x4)*(y1 - y4)) - ((oy[o] - y4)*(x1 - x4)) # back side
                    if s1 < 0 and s2 < 0 and s3 < 0 and s4 < 0:
                         crash = 1
                         crashspeed = speed[who]

                    # if any car corners are inside the obstacle
                    obno = math.trunc(o / 4)
                    for u in range (0, 4):
                         cornerx = (carx[who]+(hyp*math.cos(math.radians(cara[who] + (u*90)))))
                         cornery = (cary[who]+(hyp*math.sin(math.radians(cara[who] + (u*90)))))
                         
                         x1 = ox[4*obno]
                         x2 = ox[4*obno+1]
                         x3 = ox[4*obno+2]
                         x4 = ox[4*obno+3]
                         y1 = oy[4*obno]
                         y2 = oy[4*obno+1]
                         y3 = oy[4*obno+2]
                         y4 = oy[4*obno+3]

                         s1 = ((cornerx - x1)*(y2 - y1)) - ((cornery - y1)*(x2 - x1)) # left side       12
                         s2 = ((cornerx - x3)*(y4 - y3)) - ((cornery - y3)*(x4 - x3)) # right side     34
                         s3 = ((cornerx - x2)*(y3 - y2)) - ((cornery - y2)*(x3 - x2)) # front side     23
                         s4 = ((cornerx - x4)*(y1 - y4)) - ((cornery - y4)*(x1 - x4)) # back side      14

                         if s1 < 0 and s2 < 0 and s3 < 0 and s4 < 0:
                              crash = 2
                              crashspeed = speed[who]
                              
          if crash != False:
               crashed(crashspeed, who)

     def mark():
          for i in range(0, bots):
               moved = (math.sqrt((goalx-startx)**2 + (goaly-starty)**2)) - (math.sqrt((goalx-carx[i])**2 + (goaly-cary[i])**2))
               score[i] = (score[i]+moved)
               scores[i] = scores[i] + score[i]
               draw(genre)
          time.sleep (0.5)

     def record():
          if (len(bestnos)) > 0:
               file = open ("database"+str(database)+".csv", "rt", newline = "")
               data = [row for row in csv.reader(file)]
               for who in range (0, bots):
                    #print ((data[bestnos[who]][1]) , ">>>>", ((float(data[bestnos[who]][1])*3 + scores[who])/4))
                    data[bestnos[who]][1] = (float(data[bestnos[who]][1])*3 + scores[who])/4
               file.close()
               file = open ("database"+str(database)+".csv", "w", newline = "")
               scribe = csv.writer (file, delimiter=',')
               scribe.writerows(data)
               file.close()
          else:
               file = open ("database"+str(database)+".csv", "at", newline = "")
               data = csv.writer (file, delimiter=',')
               for who in range (0, bots):
                    data.writerow([makename(), scores[who], wsone[who], bsone[who], wstwo[who], bstwo[who], wsthree[who], bsthree[who]])
               file.close()

     scores = []
     bestnos = []
     wsone = []
     bsone = []
     wstwo = []
     bstwo = []
     wsthree = []
     bsthree = []
     hyp = 50
     timeleft = "?"
     bots = 15
     rounds = 5
     variety = 0.5
     makebots(genre, variety)
     for i in range (0, bots):
          scores.append (0)
     for obstacles in range (0, rounds):
          progress = ((run*rounds)+obstacles) / (runs*rounds)
          if progress > 0:
               timeleft = ((1-progress)/progress)*(time.time() - starttime)
               if timeleft > 60:
                    timeleft = str(round(timeleft / 60)), "mins"
               else:
                    timeleft = str(round(timeleft)), "seconds"
          w = False
          s = False
          r = False
          a = False
          d = False
          s1 = 0
          s2 = 0
          s3 = 0
          s4 = 0
          s5 = 0
          ox = []
          oy = []
          carx = []
          cary = []
          cara = []
          speed = []
          score = []
          startx= (random.randint (-round(screenwidth/3), round(screenwidth/3)))
          starty = (random.randint (-round(screenheight/3), round(screenheight/3)))
          starta = (random.randint(0, 359))
          for i in range (0, bots):
               carx.append (startx)
               cary.append (starty)
               cara.append (starta)
               speed.append (0)
               score.append (0)
          acceleration = 0.08
          sensitivity = 0.65
          count = 500

          okay = False
          while okay == False:
               okay = True
               goalx = random.randint (-round(screenwidth/2.5), round(screenwidth/2.5))
               goaly = random.randint (-round(screenheight/2.5), round(screenheight/2.5))
               goala = random.randint (0, 359)
               if (math.sqrt((goalx-startx)**2 + (goaly-starty)**2)) < hyp*3:
                    okay = False

          for i in range (0, obstacles):
               a = random.randint(0, 359)
               okay = False
               while okay == False:
                    okay = True
                    x = random.randint (-round(screenwidth/2), round(screenwidth/2))
                    y = random.randint (-round(screenheight/2), round(screenheight/2))
                    if (math.sqrt((x-startx)**2 + (y-starty)**2)) < hyp*2:
                         okay = False
                    if (math.sqrt((x-goalx)**2 + (y-goaly)**2)) < hyp*2:
                         okay = False
                    for o in range (0, len(ox)):
                         if (math.sqrt((ox[o]-x)**2 + (oy[o]-y)**2)) < hyp*1.25:
                              okay = False
               for e in range (0, 4):
                    ox.append (x+hyp*math.cos(math.radians(a+e*90)))
                    oy.append (y+hyp*math.sin(math.radians(a+e*90)))

                                   
          while count > 0:
               who = 0
               count = count - 1
               #time.sleep (0.01)
               draw(genre)
               while who < bots:
                    crash = False
                    sensors = [9999, 9999, 9999, 9999, 9999, 9999]
                    sense(who)
                    botchoose(who)
                    #humanchoose()
                    check(who)
                    confirm(who)
                    who = who + 1
          mark()

     
     record()
     canvas.close()
