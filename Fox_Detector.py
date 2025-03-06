import cv2
import pytesseract
import numpy as np

# Fonction pour prétraiter l'image (conversion en niveaux de gris et seuillage)
def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convertir en niveaux de gris
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)  # Appliquer un seuillage binaire inverse
    return thresh

# Fonction pour extraire le texte de l'image en utilisant Tesseract
# On limite la reconnaissance aux lettres "F", "O" et "X"
def extract_text(image):
    custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=FOX'
    text = pytesseract.image_to_string(image, config=custom_config)
    return text

# Fonction pour générer une matrice de taille spécifiée à partir du texte extrait
def generate_matrix(text, rows=20, cols=32):
    mapping = {'F': 1, 'O': 2, 'X': 3}  # Correspondance des lettres en valeurs numériques
    text = [char for char in text if char in mapping]  # Filtrer uniquement les lettres reconnues
    
    if len(text) != rows * cols:
        print("Erreur : Nombre de caractères détectés incorrect.")
        return None
    
    # Transformer la liste des caractères en une matrice NumPy
    matrix = np.array([mapping[char] for char in text]).reshape(rows, cols)
    return matrix

# Fonction principale qui capture l'image et affiche la matrice
def main():
    cap = cv2.VideoCapture(0)  # Ouvrir la webcam
    
    while True:
        ret, frame = cap.read()  # Capturer une image
        if not ret:
            break
        
        processed = preprocess_image(frame)  # Appliquer le prétraitement
        text = extract_text(processed)  # Extraire le texte
        matrix = generate_matrix(text)  # Convertir en matrice
        
        if matrix is not None:
            print(matrix)  # Afficher la matrice détectée
        
        # Afficher les images en direct
        cv2.imshow("Camera", frame)
        cv2.imshow("Processed", processed)
        
        # Quitter la boucle en appuyant sur 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()  # Libérer la webcam
    cv2.destroyAllWindows()  # Fermer les fenêtres

# Exécution du programme principal
if __name__ == "__main__":
    main()
