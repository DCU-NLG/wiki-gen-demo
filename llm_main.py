import os
from dotenv import load_dotenv
load_dotenv(os.path.join(os.getcwd(), 'LLM', "env_variables.env"))

from LLM.inference_model import PretrainedModel

GPT35_MODEL = PretrainedModel('650aef186eb5635dcf027941')

LLAMA2_70_CHAT_MODEL = PretrainedModel('663501866eb56340906c3491')

'''input_triples=['Robert_Bosch_Automotive_Steering | location | Statue_of_Liberty','Robert_Bosch_Automotive_Steering | location | Israel','Robert_Bosch_Automotive_Steering | industry | backpacking']
output = GPT35_MODEL.generate_api(input_triples, language='EN', prompt_type='zero_shot')
print(output)

output = LLAMA2_70_CHAT_MODEL.generate_api(input_triples, language='EN', prompt_type='zero_shot')
print(output)'''
