import cv2
import numpy as np
import torch
import os


class Visualization(object):
    def __init__(self) -> None:
        pass

    @staticmethod
    def layer_show(input, module_name='ShowLayer', show=False, save=None):

        def closest_factors(n):
            factors = []
            for i in range(1, int(n**0.5) + 1):
                if n % i == 0:
                    factors.append((i, n // i))
            if len(factors) == 1:
                return factors[0]
            min_difference = float('inf')
            closest_pair = None
            for pair in factors:
                if abs(pair[0] - pair[1]) < min_difference:
                    min_difference = abs(pair[0] - pair[1])
                    closest_pair = pair
            return closest_pair

        if show or save is not None:
            if len(input.shape) == 4:
                pair_factor = closest_factors(input.shape[1])
                img_concatenated = None
                for b in range(input.shape[0]):
                    for i in range(pair_factor[1]):
                        mid_concatenated = torch.cat(
                            [input[b, mid, :, :] for mid in range(i * pair_factor[0], pair_factor[0] * (i + 1))], dim=1)
                        if img_concatenated is None:
                            img_concatenated = mid_concatenated.clone()
                        else:
                            img_concatenated = torch.cat(
                                [img_concatenated, mid_concatenated], dim=0)
                    img_np = (img_concatenated.numpy() * 255).astype(np.uint8)
                    if show:
                        cv2.namedWindow("step" + str(b) + "_" + module_name, 0)
                        cv2.imshow("step" + str(b) + "_" + module_name, img_np)
                    if save is not None:
                        cv2.imwrite(os.path.join(save, "step" +
                                    str(b) + "_" + module_name + '.png'), img_np)
                if show:
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()

            elif len(input.shape) == 5:
                for d in range(input.shape[1]):
                    pair_factor = closest_factors(input.shape[2])
                    img_concatenated = None
                    for b in range(input.shape[0]):
                        for i in range(pair_factor[2]):
                            mid_concatenated = torch.cat(
                                [input[b, d, mid, :, :] for mid in range(i * pair_factor[0], pair_factor[0] * (i + 1))], dim=1)
                            if img_concatenated is None:
                                img_concatenated = mid_concatenated.clone()
                            else:
                                img_concatenated = torch.cat(
                                    [img_concatenated, mid_concatenated], dim=0)
                        img_np = (img_concatenated.numpy()
                                  * 255).astype(np.uint8)
                        if show:
                            cv2.namedWindow(
                                f"Depth{d}_" + "step" + str(b) + "_" + module_name, 0)
                            cv2.imshow(f"Depth{d}_" + "step" +
                                    str(b) + "_" + module_name, img_np)
                        if save is not None:
                            cv2.imwrite(os.path.join(save, f"Depth{d}_" + "step" +
                                        str(b) + "_" + module_name + '.png'), img_np)
                    if show:
                        cv2.waitKey(0)
                        cv2.destroyAllWindows()

            else:
                print("Only supports four and five dimensions!!!")

    @staticmethod
    def kernel_show(model, module_name=None, show=False, save=None):
        if save is not None:
            file = open(os.path.join(save, module_name) + '.txt', mode='w')
        for k, v in model.state_dict().items():
            if show or save:
                try:
                    img_np = (v.numpy() * 255).astype(np.uint8)
                    if save is not None:
                        cv2.imwrite(os.path.join(save, k) + '.png', img_np)
                    if show:
                        cv2.imshow(k, img_np)
                        cv2.waitKey(0)
                        cv2.destroyAllWindows()
                except:
                    pass
            if save is not None:
                file.write(k + '\n')
        if save is not None:
            file.close()


if __name__ == "__main__":
    Visualization.layer_show()
