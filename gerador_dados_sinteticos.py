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

css_file = 'pynoddy.css'
HTML(open(css_file, "r").read())

reload(pynoddy.history)
reload(pynoddy.events)
reload(pynoddy)

HISTORY = 'simple_model.his'
OUTPUT_NAME = 'simple_out'

MIN_THICKNESS = 100
MAX_THICKNESS = 500

POSSIVEIS_DENSIDADES = [2.7, 2.3, 4.0, 3.5]

DICT_FACIES = {
    'fault': [
        'fault', 'rigid deformation known or fault', 'structural discontinuity', 'tectonic fault',
        'tectonic deformation', 'geologic rigid deformation', 'structural deformation',
        'horizons displacement along fault', 'dip-slip fault'
    ],

    'seismic': [
        'geological section', 'geosection', 'geological image', 'subsurface model',
        'model', 'section', '2D section', '2D subsurface model', 'subsurface representation',
        'geomodel', '2D geomodel'
    ],

    'fold': [
        'fold', 'anticline', 'ductile deformation', 'folded deformation',
        'tectonic compression', 'antiform', 'structural compression'
    ],

    'casual': [
        'we see here', 'this image represents', 'we observe here',
        'this image demonstrates', 'this model depicts'
    ],

    'prepositions': ['of', 'with']
}

class LAYER:
    def __init__(self, thickness, density, vp):
        self.thickness = thickness
        self.density = density
        self.vp = vp

    def __repr__(self):
        return (f"\nThickness: {self.thickness}\n" +
                f"Density: {self.density}\n" +
                f"Velocity: {self.vp}")

# Randomly sample lithology values for each layer: sand, shale, silt, or limestone
def generate_layer():
    espessura = random.randint(MIN_THICKNESS, MAX_THICKNESS)
    # Then, randomly sample lithology values for each layer:
    # sand, shale, silt, or limestone, where every lithology
    # has a deterministically assigned velocity (VP) and density.
    return LAYER(espessura, density=1, vp=1)

def select_caption(face):
    possible_captions = DICT_FACIES[face]

    return random.choice(possible_captions)

########################################################
def add_gaussian_noise(synth_seismic_image, mean=0, std=1):
    noise = np.random.normal(mean, std, size=synth_seismic_image.shape)
    return synth_seismic_image + noise

########################################################

def generate_stratigraphy(nm):
    num_layers = random.randint(30, 50)
    thickness = [random.randint(100, 500) for _ in range(num_layers)]
    densidades = [random.choice(POSSIVEIS_DENSIDADES) for _ in range(num_layers)]

    strati_options = {'num_layers' : num_layers,
                      'layer_names' : [f'Layer {i+1}' for i in range(num_layers)],
                      'layer_thickness' : thickness,
                      'density' : densidades,
                      }
    nm.add_event('stratigraphy', strati_options )

def generate_fault(name, nm):
    x = np.random.normal(5000, 2000)
    y =  np.random.normal(5000, 2000)
    z =  np.random.normal(2500, 500)

    type_fault = "normal" if random.randint(0,1) > 0 else "reverse"
    # The following options define the fault geometry:
    fault_options = {'name' : name,
                     'type': type_fault,
                     'pos' : (x, y, z),
                     'dip_dir' : random.randint(90, 270),
                     'dip' : random.randint(45, 70),
                     'displacement' : random.randint(1000, 2500),
                     'slip' : random.randint(1000, 2500),
                     }

    nm.add_event('fault', fault_options)

########################################################

def generate_fold(name, nm):
    x = np.random.normal(5000, 2000)
    y =  np.random.normal(5000, 2000)
    z =  np.random.normal(2500, 500)

    fold_options = {
        'name': name,
        'pos': (x, y, z),
        #'dip': 100,
        #'dip_dir': 100,
        'amplitude': random.randint(300, 700),
        'wavelength': random.randint(4000, 5500),
        'plunge_direction': 90,
        'plunge': np.random.normal(15, 10),
    }
    nm.add_event('fold', fold_options)

#####################################################
# Generate wavelet of specified frequency
def calc_wavelet(freq, sample_rate):
    sr = sample_rate / 1000
    t = np.arange(-0.2 / 2, 0.2 / 2, sr)
    out = (1 - (2 * (np.pi * freq * t) ** 2)) * np.exp(-(np.pi * freq * t) ** 2)

    return out

def ricker_convolve(image, freq=60, sample_rate=4):
    wavelet = calc_wavelet(freq, sample_rate)
    wavelet = wavelet[:, np.newaxis]
    img_out = signal.fftconvolve(image, wavelet, mode='same')

    # img_out = signal.convolve(image.flatten(), wavelet, mode='same')
    # img_out = img_out.reshape(image.shape)

    # img_out = np.zeros(image.shape)
    # for i in range(img_out.shape[0]):
    #     img_out[i, :] = signal.convolve(image[i,:], wavelet, mode='same')
    return img_out

#####################################################
def recolor_seismic(synth_seismic_image):
    output_image = np.copy(synth_seismic_image)

    dict_colors = {
        int(px): random.choice(POSSIVEIS_DENSIDADES)
        for px in np.unique(synth_seismic_image)
    }

    for px in np.unique(synth_seismic_image):
        idx_replace = np.where(synth_seismic_image == px)
        output_image[idx_replace] = dict_colors[px]

    return output_image

#####################################################
def normalize_image(seismic_image):
    return 2 * (seismic_image       - seismic_image.min()
           ) / (seismic_image.max() - seismic_image.min()) - 1

#####################################################
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
