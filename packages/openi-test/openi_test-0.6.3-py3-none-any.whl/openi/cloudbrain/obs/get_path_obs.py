import os
from .env_check import openi_multidataset_to_env, c2net_multidataset_to_env, pretrain_to_env, obs_copy_folder

def get_dataset_path_obs(
    dataset_name: str,
):
    cluster = os.getenv("CLUSTER")
    dataset_url = os.getenv("DATASET_URL")
    dataset_path = os.getenv("DATASET_PATH")
    if cluster is None or dataset_url is None or dataset_path is None:
    		raise ValueError("环境变量设置失败，请确保设置了 DATASET_URL 和 DATASET_PATH 环境变量。")
    else:
        if not os.path.exists(dataset_path):
            os.makedirs(dataset_path)
    if dataset_name != "":
        return os.path.join(dataset_path, dataset_name)           
    return dataset_path

def get_pretrain_model_path_obs(
    pretrain_model_name: str,
):
    pretrain_model_url = os.getenv("PRETRAIN_MODEL_URL")
    pretrain_model_path= os.getenv("PRETRAIN_MODEL_PATH")
    if pretrain_model_url is None or pretrain_model_path is None:
    		raise ValueError("环境变量设置失败，请确保设置了 PRETRAIN_MODEL_URL、PRETRAIN_MODEL_PATH环境变量。")
    else:
        if not os.path.exists(pretrain_model_path):
            os.makedirs(pretrain_model_path)      
    if pretrain_model_name != "":
        return os.path.join(pretrain_model_path, pretrain_model_name)                    
    return pretrain_model_path

def get_output_path_obs():
    output_path = os.getenv("OUTPUT_PATH")
    if output_path is None:
    		raise ValueError("环境变量获取失败，请确保设置了OUTPUT_PATH环境变量。")
    else:
        if not os.path.exists(output_path):
            os.makedirs(output_path)            
    return output_path 

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
    
def upload_output_obs():
    cluster = os.getenv("CLUSTER")
    output_path = str(os.getenv("OUTPUT_PATH"))
    output_url = str(os.getenv("OUTPUT_URL"))
    if output_url is None or output_path is None:
    		raise ValueError("环境变量设置失败，请确保设置了 OUTPUT_URL、OUTPUT_PATH环境变量。")
    else:
        if not os.path.exists(output_path):
            os.makedirs(output_path) 
    if output_url != "":             
        if cluster == "C2Net":
                obs_copy_folder(output_path, output_url)
        else:
                obs_copy_folder(output_path, output_url)
    return  output_path  

     