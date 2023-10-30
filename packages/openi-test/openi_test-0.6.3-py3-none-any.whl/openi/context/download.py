import os
from .env_check import openi_multidataset_to_env, c2net_multidataset_to_env, pretrain_to_env, obs_copy_folder

def download_dataset_obs():
    cluster = os.getenv("CLUSTER")
    dataset_url = os.getenv("DATASET_URL")
    dataset_path = os.getenv("DATASET_PATH")
    if cluster is None or dataset_url is None or dataset_path is None:
    		raise ValueError("环境变量设置失败，请确保设置了 DATASET_URL 和 DATASET_PATH 环境变量。")
    else:
        if not os.path.exists(dataset_path):
            os.makedirs(dataset_path)
    if dataset_url != "":                         
        if cluster == "C2Net":
                c2net_multidataset_to_env(dataset_url, dataset_path)
        else:
                openi_multidataset_to_env(dataset_url, dataset_path)
    return dataset_path

def download_pretrain_model_obs():
    pretrain_model_url = os.getenv("PRETRAIN_MODEL_URL")
    pretrain_model_path= os.getenv("PRETRAIN_MODEL_PATH")
    if pretrain_model_url is None or pretrain_model_path is None:
    		raise ValueError("环境变量设置失败，请确保设置了 PRETRAIN_MODEL_URL、PRETRAIN_MODEL_PATH环境变量。")
    else:
        if not os.path.exists(pretrain_model_path):
            os.makedirs(pretrain_model_path) 
    if pretrain_model_url != "":             
        pretrain_to_env(pretrain_model_url, pretrain_model_path)
    return pretrain_model_path

def download_dataset_minio():
    dataset_path = os.getenv("DATASET_PATH")
    if dataset_path is None:
    		raise ValueError("环境变量获取失败，请确保设置了DATASET_PATH环境变量。")
    return dataset_path
    
def download_pretrain_model_minio():
    pretrain_model_path = os.getenv("PRETRAIN_MODEL_PATH")
    if pretrain_model_path is None:
    		raise ValueError("环境变量获取失败，请确保设置了PRETRAIN_MODEL_PATH环境变量。")
    return pretrain_model_path     

def download_dataset():
    if os.getenv("STORAGE_LOCATION") is None:
            raise ValueError("环境变量设置失败，请确保设置了STORAGE_LOCATION环境变量。")
    if os.getenv("STORAGE_LOCATION") == "obs":
            return download_dataset_obs()
    return download_dataset_minio()

def download_pretrain_model():
    if os.getenv("STORAGE_LOCATION") is None:
            raise ValueError("环境变量设置失败，请确保设置了STORAGE_LOCATION环境变量。")
    if os.getenv("STORAGE_LOCATION") == "obs":
            return download_pretrain_model_obs()
    return download_pretrain_model_minio()