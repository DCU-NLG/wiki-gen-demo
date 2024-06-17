#!/usr/bin/env python
# -*- coding: utf-8 -*-
  
import subprocess
import sys
def pipInstall(package):
  subprocess.check_call([sys.executable, "-m", "pip", "install", package])
# Install SPARQL wrapper
pipInstall('SPARQLWrapper')

import os
import zipfile
from WikipediaPage_Generator.code.queryDBpediaProps import get_dbpedia_properties
from WikipediaPage_Generator.code.utils import get_prop_index_from_table, removeReservedCharsFileName, create_xml, create_GPT_Prompt, create_jsons_SubjAndObj, prepare_variables_xml2CoNLL_conversion, clear_folder, clear_files, count_expected_texts, check_postProcessed_outputs, concatenate_files
from DCU_TCD_FORGe_WebNLG23.code.GA_inflect import run_GA_morphGen


###################### START A- What needs to come from outside of the main function that calls FORGe
root_folder = os.path.join('/content', 'webnlg_demo')
entity_name = 'Titanic'
category = 'MeanOfTransportation' #['Unknown', 'Airport', 'Artist', 'Astronaut', 'Athlete', 'Building', 'CelestialBody', 'City', 'ComicsCharacter', 'Company', 'Film', 'Food', 'MeanOfTransportation', 'Monument', 'MusicalWork', 'Politician', 'Scientist', 'SportsTeam', 'University', 'WrittenWork']
language = 'EN' #['EN, 'GA']
triple_source = 'Ontology' #['Ontology', 'Infobox']
###################### END A- What needs to come from outside of the main function that calls FORGe

###################### START B- What goes inside the main function that calls FORGe
########### START 1- Generation parameters
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
path_props = os.path.join(root_folder, 'FORGe', '/mate.properties')
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
########### END 1- Generation parameters

########### START 2- Local functions
def unzipTo(path_to_zip_file, directory_to_extract_to):
  with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
    zip_ref.extractall(directory_to_extract_to)

def install_java8():
  cmd_java1 = ["apt-get",  "install", "-y", "openjdk-8-jdk-headless", "-qq", ">", "/dev/null"]
  subprocess.Popen(cmd_java1, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
  os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-8-openjdk-amd64"     #set environment variable
  cmd_java2 = ["update-alternatives", "--set",  "java", "/usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java"]
  subprocess.Popen(cmd_java2, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
  cmd_java3 = ["java", "-version"]
  subprocess.check_output(cmd_java3, stderr=subprocess.STDOUT)

def setParametersGeneral(entity_name, input_category='Unknown', language='EN', triple_source='Ontology', ignore_properties='width, title'):
  entity_name = ('_').join(entity_name.split(' '))
  group_modules_prm = 'yes'
  split = 'test'
  return entity_name, language, input_category, triple_source, ignore_properties, group_modules_prm, split

def prepare_repo_ruleBased(root_folder):
  # Unzip components and instantiate paths
  # FORGe
  zipForge = os.path.join(root_folder, 'M-FleNS_NLG-Pipeline', 'code', 'FORGe_colab_v4.zip')
  unzipTo(zipForge, root_folder)
  # Triple2predArg
  triple2predArg = os.path.join(root_folder, 'triples2predArg')
  os.makedirs(triple2predArg)
  zipPredArg =  os.path.join(root_folder, 'WikipediaPage_Generator', 'code', 'triples2predArg.zip')
  triple2Conll_jar = os.path.join(triple2predArg, 'webNLG_triples2conll.jar')
  unzipTo(zipPredArg, triple2predArg)
  # Morph
  morph_folder_name = 'test_irish_morph_gen_v5.0'
  zipMorph = os.path.join(root_folder, 'DCU_TCD_FORGe_WebNLG23', 'code', morph_folder_name+'.zip')
  morph_input_folder = os.path.join(root_folder, morph_folder_name, 'Inputs')
  morph_output_folder = os.path.join(root_folder, morph_folder_name, 'Outputs')
  os.makedirs(morph_input_folder)
  os.makedirs(morph_output_folder)
  unzipTo(zipMorph, root_folder)
  # Make morphology flookup executable
  cmd_morph1 = ["7z", "a",  "-sfx", root_folder+"/"+morph_folder_name+"/flookup.exe", root_folder+"/"+morph_folder_name+"/flookup"]
  subprocess.Popen(cmd_morph1, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
  cmd_morph2 = ["chmod",  "755", root_folder+"/"+morph_folder_name+"/flookup"]
  subprocess.Popen(cmd_morph2, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
  # IMG
  zipWikiImg = os.path.join(root_folder, 'WikipediaPage_Generator', 'code', 'wikipedia-images.zip')
  unzipTo(zipWikiImg, triple2predArg)
  # Set other paths
  props_list_path = os.path.join(root_folder, 'DCU_TCD_FORGe_WebNLG23', 'code', 'sorted_properties.txt')
  
  return triple2predArg, triple2Conll_jar, morph_folder_name, morph_input_folder, morph_output_folder, props_list_path
########### END 2- Local functions

########### START 3- Calls to local and imported functions
# Can't get the next function to work; will have to find some other way wherever this code is hosted
install_java8()

# Prepare repo and variables
triple2predArg, triple2Conll_jar, morph_folder_name, morph_input_folder, morph_output_folder, props_list_path = prepare_repo_ruleBased(root_folder)
entity_name, language, input_category, triple_source, ignore_properties, group_modules_prm, split = setParametersGeneral(entity_name, category, language, triple_source)

# Query DBpedia
list_triple_objects, list_propObj, list_obj = get_dbpedia_properties(props_list_path, entity_name, triple_source, ignore_properties)
# What you want to use for selection is list_propObj, and get a list of IDs that we can use to select the corresponding triple object

########### END 3- Calls to local and imported functions

###################### END B- What goes inside the main function that calls FORGe

