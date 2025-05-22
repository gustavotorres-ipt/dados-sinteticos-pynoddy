import random
import pynoddy
import pynoddy.history
import pynoddy.output
import numpy as np

# https://wiki.seg.org/wiki/Velocities_in_limestone_and_sandstone
# https://wiki.seg.org/wiki/Porosities%252C_velocities%252C_and_densities_of_rocks
ROCK_INFORMATION = {
    'sand': {'velocity': (1.8, 6.8), 'density': (2.0, 2.6)},
    'limestone': {'velocity': (2.6, 6.8), 'density': (2.2, 2.75)},
    'shale': {'velocity': (1.4, 6.8), 'density': (1.9, 2.7)},
}
# POSSIBLE_DENSITIES = [2.7, 2.3, 4.0, 3.5]

class Parameters:
    MIN_THICKNESS = 100
    MAX_THICKNESS = 500

    MIN_LAYERS = 30
    MAX_LAYERS = 50

class Layer:
    def __init__(self, thickness, density, velocity):
        self.thickness = thickness
        self.density = density
        self.velocity = velocity

    def __repr__(self):
        return (f"\nThickness: {self.thickness}\n" +
                f"Density: {self.density}\n" +
                f"Velocity: {self.velocity}")

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
        possible_rocks = list(ROCK_INFORMATION.keys())
        selected_rock = random.choice(possible_rocks)
        min_velocity = ROCK_INFORMATION[selected_rock]['velocity'][0]
        max_velocity = ROCK_INFORMATION[selected_rock]['velocity'][1]
        min_density = ROCK_INFORMATION[selected_rock]['density'][0]
        max_density = ROCK_INFORMATION[selected_rock]['density'][1]

        velocity = random.uniform(min_velocity, max_velocity)
        density = random.uniform(min_density, max_density)

        return Layer(thickness, density=density, velocity=velocity)

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
    
    def calc_reflection_coefficient(self, idx_layer_1, idx_layer_2):
        idx_layer_1 = idx_layer_1 % self.num_layers
        idx_layer_2 = idx_layer_2 % self.num_layers

        vp1 = self.layers[idx_layer_1].velocity
        d1 = self.layers[idx_layer_1].density
        vp2 = self.layers[idx_layer_2].velocity
        d2 = self.layers[idx_layer_2].density

        rc = (vp1 * d1 - vp2 * d2) / (vp1 * d1 + vp2 * d2)
        return rc


    def get_synthetic_image(self, nout):
        return nout.block[:, 0, :].T[::-1]
