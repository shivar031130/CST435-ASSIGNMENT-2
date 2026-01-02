# CST 435 Assignment 2 — Parallel Image Processing Benchmark

## Project Overview

This project demonstrates **parallel image processing** using Python, applied to the **Food-101 dataset**, and benchmarked on **Google Cloud Platform (GCP)**. The goal is to evaluate and compare two parallel programming paradigms: **multiprocessing** and **concurrent.futures**, in terms of execution time, speedup, and efficiency.

The project implements a full **image processing pipeline** consisting of five filters applied to individual images:

1. Grayscale conversion
2. Gaussian blur
3. Sobel edge detection
4. Image sharpening
5. Brightness adjustment

All processing is CPU-bound, and output images are **not saved** to capture only real CPU parallelism.

### **1. Dataset Preparation**

* The `create_balanced_subset.py` script:

  * Traverses all category folders in Food-101
  * Randomly selects **50 images per category**
  * Copies images into a single flat directory
  * Renames files to avoid conflicts
* Produces a **balanced subset** of ~5050 images.

**Sample code snippet:**

```python
selected_images = random.sample(images, min(len(images), IMAGES_PER_CATEGORY))
for i, image_file in enumerate(selected_images):
    new_filename = f"{category}_{i+1:03d}.jpg"
    shutil.copy2(src_path, os.path.join(DEST_DIR, new_filename))
```

---

### **2. Benchmark Controller**

* `main_benchmark.py` executes the parallel image processing pipeline
* Worker function applies **all five filters** per image
* Two parallel paradigms:

  * **Multiprocessing** (`multiprocessing.Pool`)
  * **Concurrent.Futures** (`ProcessPoolExecutor`)
* Supports multiple core counts: **1, 2, 4, 8**
* Includes a **warm-up run** to preload libraries and OS caches
* Stores results in `performance_results.csv`

**Sample worker function:**

```python
def process_single_image(file_path):
    img = cv2.imread(file_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    sobel_x = cv2.Sobel(blur, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(blur, cv2.CV_64F, 0, 1, ksize=3)
    sharpened = cv2.filter2D(blur, -1, np.array([[0,-1,0],[-1,5,-1],[0,-1,0]]))
    final_result = cv2.add(sharpened, np.ones(sharpened.shape, dtype="uint8") * 30)
    return 1
```

---

## **Experimental Setup**

### **Hardware**

* GCP VM: e2-highcpu-8 (8 vCPUs, 8 GB RAM)
* Disk: 10 GB Standard Persistent Disk
* OS: Ubuntu 20.04 LTS
* Local machine: Laptop with access to Food-101 dataset

### **Software**

* Python 3.11 (virtual environment)
* Libraries: OpenCV (headless), NumPy, multiprocessing, concurrent.futures, gdown
* CSV handling: Python built-in module

### **Configuration**

* Input dataset folder: `dataset_subset` (5050 images)
* Parallel core counts: 1, 2, 4, 8
* Warm-up run: 100 images on 1 core
* Output disabled to reduce I/O interference
* Benchmark metrics: execution time, speedup, efficiency

---

## **Run Instructions**

### **Phase 1: Prepare Files Locally**

1. Create a clean folder and add:

   * `create_balanced_subset.py`
   * `main_benchmark.py`
2. Edit the `SOURCE_DATASET_ROOT` in `create_balanced_subset.py` to point to your Food-101 dataset.
3. Run the subset creation script:

```bash
python create_balanced_subset.py
```

4. Verify the `dataset_subset` folder is created with ~5050 images.
5. Zip the folder and upload it to **Google Drive**.
6. Copy the **file ID** from the public link.

---

### **Phase 2: Setup GCP VM**

1. Create a VM instance:

   * Name: `image-processing-node`
   * Machine type: e2-highcpu-8
   * OS: Ubuntu 20.04 LTS
   * Boot disk: 10 GB Standard Persistent Disk
2. Connect via SSH in GCP Console.
3. Upload `main_benchmark.py` to the VM using SSH/SCP.

---

### **Phase 3: Configure VM Environment**

```bash
sudo apt update
sudo apt install python3-pip python3-venv unzip htop -y
python3 -m venv venv
source venv/bin/activate
pip install numpy opencv-python-headless gdown
```

---

### **Phase 4: Download Dataset from Drive**

```bash
gdown <FILE_ID>
unzip dataset_subset.zip
ls -F  # Verify dataset_subset/ and main_benchmark.py are present
```

---

### **Phase 5: Run Benchmark**

```bash
python main_benchmark.py
```

* CPU utilization can be monitored in a second terminal using:

```bash
htop
```

* Observe execution time, speedup, and efficiency for different cores.
* Results will be saved in `performance_results.csv`.

---

## **Key Notes**

* Warm-up run ensures consistent benchmarking results.
* Output is disabled to reduce I/O bottlenecks.
* Core counts allow testing both low and high parallel workloads.
* The design ensures a fair comparison between **multiprocessing** and **concurrent.futures**.

