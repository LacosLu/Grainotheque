import cv2
import numpy as np

cap = cv2.VideoCapture(0)


while True:

    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)



    l_b = np.array([0, 0, 226])
    u_b = np.array([255, 255, 255])
    mask = cv2.inRange(hsv, l_b, u_b)


    # Création du résultat couleur du masque
    res = cv2.bitwise_and(frame, frame, mask=mask)
    
    #Réalisation des contours de chaque objet détecté
    contours= cv2.findContours(mask,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    
    for contour in contours:
        area = cv2.contourArea(contour)
        if area < 4000 and area > 100:
            cv2.drawContours(res,contour, -1, (0, 255, 0),3)
            
    #Affichage des résultats en temps réelle.
    cv2.imshow("frame", frame)
    #cv2.imshow("mask", mask)
    cv2.imshow("res", res)

    #Q POUR ETEINDRE LE SCRIPT
    if (cv2.waitKey(1) & 0xFF == ord('q')): 
        break

cap.release()
cv2.destroyAllWindows()