"""Simple flask server"""
import json
from typing import Dict, Any
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import codecs

# Simon's FORGe system
import forge_main
import setup_repo

from llm import gpt_35_turbo_model, llama2_70_chat_model
import pprint

pp = pprint.PrettyPrinter(indent=4)

app = Flask(__name__)
CORS(app)  # This will allow all origins by default

FORGE_ROOT_FOLDER = os.path.join(os.getcwd(), 'FORGe')

# FORGe paths, etc.
triple2predArg, triple2Conll_jar, morph_folder_name, morph_input_folder, morph_output_folder, props_list_path = setup_repo.prepare_repo_ruleBased(
    FORGE_ROOT_FOLDER)


# Returns a list of tuples (subject, predicate, object)
@app.route('/query-triples', methods=['POST'])
def query_triples():
    data = request.get_json()
    entity_name = data.get('entity_name')
    category = 'Unknown'
    language = data.get('language')
    data_source = data.get('data_source')

    # Set parameters and instantiate variables for parameters
    input_entity_name, _language, _input_category, triple_source, ignore_properties, _group_modules_prm, _split = forge_main.setParametersGeneral(
        entity_name, category, language, data_source)

    # Get properties for queried entity (see details at the bottom of this cell)
    list_triple_objects, _list_propObj, _list_obj, _SelectMultiple_object = forge_main.queryDBpediaProperties(
        props_list_path, input_entity_name, triple_source, ignore_properties)

    print("response: ", list_triple_objects)
    return jsonify({i: (x.DBsubj, x.DBprop, x.DBobj) for i, x in enumerate(list_triple_objects)})


# All generate functions should take the input triples (list of lists) and k-v pair args
def example_generation(triples, args: Dict[str, Any] = None):
    sentences = []
    for triple in triples.values():
        sentences.append(f"{triple[0]} {triple[1]} is {triple[2]}".replace("_", " "))
    return ".  ".join(sentences) + "."


# All generate functions should take the input triples (dict of tuples) and k-v pair args
def forge_generation(triples, args: Dict[str, Any] = None):
    pp.pprint(triples)
    pp.pprint(args)

    # Args are passed to this function as below
    language = args["language"]
    category = args["category"]
    data_source = args["data_source"]
    gender = args["gender"]

    # The entity name can be extracted from the triples
    entity_names = [x[0] for x in triples.values()]
    assert len(set(entity_names)) == 1

    # Stuff that FORGe needs from the DBpedia Query
    entity_name, input_language, input_category, triple_source, ignore_properties, group_modules_prm, split = forge_main.setParametersGeneral(
        entity_names[0], category, language, data_source)

    # Get properties for queried entity (see details at the bottom of this cell)
    list_triple_objects, list_propObj, list_obj, SelectMultiple_object = forge_main.queryDBpediaProperties(
        props_list_path, entity_name, triple_source, ignore_properties)

    class SelectedProps:
        def __init__(self, list_propObj):
            self.value = list_propObj

    # @Simon, here
    triple_ids = list(triples.keys())

    selected_properties = SelectedProps(list_propObj)

    forge_main.run_FORGe(
        FORGE_ROOT_FOLDER,
        entity_name,
        input_language,
        input_category,
        group_modules_prm,
        split,
        gender,
        list_triple_objects,
        list_obj,
        triple_ids,
        triple2predArg,
        triple2Conll_jar,
        morph_folder_name,
        morph_input_folder,
        morph_output_folder,
        props_list_path
    )

    # Now that we have run forge, we need to return the text content of the output file
    s = codecs.open(os.path.join(FORGE_ROOT_FOLDER, 'FORGe-out', 'texts', f'{entity_name}_{input_language}.txt'), 'r',
                    'utf-8').read().strip()

    return s


def llm_generation(model_fn: callable, triples, args: Dict[str, Any] = None):
    llm_triples = [f"{triple[0]} | {triple[1]} | {triple[2]}" for triple in triples.values()]
    output = model_fn.generate_api(
        llm_triples,
        language=args['language'],
        prompt_type='few_shot',
        gender=args['gender']
    )
    return output


def llm_generate_gpt35(triples, args: Dict[str, Any] = None):
    return llm_generation(gpt_35_turbo_model, triples, args)


def llm_generate_llama2(triples, args: Dict[str, Any] = None):
    return llm_generation(llama2_70_chat_model, triples, args)


CATEGORIES = [
    "Unknown",
    "Airport",
    "Artist",
    "Astronaut",
    "Athlete",
    "Building",
    "CelestialBody",
    "City",
    "ComicsCharacter",
    "Company",
    "Film",
    "Food",
    "MeanOfTransportation",
    "Monument",
    "MusicalWork",
    "Politician",
    "Scientist",
    "SportsTeam",
    "University",
    "WrittenWork"
]

DATA_SOURCES = [
    "DBpedia Ontology",
    "Wikipedia Infobox",
    "Wikidata"
]

LANGUAGES = {
    "EN": "English",
    "GA": "Irish"
}

MODELS = {
    "FORGe": {
        "full_name": "FORGe",
        "function": forge_generation,  # The name of the function (no parenthesis)
        "supported_languages": ["EN", "GA"]
    },
    "GPT3.5": {
        "full_name": "GPT-3.5 Turbo",
        "function": llm_generate_gpt35,  # The name of the function (no parenthesis)
        "supported_languages": ["EN", "GA"]
    },
    "LLaMa2-70B": {
        "full_name": "LLaMa2 70B",
        "function": llm_generate_llama2,  # The name of the function (no parenthesis)
        "supported_languages": ["EN", "GA"]
    },
    "Baseline": {
        "full_name": "Baseline Triple Generator",
        "function": example_generation,  # The name of the function (no parenthesis)
        "supported_languages": ["EN"]
    },
}

with open("data/women_in_red_by_category.json") as f:
    WIR_BY_CAT = json.load(f)


@app.route('/form-data', methods=['GET'])
def form_data():
    return jsonify({
        'categories': CATEGORIES,
        'data_sources': DATA_SOURCES,
        'languages': LANGUAGES,
        'models': {k: v["full_name"] for (k, v) in MODELS.items()},
        'women_in_red': WIR_BY_CAT,
        'occupations': list(WIR_BY_CAT.keys()),
    })


@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()

    pp.pprint(data)

    triples = {int(k): v for k, v in data["triplets"].items()}
    language = data["language"]
    data_source = data["dataSource"]
    models = data["model"]
    gender = data["gender"]
    category = 'Unknown'

    title = list(triples.values())[0][0].replace("_", " ")
    content = {}
    for model in models:
        generate_function = MODELS[model]["function"]
        if language in MODELS[model]["supported_languages"]:
            args = {
                "language": language,
                "data_source": data_source,
                "category": category,
                "gender": gender,
            }

            content[model] = generate_function(triples, args)

    return jsonify({'title': title, 'content': content})


if __name__ == '__main__':
    app.run()
