import torch
from transformers import BloomForCausalLM, BloomTokenizerFast
from transformers import LlamaTokenizer, LlamaForCausalLM
from diffusers import StableDiffusionPipeline, EulerDiscreteScheduler
from diffusers import StableDiffusionXLPipeline
import gc

from os import makedirs
from os.path import abspath, join
from a2dl.core.constants import IMAGES_WIDTH, IMAGES_HEIGHT
from a2dl.core.constants import logger
from a2dl.core.icon import Diagicon
from a2dl.core.library import Diaglibrary

from a2dl.extensions.constants import MODEL_GPU_TEXT, MODEL_CPU_TEXT, MODEL_GPU_TEXT2IMAGE, MODEL_CPU_TEXT2IMAGE
from a2dl.extensions.helpers import apply_template
from a2dl.extensions.relation import IconRelations

""" Generate with AI """

def generate_article_text_a(keyword: str, pre: str, post: str, result_length: int = 120, strategy: str = 'Sampling'):
    """

    # create descriptions for Icon Names based on context description
    >>> des = generate_article_text_a(keyword='Equalizer', pre='In the Context Audio Engineering, Mastering, Music and Sound, the Term', post='is defined as')
    >>> print(des)
    In the Context Audio Engineering, Digital Signal Processing, Mastering, Music and Sound, the Term Equalizer is defined as "a method used to alter a signal to cause it to behave as desired" [1] .
    In this work, the Equalizer is a signal processing method that is designed to create equalize the signals of two or more signals. It is necessary to be very careful and always be in good standing to use the Equalizer properly. As an example, in an audio signal, an equalizer is designed in the following way [2] :
    Where L and M are the left andாக்கள், respectively. The term is to produce the original signal that is equal to the original signal of the equalizer, which is the signal to be equalized to be the original signal in the Signal Processing Field.
    The Equalizer is a method to make the original signal, which is called a signal that is equal, in a signal of the same typeగి that the signal, which is called a signal that is not equal (also known as equalizer or equalizer). The equalizer converts a signal that is not equal to the original signal in the Signal Processing Field into a signal that is equal to the original signal of the signal.
    When the Equalizer is called, the signal of the same type than the signal that is not equal can be compared. When the signal that is equal is compared बढाउन a signal of the same type than the signal that is not equal is compared to the signal that is equal, the original signal is not equal.
    Because the signal that is equal is not equal, the signal that is equal has no effect on the signal that is not equal, and it is equal to the signal that is not equal when the signal that is not

    """
    # https://towardsdatascience.com/getting-started-with-bloom-9e3295459b65

    # Model Card: https://huggingface.co/bigscience/bloom-560m
    model = BloomForCausalLM.from_pretrained(MODEL_GPU_TEXT)
    tokenizer = BloomTokenizerFast.from_pretrained(MODEL_GPU_TEXT)

    prompt = f"{pre} {keyword} {post}"
    inputs = tokenizer(prompt, return_tensors="pt")

    match strategy:
        case 'Sampling':
            # Sampling Top-k + Top-p
            return tokenizer.decode(model.generate(inputs["input_ids"],
                                                   max_length=result_length,
                                                   do_sample=True,
                                                   top_k=50,
                                                   top_p=0.9,
                                                   num_return_sequences=1,
                                                   )[0])
        case 'Greedy':
            # Greedy Search
            return tokenizer.decode(model.generate(inputs["input_ids"],
                                                   max_length=result_length,
                                                   num_return_sequences=1,
                                                   )[0])
        case 'Beam':
            # Beam Search
            return tokenizer.decode(model.generate(inputs["input_ids"],
                                                   max_length=result_length,
                                                   num_beams=2,
                                                   no_repeat_ngram_size=2,
                                                   early_stopping=True,
                                                   num_return_sequences=1,
                                                   )[0])


def generate_article_text_b(keyword: str, pre: str, post: str, result_length: int = 77):
    gc.collect()
    torch.cuda.empty_cache()

    # Model Card: https://huggingface.co/openlm-research/open_llama_3b
    model_path = MODEL_CPU_TEXT
    # model_path = 'openlm-research/open_llama_7b'
    # model_path = 'openlm-research/open_llama_13b'

    tokenizer = LlamaTokenizer.from_pretrained(model_path)
    model = LlamaForCausalLM.from_pretrained(
        model_path, torch_dtype=torch.float16, device_map='auto',
    )

    prompt = f"{pre} {keyword} {post}"
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids

    generation_output = model.generate(
        input_ids=input_ids,
        max_new_tokens=32,
        num_return_sequences=1,
    )

    return tokenizer.decode(generation_output[0])


def generate_article_image_a(prompt):
    pipe = StableDiffusionXLPipeline.from_pretrained(
        MODEL_CPU_TEXT2IMAGE,
        torch_dtype=torch.float32,
        variant="fp32",
        use_safetensors=True
        # variant="fp16" when pipe.to('cuda')
    )
    pipe.to("cpu")
    image = pipe(prompt=prompt).images[0]

    return image


