import random
import pynoddy
import pynoddy.history
import pynoddy.output
import numpy as np


POSSIBLE_DENSITIES = [2.7, 2.3, 4.0, 3.5]

class Parameters:
    MIN_THICKNESS = 100
    MAX_THICKNESS = 500

    MIN_LAYERS = 30
    MAX_LAYERS = 50

class Layer:
    def __init__(self, thickness, density, vp):
        self.thickness = thickness
        self.density = density
        self.vp = vp

    def __repr__(self):
        return (f"\nThickness: {self.thickness}\n" +
                f"Density: {self.density}\n" +
                f"Velocity: {self.vp}")

class SyntheticModel:

    def __init__(self):

        self.num_layers = random.randint(Parameters.MIN_LAYERS, Parameters.MAX_LAYERS)
        self.nm = pynoddy.history.NoddyHistory()

        self.layers = [self.generate_layer() for _ in range(self.num_layers)]

        self.generate_stratigraphy()
        self.add_events()

        history_file = 'simple_model.his'
        output_file = 'simple_out'
        nout = self.save_events_file(history_file, output_file)

        self.synthetic_image = self.get_synthetic_image(nout)


    # Randomly sample lithology values for each layer: sand, shale, silt, or limestone
    def generate_layer(self):
        thickness = random.randint(Parameters.MIN_THICKNESS, Parameters.MAX_THICKNESS)

        # sand, shale, silt, or limestone, where every lithology
        # has a deterministically assigned velocity (VP) and density.
        density = random.choice(POSSIBLE_DENSITIES)
        vp = 1

        return Layer(thickness, density=density, vp=vp)

    def generate_stratigraphy(self):
        strati_options = {'num_layers' : self.num_layers,
                          'layer_names' : [f'Layer {i+1}' for i in range(self.num_layers)],
                          'layer_thickness' : [layer.thickness for layer in self.layers],
                          'density' : [layer.density for layer in self.layers],
                          }
        self.nm.add_event('stratigraphy', strati_options )


    def generate_fault(self, name):
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

        self.nm.add_event('fault', fault_options)

    def generate_fold(self, name):
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
        self.nm.add_event('fold', fold_options)

    def add_events(self):
        self.events = []

        self.generate_fault('Fault_1')
        self.events.append('fault')

        self.generate_fold('Fold_1')
        self.events.append('fold')

        if not self.events:
            self.events.append('layer_cake')


    def save_events_file(self, history_file, output_file):
        self.nm.write_history(history_file)

        #self.nm = pynoddy.history.NoddyHistory(history_file)
        #self.nm.write_history(history_file)

        pynoddy.compute_model(history_file, output_file)

        nout = pynoddy.output.NoddyOutput(output_file)

        return nout

    def get_synthetic_image(self, nout):
        return nout.block[:, 0, :].T[::-1]
