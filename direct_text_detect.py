import cv2
import easyocr
import numpy as np

# Instance du détecteur de texte avec utilisation du GPU si disponible
#reader = easyocr.Reader(['fr'], gpu=True)
reader = easyocr.Reader(['fr'], gpu=True, detector=True, recognizer=True)

# Ouverture de la caméra
cap = cv2.VideoCapture(0)  # 0 pour la caméra par défaut (principal)

# Seuil pour la confiance (score)
threshold = 0.25

try:
    while True:
        # Capture une image depuis la caméra
        ret, img = cap.read()

        if not ret:
            print("Erreur de lecture de la vidéo")
            break

        # Convertir l'image en niveaux de gris pour améliorer la détection
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Détecter le texte dans l'image
        text_ = reader.readtext(gray)

        # Vérifier si du texte a été détecté
        if text_:
            for t_ in text_:
                bbox, text, score = t_

                if score > threshold:
                    # Corriger les coordonnées pour cv2.rectangle() (convertir les coordonnées en tuple (x, y))
                    pt1 = tuple(map(int, bbox[0]))  # Coin supérieur gauche
                    pt2 = tuple(map(int, bbox[2]))  # Coin inférieur droit

                    # Dessiner un rectangle autour du texte détecté
                    cv2.rectangle(img, pt1, pt2, (0, 255, 0), 2)

                    # Ajouter un fond coloré pour améliorer la lisibilité du texte
                    (text_width, text_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_COMPLEX, 0.5, 2)
                    cv2.rectangle(img, pt1, (pt1[0] + text_width, pt1[1] - text_height - 5), (0, 255, 0), -1)
                    
                    # Afficher le texte détecté
                    cv2.putText(img, text, pt1, cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 2)

        # Afficher l'image avec les détections en temps réel
        cv2.imshow('Text Detection - Press "q" to exit', img)

        # Quitter la boucle si la touche 'q' est pressée
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

except Exception as e:
    print(f"Erreur: {e}")

finally:
    # Libérer la caméra et fermer toutes les fenêtres après avoir quitté la boucle
    cap.release()
    cv2.destroyAllWindows()