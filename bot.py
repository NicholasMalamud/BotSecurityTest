import pyautogui as pag
from pynput.mouse import Listener
import cv2
import numpy as np
import random
import math
import tkinter


def findPos():
    def on_click(x, y, button, pressed):
        print(x, y, button, pressed)

    with Listener(on_click=on_click) as listener:
        listener.join()

def randMove(x,y):
    #random placement of click on square button
    rX = random.randint(int(x) - 25, int(x) + 25)
    rY = random.randint(int(y) - 20, int(y) + 5)
    #variables holds current position of mouse
    curX, curY = pag.position()
    #number of intervals of random mouse movement to point
    rStep = 1/random.randint(5,10)
    #variable holds percent of distance to the point (0-1) = (0%-100%) <- 1 = destination
    pDist = rStep
    #amount of randomness between the points of movement (higher = more random)
    rAmount = 100 - 10 * int(1000/math.dist([curX, curY], [rX, rY]))

    #while mouse before destination
    while (pDist <= 1):
        #get the next position for the interval
        curX, curY = pag.getPointOnLine(curX, curY, rX, rY, pDist)
        #randomize the next point
        curY = curY + random.randint(-rAmount,rAmount)
        curX = curX + random.randint(-rAmount,rAmount)
        #move to point with random speed
        pag.moveTo(curX, curY, random.uniform(0.05,0.1))
        #go to next interval
        pDist = pDist + rStep
        #decrease random for each interval, as person gets close to button they slow down to not miss
        rAmount = int(rAmount * (1-pDist))

def replaceInvalid(str):
    str1 = str.replace('\\','�')
    str2 = str1.replace('/','�')
    str3 = str2.replace(':', '�')
    str4 = str3.replace('*', '�')
    str5 = str4.replace('?', '�')
    str6 = str5.replace('"', '�')
    str7 = str6.replace('<', '�')
    str8 = str7.replace('>', '�')
    str9 = str8.replace('|', '�')
    return str9

def recCaptcha(capCount):
    #generate 100 images
    if(capCount <= 100):
        reload = (706, 516)
        textStart = (412, 793)
        #textEnd = (556, 791)
        #Copy Text
        pag.moveTo(textStart)
        pag.doubleClick()
        pag.doubleClick()
        pag.keyDown('ctrl')
        pag.keyDown('c')
        pag.keyUp('c')
        pag.keyUp('ctrl')
        #Take screenshot of captcha
        s = pag.screenshot(region=(424, 491, 254, 60))
        capText = replaceInvalid(tkinter.Tk().clipboard_get())
        s.save("Captchas/" + capText + '.png')
        #Next One
        pag.moveTo(reload)
        pag.click()
        capCount = capCount + 1
        recCaptcha(capCount)

def main():
    #findPos()
    #recCaptcha(0)

    s = pag.screenshot()
    s.save("screen.png")

    img1 = cv2.imread('screen.png', 1)

    hsv = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)

    lower_red = np.array([0, 50, 50])
    upper_red = np.array([10, 255, 255])

    mask = cv2.inRange(hsv, lower_red, upper_red)
    res = cv2.bitwise_and(img1, img1, mask=mask)

    kernel = np.ones((30, 30), np.float32) /900
    smoothed = cv2.filter2D(res, -1, kernel)

    cv2.imwrite('found.png',smoothed)

    #smooth again to get rid of noise
    #img2 = cv2.imread('found.png', 1)
    #smoothed = cv2.filter2D(img2, -1, kernel)
    hsv = cv2.cvtColor(smoothed, cv2.COLOR_BGR2HSV)
    #create a black and white mask
    masky = cv2.inRange(hsv, lower_red, upper_red)
    cv2.imwrite('found.png', masky)

    #part2---- GET COORDINATES

    # variable and converting to gray scale.
    img = cv2.imread('found.png', cv2.IMREAD_GRAYSCALE)

    # Converting image to a binary image
    # ( black and white only image).
    _, threshold = cv2.threshold(img, 110, 255, cv2.THRESH_BINARY)

    # Detecting contours in image.
    contours, _ = cv2.findContours(threshold, cv2.RETR_TREE,
                                   cv2.CHAIN_APPROX_SIMPLE)


    # Going through every contours found in the image.
    for cnt in contours:

        approx = cv2.approxPolyDP(cnt, 0.009 * cv2.arcLength(cnt, True), True)

        # Used to flatted the array containing
        # the co-ordinates of the vertices.
        n = approx.ravel()
        i = 0

        xlist = []
        ylist = []

        for j in n:
            if (i % 2 == 0):
                x = n[i]
                y = n[i + 1]

                xlist.append(x)
                ylist.append(y)

            i = i + 1

    averageX = sum(xlist) / len(xlist)
    averageY = sum(ylist) / len(ylist)

    if (averageX != 0 and averageY != 0):
        #pag.moveTo(averageX, averageY)
        #pag.moveTo(averageX, averageY, random.uniform(0.2, 1), pag.easeOutQuad)
        #pag.moveTo(averageX, averageY, 0.5)
        randMove(averageX,averageY)
        pag.click()
        main()
    else:
        print("done!!")
    #'''

if __name__ == '__main__':
    main()