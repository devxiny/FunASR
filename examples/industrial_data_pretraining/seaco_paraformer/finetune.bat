@echo off
REM Copyright FunASR (https://github.com/alibaba-damo-academy/FunASR). All Rights Reserved.
REM  MIT License  (https://opensource.org/licenses/MIT)

set "workspace=%cd%"

REM which gpu to train or finetune
set "CUDA_VISIBLE_DEVICES=0"
for /f "tokens=1,* delims=," %%a in ("%CUDA_VISIBLE_DEVICES%") do set /a "gpu_num=1"

REM model_name from model_hub, or model_dir in local path

REM option 1, download model automatically
set "model_name_or_model_dir=iic/speech_seaco_paraformer_large_asr_nat-zh-cn-16k-common-vocab8404-pytorch"

REM data dir, which contains: train.json, val.json
set "data_dir=dataset"

set "train_data=%data_dir%\train.jsonl"
set "val_data=%data_dir%\val.jsonl"

REM exp output dir
set "output_dir=.\outputs"
set "log_file=%output_dir%\log.txt"

if not exist "%output_dir%" mkdir "%output_dir%"
echo log_file: %log_file%

REM Set default values for distributed training arguments
if not defined WORLD_SIZE set "WORLD_SIZE=1"
if not defined RANK set "RANK=0"
if not defined MASTER_ADDR set "MASTER_ADDR=127.0.0.1"
if not defined MASTER_PORT set "MASTER_PORT=26669"

set "DISTRIBUTED_ARGS=--nnodes %WORLD_SIZE% --nproc_per_node %gpu_num% --node_rank %RANK% --master_addr %MASTER_ADDR% --master_port %MASTER_PORT%"

echo %DISTRIBUTED_ARGS%

torchrun %DISTRIBUTED_ARGS% ^
funasr\bin\train_ds.py ^
++model="%model_name_or_model_dir%" ^
++train_data_set_list="%train_data%" ^
++valid_data_set_list="%val_data%" ^
++dataset="AudioDatasetHotword" ^
++dataset_conf.index_ds="IndexDSJsonl" ^
++dataset_conf.data_split_num=1 ^
++dataset_conf.batch_sampler="BatchSampler" ^
++dataset_conf.batch_size=6000 ^
++dataset_conf.sort_size=1024 ^
++dataset_conf.batch_type="token" ^
++dataset_conf.num_workers=4 ^
++train_conf.max_epoch=500 ^
++train_conf.log_interval=1 ^
++train_conf.resume=true ^
++train_conf.validate_interval=2000 ^
++train_conf.save_checkpoint_interval=2000 ^
++train_conf.avg_keep_nbest_models_type='loss' ^
++train_conf.keep_nbest_models=20 ^
++train_conf.avg_nbest_model=10 ^
++train_conf.use_deepspeed=false ^
++train_conf.deepspeed_config=%deepspeed_config% ^
++train_conf.find_unused_parameters=true ^
++optim_conf.lr=0.0001 ^
++output_dir="%output_dir%" > "%log_file%" 2>&1