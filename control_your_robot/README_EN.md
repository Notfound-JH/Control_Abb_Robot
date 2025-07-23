[![中文](https://img.shields.io/badge/中文-简体-blue)](./README.md)  
[![English](https://img.shields.io/badge/English-English-green)](./README_EN.md)

# Control Your Robot!
This project aims to help you quickly get started with a complete pipeline from controlling robotic arms, to data collection, and finally to training and deploying VLA models after entering the field of embodied intelligence.

## 🚀 Robot Control Development Progress

### 📅 Update Log
| Date       | Update Description                     | Status       |
|------------|--------------------------------------|--------------|
| 2025.5.27  | 🧪 Added and improved test samples for easier debugging and reference | ✅ Released   |
| 2025.5.26  | 💻 Client-server communication implemented for remote inference and local control | ✅ Released   |
| 2025.5.22  | 🎭 Integrated general Planner and general IK solver | ✅ Released   |
| 2025.5.10  | 🎭 Hybrid VLA, OpenVLA-oft on the way | ❌ Testing, to be released |
| 2025.4.10  | 🎮 Teleoperation device interface wrapped, pika device support | ✅ Released   |
| 2025.4.3   | 🤖 Agilex chassis control and ROS interface wrapped | ✅ Released   |
| 2025.3.25  | 🦾 Agilex robotic arm support | ✅ Released   |
| 2025.3.10  | 🏗️ RealMan robotic arm support | ✅ Released   |
| 2025.2.15  | 📊 General data collection pipeline completed | ✅ Released   |
| 2024.12.1  | 🧠 Standardized VLA model training framework | ✅ Released   |

### 🛣️ In Progress
- [✅] ⛓️‍💥 Separate controller and model inference, support remote deployment and local multi-script synchronization to solve environment compatibility issues
- [✅] 🔢 Efficient IK solver wrapper for curobo (requires URDF support)
- [ ] 🕹️ Example for pika teleoperation control of arbitrary robotic arms
- [ ] 📦 More controller and sensor support
- [ ] 🧩 More robot model integration

### 🤖 Device Support Status

#### 🎛️ Controllers
**✅ Implemented**
| Robotic Arm    | Chassis           | Dexterous Hand | Others    |
|----------------|-------------------|----------------|-----------|
| Agilex Piper   | Agilex Tracer2.0  | 🚧 In development | 📦 To be added |
| RealMan 65B    | 📦 To be added     | 📦 To be added  | 📦 To be added |
| daran aloha    | 📦 To be added     | 📦 To be added  | 📦 To be added |

**🚧 Preparing Support**
| Robotic Arm    | Chassis           | Dexterous Hand | Others    |
|----------------|-------------------|----------------|-----------|
| JAKA           | 📦 To be added     | 📦 To be added  | 📦 To be added |
| Franka         | 📦 To be added     | 📦 To be added  | 📦 To be added |
| UR5e           | 📦 To be added     | 📦 To be added  | 📦 To be added |

#### 📡 Sensors
**✅ Implemented**
| Vision Sensors    | Tactile Sensors   | Other Sensors |
|-------------------|-------------------|---------------|
| RealSense D435    | 🚧 In development  | 📦 To be added |

**🚧 Preparing Support**
If you need support for new sensors, please submit an issue or feel free to PR your sensor configuration!

## Setup Basic Environment
```bash
conda create -n my_robot python==3.10
conda activate my_robot
git clone git@github.com:Tian-Nian/control_your_robot.git
cd control_your_robot
pip install -r requirements.txt

# (Optional) Compile latest lerobot
cd ..
git clone https://github.com/huggingface/lerobot.git
cd lerobot
conda install ffmpeg
pip install --no-binary=av -e .

# (Optional) Install Python packages required by your robotic arm
pip install piper_sdk
pip install Robotic_Arm

# For model training, RDT and openpi have their own environment requirements
# Please use the respective model environments, then execute:
cd ~/control_your_robot/
pip install -r requirements.txt

# Agilex robotic arm SDK reference: https://github.com/agilexrobotics
# RealMan robotic arm SDK reference: https://develop.realman-robotics.com/robot/summarize/
# daran robotic arm SDK reference:
# If any robotic arm involves compiling or linking native code, these will be placed under ./third_party/ directory
```

## Folder Structure
| Directory         | Description                 | Main Contents                               |
|-------------------|-----------------------------|---------------------------------------------|
| **📂 controller**  | Robot controller wrappers    | Control classes for robotic arms, chassis, etc. |
| **📂 sensor**      | Sensor wrappers             | Currently only RealSense camera wrapper     |
| **📂 utils**       | Utility functions           | Helper functions like math, logging, etc.   |
| **📂 data**        | Data collection module      | Classes for data recording and processing    |
| **📂 my_robot**    | Robot integration wrapper   | Classes combining the full robot system      |
| **📂 policy**      | VLA model policies          | Vision-Language-Action model related code    |
| **📂 scripts**     | Instantiation scripts       | Main entry points, test codes                 |
| **📂 third_party** | Third-party dependencies    | External libraries requiring compilation     |
| **📂 planner**     | Path planning module        | curobo planner wrapper + simulated robot arm code |
| **📂 example**     | Example codes              | Data collection, model deployment examples    |
| **📂 docs**        | Documentation index         | Robot-related documentation links             |

## How to Control Your Robot?
This project categorizes robot parts into two types:  
`controller`: Components with control functions, such as robotic arms, dexterous hands, chassis, etc.  
`sensor`: Components only for information acquisition, such as vision sensors, tactile sensors.  

If your actuators and sensors are already in controller/sensor, you can simply call them. Otherwise, please submit an issue, and we will try to collect that robotic arm and adapt it. If you want to implement it yourself, refer to developer_README.md. Contributions for new adaptations are welcome!

**Note!**  
We expect the robotic arm joint angles to be in radians, i.e., [-pi, pi]. The gripper values are normalized opening degrees [0,1]. The end-effector 6D coordinates x,y,z are in meters; rx, ry, rz are in radians. Control and data acquisition units should be consistent.

After confirming that your required components are defined, follow the examples in `my_robot` to assemble your robot.  
After assembly, write an example to verify if key functions are implemented correctly:
```python
if __name__=="__main__":
    import time
    robot = PiperSingle()
    # Data collection test
    data_list = []
    for i in range(100):
        print(i)
        data = robot.get()
        robot.collect(data)
        time.sleep(0.1)
    robot.finish()
    # Motion test
    move_data = {
        "left_arm": {
            "qpos": [0.057, 0.0, 0.216, 0.0, 0.085, 0.0],
            "gripper": 0.2,
        },
    }
    robot.move(move_data)
```

## How to Collect Data
Your robot implementation should have a `self.collection = CollectAny()` to facilitate saving collected data based on configuration.  
A data collection example is provided in `example/collect`, which you can refer to. If you have passed the basic data collection test above, just replace the robot with yours.

If you don't have teleoperation devices, you may consider using the script `scripts/collect_omving_skpt.py` for trajectory collection and reproduction.  
Some devices may not allow multiple scripts to communicate; in that case, refer to comments in the script for multi-threaded data collection.

## How to Convert Data
Scripts for converting to lerobot format and RDT-compatible hdf5 format are provided in `scripts/`. For single or dual arm, follow respective file instructions to map parameters correctly.  

### RDT hdf5 format  
This conversion is for single tasks by default. Convert tasks one by one, e.g., for `datasets/task_1/episode_*.hdf5` run:  
```bash
python scripts/convert2rdt_hdf5.py datasets/task_1
# To customize output location
python scripts/convert2rdt_hdf5.py datasets/task_1 your_output_path
```
By default, outputs save under `datasets/RDT/`.

### openpi lerobot format
**Note**  
Converting to openpi lerobot format requires first converting to RDT hdf5 format. This conversion does not require configuring the RDT environment!

After converting to RDT hdf5, move the corresponding task's instruction file into the task folder and rename it to `instructions.json`, for example:  
`datasets/RDT/task_1/instructions.json`  

If multiple tasks exist, organize as:  
```bash
datasets/  
├── RDT  
│   ├── my_task
│   │   ├── task_1
│   │   │   ├── instructions.json  
│   │   │   ├── episode_0.hdf5  
│   │   │   ├── episode_1.hdf5  
│   │   │   ├── ...  
│   │   ├── task_2
│   │   ├── ...
```
Run:
```bash
python scripts/convert2openpi.py --raw_dir datasets/my_task --repo_id your_repo_id
```

### lerobot 2.0 version
We support converting your data to the latest lerobot dataset format and multi-task dataset generation!  
For multi-task, arrange data similarly to the openpi format, but with original collected data (not RDT hdf5).  
```bash
datasets/  
├── my_task
│   ├── task_1
│   │   ├── config.json  
│   │   ├── episode_0.hdf5  
│   │   ├── episode_1.hdf5  
│   │   ├── ...  
│   ├── task_2
│   ├── ...
```
```bash
# Single task
python scripts/convert2lerobot.py datasets/task_1 repo_id 
# Multi-task
python scripts/convert2lerobot.py datasets/my_task repo_id True
```
### TFDS data format
**Note**  
Similar to lerobot, you must first convert to RDT-compatible hdf5 format!  

TFDS conversion is special; see some examples in `./policy/rlds_dataset_builder`.  
The required structure is:
```bash
├── ${my_dataset_example}
│   ├── ${my_dataset_example}_dataset_builder
│   │   ├── class ${my_dataset_example}
│   ├── CITATION.bib
│   ├── __init__.py   
```
`__init__.py` and `CITATION.bib` can be copied as is.

## How to Train Models
The `policy/` folder provides official training scripts for `openpi` and `RDT`, modified for ease of use with detailed instructions. Please configure accordingly.  

### RDT
Move generated `datasets/RDT/my_task` manually under `policy/RDT/training_data/`!  
Do not use `ln -s` because `os.walk` won't follow symlinks causing errors.

After converting to RDT hdf5, encode the language instructions for each task:  
```bash
cd policy/RDT
python scripts/encode_lang_batch_once.py task_name output_dir gpu_id
# Example:
python scripts/encode_lang_batch_once.py task_1 ./training_data/task_1 0
```

### openpi
Note that openpi requires not lerobot 2.0 data; using lerobot 2.0 will cause data reading errors!  
After generating openpi data, follow instructions in `policy/openpi/README.md`. Remember to distinguish single vs dual arm.

## How to Deploy Models
Deployment scripts are available in `example/deploy`, though minor modifications might be needed for different robotic arms.

If local devices don't support inference, this project supports an excellent client-server mechanism. Run `scripts/client.py` and `scripts/server.py`, modify IP and port, and replace robot and model with yours.
