#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import zipfile
import subprocess
import sys

def unzipTo(path_to_zip_file, directory_to_extract_to):
  with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
    zip_ref.extractall(directory_to_extract_to)

def pipInstall(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# def install_java():
#   !apt-get install -y openjdk-8-jdk-headless -qq > /dev/null      #install openjdk
#   os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-8-openjdk-amd64"     #set environment variable
#   !update-alternatives --set java /usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java
#   !java -version       #check java version

def prepare_repo(root_folder):
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
  cmd_morph1 = ["7z", "a",  "-sfx", morph_folder_name+"'/flookup.exe'", morph_folder_name+"'/flookup'"]
  subprocess.Popen(cmd_morph1, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
  cmd_morph2 = ["chmod",  "755", morph_folder_name+"'/flookup'"]
  subprocess.Popen(cmd_morph2, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
  # IMG
  zipWikiImg = os.path.join(root_folder, 'WikipediaPage_Generator', 'code', 'wikipedia-images.zip')
  unzipTo(zipWikiImg, triple2predArg)
  # SPARQL wrapper
  pipInstall(SPARQLWrapper)
  # Set other paths
  props_list_path = os.path.join(root_folder, 'DCU_TCD_FORGe_WebNLG23', 'code', 'sorted_properties.txt')

prepare_repo(os.path.join('/content', 'webnlg_demo')