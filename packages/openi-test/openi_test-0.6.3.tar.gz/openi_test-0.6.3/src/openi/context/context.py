from .download import download_dataset, download_pretrain_model
from .upload import upload_output

class OpeniContext:
    def __init__(self, dataset_path, pretrain_model_path):
        self.dataset_path = dataset_path
        self.pretrain_model_path = pretrain_model_path
        self.output_path = None

    def upload_openi():
        return upload_output()
        
def prepare():
    dataset_path = download_dataset()
    pretrain_model_path = download_pretrain_model()
    t = OpeniContext(dataset_path, pretrain_model_path)
    return t
