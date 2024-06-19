from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

import json
import os
import pprint
from collections import OrderedDict
from copy import copy

# Simon's FORGe system
import forge_main
import setup_repo

# Setup the pretty printer
pp = pprint.PrettyPrinter(indent=4)

# FORGE_ROOT_FOLDER = os.path.join('/content', 'webnlg_demo', 'FORGe')
FORGE_ROOT_FOLDER = os.path.join(os.getcwd(),'FORGe')

# FORGe paths, etc.
triple2predArg, triple2Conll_jar, morph_folder_name, morph_input_folder, morph_output_folder, props_list_path = setup_repo.prepare_repo_ruleBased(FORGE_ROOT_FOLDER)






# Returns a list of tuples (subject, predicate, object)
def query_triples(entity_name, category, language, data_source):
	# @Simon, I have changed the below so that the code does not update the above input arguments

	# Set parameters and instantiate variables for parameters
	_entity_name, _language, _input_category, triple_source, ignore_properties, _group_modules_prm, _split = forge_main.setParametersGeneral(entity_name, category, language, data_source)

	# Get properties for queried entity (see details at the bottom of this cell)
	list_triple_objects, _list_propObj, _list_obj, _SelectMultiple_object = forge_main.queryDBpediaProperties(props_list_path, entity_name, triple_source, ignore_properties)

	return [tuple([x.DBsubj, x.DBprop, x.DBobj]) for x in list_triple_objects]



# All generate functions should take the input triples (list of lists) and k-v pair args
def example_generation(triples, args={}):
	sentences = []
	for triple in triples:
		sentences.append(f"{triple[0]} {triple[1]} is {triple[2]}")
	return ".  ".join(sentences) + "."



# @Simon, we need to be able to call your generator here
# Triples is a list of lists
def forge_generation(triples, args={}):
	# @Simon, I have changed the below so that the code does not update the above input arguments

	# Args are passed to this function as below
	language = args["language"]
	category = args["category"]
	data_source = args["data_source"]

	# The entity name can be extracted from the triples
	entity_names = [x[0] for x in triples]
	assert len(set(entity_names)) == 1

	# Stuff that FORGe needs from the DBPedia Query
	entity_name, input_language, input_category, triple_source, ignore_properties, group_modules_prm, split = forge_main.setParametersGeneral(entity_names[0], category, language, data_source)

	# Get properties for queried entity (see details at the bottom of this cell)
	list_triple_objects, list_propObj, list_obj, SelectMultiple_object = forge_main.queryDBpediaProperties(props_list_path, entity_name, triple_source, ignore_properties)

	class SelectedProps:
	  def __init__(self, list_propObj):
	    self.value = list_propObj
	selected_properties = SelectedProps(list_propObj)

	forge_main.run_FORGe(
		entity_name,
		FORGE_ROOT_FOLDER,
		input_language,
		input_category,
		group_modules_prm,
		split,
		list_triple_objects,
		list_obj,
		selected_properties,
		triple2predArg,
		triple2Conll_jar,
		morph_folder_name,
		morph_input_folder,
		morph_output_folder,
		props_list_path
	)

	# Now that we have run forge, we need to return the text content of the output file

	# TODO - load this from wherever the FORGe generation went
	s = "Lorum Ipsum"

	return s



# @Michela, we need to be able to call your generator here
# Triples is a list of lists
def llm_generation(triples, args={}):
	return "Lorum Ipsum"




test_triples = query_triples(
	entity_name="Dublin_Airport",
	category="Airport",
	language="EN",
	data_source="Ontology"
)

pp.pprint(test_triples)

test_generation = forge_generation(
	test_triples,
	args={
		"language": "EN",
		"category": "Airport",
		"data_source": "Ontology"
	}
)







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
	"Ontology",
	"Infobox"
]

LANGUAGES = {
	"EN": "English",
	"GA": "Irish"
}

MODELS = {
	"example": {
		"full_name": "Example Triple Generator",
		"function": example_generation, # The name of the function (no parenthesis)
		"supported_languages": ["EN"]
	},
	"forge": {
		"full_name": "FORGe",
		"function": forge_generation, # The name of the function (no parenthesis)
		"supported_languages": ["EN", "GA"]
	},
	"llm": {
		"full_name": "TODO",
		"function":llm_generation, # The name of the function (no parenthesis)
		"supported_languages": ["EN", "GA"]
	}
}





@app.route('/search', methods=['GET']) 
def search():
	return render_template('search.html')



@app.route('/home', methods=['GET']) 
def home():
	return render_template('home.html')




# By placing the <entity_name> here, it will show 
@app.route('/generate/<model_name>/<language>/<entity_name>', methods=['GET', 'POST']) 
def generate(model_name, language, entity_name):
	generate_function = MODELS[model_name]["function"]

	all_triples = format_triples(query_triples(entity_name))
	pp.pprint(all_triples)

	h = request.form.to_dict()
	# TODO - find a cleaner way to do this
	s = "selected_triples["
	selected_triples = {k[len(s):-1]:("checked" if v == "on" else "") for k,v in h.items() if k[:len(s)] == s}
	pp.pprint(selected_triples)

	generate_triples = format_triples(selected_triples.keys()).values()
	pp.pprint(generate_triples)

	# args_string = request.args.get("args_string");
	args = {}

	generated_text = generate_function(generate_triples, args)
	pp.pprint(generated_text)
	

	return render_template(
		'generate.html',
		model_name=model_name,
		entity_name=entity_name,
		generated_text=generated_text,
		all_triples=all_triples,
		selected_triples=selected_triples
	)



if __name__ == '__main__': 
    app.run() 