# general imports
import os
import json

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

        with open(os.path.join(os.getcwd(), 'LLM', "hyperparameters.json"), "r") as f:
            hyperparameters = json.load(f)    
        self.hyperparameters = hyperparameters[model_id]

        self.model = ModelFactory.get(model_id)


    def construct_prompt(self, sample, lan, prompt_type):
        start_instr = self.hyperparameters['start_instr']
        end_instr = self.hyperparameters['end_instr']
        start_ans = self.hyperparameters['start_ans']

        language = self.lan2text[lan] if lan in self.lan2text else lan

        if prompt_type == 'zero_shot':
            return self.hyperparameters['zero_shot'].format(triples=preprocess_triples(sample, triples_div=self.hyperparameters['triples_div']), 
                                                    language=language, start_instr=start_instr, end_instr=end_instr, 
                                                    start_ans=start_ans)
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
                                                                    examples=examples)
            else:
                return self.hyperparameters['zero_shot'].format(triples=preprocess_triples(sample, triples_div=self.hyperparameters['triples_div']), 
                                                    language=language, start_instr=start_instr, end_instr=end_instr, 
                                                    start_ans=start_ans)
        return
    

    def generate_api(self, input_triples, language='EN', prompt_type='zero_shot'):
        input_prompt = self.construct_prompt(input_triples, language, prompt_type)

        result = self.model.run({
            'text': input_prompt,
            'max_tokens': self.hyperparameters['max_new_tokens'],
        })

        if result['status'] == 'SUCCESS':
            output = result['data']
        else:
            output = "Error in generating text"

        return output
    
