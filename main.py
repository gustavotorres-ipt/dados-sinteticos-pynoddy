import random
import numpy as np
import pynoddy
import pynoddy.history
import pynoddy.events
import matplotlib.pyplot as plt
from IPython.core.display import HTML
from importlib import reload
from captioner import Captioner
from geological_model import GeologicalModel
from seismic_model import SeismicModel

css_file = 'pynoddy.css'
HTML(open(css_file, "r").read())

def random_event():
    possible_events = ['fault', 'fold', 'tilt', 'flat']
    event_occurrence = {}

    for event in possible_events:
        event_occurrence[event] = False

    event = random.choice(possible_events)

    if event != 'flat':
        event_occurrence[event] = True

    return event_occurrence

def plot_image(image, title=None):
    plt.imshow(image, cmap='gray')
    if title is not None:
        plt.title(title)
    plt.show()
    plt.close()

def generate_seismic_images(plot):
    n_images = 100

    for i in range(n_images):
        reload(pynoddy.history)
        reload(pynoddy.events)
        reload(pynoddy)

        events = random_event()

        # gm = GeologicalModel(True)
        gm = GeologicalModel(events['fault'], events['fold'], events['tilt'])

        # np.save(f"volume_{i}.npy", gm.synthetic_volume)
        # plot_image(gm.synthetic_image)
        sm = SeismicModel(gm)
        sm.transform_image()

        # Generate 2 to 7 captions
        captioner = Captioner(gm, sm, n_captions=random.randint(2, 7))
        captioner.generate_captions_and_labels()

        sm.save_image()
        captioner.save_captions_and_labels(f"{sm.base_filename}.json")

        if plot:
            plot_image(sm.synthetic_image, title=random.choice(captioner.captions))

def main():
    generate_seismic_images(plot=True)


if __name__ == "__main__":
    main()
