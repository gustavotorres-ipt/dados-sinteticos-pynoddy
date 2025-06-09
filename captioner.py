import random
import os

DICT_EVENTS = {
    'fault': [
        'fault', 'rigid deformation known or fault', 'structural discontinuity',
        'tectonic fault', 'tectonic deformation', 'geologic rigid deformation',
        'structural deformation', 'horizons displacement along fault', 'dip-slip fault',
    ],
    'fault_reverse': [
        'reverse fault', 'compressional fault', 'reverse tectonics',
        'compressional tectonics', 'compressional tectonic settings',
        'downward tectonic', 'movement', 'compressional structural fault',
        'reverse-slip fault'
    ],
    'seismic': [
        'sesimic section', 'seismic image', 'subsurface model', 'model',
        'section', '2D section', '2D subsurface model',
        'subsurface representation', 'seismic model', '2D seismic model',
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
        'this image demonstrates', 'this depicts', '',
    ],
    'flat': [
        'layer-cake model', 'flat bed stratigraphy section',
        'section with flat horizons', 'undeformed section',
        'layer-cake stratigraphy section', 'model with no structural deformation',
        'model with no tectonic deformation', 'layer-cake structural model',
    ],
    'prepositions': [' of', ' with', '. It is', '. It has'],
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

    # def generate_label(self, event):
    #     """TODO: generate label

    #     pass

    def add_fault_direction(self, caption, fault_event):
        # 50% of chance of nothing being added.
        if random.random() < 0.5:
            return caption

        if fault_event.options['dip_dir'] > 180:
            direction = random.choice(["west", "left"])
        else:
            direction = random.choice(["east", "right"])

        return f"{caption} dipping {direction}"


    def create_caption(self):
        assert(hasattr(self.geological_model, "events")), \
            "Error: Synthetic Model does not contain any event."

        caption = f"{self.select_caption('casual')} a {self.select_caption('seismic')}"

        # Shuffle events in random order to increase variability
        events = self.geological_model.events.copy()
        random.shuffle(events)

        for event in self.geological_model.events:
            event_type = event.event_type

            preposition = self.select_caption('prepositions')
            name_event = self.select_caption(event_type)
            article = 'an' if name_event[0].lower() in 'aeiou' else 'a'
            caption += f'{preposition} {article} {name_event}'

            if event_type == 'fault' or event_type == 'fault_reverse':
                caption = self.add_fault_direction(caption, event)

        caption = self.add_noise_information(caption)

        return f'{caption.strip()}.'

    def add_noise_information(self, caption):
        # 50% of chance of nothing being added.
        if random.random() < 0.5:
            return caption

        frequency_level = self.seismic_model.freq_level
        noise_level = self.seismic_model.noise_level

        preposition = self.select_caption('prepositions')

        caption += f"{preposition} {frequency_level} frequency and {noise_level} noise"
        return caption

    def generate_captions(self):
        for _ in range(self.n_captions):
            caption = self.create_caption()
            # label = self.get_label()

            self.captions.append(caption)

    def save_captions(self, filename):
        dir_captions = "captions"
        os.makedirs(dir_captions, exist_ok=True)

        path_caption_file = os.path.join(dir_captions, filename)
        f = open(path_caption_file, 'w')

        for caption in self.captions:
            print(caption, file=f)

        f.close()
        print(filename, "saved successfully.")
