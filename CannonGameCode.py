"""
Program name: The Cannon Game
Author: Bobby Craig
Date: December 10, 2014
"""

import math
import urllib.request as web
import time
import random

def windSpeed(zipCode):
    """ Finds the wind speed for a specific area
        Parameters:
           zipCode: the zip code of the desired wind speed (must be input as string)
        Return value: the wind speed, in meters/sec, of the specific zip code
    """
    try:
        with web.urlopen("http://www.wunderground.com/cgi-bin/findweather/getForecast?query="+zipCode) as html:
            while True:
                sourceCode = html.readline()
                sourceCode = str(sourceCode)
                if "Forecast | Weather Underground" in sourceCode: #in same line as city name
                    beginning = '<title>'
                    end = ' Conditions &amp'
                    cityName = sourceCode[sourceCode.find(beginning)+7:sourceCode.find(end)] #find value between beginning and end
                    print("\t",cityName)
                if "wind_speed" in sourceCode: #unique instance before line with wind speed
                    newline = html.readline() #skip line to get to what is needed
                    newline = str(newline)
                    beginning = '<span class="wx-value">'
                    end = '</span>'
                    speed = newline[(newline.find(beginning)+len(beginning)):newline.find(end)] #find value between beginning and end
                    print("\t The tailwind is blowing at",speed,"miles/hour or",float(speed)*0.44704,"meters/sec.\n")
                    print("--------------------------------\n")
                    return float(speed) * 0.44704 #wind value converted from mph to mps
                if "Oops! There's been an error." in sourceCode: #breaks loop to return error message
                    print("\t This is not a valid zip code.\n\t Wind speed set to 10 meters/second.")
                    return 10
    except BaseException:
        print("\tWind data not available.\n\tWind speed set to 10 meters/second.")
        return 10

def level(windspeed, Cd, gusting, obstacle, level):
    """ Does the basic running for individual levels
        Parameters:
           windspeed: the windspeed generated in the windSpeed function
           Cd: coefficient of drag, used for switch between drag and non-drag
           gusting: boolean value indicating if the level is a gusting level
           obtacle: boolean value indicating if the level is a obstacle level
           level: the level number
        Return value: returns the level score to add to game score
    """
    
    print("--------------------------------\n\nLevel",level,"\n\n--------------------------------\n")
    if level == 1:
        pointsPossible = 5
    elif level == 2:
        pointsPossible = 25
    elif level == 3:
        pointsPossible = 50
    elif level == 4:
        pointsPossible = 125
    else:
        pointsPossible = 250
    print("You have 5 tries to hit the platform.\n\nEach time you miss on this level,",int(pointsPossible / 5),\
          "point(s) will be subtracted from your total.")

    #reminders for certain levels
    if level > 1:
        print("\tRemember, you now have drag.")
    if level > 2:
        print("\t\tRemember, you will have a tailwind.")
    if level == 5:
        print("\t\t\tRemember to watch out for obstacles!\n\n*** This simulation will be slower due to decreased change in time in calculation. ***")

    attempts = 5 #initializes attempts
    score = pointsPossible
    distancelandzone = random.randrange(200, 600) #randomly generates distance to platform
    print("\nThe platform is",distancelandzone,"meters away and 15 meters long.\n")

    #more reminders for level 5
    if level == 5:
        print("********************************\n\nWatch out for the obstacle",int((distancelandzone / 2) + 50),\
              "meters away and 400 meters tall.\n\n********************************\n")
        
    if windspeed == True:
        zipCode = input("Please enter the zip code of your location you wish to simulate wind for: ")
        zipCode = str(zipCode)
        wind = windSpeed(zipCode) * Cd
    #one more reminder if past level 3
    if level > 3:
        print("\t Remember, that tailwind is now gusting from",int((wind/Cd)-10),"to",int((wind/Cd)+10),"meters/sec.\n\n--------------------------------\n")

    #loop so invalid inputs aren't accepted and the user is reprompted until given a valid input
    while True:
        #angle prompt
        while True:
            try:
                angle = int(input("Please enter an angle between 0 and 89 degrees to fire the ball: "))
                assert angle > 0 and angle < 89, "Angle must be between 0 and 89"
                break
            except (ValueError, AssertionError):
                print("\tInvalid input. Try again!\n")
        #velocity prompt
        while True:
            try:
                velocity = int(input("Please enter a positive velocity less than 3000m/s to fire the ball: "))
                assert velocity >= 0, "The velocity must be positive."
                if velocity > 3000:
                    print("\tAre you trying to send the ball into orbit?!")
                assert velocity < 3000, "The velocity must be less than 3000."
                break
            except (ValueError, AssertionError):
                print("\tInvalid input. Try again!\n")

        #the trajectory simulation is ran and plotted by turtle (within the traj function)
        #results are then stated and/or successes/failures are returned
        distanceshot = traj(velocity, angle, windspeed, distancelandzone, attempts, Cd, gusting, obstacle)
        if distanceshot > distancelandzone + 15:
            score = score - (pointsPossible / 5)
            print("\n--------------------------------\n\nWoops! You overshot by about",\
                  int(distanceshot-distancelandzone),"meters!\n")
        elif distanceshot < distancelandzone:
            score = score - (pointsPossible / 5)
            print("\n--------------------------------\n\nYou undershot by about",\
                  int(distancelandzone-distanceshot),"meters! Try adding power or adjusting the angle.\n")
        else:
            print("\n--------------------------------\n\nSuccess!\n\n--------------------------------")
            return score
        attempts = attempts - 1
        if attempts == 0:
            print("--------------------------------\n\nYou lose!")
            return 0
        elif attempts == 1:
            print("You have 1 attempt left. Points possible left in this level:",int(score),"points.\n")
        else:
            print("You have",attempts,"attempts left. Points possible left in this level:",int(score),"points.\n")

