# CST435-ASSIGNMENT-2

CST 435 ASSIGNMENT 2 INSTRUCTIONS
💻Phase 1: Prepare Files on Your Laptop
1.Create a clean folder on your laptop. Put these two things inside:
The create_balanced_subset.py file.( for creating subset:10 images from the food item folders in food-101 dataset folder)
The main_benchmark.py file.( for applying 5 filters and run python multiprocessing & concurrent.futures paradigm)
Edit the SOURCE_DATASET_ROOT = 'C:\\Users\\shivar\\OneDrive\\Desktop\\CST435 Assign2\\food-101\\food-101\\images' (change to path of food-101 images dataset)
2.Run create_balanced_subset file, dataset_subset folder created
3.Zip the folder and upload in Google drive
4.Get the Public Link:
Change "Restricted" to "Anyone with the link".
Click Copy Link.
5.Extract the File ID:
Paste the link in a notepad. It looks like:
https://drive.google.com/file/d/1A2b3C4d5-Example-ID-Here/view?usp=sharing
Copy only the ID: after d/ till /view
☁️ Phase 2: Create & Connect to GCP VM
1.Go to GCP Console > Compute Engine > VM Instances.
2.Create Instance:
Name: image-processing-node
Machine Type: e2-highcpu-8 (8 vCPUs, 8 GB memory).
Boot Disk: Ubuntu 20.04 LTS (Standard Persistent Disk 10GB storage).
Click Create.
Once running, click SSH to open the terminal.
3.Upload main_benchmark.py to SSH.
⚙️ Phase 3: Server Setup (Commands)
1.Step A: Update and Install System Tools
sudo apt update
sudo apt install python3-pip python3-venv unzip htop -y
2.Step B: Install the Google Drive Downloader
pip3 install gdown
📥 Phase 4: Download Files from Drive
1.Step A: Download the Zip
Replace YOUR_FILE_ID with the ID you copied in Phase 1.
gdown YOUR_FILE_ID
2.Step B: Unzip the subset
unzip dataset_subset.zip
3.Step C: Verify Files
Run ls -F. You should see:
dataset_subset/ (Folder)
main_benchmark.py (File)
🐍 Phase 5: Python Setup (Manual Installation)
1.Step A: Create Virtual Environment
python3 -m venv venv
2.Step B: Activate Virtual Environment
source venv/bin/activate
3.Step C: Manually Install Libraries
We need numpy and the "headless" version of OpenCV (since there is no monitor).
pip install numpy opencv-python-headless
🚀 Phase 6: Run the Program
1.Run the benchmark.
python main_benchmark.py
2.In Window 2, type:
htop
3.What to observe for Bottlenecks:
Green Bars: CPU is working hard (Good).
Bars Drop/Empty: CPU is idle (Bad).
The Bottleneck Moment: If the Python script is still running (timer is ticking) but the CPU bars in htop suddenly drop to 0-10%, that is the bottleneck. The CPU has stopped working because it is waiting for the Hard Drive to finish saving the image.
📊 Summary of Phase 6 Output
1.The terminal will show the Speedup/Efficiency table.
2.A file performance_results.csv will be created.
3.A folder processed_images/ will be created.
