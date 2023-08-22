from flask import Flask, render_template, send_from_directory
import os

from functions_utils import predict
app = Flask(__name__)

# Route pour la page d'accueil
@app.route('/')
def home():
    return render_template('index.html')

# Route pour le traitement de l'image
@app.route('/process_image', methods=['GET', 'POST'])
def process_image():
    image_list = []

    # Chemin vers le dossier "static/images"
    images_folder = os.path.join(os.getcwd(), 'static/images')

    # Vérifie si le dossier "static/images" existe et s'il est un répertoire
    if os.path.exists(images_folder) and os.path.isdir(images_folder):
        # Liste les fichiers du dossier "static/images"
        image_list = [f for f in os.listdir(images_folder) 
                      if os.path.isfile(os.path.join(images_folder, f))]

    # Rend la page "image_list.html" en passant la liste des images comme variable
    return render_template('image_list.html', image_list=image_list)

# Route pour servir les images depuis le dossier "static/images"
@app.route('/static/images/<path:filename>')
def images(filename):
    images_folder = os.path.join(os.getcwd(), 'static/images')
    return send_from_directory(images_folder, filename)

# Route pour servir les images depuis le dossier "static/images"
@app.route('/static/generated_mask/<path:filename>')
def generated_mask(filename):
    generated_mask_folder = os.path.join(os.getcwd(), 'static/generated_mask')
    return send_from_directory(generated_mask_folder, filename)


# Route pour afficher une image sélectionnée avec son masque
@app.route('/show_selected_image/<filename>')
def show_selected_image(filename):
    # Chemin relatif au dossier 'static/images'
    selected_image_path = 'images' + '/' + filename
    # Chemin relatif au dossier 'static/masks'
    mask_image_path = os.path.join('static', 'masks', filename.replace("\\", "/"))

    # Effectuer des prédictions sur l'image sélectionnée
    prediction = predict('static/' + selected_image_path)

    # Chemin de sauvegarde pour l'image de masque générée
    generated_mask_path = os.path.join('static/generated_mask/', 'generated_mask.png')
    
    # Sauvegarder l'image de masque générée
    prediction.save(generated_mask_path)
    generated_mask_path = os.path.join('generated_mask/', 'generated_mask.png')

    # Rend la page "show_selected_image.html" en passant 
    # #les chemins des images sélectionnée et du masque
    return render_template('show_selected_image.html', 
                           selected_image_path=selected_image_path, 
                           mask_image_path=mask_image_path, 
                           generated_mask_path=generated_mask_path)


# Exécute l'application si le script est exécuté directement
if __name__ == '__main__':
    app.run(debug=True)
