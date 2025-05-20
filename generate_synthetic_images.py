import os
import random
import numpy as np
import pynoddy
import pynoddy.history
import pynoddy.events
import pynoddy.output
from IPython.core.display import HTML
import matplotlib.pyplot as plt

MIN_NUM_OF_LAYERS, MAX_NUM_OF_LAYERS = 30, 50
MIN_THICKNESS, MAX_THICKNESS = 100, 500


class Layer:
    def __init__(self, thickness, density, vp):
        self.thickness = thickness
        self.density = density
        self.vp = vp

    def __repr__(self):
        return (f"\nThickness: {self.thickness}\n" +
                f"Density: {self.density}\n" +
                f"Velocity: {self.vp}")


def generate_layer():
    thickness = np.random.uniform(MIN_THICKNESS, MAX_THICKNESS)
    # Then, randomly sample lithology values for each layer:
    # sand, shale, silt, or limestone, where every lithology
    # has a deterministically assigned velocity (VP) and density.
    return Layer(thickness, density=1, vp=1)


def teste():
    nm = pynoddy.history.NoddyHistory()
    # add stratigraphy
    strati_options = {'num_layers' : 8,
                      'layer_names' : ['layer 1', 'layer 2', 'layer 3', 'layer 4', 'layer 5', 'layer 6', 'layer 7', 'layer 8'],
                      'layer_thickness' : [1500, 500, 500, 500, 500, 500, 500, 500]}
    nm.add_event('stratigraphy', strati_options )

    # The following options define the fault geometry:
    fault_options = {'name' : 'Fault_W',
                     'pos' : (4000, 3500, 5000),
                     'dip_dir' : 90,
                     'dip' : 60,
                     'slip' : 1000}

    nm.add_event('fault', fault_options)
    # The following options define the fault geometry:
    fault_options = {'name' : 'Fault_E',
                     'pos' : (6000, 3500, 5000),
                     'dip_dir' : 270,
                     'dip' : 60,
                     'slip' : 1000}

    nm.add_event('fault', fault_options)
    history = "two_faults_sensi.his"
    nm.write_history(history)
    output_name = "two_faults_sensi_out"
    # Compute the model
    pynoddy.compute_model(history, output_name)
    nout = pynoddy.output.NoddyOutput(output_name)

    plt.imshow(nout.block[:, 1, :].T[::-1], cmap="RdBu_r")
    plt.show()


def main():
    # https://github.com/cgre-aachen/pynoddy/blob/master/docs/notebooks/8-Sensitivity-Analysis.ipynb
    number_of_layers = random.randint(MIN_NUM_OF_LAYERS, MAX_NUM_OF_LAYERS)
    layers = [generate_layer() for _ in range(number_of_layers)]

    strati_options = {'num_layers' : 8,
                      'layer_names' : [f"Layer {i+1}" for i  in range(len(layers))],
                      'layer_thickness' : [layer.thickness for layer in layers]}
    fault_options = {'name' : 'Fault_E',
                     'pos' : (6000, 3500, 5000),
                     'dip_dir' : 270,
                     'dip' : 60,
                     'slip' : 1000}


    output_name = "noddy_out"
    history = 'simple_two_faults.his'

    nm = pynoddy.history.NoddyHistory()
    nm.change_cube_size(256)

    nm.add_event('stratigraphy', strati_options )
    # nm.add_event('fault', fault_options)

    nm.write_history(history)

    pynoddy.compute_model(history, output_name)
    nout = pynoddy.output.NoddyOutput(output_name)


if __name__ == "__main__":
    teste()
