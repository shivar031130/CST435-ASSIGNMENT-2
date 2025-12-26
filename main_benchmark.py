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
RESULTS_FILE = 'performance_results.csv'
CORE_COUNTS = [1, 2, 4, 8]

# --- WORKER FUNCTION ---
def process_single_image(file_path):
    """
    Reads an image and applies a LINEAR pipeline of 5 filters.
    No output is saved (pure computation benchmark).
    """
    try:
        img = cv2.imread(file_path)
        if img is None:
            return 0

        # --- FILTER 1: GRAYSCALE ---
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # --- FILTER 2: GAUSSIAN BLUR ---
        blur = cv2.GaussianBlur(gray, (3, 3), 0)

        # --- FILTER 3: SOBEL EDGE DETECTION ---
        sobel_x = cv2.Sobel(blur, cv2.CV_64F, 1, 0, ksize=3)
        sobel_y = cv2.Sobel(blur, cv2.CV_64F, 0, 1, ksize=3)
        edges = cv2.magnitude(sobel_x, sobel_y)

        # --- FILTER 4: SHARPENING ---
        kernel = np.array([[0, -1, 0],
                           [-1, 5, -1],
                           [0, -1, 0]])
        sharpened = cv2.filter2D(blur, -1, kernel)

        # --- FILTER 5: BRIGHTNESS ADJUSTMENT ---
        brightness_matrix = np.ones(sharpened.shape, dtype="uint8") * 30
        final_result = cv2.add(sharpened, brightness_matrix)

        # Result is intentionally NOT saved
        return 1

    except Exception:
        return 0

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
    image_files = glob.glob(os.path.join(INPUT_FOLDER, "*.jpg"))
    if not image_files:
        print(f"ERROR: No images found in '{INPUT_FOLDER}'")
        return

    print(f"--- Benchmarking {len(image_files)} Images (No Output Saving) ---")

    # ---------------- WARM-UP ----------------
    print(">>> Warm-up run")
    run_multiprocessing(image_files[:100], 1)
    print(">>> Warm-up complete\n")

    results_data = []
    baseline_mp = 0.0
    baseline_cf = 0.0

    print(f"{'Paradigm':<20} | {'Cores':<5} | {'Time(s)':<8} | {'Speedup':<8} | {'Efficiency':<10}")
    print("-" * 75)

    for paradigm in ['Multiprocessing', 'Concurrent.Futures']:
        for cores in CORE_COUNTS:
            time.sleep(1)

            start = time.time()
            if paradigm == 'Multiprocessing':
                run_multiprocessing(image_files, cores)
            else:
                run_concurrent_futures(image_files, cores)
            duration = time.time() - start

            # --- METRICS ---
            if paradigm == 'Multiprocessing':
                if cores == 1:
                    baseline_mp = duration
                speedup = baseline_mp / duration
            else:
                if cores == 1:
                    baseline_cf = duration
                speedup = baseline_cf / duration

            efficiency = speedup / cores

            print(f"{paradigm:<20} | {cores:<5} | {duration:<8.4f} | {speedup:<8.2f} | {efficiency:<10.2f}")
            results_data.append([
                paradigm, cores,
                round(duration, 4),
                round(speedup, 2),
                round(efficiency, 2)
            ])

    # --- SAVE CSV ---
    with open(RESULTS_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Paradigm', 'Cores', 'Time(s)', 'Speedup', 'Efficiency'])
        writer.writerows(results_data)

    print("\nBenchmark complete.")
    print(f"Results saved to '{RESULTS_FILE}'")

if __name__ == '__main__':
    main()
