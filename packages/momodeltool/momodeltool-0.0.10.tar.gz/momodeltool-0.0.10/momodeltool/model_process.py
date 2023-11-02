import torch

class ModelProcess(object):
    def __init__(self) -> None:
        pass

    #key_replace_list = [(str, str),(str, str),(str, str), ...]
    def merge_model(self, model, path_src, path_merged, key_replace_list=None):
        checkpoint = torch.load(path_src)
        checkpoint_dict = dict(checkpoint.items())
        for mitemk, mitemv in torch.load(path_merged).items():
            if mitemk.split(".")[0] == "inst_head":
                mitemk = mitemk.replace("inst_head", "instance")
                checkpoint_dict.update({mitemk: mitemv})
            elif mitemk.split(".")[0] == "mask_head":
                mitemk = mitemk.replace("mask_head", "mask")
                checkpoint_dict.update({mitemk: mitemv})
        # for k ,v in checkpoint_dict.items():
        #     print(k)
        # print(checkpoint.items().append())
        model.load_state_dict(
            {k.replace('module.', ''): v for k, v in checkpoint_dict.items()})
        pass

    def show_keys(self, model):
        for key, v in model.cpu().state_dict().items():
            print(key)
    
    def auto_adapt(self, model, weight_path): 
        new_weights = None
        new_weights = self.auto_remove_items(model, weight_path)
        new_weights = self.auto_add_items(model, weight_path)
        return new_weights

    def auto_remove_items(self, model, weight_path):
        pretrained_weights = torch.load(weight_path, map_location=torch.device('cpu'))
        model.cpu()
        keys_to_remove = [key for key in model.state_dict().keys() if key not in pretrained_weights.keys()]
        for key in keys_to_remove:
            print("del", key)
            del model.state_dict()[key]
        return model

    def auto_add_items(self, model, weight_path):
        pretrained_weights = torch.load(weight_path, map_location=torch.device('cpu'))
        model.cpu()
        keys_to_add = [key for key in pretrained_weights.keys() if key not in model.state_dict().keys()]
        for key in keys_to_add:
            print("add", key)
            model.state_dict()[key] = pretrained_weights[key]
        return model
