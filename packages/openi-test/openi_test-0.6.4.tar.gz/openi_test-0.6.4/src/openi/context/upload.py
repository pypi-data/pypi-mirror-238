import os
from .env_check import obs_copy_folder

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

def upload_output_minio():
    output_path = os.getenv("OUTPUT_PATH")
    if output_path is None:
    		raise ValueError("环境变量设置失败，请确保设置了OUTPUT_PATH环境变量。")
    return output_path      

def upload_output():
    """
    推送输出结果到启智平台
    """
    if os.getenv("STORAGE_LOCATION") is None:
        raise ValueError("Failed to get the environment variable, please make sure the STORAGE_LOCATION environment variable has been set.")
    if os.getenv("STORAGE_LOCATION") == "obs":
            return upload_output_obs()
    return upload_output_minio()
 