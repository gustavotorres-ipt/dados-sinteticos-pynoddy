import random

DICT_EVENTS = {
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
    'layer_cake': ['layer cake'],
    'prepositions': ['of', 'with'],
}


class Captioner:
    def __init__(self, synthetic_model, n_captions = 2, freq = None, noise = None):
        self.synthetic_model = synthetic_model
        self.n_captions = n_captions

        self.captions = []

    def select_caption(self, event):
        possible_captions = DICT_EVENTS[event]

        return random.choice(possible_captions)


    def create_caption(self):
        assert(hasattr(self.synthetic_model, "events")), "Error: Synthetic Model does not contain any event."

        caption = f"{self.select_caption('casual')} a {self.select_caption('seismic')} "

        for event in self.synthetic_model.events:

            caption += f"{self.select_caption('prepositions')} a {self.select_caption(event)} "

        return caption

    def generate_captions(self):
        for _ in range(self.n_captions):
            caption = self.create_caption()
            self.captions.append(caption)