def visualSim(width, xlist, ylist, attempts, distObj):
    """ Sets up screen for visual simulation of projectile motion
        Parameters:
           width: the distance to the landing zone (black area)
           xlist: the list of x-values from the traj function
           ylist: the list of y-values from the traj function
           attempts: indicates which attempt the game is on
           distObj: the object distance if on level 5; otherwise, false
           score: the current score possible
        Return value: none
    """
    import turtle
    turtle = turtle.Turtle()
    screen = turtle.getscreen()
    turtle.ht()
    screen.setworldcoordinates(-10, -10, width + 15, 1000) #sets edges of screen
    turtle.up()
    turtle.setposition(-10, 0) #drawing of ground
    turtle.down()
    turtle.pensize(5)
    turtle.pencolor("green")
    turtle.setposition(width,0)
    turtle.pencolor("black")
    turtle.setposition(width+15,0)
    turtle.up()

    #draws the object
    if distObj != False:
        turtle.pencolor("blue")
        turtle.setposition(distObj,0)
        turtle.down()
        turtle.setposition(distObj, 400)
        turtle.setposition(distObj+5,400)
        turtle.setposition(distObj+5,0)
        turtle.up()

    turtle.pensize(1)
    turtle.setposition(0,0) #drawing of trajectory begins here
    turtle.shape("circle")
    turtle.down()
    
    if attempts == 5: #changes color of path depending on which attempt it is...purely aesthetic
        turtle.pencolor("blue")
    elif attempts == 4:
        turtle.pencolor("orange")
    elif attempts == 3:
        turtle.pencolor("yellow")
    elif attempts == 2:
        turtle.pencolor("purple")
    else:
        turtle.pencolor("red")
    turtle.showturtle()

    #draws the trajectory with a turtle object; stops if the turtle goes off of the screen to the left or right
    for position in range(len(xlist)):
        turtle.setposition(xlist[position], ylist[position])
        if xlist[position] > width + 15 or xlist[position] < 0: #line that stops an offscreen turtle
            turtle.hideturtle()
            break       
    time.sleep(1.5)
    screen.bye()

