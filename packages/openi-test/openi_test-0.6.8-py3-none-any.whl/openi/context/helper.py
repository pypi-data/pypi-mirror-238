import os
import emoji
import json
import moxing as mox

def openi_dataset_to_env(data_url, data_dir):
    """
    openi copy single dataset to training image 
    """
    try:     
        mox.file.copy_parallel(data_url, data_dir)
        print(f'{emoji.emojize(":thumbs_up:")} Successfully Download {data_url} to {data_dir}.')
    except Exception as e:
        print(f'❌ moxing download {data_url} to {data_dir} failed.')
    return 

def openi_multidataset_to_env(multi_data_url, data_dir):
    """
    copy single or multi dataset to training image 
    """
    multi_data_json = json.loads(multi_data_url)  
    for i in range(len(multi_data_json)):
        path = data_dir + "/" + multi_data_json[i]["dataset_name"]
        if not os.path.exists(path):
            os.makedirs(path)
        try:
            mox.file.copy_parallel(multi_data_json[i]["dataset_url"], path) 
            print(f'{emoji.emojize(":thumbs_up:")} Successfully Download {multi_data_json[i]["dataset_url"]} to {path}.')
        except Exception as e:
            print(f'❌ moxing download {data_umulti_data_json[i]["dataset_url"]} to {path} failed.')
    return   

def pretrain_to_env(pretrain_url, pretrain_dir):
    """
    copy pretrain to training image
    """
    pretrain_url_json = json.loads(pretrain_url)  
    for i in range(len(pretrain_url_json)):
        modelfile_path = pretrain_dir + "/" + pretrain_url_json[i]["model_name"]
        try:
            mox.file.copy_parallel(pretrain_url_json[i]["model_url"], modelfile_path) 
            print(f'{emoji.emojize(":thumbs_up:")} Successfully Download {pretrain_url_json[i]["model_url"]} to {modelfile_path}.')
        except Exception as e:
            print(f'❌ moxing download {pretrain_url_json[i]["model_url"]} to {modelfile_path} failed.')
    return          

def obs_copy_file(obs_file_url, file_url):
    """
    cope file from obs to obs, or cope file from obs to env, or cope file from env to obs
    """
    try:
        mox.file.copy(obs_file_url, file_url)
        print(f'{emoji.emojize(":thumbs_up:")} Successfully Download {obs_file_url} to {file_url}.')
    except Exception as e:
        print(f'❌ moxing download {obs_file_url} to {file_url} failed.')
    return    
    
def obs_copy_folder(folder_dir, obs_folder_url):
    """
    copy folder from obs to obs, or copy folder from obs to env, or copy folder from env to obs
    """
    try:
        mox.file.copy_parallel(folder_dir, obs_folder_url)
        print(f'{emoji.emojize(":thumbs_up:")} Successfully Download {folder_dir} to {obs_folder_url}.')
    except Exception as e:
        print(f'❌ moxing download {folder_dir} to {obs_folder_url} failed.')
    return     

def c2net_multidataset_to_env(multi_data_url, data_dir):
    """
    c2net copy single or multi dataset to training image 
    """
    multi_data_json = json.loads(multi_data_url)  
    for i in range(len(multi_data_json)):
        zipfile_path = data_dir + "/" + multi_data_json[i]["dataset_name"]
        try:
            mox.file.copy(multi_data_json[i]["dataset_url"], zipfile_path) 
            print(f'{emoji.emojize(":thumbs_up:")} Successfully Download {multi_data_json[i]["dataset_url"]} to {zipfile_path}.')
            filename = os.path.splitext(multi_data_json[i]["dataset_name"])[0]
            filePath = data_dir + "/" + filename
            if not os.path.exists(filePath):
                os.makedirs(filePath)
            if zipfile_path.endswith(".tar.gz"):
                try:
                    os.system("tar -zxvf {} -C {}".format(zipfile_path, filePath))
                    print(f'{emoji.emojize(":thumbs_up:")} Successfully Extracted {zipfile_path}.')
                except Exception as e:
                    print(f'❌ tar extraction failed for {zipfile_path}: {str(e)}')
                finally:
                    os.system("rm -r {}".format(zipfile_path))
                    
            elif zipfile_path.endswith(".zip"):
                try:
                    os.system("unzip {} -d {}".format(zipfile_path, filePath))
                    print(f'{emoji.emojize(":thumbs_up:")} Successfully Extracted {zipfile_path}.')
                except Exception as e:
                    print(f'❌ zip extraction failed for {zipfile_path}: {str(e)}')
                finally:
                    os.system("rm {}".format(zipfile_path))
                    print(f'{emoji.emojize(":thumbs_up:")} Successfully Extracted and Deleted {zipfile_path}.')
            else:
                print(f'❌ The dataset is not in tar.gz or zip format!')
        except Exception as e:
            print(f'❌ moxing download {multi_data_json[i]["dataset_url"]} to {zipfile_path} failed.')
    return       