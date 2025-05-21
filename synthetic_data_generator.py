import pdb
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
from captioner import Captioner
from synthetic_model import SyntheticModel
from seismic_transformer import SeismicTransformer

css_file = 'pynoddy.css'
HTML(open(css_file, "r").read())

reload(pynoddy.history)
reload(pynoddy.events)
reload(pynoddy)

def plot_image(image, title=None):
    plt.imshow(image, cmap='gray')
    if title is not None:
        plt.title(title)
    plt.show()
    plt.close()


if __name__ == "__main__":
    sm = SyntheticModel()
    # sm.plot_synthetic_image()
    st = SeismicTransformer(sm)
    st.transform_image()

    captioner = Captioner(sm)
    captioner.generate_captions()

    plot_image(st.synthetic_image, title=captioner.captions[0])


#####################################################


"""
N_IMAGES = 10

eventos = []

nm = pynoddy.history.NoddyHistory()

generate_stratigraphy(nm)

#generate_fold("Fold_1", nm)
#eventos.append('fold')

generate_fault('Fault_1', nm)
eventos.append('fault')

nm.write_history(HISTORY)

nm = pynoddy.history.NoddyHistory(HISTORY)
nm.write_history(HISTORY)

pynoddy.compute_model(HISTORY, OUTPUT_NAME)

nout = pynoddy.output.NoddyOutput(OUTPUT_NAME)

synth_seismic_image = nout.block[:, 0, :].T[::-1]

synth_seismic_image = recolor_seismic(synth_seismic_image)
synth_seismic_image = normalize_image(synth_seismic_image)

# __import__('pdb').set_trace()
# nout.plot_section('y', colorbar = True)

#####################################################
caption = f"{select_caption('casual')} a {select_caption('seismic')} "

for evento in eventos:

    caption += f"{select_caption('prepositions')} a {select_caption(evento)} "

synth_seismic_image = add_gaussian_noise(synth_seismic_image, std=0.2)

freq = random.randint(20, 60)
synth_seismic_image = ricker_convolve(synth_seismic_image, freq=freq)

print(caption)
plt.imshow(synth_seismic_image, cmap='gray')
plt.title(caption)

plt.show()
"""
