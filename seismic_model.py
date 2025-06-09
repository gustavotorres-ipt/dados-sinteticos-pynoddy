import random
import os
import numpy as np
from scipy import signal
from datetime import datetime
from PIL import Image
import matplotlib.pyplot as plt

def plot_image(image, title=None):
    plt.imshow(image, cmap='gray')
    if title is not None:
        plt.title(title)
    plt.show()
    plt.close()

class SeismicModel:
    def __init__(self, synthetic_model, freq=0.0, noise=0.0):
        self.geological_model = synthetic_model
        self.synthetic_image = self.geological_model.synthetic_image

        if freq <= 0:
            freq = random.uniform(10, 50)

        if noise <= 0:
            noise = random.random() * 0.4

        self.freq = freq
        self.noise = noise

        if freq >= 30:
            self.freq_level = "high"
        else:
            self.freq_level = "low"

        if noise >= 0.2:
            self.noise_level = "high"
        else:
            self.noise_level = "low"

    def add_gaussian_noise(self, synth_image, mean=0.0, std=1.0):
        noise = np.random.normal(mean, std, size=synth_image.shape)
        return synth_image + noise

    # Generate wavelet of specified frequency
    def calc_wavelet(self, freq, sample_rate):
        sr = sample_rate / 1000
        t = np.arange(-0.2 / 2, 0.2 / 2, sr)
        out = (1 - (2 * (np.pi * freq * t) ** 2)) * np.exp(-(np.pi * freq * t) ** 2)

        return out

    def ricker_convolve(self, image, freq, sample_rate=4):
        wavelet = self.calc_wavelet(freq, sample_rate)
        wavelet = wavelet[:, np.newaxis]
        img_out = signal.fftconvolve(image, wavelet, mode='same')

        # img_out = signal.convolve(image.flatten(), wavelet, mode='same')
        # img_out = img_out.reshape(image.shape)

        # img_out = np.zeros(image.shape)
        # for i in range(img_out.shape[0]):
        #     img_out[i, :] = signal.convolve(image[i,:], wavelet, mode='same')
        return img_out

    def recolor_image_reflection(self, synthetic_image):
        output_image = np.copy(synthetic_image)
        n_layers = self.geological_model.num_layers

        dict_colors = {
            int(px): self.geological_model.calc_reflection_coefficient(
                (n_layers - layer), (n_layers - layer - 1)) # index of layer 1 and index of layer 2
            # int(px): random.choice([2.7, 2.3, 4.0, 3.5])
            for layer, px in enumerate(np.unique(synthetic_image))
        }

        for px in np.unique(synthetic_image):
            idx_replace = np.where(synthetic_image == px)
            output_image[idx_replace] = dict_colors[px]

        return output_image

    def transform_image(self):

        synthetic_image = self.synthetic_image

        synthetic_image = self.recolor_image_reflection(synthetic_image)
        # plot_image(synthetic_image)

        synthetic_image = self.add_gaussian_noise(synthetic_image, std=self.noise)

        #plot_image(synthetic_image)
        synthetic_image = self.ricker_convolve(synthetic_image, freq=self.freq)

        self.synthetic_image = synthetic_image
        self.base_filename = self.get_filename()

    def convert_array_to_image(self, arr_img):
        normalized_image = (255 * (
            arr_img - arr_img.min()) / (arr_img.max() - arr_img.min()
        )).astype(np.uint8)

        image_output = Image.fromarray(normalized_image, 'L')
        return image_output

    def get_filename(self):
        events = set([event.event_type for event in self.geological_model.events])
        events = sorted(list(events))
        filename = "_".join(events)

        dt = datetime.now()

        filename += f"_{dt.year}-{dt.month:02}-{dt.day:02}_" + \
                    f"{dt.hour:02}-{dt.minute:02}-{dt.microsecond}"
        return filename

    def save_image(self):
        dir_images = "images"
        os.makedirs(dir_images, exist_ok=True)

        image_png = self.convert_array_to_image(self.synthetic_image)

        fullpath = os.path.join(dir_images, f"{self.base_filename}.png")
        image_png.save(fullpath)

        print(f"{self.base_filename}.png", "saved successfully.")


    #def normalize_image(self):
    #    return 2 * (self.seismic_image       - self.seismic_image.min()
    #           ) / (self.seismic_image.max() - self.seismic_image.min()) - 1

