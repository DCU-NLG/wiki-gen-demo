#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import sys
# def pipInstall(package):
#   subprocess.check_call([sys.executable, "-m", "pip", "install", package])
# # Install SPARQL wrapper
# pipInstall('SPARQLWrapper')

import os
import shutil
import time
import ipywidgets as widgets
from webnlg_demo.FORGe.WikipediaPage_Generator.code.queryDBpediaProps import get_dbpedia_properties
from webnlg_demo.FORGe.WikipediaPage_Generator.code.utils import get_prop_index_from_table, removeReservedCharsFileName, create_xml, create_GPT_Prompt, create_jsons_SubjAndObj, prepare_variables_xml2CoNLL_conversion, clear_folder, clear_files, count_expected_texts, check_postProcessed_outputs, concatenate_files_UI
from webnlg_demo.FORGe.DCU_TCD_FORGe_WebNLG23.code.GA_inflect import run_GA_morphGen


###################### START A- Arguments to pass to the function that runs FORGe
# root_folder = os.path.join('/content', 'webnlg_demo', 'FORGe')
# root_folder = os.path.join(os.getcwd(),'forge') # CT changed this
# entity_name = 'Titanic'
# category = 'MeanOfTransportation' #['Unknown', 'Airport', 'Artist', 'Astronaut', 'Athlete', 'Building', 'CelestialBody', 'City', 'ComicsCharacter', 'Company', 'Film', 'Food', 'MeanOfTransportation', 'Monument', 'MusicalWork', 'Politician', 'Scientist', 'SportsTeam', 'University', 'WrittenWork']
# language = 'EN' #['EN, 'GA']
# triple_source = 'Ontology' #['Ontology', 'Infobox']
# Also look for "### INPUT NEEDED:" lines in the codes below
###################### END A- Arguments to pass to the function that runs FORGe

def setParametersGeneral(entity_name, input_category='Unknown', language='EN', triple_source='Ontology', ignore_properties='width, title'):
  entity_name = ('_').join(entity_name.split(' '))
  group_modules_prm = 'yes'
  split = 'test'
  return entity_name, language, input_category, triple_source, ignore_properties, group_modules_prm, split
    