def traj(velocity, attitude, windspeed, distancelandzone, attempts, Cd, gusts, obstacle):
    """ Calculates the trajectory of a ball (with air resistance)
        Parameters:
           velocity: the velocity of the object; 0 < velocity < 3000
           attitude: the attitude of the object; 0 < attitude < 89
           windspeed: the windspeed taken from the internet from the zip code given
           distancelandzone: the distance to the landing zone
           attempts: indicates which attempt the game is on
           Cd: coefficient of drag; used to change between no drag and drag
           gusts: boolean value indicating whether or not the simulation should include gusting
           obstacle: boolean value indicating whether or not the simulation includes an obstacle
        Return value: the distance the ball travelled
    """
    if obstacle == True:    #eliminates problems with object simulation
        dt = 0.01           #if the dt is too large and the velocity is large too,
    else:                   #the ball goes through the wall
        dt = 0.05
    
    attitude = attitude * (math.pi/180) #changes degrees to radians
    yVel = velocity * math.sin(attitude)
    xVel = velocity * math.cos(attitude) + windspeed #tailwind

    massBall = 200 #ball's mass
    ballArea = math.pi * 1 ** 2 #ball has radius of 1m

    time = 0
    x = 0
    y = 0

    # values taken from engineeringtoolbox.com
    density = 1.112
    gravity = 9.804

    # initializes lists to simulate values
    xPos = []
    yPos = []

    if obstacle == True:
        distObj = (distancelandzone / 2) + 50 #position of object that is 2 meters wide
        objHeight = 400
    else:
        distObj = False

    #initializes gust value
    gustVal = 0

    while y >= 0:

        drag = density * Cd * ballArea * 0.5 #drag equation
        velocity = math.sqrt(xVel**2 + yVel**2) #calculates velocity (non-component)

        ax = -1 * (drag / massBall) * xVel * velocity #accel equations
        ay = - gravity - (drag / massBall) * yVel * velocity
        
        xVel = xVel + ax * dt #velocity equations
        yVel = yVel + ay * dt

        #if gusts are enabled
        if gusts != False:
            gustChange = random.uniform(-10,10)
            gustVal = gustVal + gustChange #smoothens the gust values
            if gustVal > 10 or gustVal < -10:
                gustVal = gustVal - gustChange
            xVel = xVel + (gustVal * dt)

        x = x + xVel * dt + 0.5 * ax * dt ** 2 #position from velocity and accel
        y = y + yVel * dt + 0.5 * ay * dt ** 2

        #appends points to list to later be graphed or analyzed
        if obstacle == True:
            if x >= distObj and x <= distObj + 5 and y <= objHeight:
                xVel = (-1 * xVel) / 2 #not necessarily the correct physics, just looks the best
                x = distObj - 0.01
                xPos.append(distObj)
                yPos.append(y)
            else:
                xPos.append(x)
                yPos.append(y)
        else:
            xPos.append(x)
            yPos.append(y)
        
        time = time + dt #increments time

    visualSim(distancelandzone,xPos,yPos,attempts, distObj)
    
    return xPos[-1]

def highScore(newName, newScore):
    """ controls the high score page
        Parameters:
           newName: the player's name via input
           newScore: the score the player attained
        Return value: None
    """
    
    import turtle
    names = []
    scores = []
    with open("HighScore.txt","r") as file: #opens file with name of "HighScore.txt" to read
        for line in file:
            line = line.strip("\n")
            line = line.split("\t")
            names.append(line[0])
            scores.append(int(line[1]))
            
        scores.append(newScore)
        names.append(newName)

        names = [x for (y,x) in sorted(zip(scores,names))]
        scores.sort()

        names.pop(0) #yields new high score names
        scores.pop(0) #yields new high scores

    with open("HighScore.txt","w") as file: #reopens file, but overwrites this time
        for person in range(4,-1,-1):
            name = names[person]
            score = scores[person]
            score = str(score)
            file.write(name)
            file.write("\t")
            file.write(score)
            file.write("\n")

    turtle = turtle.Turtle()
    screen = turtle.getscreen()
    screen.setup(1260, 708)
    screen.bgpic("HighScores.gif")
    turtle.setposition(-175,85)
    turtle.pencolor("white")
    turtle.hideturtle()
    turtle.right(90)

    #writes the names on the high score screen
    for person in range(4,-1,-1):
        turtle.down()
        turtle.write(names[person],move=False, align="left", font=("Arial", 28, "bold"))
        turtle.up()
        turtle.forward(70)
    turtle.setposition(175,85)
    turtle.pencolor("white")
    turtle.hideturtle()

    #writes the scores on the high score screen
    for person in range(4,-1,-1):
        turtle.down()
        turtle.write(scores[person],move=False, align="right", font=("Arial", 28, "bold"))
        turtle.up()
        turtle.forward(70)
    screen.exitonclick()
    
