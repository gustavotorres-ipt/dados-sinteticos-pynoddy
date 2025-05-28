import random
import pynoddy
import pynoddy.history
import pynoddy.events
# import pynoddy.output
import matplotlib.pyplot as plt
# import numpy as np
# from scipy import signal
from IPython.core.display import HTML
from importlib import reload
from captioner import Captioner
from synthetic_model import SyntheticModel
from seismic_transformer import SeismicTransformer

css_file = 'pynoddy.css'
HTML(open(css_file, "r").read())

def plot_image(image, title=None):
    plt.imshow(image, cmap='gray')
    if title is not None:
        plt.title(title)
    plt.show()
    plt.close()


if __name__ == "__main__":
    n_images = 200

    for _ in range(n_images):
        reload(pynoddy.history)
        reload(pynoddy.events)
        reload(pynoddy)

        sm = SyntheticModel()
        st = SeismicTransformer(sm)
        st.transform_image()

        # Generate 2 to 7  images
        captioner = Captioner(sm, n_captions=random.randint(2, 7))
        captioner.generate_captions()

        st.save_image()
        captioner.save_captions(f"{st.base_filename}.txt")
        # plot_image(st.synthetic_image, title=captioner.captions[0])