def run_FORGe(root_folder, entity_name, language, category, triple_source, triple2predArg, triple2Conll_jar, morph_folder_name, morph_input_folder, morph_output_folder, props_list_path):
  ############### Generation parameters
  # Modules to run, with type of processing (FORGe, Model1, SimpleNLG, etc.).
  # Only FORGe is supported for this prototype version.
  PredArg_Normalisation = 'FORGe'
  # To have an external module assigning triples to aggregate
  PredArg_AggregationMark = 'None'
  PredArg_Aggregation = 'FORGe'
  PredArg_PoSTagging = 'FORGe'
  PredArg_CommStructuring = 'FORGe'
  DSynt_Structuring = 'FORGe'
  SSynt_Structuring = 'FORGe'
  SSynt_Aggregation = 'FORGe'
  RE_Generation = 'FORGe'
  DMorph_AgreementsLinearisation = 'FORGe'
  SMorph_Processing = 'FORGe'
  # Paths to python files
  path_MFleNS = os.path.join(root_folder, 'M-FleNS_NLG-Pipeline', 'code', 'M-FleNS.py')
  path_checkOutputs = os.path.join(root_folder, 'M-FleNS_NLG-Pipeline', 'code', 'M-FleNS-checkOutputs.py')
  path_postProc = os.path.join(root_folder, 'M-FleNS_NLG-Pipeline', 'code', 'postProcess.py')
  path_FORGe2Morph = os.path.join(root_folder, 'DCU_TCD_FORGe_WebNLG23', 'code', 'FORGe2Morph.py')
  path_concatenate = os.path.join(root_folder, 'M-FleNS_NLG-Pipeline', 'code', 'concatenate_files.py')
  path_getClassGenderDBp = os.path.join(root_folder, 'M-FleNS_NLG-Pipeline', 'code', 'getClassGenderDBpedia.py')
  # Paths to FORGe/MATE folders and property files
  FORGe_input_folder = os.path.join(root_folder, 'FORGe', 'buddy_project', 'struct')
  path_MATE = os.path.join(root_folder, 'FORGe', 'buddy-patched.jar')
  path_props_resources_template = os.path.join(root_folder, 'FORGe', 'mateColabDrive.properties')
  path_props_levels = os.path.join(root_folder, 'FORGe', 'mateLevels.properties')
  path_props = os.path.join(root_folder, 'FORGe', 'mate.properties')
  # Paths to general folders
  # The input structure(s) of the correct type should be placed in the folder that corresponds to the first module called in the next cell
  path_strs = os.path.join(root_folder, 'FORGe', 'structures')
  str_PredArg_folder = os.path.join(path_strs, '00-PredArg')
  str_PredArgNorm_folder = os.path.join(path_strs, '01-PredArgNorm')
  str_PredArgAggMark_folder = os.path.join(path_strs, '02-PredArgAggMark')
  str_PredArgAgg_folder = os.path.join(path_strs, '03-PredArgAgg')
  str_PredArgPoS_folder = os.path.join(path_strs, '04-PredArgPoS')
  str_PredArgComm_folder = os.path.join(path_strs, '05-PredArgComm')
  str_DSynt_folder = os.path.join(path_strs, '06-DSynt')
  str_SSynt_folder = os.path.join(path_strs, '07-SSynt')
  str_SSyntAgg_folder = os.path.join(path_strs, '08-SSyntAgg')
  str_REG_folder = os.path.join(path_strs, '09-REG')
  str_DMorphLin_folder = os.path.join(path_strs, '10-DMorphLin')
  str_SMorphText_folder = os.path.join(path_strs, '11-SMorphText')
  log_folder = os.path.join(root_folder, 'FORGe', 'log')
  if not os.path.exists(log_folder):
    os.makedirs(log_folder)
  temp_input_folder_morph = os.path.join(root_folder, 'FORGe-out')
  if not os.path.exists(temp_input_folder_morph):
    os.makedirs(temp_input_folder_morph)
  
  ############### Calls to local and imported functions    
  # Set variables for general parameters
  entity_name, language, input_category, triple_source, ignore_properties, group_modules_prm, split = setParametersGeneral(entity_name, category, language, triple_source)
  
  # Query DBpedia
  print('Querying DBpedia for information related to the selected entity...')
  list_triple_objects, list_propObj, list_obj = get_dbpedia_properties(props_list_path, entity_name, triple_source, ignore_properties)
  # What you want to use for selection is list_propObj, and get a list of IDs that we can use to select the corresponding triple object
  
  ### START INPUT NEEDED: that's the output I was getting with my selection tool
  selected_properties = widgets.SelectMultiple(
      options=list_propObj,
      value=[],
      rows=len(list_propObj),
      description='Properties',
      disabled=False
  )
  # Expected object looks like this; wouldn't be difficult to adapt the code to some other data structure.
  # selected_properties = SelectMultiple(description='Properties', index=(0, 1, 3, 4, 6), layout=Layout(width='642px'), options=('0 - height: 53340.0', '1 - length: 268833.6', '2 - activeYearsEndDate: 1912-04-15', '3 - completionDate: 1912-04-02', '4 - cost: 1500000.0', '5 - height: 53.34', '6 - length: 268.8336', '7 - shipBeam: 28.0416', '8 - shipLaunch: 1911-05-31', '9 - status: Wreck', "10 - status: Struck an iceberg at 11:40 pm (ship's time) 14 April 1912 on her maiden voyage andsank2 h 40 min later on.", '11 - topSpeed: 38.892', '12 - maidenVoyage: 1912-04-10', '13 - orderDate: 1908-09-17', '14 - builder: Belfast', '15 - country: United_Kingdom_of_Great_Britain_and_Ireland', '16 - operator: White_Star_Line', '17 - owner: White_Star_Line', '18 - powerType: Horsepower', '19 - powerType: Boiler'), rows=20, value=('0 - height: 53340.0', '1 - length: 268833.6', '3 - completionDate: 1912-04-02', '4 - cost: 1500000.0', '6 - length: 268.8336'))
  ### END INPUT NEEDED: list of indices of selected triples
  
  print('Retrieving class information from DBpedia and converting triples into linguistic structures...')
  # Convert chosen triples to XML and create LLM prompt
  # Generate list of indices of properties selected by user (index in the list of Triple objects that contains all retrieved triples)
  properties_selected_by_user = get_prop_index_from_table(selected_properties, list_triple_objects)
  # create xml file and retrieve the list of triples in a text format to build a ChatGPT query, saved in GPT_prompt_{entity}.txt on the left
  list_triples_text = create_xml(list_triple_objects, properties_selected_by_user, input_category, triple2predArg)
  # Create a text file that contains a prompt that can be used to produce another version of the current text with GPT.
  dest_path_prompt = os.path.join(temp_input_folder_morph, 'prompts')
  create_GPT_Prompt(entity_name, language, list_triples_text, dest_path_prompt)
  
  # Get and write class and gender information from DBpedia
  filepath_subj, filepath_obj = create_jsons_SubjAndObj(entity_name, list_obj, triple2predArg)
  subprocess.run(['python', path_getClassGenderDBp, filepath_subj, filepath_obj, root_folder])
  
  # Create FORGe input file (conll format)
  # Get all variables
  new_triple2predArg, name_conll_templates, path_t2p_out, language_t2p, newEntityName = prepare_variables_xml2CoNLL_conversion(str_PredArg_folder, language, entity_name, triple2predArg)
  # Convert xml into predArg
  subprocess.Popen(['java', '-jar', triple2Conll_jar, new_triple2predArg, name_conll_templates, '230528-WebNLG23_EN-GA_properties.txt', path_t2p_out, language_t2p, newEntityName], stdout = subprocess.PIPE, universal_newlines=True)
  # There seems to be a lag here between the moment the file is created and the moment it becomes available; I get a FileNotFoundError even though the file seems to be created there correctly
  print('Contemplating life and its purpose...')
  time.sleep(1)
  # Copy conll file to FORGe input folder
  shutil.copy(os.path.join(path_t2p_out, newEntityName+'_'+language_t2p+'.conll'), str_PredArg_folder)
  
  # Convert linguistic structures into English text or non-inflected Irish text (FORGe generator)
  print('Generating text with FORGe...')
  subprocess.run(['python', path_MFleNS, language, split, group_modules_prm, PredArg_Normalisation, PredArg_AggregationMark, PredArg_Aggregation, PredArg_PoSTagging, PredArg_CommStructuring, DSynt_Structuring, SSynt_Structuring, SSynt_Aggregation, RE_Generation, DMorph_AgreementsLinearisation, SMorph_Processing, FORGe_input_folder, path_MATE, path_props_resources_template, path_props_levels, path_props, str_PredArg_folder, str_PredArgNorm_folder, str_PredArgAggMark_folder, str_PredArgAgg_folder, str_PredArgPoS_folder, str_PredArgComm_folder, str_DSynt_folder, str_SSynt_folder, str_SSyntAgg_folder, str_REG_folder, str_DMorphLin_folder, str_SMorphText_folder, log_folder])
  # Check outputs
  subprocess.run(['python', path_checkOutputs, str_PredArg_folder, str_SMorphText_folder, log_folder, temp_input_folder_morph, language])
  
  # Copy files to morph folder
  if not language == 'GA':
    clear_folder(os.path.join(temp_input_folder_morph, split))
    # For GA, files are copied from the python code called above
    subprocess.run(['python', path_concatenate, str_SMorphText_folder, temp_input_folder_morph, split])
  
  # Process raw FORGe output and format it for Morphology
  count_strs_all_FORGe = count_expected_texts(root_folder)
  print('  Expected texts: '+str(count_strs_all_FORGe)+'.\n')
  if language == 'GA':
    subprocess.run(['python', path_FORGe2Morph, language, temp_input_folder_morph, morph_input_folder])
    clear_files(temp_input_folder_morph)
  
  # Run the morphology generation
  show_input = False #@param {type:"boolean"}
  if language == 'GA':
    print('Inflecting Irish text with Irish NLP tools...')
    full_morph_folder_path = os.path.join(root_folder, morph_folder_name)
    run_GA_morphGen(root_folder, full_morph_folder_path, morph_input_folder, morph_output_folder, count_strs_all_FORGe, show_input)
  
  print('Post-processing text...')
  # Post-process output
  prefinal_output_folder = ''
  if language == 'GA':
    prefinal_output_folder = morph_output_folder
  else:
    prefinal_output_folder = os.path.join(temp_input_folder_morph, split)
  # Process texts
  subprocess.run(['python', path_postProc, language, prefinal_output_folder])
  # Check post-processed texts
  check_postProcessed_outputs(root_folder, prefinal_output_folder, count_strs_all_FORGe)
  # Concatenate files
  dest_path_final = os.path.join(temp_input_folder_morph, 'texts')
  filename = concatenate_files_UI(root_folder, morph_output_folder, temp_input_folder_morph, split, language, count_strs_all_FORGe, entity_name, dest_path_final)
