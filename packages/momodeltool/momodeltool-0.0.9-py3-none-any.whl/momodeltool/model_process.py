import torch

class ModelProcess(object):
    def __init__(self) -> None:
        pass

    #key_replace_list = [(str, str),(str, str),(str, str), ...]
    def merge_model(self, model, path_src, path_merged, key_replace_list=None):
        checkpoint = torch.load(path_src)
        checkpoint_dict = dict(checkpoint.items())
        for mitemk, mitemv in torch.load("/moak/edisk/src/ADAS/StereoMatching/PlaneRecNet-main/weights/resnet50-19c8e357.pth").items():
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

    def show_keys(self, path_weight):
        pass

    
    def auto_adapt(self, model, weight_path): 
        new_weights = None
        self.auto_remove_items(model, weight_path)
        self.auto_add_items(model, weight_path)
        return new_weights

    def auto_remove_items(self, model, weight_path):
        new_weights = None
        return new_weights

    def auto_add_items(self, model, weight_path):
        new_weights = None
        return new_weights