def main():
    """the main function...runs everything in the correct order"""
    import turtle

    totalScore = 0
    
    #show title screen
    background = turtle.Turtle()
    screen = turtle.getscreen()
    screen.title("The Cannon Game")
    screen.setup(1260, 708)
    screen.bgpic("TitleScreen.gif")
    screen.exitonclick()

    #show level 1 screen
    background1 = turtle.Turtle()
    screen = turtle.getscreen()
    screen.setup(1260, 708)
    screen.bgpic("level1.gif")
    screen.exitonclick()
    #play level 1
    level1score = level(False, 0, False, False, 1)
    EndGame = level1score
    totalScore = totalScore + level1score
    if EndGame != 0:
        print("\nYour total score at this point is",int(totalScore),"points.\n")
    
    if EndGame != 0:
        #show level 2 screen
        background2 = turtle.Turtle()
        screen = turtle.getscreen()
        screen.setup(1260, 708)
        screen.bgpic("level2.gif")
        screen.exitonclick()
        #play level 2
        level2score = level(False, 0.5, False, False, 2)
        EndGame = level2score
        totalScore = totalScore + level2score
        if EndGame != 0:
            print("\nYour total score at this point is",int(totalScore),"point(s).\n")

    if EndGame != 0:
        #show level 3 screen
        background3 = turtle.Turtle()
        screen = turtle.getscreen()
        screen.setup(1260, 708)
        screen.bgpic("level3.gif")
        screen.exitonclick()
        #play level 3
        level3score = level(True, 0.5, False, False, 3)
        EndGame = level3score
        totalScore = totalScore + level3score
        if EndGame != 0:
            print("\nYour total score at this point is",int(totalScore),"points.\n")

    if EndGame != 0:
        #show level 4 screen
        background4 = turtle.Turtle()
        screen = turtle.getscreen()
        screen.setup(1260, 708)
        screen.bgpic("level4.gif")
        screen.exitonclick()
        #play level 4
        level4score = level(True, 0.5, True, False, 4)
        EndGame = level4score
        totalScore = totalScore + level4score
        if EndGame != 0:
            print("\nYour total score at this point is",int(totalScore),"points.\n")

    if EndGame != 0:
        #show level 5 screen
        background5 = turtle.Turtle()
        screen = turtle.getscreen()
        screen.setup(1260, 708)
        screen.bgpic("level5.gif")
        screen.exitonclick()
        #play level 5
        level5score = level(True, 0.5, True, True, 5)
        EndGame = level5score
        totalScore = totalScore + level5score
        if EndGame != 0:
            print("\nYour total score was",int(totalScore),"points. Nice job!\n")
            background = turtle.Turtle()
            screen = turtle.getscreen()
            screen.setup(1260, 708)
            screen.bgpic("Winner.gif")
            screen.exitonclick()

    #shows the "you lose" screen if no points were scored on a level
    if EndGame == 0:
        background6 = turtle.Turtle()
        screen = turtle.getscreen()
        screen.setup(1260, 708)
        screen.bgpic("youLose.gif")
        screen.exitonclick()

    totalScore = int(totalScore)
    #input name for leaderboard
    newName = str(input("\n--------------------------------\n\nWhat's your name?: "))
    highScore(newName, totalScore)

    print("\n--------------------------------\n\nThanks for playing!\n\n--------------------------------\n")

if __name__ == "__main__":
    main()
