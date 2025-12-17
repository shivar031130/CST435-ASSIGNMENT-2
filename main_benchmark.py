import time
import os
import glob
import cv2
import numpy as np
import multiprocessing
import concurrent.futures
import csv

# --- CONFIGURATION ---
INPUT_FOLDER = 'dataset_subset'
OUTPUT_FOLDER = 'processed_images'
RESULTS_FILE = 'performance_results.csv'

# Updated to test 1, 2, 4, and 8 cores as requested
CORE_COUNTS = [1, 2, 4, 8]

def setup_directories():
    """Creates the output directory if it doesn't exist."""
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

# --- WORKER FUNCTION (The "Unit of Work") ---
def process_single_image(file_path):
    """
    Reads an image and applies a LINEAR pipeline of 5 filters.
    The result will be a Grayscale (B&W) image.
    """
    try:
        # 1. LOAD IMAGE
        filename = os.path.basename(file_path)
        img = cv2.imread(file_path)
        if img is None: 
            return 0

        # --- FILTER 1: GRAYSCALE CONVERSION ---
        # Requirement: Convert RGB to Grayscale using luminance formula.
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # --- FILTER 2: GAUSSIAN BLUR ---
        # Requirement: Apply 3x3 Gaussian kernel for smoothing.
        blur = cv2.GaussianBlur(gray, (3, 3), 0)

        # --- FILTER 3: EDGE DETECTION (Sobel) ---
        # Requirement: Sobel filter to detect edges.
        # Calculated to satisfy CPU workload requirement.
        sobel_x = cv2.Sobel(blur, cv2.CV_64F, 1, 0, ksize=3)
        sobel_y = cv2.Sobel(blur, cv2.CV_64F, 0, 1, ksize=3)
        edges = cv2.magnitude(sobel_x, sobel_y)
        
        # --- FILTER 4: IMAGE SHARPENING ---
        # Requirement: Enhance edges and details.
        kernel = np.array([[0, -1, 0], 
                           [-1, 5, -1], 
                           [0, -1, 0]])
        sharpened = cv2.filter2D(blur, -1, kernel)

        # --- FILTER 5: BRIGHTNESS ADJUSTMENT ---
        # Requirement: Increase brightness.
        brightness_matrix = np.ones(sharpened.shape, dtype="uint8") * 30
        
        # Prevent overflow (255+30 -> 255)
        final_result = cv2.add(sharpened, brightness_matrix)

        # 2. SAVE RESULT
        save_path = os.path.join(OUTPUT_FOLDER, f"proc_{filename}")
        cv2.imwrite(save_path, final_result)
        
        return 1 # Success
    except Exception as e:
        return 0 # Failure

# --- PARADIGM 1: MULTIPROCESSING ---
def run_multiprocessing(image_files, cores):
    with multiprocessing.Pool(processes=cores) as pool:
        pool.map(process_single_image, image_files)

# --- PARADIGM 2: CONCURRENT.FUTURES ---
def run_concurrent_futures(image_files, cores):
    with concurrent.futures.ProcessPoolExecutor(max_workers=cores) as executor:
        list(executor.map(process_single_image, image_files))

# --- MAIN BENCHMARK LOGIC ---
def main():
    setup_directories()
    
    # 1. Prepare Data
    image_files = glob.glob(os.path.join(INPUT_FOLDER, "*.jpg"))
    if not image_files:
        print(f"CRITICAL ERROR: No images found in '{INPUT_FOLDER}'.")
        print("Please run 'create_balanced_subset.py' first.")
        return

    print(f"--- Starting Benchmark on {len(image_files)} Images ---")
    
    # --- WARM-UP PHASE (NEW) ---
    print(">>> Warming up system cache (Running dummy pass)...")
    # Run a small batch (up to 100 images) on 1 core to load libraries/files
    warmup_subset = image_files[:100]
    run_multiprocessing(warmup_subset, 1)
    print(">>> Warm-up complete. Starting Actual Benchmark.")
    print("-" * 75)
    
    print(f"Testing Core Counts: {CORE_COUNTS}")
    print(f"Note: Output images will be saved in '{OUTPUT_FOLDER}' (Grayscale)")
    print("-" * 75)
    print(f"{'Paradigm':<20} | {'Cores':<5} | {'Time(s)':<8} | {'Speedup':<8} | {'Efficiency':<10}")
    print("-" * 75)

    results_data = []

    # Variables to hold the execution time of 1 core (Baseline)
    baseline_mp = 0
    baseline_cf = 0

    # 2. Loop through both Paradigms
    for paradigm in ['Multiprocessing', 'Concurrent.Futures']:
        
        for cores in CORE_COUNTS:
            
            # --- GARBAGE COLLECTION / PAUSE ---
            # Optional: Sleep briefly between runs to let disk I/O settle
            time.sleep(1)

            start_time = time.time()
            
            # Execute
            if paradigm == 'Multiprocessing':
                run_multiprocessing(image_files, cores)
            else:
                run_concurrent_futures(image_files, cores)
            
            end_time = time.time()
            duration = end_time - start_time
            
            # 3. Calculate Metrics
            speedup = 0.0
            efficiency = 0.0
            
            if paradigm == 'Multiprocessing':
                if cores == 1: baseline_mp = duration
                if duration > 0: speedup = baseline_mp / duration
            else:
                if cores == 1: baseline_cf = duration
                if duration > 0: speedup = baseline_cf / duration
            
            if cores > 0:
                efficiency = speedup / cores

            # 4. Print & Save
            print(f"{paradigm:<20} | {cores:<5} | {duration:<8.4f} | {speedup:<8.2f} | {efficiency:<10.2f}")
            results_data.append([paradigm, cores, round(duration, 4), round(speedup, 2), round(efficiency, 2)])

    # 5. Save Results to CSV
    with open(RESULTS_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Paradigm', 'Cores', 'Time(s)', 'Speedup', 'Efficiency'])
        writer.writerows(results_data)
    
    print("-" * 75)
    print(f"Benchmark Complete. Data saved to '{RESULTS_FILE}'.")

if __name__ == '__main__':
    main()