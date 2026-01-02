Here is your **clean, properly formatted Markdown version** of the **CST 435 Assignment 2 Instructions**.
You can **directly save this as `README.md`** or include it as an **Instructions section** in your repository.

---

````markdown
# CST 435 – Assignment 2 Instructions
## Parallel Image Processing on Google Cloud Platform

---

## 💻 Phase 1: Prepare Files on Your Laptop

### 1. Create Project Folder
Create a clean folder on your laptop and place the following files inside:

- `create_balanced_subset.py`  
  *(Creates a balanced subset of images from the Food-101 dataset)*

- `main_benchmark.py`  
  *(Applies 5 image filters and runs Python `multiprocessing` and `concurrent.futures` paradigms)*

### 2. Configure Dataset Path
Edit the following line in `create_balanced_subset.py` to match your local Food-101 dataset location:

```python
SOURCE_DATASET_ROOT = "path/to/food-101/images"
````

### 3. Generate Dataset Subset

Run the script:

```bash
python create_balanced_subset.py
```

A folder named `dataset_subset/` will be created.

### 4. Upload to Google Drive

* Zip the project folder
* Upload it to Google Drive
* Change sharing from **Restricted** to **Anyone with the link**
* Click **Copy Link**

### 5. Extract Google Drive File ID

Paste the copied link into a text editor. Example:

```
https://drive.google.com/file/d/1A2b3C4d5-Example-ID-Here/view?usp=sharing
```

Copy only the **File ID** (between `/d/` and `/view`).

---

## ☁️ Phase 2: Create & Connect to GCP VM

### 1. Create Virtual Machine

Navigate to:

```
GCP Console → Compute Engine → VM Instances
```

Create a new instance with the following configuration:

* **Name:** `image-processing-node`
* **Machine Type:** `e2-highcpu-8` (8 vCPUs, 8 GB RAM)
* **Boot Disk:** Ubuntu 20.04 LTS
* **Storage:** 10 GB Standard Persistent Disk

Click **Create**.

### 2. Connect via SSH

Once the VM is running, click **SSH** to open the terminal.

### 3. Upload Files

Upload `main_benchmark.py` to the VM using SSH or SCP.

---

## ⚙️ Phase 3: Server Setup

### Step A: Update and Install System Tools

```bash
sudo apt update
sudo apt install python3-pip python3-venv unzip htop -y
```

### Step B: Install Google Drive Downloader

```bash
pip3 install gdown
```

---

## 📥 Phase 4: Download Files from Google Drive

### Step A: Download the Zip File

Replace `YOUR_FILE_ID` with your actual file ID:

```bash
gdown YOUR_FILE_ID
```

### Step B: Unzip Dataset

```bash
unzip dataset_subset.zip
```

### Step C: Verify Files

```bash
ls -F
```

Expected output:

```
dataset_subset/
main_benchmark.py
```

---

## 🐍 Phase 5: Python Setup (Manual Installation)

### Step A: Create Virtual Environment

```bash
python3 -m venv venv
```

### Step B: Activate Virtual Environment

```bash
source venv/bin/activate
```

### Step C: Install Required Libraries

```bash
pip install numpy opencv-python-headless
```

---

## 🚀 Phase 6: Run the Program

### 1. Execute the Benchmark

```bash
python main_benchmark.py
```

### 2. Monitor CPU Utilization

Open a second terminal window and run:

```bash
htop
```

### 3. Observe Bottlenecks

* **Green CPU bars:** CPU is actively processing (Good)
* **Low or empty bars:** CPU is idle (Bad)
* **Bottleneck moment:**
  If the program is still running but CPU usage suddenly drops to 0–10%, the system is waiting on I/O operations.

---

## 📊 Summary of Phase 6 Output

* Terminal displays **Execution Time, Speedup, and Efficiency**
* A CSV file named `performance_results.csv` is generated

---

## ✅ End of Instructions

```

---

If you want, I can:
- Add **screenshots placeholders**
- Convert this into a **PDF submission version**
- Align wording exactly to **CST435 rubric**

Just let me know 👍
```
