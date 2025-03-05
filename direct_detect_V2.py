import cv2
import easyocr
import numpy as np

# Instance du détecteur de texte
reader = easyocr.Reader(['fr'], gpu=False)

# Ouverture de la caméra
cap = cv2.VideoCapture(0)  # 0 pour la caméra par défaut (principal)

# Seuil pour la confiance (score)
threshold = 0.25

# Définir le facteur de réduction de taille de l'image
resize_factor = 0.5  # 0.5 veut dire réduction de la taille par deux

# Compteur de frames pour traiter une image sur 2 ou 3
frame_counter = 0
frame_interval = 2  # Traiter une frame sur 2

while True:
    # Capture une image depuis la caméra
    ret, img = cap.read()

    if not ret:
        print("Erreur de lecture de la vidéo")
        break

    # Augmenter les FPS en réduisant la taille de l'image
    small_img = cv2.resize(img, (0, 0), fx=resize_factor, fy=resize_factor)

    # Incrémenter le compteur de frames
    frame_counter += 1

    # Traiter une image sur 2 ou 3 (dépend de frame_interval)
    if frame_counter % frame_interval == 0:
        # Détecter le texte dans l'image
        text_ = reader.readtext(small_img)

        # Dessiner les boîtes et le texte détecté
        for t_ in text_:
            bbox, text, score = t_

            if score > threshold:
                # Corriger les coordonnées pour cv2.rectangle() (convertir les coordonnées en tuple (x, y))
                pt1 = tuple(map(int, bbox[0]))  # Coin supérieur gauche
                pt2 = tuple(map(int, bbox[2]))  # Coin inférieur droit

                # Dessiner un rectangle autour du texte détecté
                cv2.rectangle(img, pt1, pt2, (0, 255, 0), 2)
                # Afficher le texte détecté
                cv2.putText(img, text, pt1, cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0), 2)

    # Afficher l'image avec les détections en temps réel
    cv2.imshow('Text Detection - Press "q" to exit', img)

    # Quitter la boucle si la touche 'q' est pressée
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libérer la caméra et fermer toutes les fenêtres après avoir quitté la boucle
cap.release()
cv2.destroyAllWindows()
