import cv2
import numpy as np
import torch
import os


class Visualization(object):
    def __init__(self) -> None:
        pass

    @staticmethod
    def layer_show(input, module_name='ShowImage', show=False, save=None, norm=False, pseudo=False, hist=False):

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

        def draw_hist(image_index):
            # image_index = image_index[image_index != 0]
            hist, bins = np.histogram(
                image_index, bins=256, range=(0, 256))
            hist_img = np.ones((600, 1300, 3), dtype=np.uint8) * 255
            h, w, _ = hist_img.shape
            bin_width = int(round((w - 200) / len(hist)))
            hist_max, peak_count = np.max(hist), np.max(hist)
            peak_value = bins[np.argmax(hist)]
            hist_max_pox = 0
            while hist_max != 0:
                hist_max //= 10
                hist_max_pox += 1
            hist_max = round(np.max(hist), -(hist_max_pox - 1)) + \
                10**(hist_max_pox - 1)
            cv2.line(hist_img, (100, h - 100), (100, 100), (0, 0, 0), 2)
            cv2.line(hist_img, (100, h - 100),
                     (w - 170, h - 100), (0, 0, 0), 2)
            font = cv2.FONT_HERSHEY_SIMPLEX
            for i in range(6):
                y = h - 100 - i * (h - 200) // 5
                value = int(i * hist_max / 5)
                cv2.line(hist_img, (90, y), (100, y), (0, 0, 0), 2)
                cv2.putText(hist_img, str(value), (20, y + 5),
                            font, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            colormap = cv2.applyColorMap(
                np.uint8(np.linspace(0, 255, 256)), cv2.COLORMAP_JET)
            x_ticks = list(map(int, np.linspace(100, w - 178, 6)))
            x_labels = list(range(0, 256, 51))
            for i, x in enumerate(x_ticks):
                cv2.line(hist_img, (int(x), h - 100),
                         (int(x), h - 90), (0, 0, 0), 2)
                cv2.putText(hist_img, str(x_labels[i]), (int(
                    x) - 10, h - 70), font, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            for i in range(len(hist)):
                if hist[i] == 0:
                    continue
                norm_value = int(hist[i] / hist_max * (h - 200))
                x1 = i * bin_width + 100
                y1 = h - 100
                x2 = (i + 1) * bin_width + 100
                y2 = h - 100 - norm_value
                color_value = np.uint8(255 * (i / len(hist)))
                color = tuple(map(int, colormap[color_value][0]))
                color = color[::-1]
                cv2.rectangle(hist_img, (x1, y1), (x2, y2), color, -1)
            cv2.putText(hist_img, "peak: {}({})".format(peak_value, peak_count), (int(
                hist_img.shape[1] - 500), 80), 1, 2, (0, 0, 0), 2)
            return hist_img

        if show or save:
            if len(input.shape) == 4:
                pair_factor = closest_factors(input.shape[1])
                for b in range(input.shape[0]):
                    img_slices = []
                    hist_slices = []
                    for i in range(pair_factor[1]):
                        mid_slices = []
                        hist_mid_slices = []
                        for mid in range(i * pair_factor[0], pair_factor[0] * (i + 1)):
                            mid_slice = input[b, mid, :, :].cpu().numpy()
                            if norm:
                                mid_slice = (mid_slice - np.min(mid_slice)) / \
                                    (np.max(mid_slice) - np.min(mid_slice)) * 255
                            mid_slice = mid_slice.astype(np.uint8)
                            if pseudo:
                                mid_slice = cv2.applyColorMap(
                                    mid_slice, cv2.COLORMAP_JET)
                            mid_slices.append(mid_slice)
                            if hist:
                                hist_mid_slice = draw_hist(mid_slice)
                                hist_mid_slices.append(hist_mid_slice)

                        mid_concatenated = np.concatenate(mid_slices, axis=1)
                        img_slices.append(mid_concatenated)
                        if hist:
                            mid_hist_concatenated = np.concatenate(
                                hist_mid_slices, axis=1)
                            hist_slices.append(mid_hist_concatenated)

                    img_np = np.concatenate(img_slices, axis=0)
                    hist_show = np.concatenate(hist_slices, axis=0)
                    if show:
                        cv2.namedWindow("step" + str(b) + "_" + module_name, 0)
                        cv2.imshow("step" + str(b) + "_" + module_name, img_np)
                        if hist:
                            cv2.namedWindow("step" + str(b) +
                                            "_" + module_name + "_hist", 0)
                            cv2.imshow("step" + str(b) + "_" +
                                       module_name + "_hist", hist_show)
                    if save is not None:
                        save = os.path.join(save, 'output_layer_show')
                        if os.path.exists(save) is False:
                            os.mkdir(save)
                        cv2.imwrite(os.path.join(save, "step" +
                                    str(b) + "_" + module_name + '.png'), img_np)
                        if hist:
                            cv2.imwrite(os.path.join(save, "step" +
                                                     str(b) + "_" + module_name + '_hist.png'), hist_show)
                if show:
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()
            elif len(input.shape) == 5:
                for d in range(input.shape[1]):
                    pair_factor = closest_factors(input.shape[2])
                    for b in range(input.shape[0]):
                        img_slices = []
                        hist_slices = []
                        for mid in range(i * pair_factor[0], pair_factor[0] * (i + 1)):
                            mid_slice = input[b, mid, :, :].cpu().numpy()
                            if norm:
                                mid_slice = (mid_slice - np.min(mid_slice)) / \
                                    (np.max(mid_slice) - np.min(mid_slice)) * 255
                            mid_slice = mid_slice.astype(np.uint8)
                            if pseudo:
                                mid_slice = cv2.applyColorMap(
                                    mid_slice, cv2.COLORMAP_JET)
                            mid_slices.append(mid_slice)
                            if hist:
                                hist_mid_slice = draw_hist(mid_slice)
                                hist_mid_slices.append(hist_mid_slice)

                        mid_concatenated = np.concatenate(mid_slices, axis=1)
                        img_slices.append(mid_concatenated)
                        if hist:
                            mid_hist_concatenated = np.concatenate(
                                hist_mid_slices, axis=1)
                            hist_slices.append(mid_hist_concatenated)

                        if show:
                            cv2.namedWindow(
                                f"Depth{d}_" + "step" + str(b) + "_" + module_name, 0)
                            cv2.imshow(f"Depth{d}_" + "step" +
                                       str(b) + "_" + module_name, img_np)
                            if hist:
                                cv2.namedWindow(
                                    f"Depth{d}_" + "step" + str(b) + "_" + module_name + '_hist', 0)
                                cv2.imshow(f"Depth{d}_" + "step" +
                                           str(b) + "_" + module_name + '_hist', img_np)
                        if save is not None:
                            cv2.imwrite(os.path.join(save, f"Depth{d}_" + "step" +
                                        str(b) + "_" + module_name + '.png'), img_np)
                            if hist:
                                cv2.imwrite(os.path.join(save, f"Depth{d}_" + "step" +
                                                         str(b) + "_" + module_name + '_hist.png'), img_np)
                if show:
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()
            else:
                print("Only supports four and five dimensions!!!")

    @staticmethod
    def kernel_show(model, module_name="SaveKernel", show=False, save=None):
        if save is not None:
            file = open(os.path.join(save, module_name) + '.txt', mode='w')
        if save is not None:
            save = os.path.join(save, 'output_kernel_show')
            if os.path.exists(save) is False:
                os.mkdir(save)
        for k, v in model.state_dict().items():
            if show or save:
                try:
                    if save is not None:
                        img_np = (v.cpu().numpy() * 255).astype(np.uint8)
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
