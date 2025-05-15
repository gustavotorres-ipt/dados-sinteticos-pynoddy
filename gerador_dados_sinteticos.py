import random
import pynoddy
import pynoddy.history
import pynoddy.events
import pynoddy.output
import matplotlib.pyplot as plt

history = 'simple_model.his'
output_name = 'simple_out'

dicionario_feicoes = {
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

def selecionar_legenda(feicao):
    possiveis_legendas = dicionario_feicoes[feicao]

    return random.choice(possiveis_legendas)

eventos = []

nm = pynoddy.history.NoddyHistory()
num_layers = random.randint(30, 50)
strati_options = {'num_layers' : num_layers,
                  'layer_names' : [f'layer_{i+1}' for i in range(num_layers)],
                  'layer_thickness' : [random.randint(100, 500) for _ in range(num_layers)]}
nm.add_event('stratigraphy', strati_options )
 

# The following options define the fault geometry:
fault_options = {'name' : 'Fault_W',
                 'pos' : (4000, 3500, 5000),
                 'dip_dir' : random.randint(90, 270),
                 'dip' : 60,
                 'slip' : 1000}

nm.add_event('fault', fault_options)
eventos.append('fault')

seismic_options = {'frequency': 'low'}
#nm.add_event('seismic', seismic_options)


# The following options define the fault geometry:
#fault_options = {'name' : 'Fault_E',
#                 'pos' : (6000, 3500, 5000),
#                 'dip_dir' : 270,
#                 'dip' : 60,
#                 'slip' : 1000}

#nm.add_event('fault', fault_options)
#eventos.append('fault')

fold_options = {
    'name': 'Fold_1',
    'type':'normal',
    'pos': (random.randint(2000, 5000), random.randint(2000, 5000), random.randint(500, 2500)),
    #'dip': 100,
    #'dip_dir': 100,
    'wavelength': random.randint(4000,5500),
    'amplitude': random.randint(300,700),
    'plunge_direction': 90
}
nm.add_event('fold', fold_options)
eventos.append('fold')

nm.write_history(history)
pynoddy.compute_model(history, output_name)

nout = pynoddy.output.NoddyOutput(output_name)
slice_output = nout.block[:, 0, :]

legenda = f"{selecionar_legenda('casual')} a {selecionar_legenda('seismic')} "

for evento in eventos:

    legenda += f"{selecionar_legenda('prepositions')} a {selecionar_legenda(evento)} "

print(legenda)
plt.imshow(slice_output.T[::-1], cmap='gray')
plt.title(legenda)

plt.show()
#nout.plot_section('y', layer_labels = strati_options['layer_names'][::-1],
#                  colorbar = True, title = '',
#                  savefig = False, fig_filename = 'ex01_fault_E.eps')