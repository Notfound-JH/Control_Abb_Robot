[![中文](https://img.shields.io/badge/中文-简体-blue)](./README.md)  
[![English](https://img.shields.io/badge/English-English-green)](./README_EN.md)

## How to Train with OpenPI
 
### 1. Data Collection  
You can collect data using the provided API and store it with the `CollectAny` utility, or use your own pre-collected dataset.

### 2. Data Format Conversion  
For data collected with `CollectAny`, there are scripts available to convert it into the `lerobot` format.  
- If you are working with a **single-arm** robot, it is recommended to use the **libero** format for training.  
- For **dual-arm** robots, use the **aloha** format.

### 3. Select Your Config  
In `src/openpi/training/config.py`, choose the training configuration that fits your scenario: single-arm / dual-arm, base / fast, full / lora.  
- Set `repo_id` to match the ID used during your data conversion.  
- Adjust parameters such as:  
  - `batch_size`: Total training batch size. Larger batch sizes require more GPU memory. We recommend starting with 32 for good performance.  
  - `num_train_steps`: 30,000 steps typically suffice for convergence; you can increase this if you want more training.  
  - `fsdp_devices`: If a single GPU doesn’t have enough memory, you can use multiple GPUs. Note that FSDP splits a single model across GPUs, **not** one model per GPU.

#### Important!  
Verify the action dimension your robotic arm requires, and update the policy’s output dimension accordingly.  
- For a 7+1 DOF single-arm robot, use the first 8 outputs of the `libero` policy.  
- For dual-arm, use the first 16 outputs of the `aloha` policy.

### 4. Run Training  
Start training by running `finetune.sh`:  
- `your_train_config_name` refers to a key in the `_CONFIGS` dictionary in `config.py`.  
- `your_model_name` is an arbitrary name used for wandb logging and saved models.  
- `gpu_id` specifies which GPU(s) to use; for a single GPU, use `0`.  

Example:  
```bash
bash finetune.sh pi0_single_base_full my_model 0,1,2
