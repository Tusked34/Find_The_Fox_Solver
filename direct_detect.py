# Importation de la bibliothèque OpenCV
import cv2

# Ouvre la caméra (index 0, souvent utilisé pour une webcam principale, si disponible)
cap = cv2.VideoCapture(0)

# Verifie l'ouverture de la caméra
if not cap.isOpened():
    print("\n*** Erreur: Impossible d'ouvrir la caméra ***\n")
    exit()
    
else : 
    print("\n*** Ouverture de la caméra ***\n")

# Boucle infinie pour capturer et afficher les images vidéo en temps réel
while True:
    # Capture une image depuis la caméra
    ret, frame = cap.read()

    # Si la capture est réussie, afficher l'image dans une fenêtre nommée 'frame'
    if ret:
        cv2.imshow('frame', frame)

    # Vérifie si la touche 'q' a été pressée pour quitter la boucle
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libère la caméra et ferme toutes les fenêtres OpenCV après la fin de la capture
cap.release()
cv2.destroyAllWindows()
print("\n*** Fermeture de la caméra ***\n")
