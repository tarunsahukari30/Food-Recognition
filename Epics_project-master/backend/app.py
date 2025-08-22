from flask import Flask, request, jsonify
from PIL import Image
import numpy as np
import tensorflow as tf
import torch
from torchvision.models.detection import maskrcnn_resnet50_fpn
from torchvision.transforms import functional as F
import cv2
import io
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
classification_model = tf.keras.models.load_model('./food101_inceptionv3_model.h5')
detection_model = maskrcnn_resnet50_fpn(pretrained=True)
detection_model.eval()
class_names = [
    'apple_pie', 'baby_back_ribs', 'baklava', 'beef_carpaccio', 'beef_tartare', 'beet_salad', 
    'beignets', 'bibimbap', 'bread_pudding', 'breakfast_burrito', 'bruschetta', 'caesar_salad', 
    'cannoli', 'caprese_salad', 'carrot_cake', 'ceviche', 'cheesecake', 'cheese_plate', 'chicken_curry', 
    'chicken_quesadilla', 'chicken_wings', 'chocolate_cake', 'chocolate_mousse', 'churros', 'clam_chowder', 
    'club_sandwich', 'crab_cakes', 'creme_brulee', 'croque_madame', 'cup_cakes', 'deviled_eggs', 
    'donuts', 'dumplings', 'edamame', 'eggs_benedict', 'escargots', 'falafel', 'filet_mignon', 'fish_and_chips', 
    'foie_gras', 'french_fries', 'french_onion_soup', 'french_toast', 'fried_calamari', 'fried_rice', 
    'frozen_yogurt', 'garlic_bread', 'gnocchi', 'greek_salad', 'grilled_cheese_sandwich', 'grilled_salmon', 
    'guacamole', 'gyoza', 'hamburger', 'hot_and_sour_soup', 'hot_dog', 'huevos_rancheros', 'hummus', 
    'ice_cream', 'lasagna', 'lobster_bisque', 'lobster_roll_sandwich', 'macaroni_and_cheese', 'macarons', 
    'miso_soup', 'mussels', 'nachos', 'omelette', 'onion_rings', 'oysters', 'pad_thai', 'paella', 
    'pancakes', 'panna_cotta', 'peking_duck', 'pho', 'pizza', 'pork_chop', 'poutine', 'prime_rib', 
    'pulled_pork_sandwich', 'ramen', 'ravioli', 'red_velvet_cake', 'risotto', 'samosa', 'sashimi', 
    'scallops', 'seaweed_salad', 'shrimp_and_grits', 'spaghetti_bolognese', 'spaghetti_carbonara', 
    'spring_rolls', 'steak', 'strawberry_shortcake', 'sushi', 'tacos', 'takoyaki', 'tiramisu', 
    'tuna_tartare', 'waffles'
]
calorie_map = {
    'apple_pie': 300, 'baby_back_ribs': 500, 'baklava': 350, 'beef_carpaccio': 250, 'beef_tartare': 220,
    'beet_salad': 150, 'beignets': 290, 'bibimbap': 550, 'bread_pudding': 330, 'breakfast_burrito': 450,
    'bruschetta': 170, 'caesar_salad': 220, 'cannoli': 240, 'caprese_salad': 200, 'carrot_cake': 400,
    'ceviche': 180, 'cheesecake': 430, 'cheese_plate': 500, 'chicken_curry': 300, 'chicken_quesadilla': 340,
    'chicken_wings': 430, 'chocolate_cake': 450, 'chocolate_mousse': 310, 'churros': 370, 'clam_chowder': 210,
    'club_sandwich': 350, 'crab_cakes': 290, 'creme_brulee': 320, 'croque_madame': 380, 'cup_cakes': 200,
    'deviled_eggs': 70, 'donuts': 250, 'dumplings': 150, 'edamame': 120, 'eggs_benedict': 400, 'escargots': 90,
    'falafel': 330, 'filet_mignon': 450, 'fish_and_chips': 600, 'foie_gras': 500, 'french_fries': 400,
    'french_onion_soup': 200, 'french_toast': 250, 'fried_calamari': 300, 'fried_rice': 350, 'frozen_yogurt': 200,
    'garlic_bread': 210, 'gnocchi': 300, 'greek_salad': 150, 'grilled_cheese_sandwich': 400, 'grilled_salmon': 350,
    'guacamole': 230, 'gyoza': 160, 'hamburger': 500, 'hot_and_sour_soup': 100, 'hot_dog': 350, 'huevos_rancheros': 400,
    'hummus': 150, 'ice_cream': 210, 'lasagna': 450, 'lobster_bisque': 310, 'lobster_roll_sandwich': 500,
    'macaroni_and_cheese': 500, 'macarons': 110, 'miso_soup': 90, 'mussels': 150, 'nachos': 600, 'omelette': 220,
    'onion_rings': 300, 'oysters': 120, 'pad_thai': 550, 'paella': 400, 'pancakes': 220, 'panna_cotta': 250,
    'peking_duck': 350, 'pho': 300, 'pizza': 280, 'pork_chop': 430, 'poutine': 740, 'prime_rib': 600,
    'pulled_pork_sandwich': 450, 'ramen': 500, 'ravioli': 400, 'red_velvet_cake': 430, 'risotto': 300,
    'samosa': 250, 'sashimi': 120, 'scallops': 200, 'seaweed_salad': 60, 'shrimp_and_grits': 420,
    'spaghetti_bolognese': 480, 'spaghetti_carbonara': 450, 'spring_rolls': 130, 'steak': 600,
    'strawberry_shortcake': 350, 'sushi': 150, 'tacos': 210, 'takoyaki': 200, 'tiramisu': 400,
    'tuna_tartare': 160, 'waffles': 310
}
food_reference = {food: {"reference_pixels": 400000, "reference_calories": 300} for food in class_names}

