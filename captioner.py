import random
import os

DICT_EVENTS = {
    'fault': [
        'fault', 'rigid deformation known or fault', 'structural discontinuity',
        'tectonic fault', 'tectonic deformation', 'geologic rigid deformation',
        'structural deformation', 'horizons displacement along fault', 'dip-slip fault',
    ],

    'seismic': [
        'sesimic section', 'seismic image', 'subsurface model', 'model',
        'section', '2D section', '2D subsurface model',
        'subsurface representation', # 'geomodel', '2D geomodel',
    ],

    'fold': [
        'fold', 'anticline', 'ductile deformation', 'folded deformation',
        'tectonic compression', 'antiform', 'structural compression',
    ],
    'tilt': [
        'tilt', 'tectonic tilting', 'subsurface layer rotation',
        'inclined horizontal beds', 'tilted horizontal beds'
    ],

    'unconformity': [
        'unconformity', 'disconformity', 'angular unconformity',
        'nonconformity', 'erosional unconformity'
    ],
    'casual': [
        'we see here', 'this image represents', 'we observe here',
        'this image demonstrates', 'this model depicts',
    ],
    'layer_cake': [
        'layer-cake model', 'flat bed stratigraphy section',
        'section with flat horizons', 'undeformed section',
        'layer-cake stratigraphy section', 'model with no structural deformation',
        'model with no tectonic deformation', 'layer-cake structural model',
    ],
    'prepositions': ['of', 'with'],
}


class Captioner:
    def __init__(self, synthetic_model, seismic_transformer, n_captions = 2):
        self.geological_model = synthetic_model
        self.seismic_model = seismic_transformer
        self.n_captions = n_captions

        self.captions = []

    def select_caption(self, event):
        possible_captions = DICT_EVENTS[event]

        return random.choice(possible_captions)


    def create_caption(self, add_events_info=True, add_freq_noise_info=True):
        assert(hasattr(self.geological_model, "events")), \
            "Error: Synthetic Model does not contain any event."

        caption = f"{self.select_caption('casual')} a {self.select_caption('seismic')} "

        if add_events_info:
            # Shuffle events in random order to increase variability
            events = self.geological_model.events.copy()
            random.shuffle(events)

            for event in self.geological_model.events:
                preposition = self.select_caption('prepositions')
                name_event = self.select_caption(event)
                article = 'an' if name_event[0].lower() in 'aeiou' else 'a'

                caption += f"{preposition} {article} {name_event} "

        if add_freq_noise_info:
            frequency_level = self.seismic_model.freq_level
            noise_level = self.seismic_model.noise_level

            preposition = self.select_caption('prepositions')

            caption += f"{preposition} {frequency_level} frequency and {noise_level} noise"

        return f'{caption.strip()}.'

    def generate_captions(self):
        for _ in range(self.n_captions):
            add_events_info = bool(random.randint(0, 1))
            add_freq_noise_info = bool(random.randint(0, 1))

            if not(add_events_info) and not(add_freq_noise_info):
                add_events_info = True

            caption = self.create_caption(add_events_info, add_freq_noise_info)
            self.captions.append(caption)

    def save_captions(self, filename):
        dir_captions = "captions"
        os.makedirs(dir_captions, exist_ok=True)

        path_caption_file = os.path.join(dir_captions, filename)
        f = open(path_caption_file, 'w')

        for caption in self.captions:
            print(caption, file=f)

        f.close()
        print(filename, "saved successfully")