def generate_article_image_b(prompt):
    model_id = MODEL_GPU_TEXT2IMAGE
    scheduler = EulerDiscreteScheduler.from_pretrained(model_id, subfolder="scheduler")
    pipe = StableDiffusionPipeline.from_pretrained(model_id, scheduler=scheduler, torch_dtype=torch.float16)
    pipe = pipe.to("cuda")

    image = pipe(prompt).images[0]

    return image


def feed(rels: list, pre, post, target='.', title='Fully Generated'):
    """


    # rels = list of tuples with each:
    #      0 - Source Icon Name, # -> Keyword for the prompt
    #      1 - Target Icon Name,
    #      2 - True/False for arrow on a connection,
    #      3 - List of Labels to show on the connection,
    #      4 - For the text generator, additional context, # -> Text before the Keyword
    #      5 - For the text generator, additional context # -> Text after the Keyword

    >>> IRL = [
    >>>     ('Equalization', 'Compression', False, ['influences'], '', ''),
    >>>     ('Compression', 'Limiting', False, ['can lead to'], '', 'is a method of reducing the dynamic range of music. '),
    >>>     ('Limiting', 'Equalization', True, ['is influenced by'], 'When we talk about', ',in the sense of Music creation and audio engineering then we refer to'),
    >>>     ('Spatialization', 'Equalization', False, ['depends'], 'Bei der Produktion von Audiomaterial können Schallereignisse akustisch im Raum verortet werden. Dabei spricht man von', ''),
    >>> ]
    >>> pre='In the Context Audio Engineering, Mastering, Music and Sound, the Term'
    >>> post='is defined as'
    >>> feed(IRL, pre, post)
    """
    logger.info(f'Feeding startet')
    tl = len(rels)
    cnt = 0

    logger.info(f'{cnt} / {tl} Generating text and images: This will take a while.')

    # Make Folders
    makedirs(abspath(join(target, title)), exist_ok=True)
    makedirs(abspath(join(target, title, 'img')), exist_ok=True)
    makedirs(abspath(join(target, title, 'doc')), exist_ok=True)
    makedirs(abspath(join(target, title, 'dio')), exist_ok=True)
    makedirs(abspath(join(target, title, 'lib')), exist_ok=True)
    makedirs(abspath(join(target, title, 'public')), exist_ok=True)

    logger.info(f'Initializing Library.')
    library = Diaglibrary()

    for ir in rels:
        cnt += 1

        # Make Text
        logger.info(f'{cnt} / {tl} Icon: {ir[0]}. Generating text.')
        # set context by relationship setting, instead of the pre, post parameters.
        # Use pre/post if the individual context is not set.
        try:
            if not len(ir[4]) > 0 and not len(ir[5]) > 0:
                txt = generate_article_text_a(keyword=ir[0], pre=pre, post=post)
            else:
                txt = generate_article_text_a(keyword=ir[0], pre=ir[4], post=ir[5])
        except IndexError:
            txt = generate_article_text_a(keyword=ir[0], pre=pre, post=post)

        # Make Image
        logger.info(f'{cnt} / {tl} Icon: {ir[0]}. Generating Image.')
        img = generate_article_image_b(txt)
        img.save(abspath(join(target, title, 'img', f'{ir[0]}.png')))

        # todo: Crop, Scale, Size the Image

        # Make Asciidoc
        logger.info(f'{cnt} / {tl} Icon: {ir[0]}. Generating Asciidoc.')
        art = apply_template(
            image_name=f"{ir[0]}",
            image_rel_path=f"../img/{ir[0]}.png",
            image_link=f"#{ir[0]}",
            image_alt_text=f'A randomly generated Image maybe illustrating {ir[0]} ',
            image_h=IMAGES_WIDTH,
            image_w=IMAGES_HEIGHT,
            image_text=txt
        )
        tap = join(abspath(target), title, 'doc', f'{ir[0]}.adoc')
        targetarticle = open(tap, "w")
        targetarticle.writelines(art)
        targetarticle.close()

        # Make Icon and append to Library
        # HIER
        # IS
        # WAS
        # KAPUTT | DAS
        # ICON
        # hat
        # nicht
        # mehr
        # den
        # generierten
        # Text im tooltip. in der bibliothek ist der aber schon noch

        logger.info(f'{cnt} / {tl} Icon: {ir[0]}. Generating Icon and adding to library.')
        icon = Diagicon(name=str(ir[0]))
        icon.from_adoc(tap)

        print(icon.as_diagram_s())

        library.icons.append(icon)
        library.names.append(ir[0])

    # Make Library
    logger.info(f'Generating Library.')
    library.name = title
    library.write(join(target, title, 'lib', f'{title}.xml'))

    # Make Graph
    logger.info(f'Generating Graph of Icons and Diagram.')
    irs = IconRelations()
    irs.set(rels, libraries=[library])
    irs.write_diagram(join(abspath(target), title, 'dio', f'{title}.drawio'))

    logger.info(f'Feeding ended')