def estimate_calories(food_label, area):
    if food_label in food_reference:
        ref_data = food_reference[food_label]
        portion_ratio = area / ref_data["reference_pixels"]
        estimated_calories = portion_ratio * calorie_map.get(food_label, 0)
        return round(estimated_calories, 2)
    else:
        return 0
@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        print("No image in request.")
        return jsonify({'error': 'No image uploaded'}), 400
    try:
        image_file = request.files['image']
        image = Image.open(image_file)
        print("Image received and opened.")

        image_resized = image.resize((299, 299))
        image_array = np.array(image_resized) / 255.0
        image_array = np.expand_dims(image_array, axis=0)

        predictions = classification_model.predict(image_array)
        predicted_index = np.argmax(predictions)
        predicted_label = class_names[predicted_index]
        predicted_probability = predictions[0][predicted_index]

        print(f"Predicted label: {predicted_label}, Probability: {predicted_probability}")

        image_cv = np.array(image)
        image_rgb = cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB)
        image_tensor = F.to_tensor(Image.fromarray(image_rgb)).unsqueeze(0)

        with torch.no_grad():
            detection = detection_model(image_tensor)

        masks = detection[0]['masks']
        scores = detection[0]['scores']
        threshold = 0.5
        filtered_indices = [i for i in range(len(scores)) if scores[i] > threshold]

        total_area = 0
        for idx in filtered_indices:
            mask = masks[idx, 0].cpu().numpy()
            binary_mask = mask > 0.5
            area = np.sum(binary_mask)
            total_area += area

        print(f"Total detected area: {total_area}")

        estimated_calories = estimate_calories(predicted_label, total_area)
        print(f"Estimated calories: {estimated_calories}")

        response = {
            'predicted_label': predicted_label,
            'predicted_probability': float(predicted_probability),
            'estimated_calories': estimated_calories,
            'total_area': int(total_area)
        }

        return jsonify(response)

    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({'error': 'An internal error occurred'}), 500

if __name__ == '__main__':
    app.run(debug=True)
