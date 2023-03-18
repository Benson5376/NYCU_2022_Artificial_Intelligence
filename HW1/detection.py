import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

def detect(dataPath, clf):
    """
    Please read detectData.txt to understand the format. Load the image and get
    the face images. Transfer the face images to 19 x 19 and grayscale images.
    Use clf.classify() function to detect faces. Show face detection results.
    If the result is True, draw the green box on the image. Otherwise, draw
    the red box on the image.
      Parameters:
        dataPath: the path of detectData.txt
      Returns:
        No returns.
    """
    # Begin your code (Part 4)
 
    x_coordinate = []
    y_coordinate = []
    beatles = [] 
    obama = []
    spidermen = []
    size = []
    
    ## each line in txt is an element in the list 'str1'                     
    ## str1 = [the-beatles.jpg 4 , 242 78 55 55 , 368 175 71 71, ...]
    F = open(dataPath)
    str1 = F.readlines()
    
       
    
    for i in range(len(str1)):
        
        if(i==0):
            beatles = str1[0].split(' ') ## beatles = [the-beatles.jpg , 4]
        
        elif(i==5):
            obama = str1[5].split(' ') ## obama = [p110912sh-0083.jpg , 15]
        elif(i==21):
            spidermen = str1[21].split(' ')
        else:
            str2 = []
            str2 = str1[i].split(' ') ## i.e. str2 = [242,78,55,55]
            x_coordinate.append(int(str2[0]))
            y_coordinate.append(int(str2[1]))
            size.append(int(str2[2]))
            str2 = []  ## initialize the list 'str2' and run next line in str1
            
            
    image1 = 'data/detect/' + beatles[0] ## The path to the image of the beatles
    image2 = 'data/detect/' + obama[0] ## The path to the image of Obama
    image3 = 'data/detect/' + spidermen[0]
    img1 = cv2.imread(image1)
    img2 = cv2.imread(image2)
    img3 = cv2.imread(image3)
      
    print(image3)
    for i in range(0,4): ## face0 to face3 in the beatles' image
        
    ## Turn the image to grayscale and find out the position of the face then resize it                  
        imagegray = cv2.imread(image1,cv2.IMREAD_GRAYSCALE) 
        imagechop = imagegray[x_coordinate[i]:size[i],y_coordinate[i]:size[i]]
        imagesmall = np.resize(imagechop,(19,19))

        ## Run the classiflier and draw a red or green rectangle on the faces of the original images
        if(clf.classify(imagesmall)):
            cv2.rectangle(img1,(x_coordinate[i],y_coordinate[i]),(x_coordinate[i] + size[i],y_coordinate[i] + size[i]),(0,255,0),2)
        else:
            cv2.rectangle(img1,(x_coordinate[i],y_coordinate[i]),(x_coordinate[i] + size[i],y_coordinate[i] + size[i]),(0,0,255),2)
            
    for i in range(4,19): ## face4 to face18 in the Obama's image
         
         ## Turn the image to grayscale and find out the position of the face then resize it 
         imagegray = cv2.imread(image2,cv2.IMREAD_GRAYSCALE) 
         imagechop = imagegray[x_coordinate[i]:x_coordinate[i] + size[i],y_coordinate[i]:y_coordinate[i] + size[i]]
         imagesmall = np.resize(imagechop,(19,19))

         ## Run the classiflier and draw a red or green rectangle on the faces of the original images   
         if(clf.classify(imagesmall)):
            cv2.rectangle(img2,(x_coordinate[i],y_coordinate[i]),(x_coordinate[i] + size[i],y_coordinate[i] + size[i]),(0,255,0),2)
         else:
            cv2.rectangle(img2,(x_coordinate[i],y_coordinate[i]),(x_coordinate[i] + size[i],y_coordinate[i] + size[i]),(0,0,255),2)
    for i in range(19,22): ## face4 to face18 in the Obama's image
        
        ## Turn the image to grayscale and find out the position of the face then resize it 
        imagegray = cv2.imread(image3,cv2.IMREAD_GRAYSCALE) 
        imagechop = imagegray[x_coordinate[i]:x_coordinate[i] + size[i],y_coordinate[i]:y_coordinate[i] + size[i]]
        imagesmall = np.resize(imagechop,(19,19))

        ## Run the classiflier and draw a red or green rectangle on the faces of the original images   
        if(clf.classify(imagesmall)):
           cv2.rectangle(img3,(x_coordinate[i],y_coordinate[i]),(x_coordinate[i] + size[i],y_coordinate[i] + size[i]),(0,255,0),2)
        else:
           cv2.rectangle(img3,(x_coordinate[i],y_coordinate[i]),(x_coordinate[i] + size[i],y_coordinate[i] + size[i]),(0,0,255),2)
    
   
    
    cv2.namedWindow("obama",0)
    cv2.resizeWindow("obama",20000,20000)
    cv2.imshow("obama",img2)
    cv2.waitKey(0)  
    cv2.namedWindow("beatles",0)
    cv2.resizeWindow("beatles",20000,20000)
    cv2.imshow("beatles",img1)
    cv2.waitKey(0)
   
    cv2.imshow("spidermen",img3)
    cv2.waitKey(0)
    # raise NotImplementedError("To be implemented")
    # End your code (Part 4)
