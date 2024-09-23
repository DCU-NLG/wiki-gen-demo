# general imports
import os
import json
from functools import lru_cache

# model related imports
from aixplain.factories.model_factory import ModelFactory


def preprocess_triples(triples, triples_div="; "):
    return triples_div.join(triples).replace(" | ", " ")


class PretrainedModel:
    def __init__(self, model_id, seed=42):

        self.lan2text = {
            'EN': 'English',
            'ZH': 'Chinese',   
            'DE': 'German',  
            'RU': 'Russian',   
            'ES': 'Spanish',   
            'KO': 'Korean',   
            'HI': 'Hindi',   
            'SW': 'Swahili',   
            'AR': 'Arabic' 
        }

        self.possible_genders = ['Feminine', 'Masculine', 'Other']

        with open(os.path.join(os.getcwd(), 'llm', "hyperparameters.json"), "r") as f:
            hyperparameters = json.load(f)    
        self.hyperparameters = hyperparameters[model_id]

        self.model = ModelFactory.get(model_id)

    def construct_prompt(self, sample, lan, prompt_type, gender=None):
        start_instr = self.hyperparameters['start_instr']
        end_instr = self.hyperparameters['end_instr']
        start_ans = self.hyperparameters['start_ans']

        language = self.lan2text[lan] if lan in self.lan2text else lan

        gender_text = ""
        if gender in self.possible_genders:
            gender_text = self.hyperparameters['gender_template'].format(gender=gender)

        if prompt_type == 'zero_shot':
            return self.hyperparameters['zero_shot'].format(triples=preprocess_triples(sample, triples_div=self.hyperparameters['triples_div']), 
                                                    language=language, start_instr=start_instr, end_instr=end_instr, 
                                                    start_ans=start_ans, gender=gender_text)
        elif prompt_type == 'few_shot':
            examples = self.hyperparameters['few_shot']['fixed_examples']

            if lan in examples[0]['target']:

                examples = [self.hyperparameters['few_shot']['example'].format(triples=preprocess_triples(example['input'], 
                                                                                                    triples_div=self.hyperparameters['triples_div']), 
                                                                        i=i+1, target=example['target'][lan]) 
                                                                        for i, example in enumerate(examples)]
            
                examples = self.hyperparameters['few_shot']['examples_divider'].join(examples)
            
                return self.hyperparameters['few_shot']['instruction'].format(triples=preprocess_triples(sample, 
                                                                                            triples_div=self.hyperparameters['triples_div']), 
                                                                    language=language, 
                                                                    start_instr=start_instr, 
                                                                    end_instr=end_instr, 
                                                                    start_ans=start_ans, 
                                                                    examples=examples,
                                                                    gender=gender_text)
            else:
                return self.hyperparameters['zero_shot'].format(triples=preprocess_triples(sample, triples_div=self.hyperparameters['triples_div']), 
                                                    language=language, start_instr=start_instr, end_instr=end_instr, 
                                                    start_ans=start_ans, gender=gender_text)
        return

    def generate_api(self, input_triples, language='EN', prompt_type='zero_shot', gender=None):
        input_prompt = self.construct_prompt(input_triples, language, prompt_type, gender=gender)

        result = self.model.run({
            'text': input_prompt,
            'max_tokens': self.hyperparameters['max_new_tokens'],
        })

        if result['status'] == 'SUCCESS':
            output = result['data']
        else:
            output = "Error in generating text"

        return output
    

@lru_cache(maxsize=None)
def get_gpt35_turbo():
    return PretrainedModel('640b517694bf816d35a59125')


@lru_cache(maxsize=None)
def get_llama2_70_chat():
    return PretrainedModel('663501866eb56340906c3491')


@lru_cache(maxsize=None)
def get_mistral_instruct_v3():
    return PretrainedModel('66a15b16b1c031832a163bde')


# instantiate for export to other modules
gpt_35_turbo_model = get_gpt35_turbo()
llama2_70_chat_model = get_llama2_70_chat()
#mistral_instruct_v3_model = get_mistral_instruct_v3()

