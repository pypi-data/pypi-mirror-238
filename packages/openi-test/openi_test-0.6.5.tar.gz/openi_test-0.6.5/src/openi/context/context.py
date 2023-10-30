from .download import download_dataset, download_pretrain_model, get_output_path
from .upload import upload_output

class OpeniContext:
    def __init__(self, dataset_path, pretrain_model_path, output_path):
        self.dataset_path = dataset_path
        self.pretrain_model_path = pretrain_model_path
        self.output_path = output_path
        
def prepare():
    dataset_path = download_dataset()
    pretrain_model_path = download_pretrain_model()
    output_path = get_output_path()
    t = OpeniContext(dataset_path, pretrain_model_path, output_path)
    return t

def upload_openi():
    return upload_output()    
