import os
from ..obs.get_path_obs import get_dataset_path_obs, get_pretrain_model_path_obs, get_output_path_obs
from ..minio.get_path_minio import get_dataset_path_minio, get_pretrain_model_path_minio, get_output_path_minio

def get_dataset_path(
    dataset_name: str = "",
):
    """
    获取数据集路径
    """
    if os.getenv("STORAGE_LOCATION") is None:
        raise ValueError("Failed to get the environment variable, please make sure the STORAGE_LOCATION environment variable has been set")
    if os.getenv("STORAGE_LOCATION") == "obs":
        return get_dataset_path_obs(dataset_name)
    return get_dataset_path_minio(dataset_name)

def get_pretrain_model_path(
    pretrain_model_name: str = "",
):
    """
    获取预训练模型路径
    """
    if os.getenv("STORAGE_LOCATION") is None:
        raise ValueError("Failed to get the environment variable, please make sure the STORAGE_LOCATION environment variable has been set.")
    if os.getenv("STORAGE_LOCATION") == "obs":
        return get_pretrain_model_path_obs(pretrain_model_name)
    return get_pretrain_model_path_minio(pretrain_model_name)

def get_output_path():
    """
    获取输出路径
    """
    if os.getenv("STORAGE_LOCATION") is None:
        raise ValueError("Failed to get the environment variable, please make sure the STORAGE_LOCATION environment variable has been set.")
    if os.getenv("STORAGE_LOCATION") == "obs":
        return get_output_path_obs()
    return get_output_path_minio()

