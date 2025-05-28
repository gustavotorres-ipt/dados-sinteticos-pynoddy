import random
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

def random_events():
    events = {}
    events['fault'] = True if random.random() >= 0.5 else False
    events['fold'] = True if random.random() >= 0.5 else False
    events['tilt'] = True if random.random() >= 0.5 else False
    events['unconformity'] = True if random.random() >= 0.5 else False
    return events

def plot_image(image, title=None):
    plt.imshow(image, cmap='gray')
    if title is not None:
        plt.title(title)
    plt.show()
    plt.close()


if __name__ == "__main__":
    n_images = 1000

    for _ in range(n_images):
        reload(pynoddy.history)
        reload(pynoddy.events)
        reload(pynoddy)

        events = random_events()

        gm = GeologicalModel(events['fault'], events['fold'], events['tilt'],
                             events['unconformity'])
        sm = SeismicModel(gm)
        sm.transform_image()

        # Generate 2 to 7  images
        captioner = Captioner(gm, sm, n_captions=random.randint(2, 7))
        captioner.generate_captions()

        sm.save_image()
        captioner.save_captions(f"{sm.base_filename}.txt")
        # plot_image(sm.synthetic_image, title=random.choice(captioner.captions))
