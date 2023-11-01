import os
from .env_check import obs_copy_folder

def upload_output_obs():
    cluster = os.getenv("CLUSTER")
    output_path = str(os.getenv("OUTPUT_PATH"))
    output_url = str(os.getenv("OUTPUT_URL"))
    if output_url is None or output_path is None:
        raise ValueError(f'Failed to obtain environment variables. Please set the CLUSTER, OUTPUT_URL and OUTPUT_PATH environment variables.')
    else:
        if not os.path.exists(output_path):
            os.makedirs(output_path) 
    if output_url != "":             
        if cluster == "C2Net":
                obs_copy_folder(output_path, output_url)
        else:
                obs_copy_folder(output_path, output_url)
    print(f'upload {output_path} to openi')
    return  output_path  

def upload_output_minio():
    output_path = os.getenv("OUTPUT_PATH")
    if output_path is None:
        raise ValueError(f'Failed to obtain environment variables. Please set the OUTPUT_PATH environment variables.')
    print(f'upload {output_path} to openi')            
    return output_path      

def upload_output():
    """
    upload output to openi
    """
    if os.getenv("STORAGE_LOCATION") is None:
        raise ValueError("Failed to get the environment variable, please make sure the STORAGE_LOCATION environment variable has been set.")
    if os.getenv("STORAGE_LOCATION") == "obs":
            return upload_output_obs()
    return upload_output_minio()
 