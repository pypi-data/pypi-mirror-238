import os
from .env_check import openi_multidataset_to_env, c2net_multidataset_to_env, pretrain_to_env, obs_copy_folder

def download_dataset_obs():
    cluster = os.getenv("CLUSTER")
    dataset_url = os.getenv("DATASET_URL")
    dataset_path = os.getenv("DATASET_PATH")
    if cluster is None or dataset_url is None or dataset_path is None:
                raise ValueError(f'Failed to obtain environment variables. Please set the CLUSTER, DATASET_URL and DATASET_PATH environment variables.')
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
        raise ValueError(f'Failed to obtain environment variables. Please set the PRETRAIN_MODEL_URL and PRETRAIN_MODEL_PATH environment variables.')
    else:
        if not os.path.exists(pretrain_model_path):
            os.makedirs(pretrain_model_path) 
    if pretrain_model_url != "":             
        pretrain_to_env(pretrain_model_url, pretrain_model_path)
    return pretrain_model_path

def download_dataset_minio():
    dataset_path = os.getenv("DATASET_PATH")
    if dataset_path is None:
        raise ValueError(f'Failed to obtain environment variables. Please set the DATASET_PATH environment variables.')
    print(f'the dataset is mounted on {dataset_path}.')                
    return dataset_path
    
def download_pretrain_model_minio():
    pretrain_model_path = os.getenv("PRETRAIN_MODEL_PATH")
    if pretrain_model_path is None:
        raise ValueError(f'Failed to obtain environment variables. Please set the PRETRAIN_MODEL_PATH environment variables.')
    print(f'the pretrain model is mounted on {pretrain_model_path}.')  
    return pretrain_model_path     

def get_output_path_minio():	   	
    output_path = os.getenv("OUTPUT_PATH")	
    if output_path is None:	
        raise ValueError(f'Failed to obtain environment variables. Please set the OUTPUT_PATH environment variables.')
    print(f'please set the output location to {output_path}.')
    return output_path

def get_output_path_obs():	
    output_path = os.getenv("OUTPUT_PATH")	
    if output_path is None:	
        raise ValueError(f'Failed to obtain environment variables. Please set the OUTPUT_PATH environment variables.')
    else:	
        if not os.path.exists(output_path):	
            os.makedirs(output_path)     
    print(f'please set the output location to {output_path}.')
    return output_path 	

def download_dataset():
    if os.getenv("STORAGE_LOCATION") is None:
        raise ValueError(f'Failed to obtain environment variables. Please set the STORAGE_LOCATION environment variables.')
    if os.getenv("STORAGE_LOCATION") == "obs":
            return download_dataset_obs()
    return download_dataset_minio()

def download_pretrain_model():
    if os.getenv("STORAGE_LOCATION") is None:
        raise ValueError(f'Failed to obtain environment variables. Please set the STORAGE_LOCATION environment variables.')
    if os.getenv("STORAGE_LOCATION") == "obs":
            return download_pretrain_model_obs()
    return download_pretrain_model_minio()

def get_output_path():
        if os.getenv("STORAGE_LOCATION") is None:
                raise ValueError(f'Failed to obtain environment variables. Please set the STORAGE_LOCATION environment variables.')
        if os.getenv("STORAGE_LOCATION") == "obs":
                return get_output_path_obs()
        return get_output_path_minio()