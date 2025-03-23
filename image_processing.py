from PIL import Image
import numpy as np

def auto_resize(image_path, target_size=(224, 224)):
    """
    Automatically resize an image to the target size while maintaining aspect ratio.
    
    Args:
        image_path (str): Path to the input image
        target_size (tuple): Desired output size (width, height)
        
    Returns:
        PIL.Image: Resized image
    """
    try:
        # Open the image
        img = Image.open(image_path)
        
        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Calculate aspect ratio
        aspect_ratio = img.size[0] / img.size[1]
        
        # Calculate new dimensions maintaining aspect ratio
        if aspect_ratio > 1:
            # Width is greater than height
            new_width = target_size[0]
            new_height = int(target_size[0] / aspect_ratio)
        else:
            # Height is greater than width
            new_height = target_size[1]
            new_width = int(target_size[1] * aspect_ratio)
            
        # Resize image
        img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Create new image with target size and paste resized image in center
        new_img = Image.new('RGB', target_size, (0, 0, 0))
        paste_x = (target_size[0] - new_width) // 2
        paste_y = (target_size[1] - new_height) // 2
        new_img.paste(img_resized, (paste_x, paste_y))
        
        return new_img
        
    except Exception as e:
        print(f"Error processing image: {str(e)}")
        return None

def preprocess_image(image_path):
    """
    Preprocess image for model input:
    1. Resize to standard size
    2. Normalize pixel values
    
    Args:
        image_path (str): Path to the input image
        
    Returns:
        numpy.ndarray: Preprocessed image array
    """
    try:
        # Resize image
        img = auto_resize(image_path)
        if img is None:
            return None
            
        # Convert to numpy array and normalize
        img_array = np.array(img)
        img_array = img_array / 255.0  # Normalize to [0,1]
        
        return img_array
        
    except Exception as e:
        print(f"Error preprocessing image: {str(e)}")
        return None

def crop_marked_region(image_path, points):
    """
    Crop the region marked by the user.
    
    Args:
        image_path (str): Path to the input image
        points (list): List of (x,y) coordinates marking the region
        
    Returns:
        PIL.Image: Cropped image
    """
    try:
        if not points or len(points) < 2:
            return None
            
        img = Image.open(image_path)
        
        # Calculate bounding box
        x_coords = [p.x() for p in points]
        y_coords = [p.y() for p in points]
        
        left = max(0, min(x_coords))
        top = max(0, min(y_coords))
        right = min(img.width, max(x_coords))
        bottom = min(img.height, max(y_coords))
        
        # Crop image
        cropped = img.crop((left, top, right, bottom))
        
        return cropped
        
    except Exception as e:
        print(f"Error cropping image: {str(e)}")
        return None