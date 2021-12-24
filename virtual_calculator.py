# importing all the dependency
import cv2
from cvzone.HandTrackingModule import HandDetector
# import mediapipe

#  making class for button
class Button:

    def __init__(self,pos,width,height,value):
        self.pos = pos
        self.width = width
        self.height = height
        self.value = value

    def draw(self, img):
        cv2.rectangle(img,self.pos,(self.pos[0]+self.width, self.pos[1]+self.height) ,(225,225,225),cv2.FILLED)
        cv2.rectangle(img,self.pos,(self.pos[0]+self.width, self.pos[1]+self.height) ,(50,50,50), 3)
        cv2.putText(img,self.value,(self.pos[0]+30,self.pos[1]+60),cv2.FONT_HERSHEY_PLAIN,2,(50,50,50),2)
    
    def checkClick(self,x,y):
        
        if self.pos[0] < x < self.pos[0] + self.width:
            if self.pos[1] < y < self.pos[1] + self.height:
                cv2.rectangle(img,self.pos,(self.pos[0]+self.width, self.pos[1]+self.height) ,(255,255,255),cv2.FILLED)
                cv2.rectangle(img,self.pos,(self.pos[0]+self.width, self.pos[1]+self.height) ,(50,50,50), 3)
                cv2.putText(img,self.value,(self.pos[0]+30,self.pos[1]+70),cv2.FONT_HERSHEY_PLAIN,4,(0,0,0),4)

                return True
        return False
# makeing button
buttonListValue = [['7','8','9','+'],
                   ['4','5','6','-'],
                   ['1','2','3','*'],
                   ['0','.','=','/'],
                   ['00','C','**','%']]

buttonList = []
for x in range(4):
    for y in range(5):
        xpos = x * 100 + 500
        ypos = y * 100 + 150
        buttonList.append(Button((xpos,ypos),100,100,buttonListValue[y][x]))



# "EndsWith value" for validating the string  for calcuation in eval():
endValue = ['+','-','*','/','**','%','C','.',"=","==",'===','====','=====','======','=======',"error"]

# calculation variable
myEquation = ""

# counter 
delayCounter = 0

# to capturing video
cap = cv2.VideoCapture(0)
# width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
# height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
# print(width,"++",height)
cap.set(3,1280)
cap.set(4,720)

# hand detection
detector = HandDetector(detectionCon=0.8, maxHands=1)
while True:

    # adding frame
    success , img = cap.read()
    img = cv2.flip(img , 1)
    # img = cv2.resize(img,(1200,700))

    # detecting hands 
    hands, img = detector.findHands(img, flipType = False)

    # button
    for button in buttonList:
        button.draw(img)
    
    # drawing the display rectangle
    cv2.rectangle(img,(500,50),(500+400,50+100),(225,225,225),cv2.FILLED)
    cv2.rectangle(img,(500,50),(500+400,50+100),(50,50,50),3)

    # check for hands
    if hands:
        lmList = hands[0]['lmList']
        length,_,img = detector.findDistance(lmList[8],lmList[12],img)
        # print(length)
        x,y = lmList[8]
        if length < 40:
            for i, button in enumerate(buttonList):
                # print(i)
                if button.checkClick(x,y) and delayCounter == 0:
                    # print(i)
                    buttonVal = buttonListValue[int(i%5)][int(i/5)]
                    print(buttonVal)
                    if buttonVal == '=':
                        
                        if myEquation[-1] in endValue:  # endValue is the list of operation which should not be ended in myEquation
                            myEquation = "error"
                        else:   
                            myEquation = str(eval(myEquation))
                        # print("++++",myEquation)
                    elif buttonVal == 'C':  # it will clear the display screen
                        myEquation = ""
                    else:                   # the clicked element  will add in the string 
                        myEquation += buttonVal                    

                    delayCounter = 1

    # Avoid duplictes
    if delayCounter != 0:
        delayCounter += 1
        if delayCounter > 20 :
            delayCounter = 0

    cv2.putText(img,myEquation,(500+25 ,50+70) , cv2.FONT_HERSHEY_PLAIN,4,(25,25,25),4)


    cv2.imshow("result",img)
    key = cv2.waitKey(1)
    if key == ord("q"):
        break

cv2.destroyAllWindows()