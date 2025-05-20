import pdb
import random
from numpy.ma import add
import pynoddy
import pynoddy.history
import pynoddy.events
import pynoddy.output
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

HISTORY = 'simple_model.his'
OUTPUT_NAME = 'simple_out'

MIN_THICKNESS = 100
MAX_THICKNESS = 500

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

class Layer:
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
    thickness = random.randint(MIN_THICKNESS, MAX_THICKNESS)
    # Then, randomly sample lithology values for each layer:
    # sand, shale, silt, or limestone, where every lithology
    # has a deterministically assigned velocity (VP) and density.
    return Layer(thickness, density=1, vp=1)

def selecionar_legenda(feicao):
    possiveis_legendas = DICT_FACIES[feicao]

    return random.choice(possiveis_legendas)

########################################################
def add_gaussian_noise(synth_seismic_image, mean=0, std=1):
    noise = np.random.normal(mean, std, size=synth_seismic_image.shape)
    return synth_seismic_image + noise

########################################################

def generate_fault(name):
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

def generate_fold(name):
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
def ricker_convolve(seismic_image, wavelet_length=50, wavelet_param=0.1):
    wavelet = signal.ricker(wavelet_length, wavelet_param)
    wavelet = np.reshape(wavelet, (5,10))
    # __import__('pdb').set_trace()
    ricker_seismic = signal.convolve2d(seismic_image, wavelet, mode='same', boundary='symm')
    return ricker_seismic

#####################################################
N_IMAGES = 10

for _ in range(N_IMAGES):
    eventos = []

    nm = pynoddy.history.NoddyHistory()
    num_layers = random.randint(30, 50)
    strati_options = {'num_layers' : num_layers,
                      'layer_names' : [f'Layer {i+1}' for i in range(num_layers)],
                      'layer_thickness' : [random.randint(100, 500) for _ in range(num_layers)]}
    nm.add_event('stratigraphy', strati_options )

    generate_fault('Fault_1')
    eventos.append('fault')

    generate_fold("Fold_1")
    eventos.append('fold')

    nm.write_history(HISTORY)
    pynoddy.compute_model(HISTORY, OUTPUT_NAME)

    nout = pynoddy.output.NoddyOutput(OUTPUT_NAME)
    slice_output = nout.block[:, 0, :]

    #####################################################
    legenda = f"{selecionar_legenda('casual')} a {selecionar_legenda('seismic')} "

    for evento in eventos:

        legenda += f"{selecionar_legenda('prepositions')} a {selecionar_legenda(evento)} "

    print(legenda)

    synth_seismic_image = slice_output.T[::-1]
    synth_seismic_image = add_gaussian_noise(synth_seismic_image)
    synth_seismic_image = ricker_convolve(synth_seismic_image)
    plt.imshow(synth_seismic_image, cmap='gray')
    plt.title(legenda)

    plt.show()
#nout.plot_section('y', layer_labels = strati_options['layer_names'][::-1],
#                  colorbar = True, title = '',
#                  savefig = False, fig_filename = 'ex01_fault_E.eps')
