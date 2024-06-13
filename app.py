from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

import json
import pprint
from collections import OrderedDict
from copy import copy

import wget

# Setup the pretty printer
pp = pprint.PrettyPrinter(indent=4)



INTER_TRIPLE_DELIMITER = "‖"
INTRA_TRIPLE_DELIMITER = "|"




"""
	All generate functions should take the input triples (list of lists) and k-v pair args
"""
def example_generation(triples, args={}):
	sentences = []
	for triple in triples:
		sentences.append(f"{triple[0]} {triple[1]} is {triple[2]}")
	return ".  ".join(sentences) + "."



# @Simon setup your rules-based Java stuff here.
# - You can load the model and leave it in memory to save loading it on each call
# - Make a function with the same arguments as my example_generation and add it to MODELS below



MODELS = {
	"example": {
		"full_name": "Example Triple Generator",
		"function": example_generation # The name of the function (no parenthesis)
	}
}



# @Simon, put a function here that, given the entity name returns the triples in this format
def query_triples(entity_name):
	return [
		"Agustín_Barboza|birthPlace|Paraguay",
        "Agustín_Barboza|recordLabel|Philips_Records"
	]

def format_triples(queried_triples):
	return {t:t.split(INTRA_TRIPLE_DELIMITER) for t in queried_triples}



@app.route('/search', methods=['GET']) 
def search():
	return render_template('search.html')



@app.route('/home', methods=['GET']) 
def home():
	return render_template('home.html')




# By placing the <entity_name> here, it will show 
@app.route('/generate/<model_name>/<entity_name>', methods=['GET', 'POST']) 
def generate(model_name, entity_name):
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