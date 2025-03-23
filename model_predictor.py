import random
import time
from PIL import Image

def predict_tumor(image_path):
    """
    Simulates tumor prediction with a 5-second processing time.
    Returns either "Tumor" or "No Tumor".
    """
    try:
        # Validate image
        img = Image.open(image_path)
        img.verify()  # Verify it's a valid image
        
        # Simulate processing time (5 seconds)
        time.sleep(5)
        
        # Simulate prediction
        # For demonstration, we'll randomly choose between tumor types
        # and convert any tumor type to just "Tumor"
        possible_results = ['glioma', 'meningioma', 'pituitary', 'no_tumor']
        prediction = random.choice(possible_results)
        
        # Convert specific tumor types to generic "Tumor" response
        if prediction in ['glioma', 'meningioma', 'pituitary']:
            return "Tumor"
        else:
            return "No Tumor"
            
    except Exception as e:
        print(f"Error during prediction: {str(e)}")
        return "Error: Invalid image or processing failed"