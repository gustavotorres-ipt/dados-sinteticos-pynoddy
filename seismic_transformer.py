import random
import pynoddy
import pynoddy.history
import pynoddy.events
import pynoddy.output
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from IPython.core.display import HTML
from importlib import reload
from synthetic_model import SyntheticModel


class SeismicTransformer:
    def __init__(self, synthetic_model, freq=30, noise=0.25):
        self.synthetic_model = synthetic_model
        self.synthetic_image = self.synthetic_model.synthetic_image

        self.freq = freq
        self.noise = noise

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
        n_layers = self.synthetic_model.num_layers

        dict_colors = {
            int(px): self.synthetic_model.calc_reflection_coefficient(
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
        synthetic_image = self.add_gaussian_noise(synthetic_image, std=self.noise)
        synthetic_image = self.ricker_convolve(synthetic_image, freq=self.freq)

        self.synthetic_image = synthetic_image

    #def normalize_image(self):
    #    return 2 * (self.seismic_image       - self.seismic_image.min()
    #           ) / (self.seismic_image.max() - self.seismic_image.min()) - 1

