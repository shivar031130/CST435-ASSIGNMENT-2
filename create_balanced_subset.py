import os
import shutil
import random

# --- CONFIGURATION ---
SOURCE_DATASET_ROOT = 'C:\\Users\\shivar\\OneDrive\\Desktop\\CST435 Assign2\\food-101\\food-101\\images' 
DEST_DIR = 'dataset_subset'
IMAGES_PER_CATEGORY = 10  # Target number of images to grab from EACH folder

def create_balanced_subset():
    # 1. Validation
    if not os.path.exists(SOURCE_DATASET_ROOT):
        print(f"Error: '{SOURCE_DATASET_ROOT}' not found.")
        return

    # 2. Setup Destination
    if os.path.exists(DEST_DIR):
        print(f"Cleaning up old '{DEST_DIR}'...")
        shutil.rmtree(DEST_DIR)
    os.makedirs(DEST_DIR)

    # 3. Get list of all category folders
    try:
        categories = sorted(os.listdir(SOURCE_DATASET_ROOT))
        # Filter to ensure we only look at directories
        categories = [c for c in categories if os.path.isdir(os.path.join(SOURCE_DATASET_ROOT, c))]
    except Exception as e:
        print(f"Error reading directories: {e}")
        return

    print(f"Found {len(categories)} categories. Starting extraction...")
    
    total_copied_count = 0
    
    # 4. Loop through ALL categories
    for category in categories:
        category_path = os.path.join(SOURCE_DATASET_ROOT, category)
        
        # Get list of valid images in this specific category
        images = [f for f in os.listdir(category_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        
        # Determine how many to take (take 50, or all if less than 50 exist)
        num_to_select = min(len(images), IMAGES_PER_CATEGORY)
        
        if num_to_select > 0:
            # Randomly pick 50 unique images
            selected_images = random.sample(images, num_to_select)
            
            for i, image_file in enumerate(selected_images):
                src_path = os.path.join(category_path, image_file)
                
                # Rename: "apple_pie_001.jpg", "apple_pie_002.jpg"
                # This ensures unique names in the flat destination folder
                new_filename = f"{category}_{i+1:03d}.jpg"
                dst_path = os.path.join(DEST_DIR, new_filename)
                
                shutil.copy2(src_path, dst_path)
                total_copied_count += 1

            print(f"  -> Copied {num_to_select} images from: {category}")
        else:
            print(f"  -> Skipped {category} (No images found)")

    print("-" * 10)
    print(f"SUCCESS: Dataset creation complete.")
    print(f"Total Images Copied: {total_copied_count}")
    print(f"Location: {os.path.abspath(DEST_DIR)}")

if __name__ == "__main__":
    create_balanced_subset()