DEBUG=False

task_name=${1}
train_config_name=${2} 
model_name=${3}
checkpoint_num=${4}
gpu_id=${5}
save_images=${6:-false}  # Default to false if not provided

export CUDA_VISIBLE_DEVICES=${gpu_id}

# Build command with optional arguments
cmd="python ./scripts/run_single.py $task_name $train_config_name $model_name $checkpoint_num"

# Add optional flags if enabled
if [ "$save_images" = "true" ]; then
    cmd="$cmd --save_images"
    echo "Image saving enabled"
fi

source .venv/bin/activate
cd ../..
echo "Running: $cmd"
$cmd