import os
import openai
import json


OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
print('sinde', OPENAI_API_KEY)
openai.organization = 'org-ehFJel4pn7hkAYdl3HHe4zxd'
openai.api_key = OPENAI_API_KEY


def best_match(raw, candidates):
    candidatesString = ';'.join(candidates)
    return openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {
                'role': 'system',
                'content': 'You are a classifying system, you will receive a an expression or word and pick the best match from a list of possible answers.'
            },
            {
                'role': 'user',
                'content': f'Here are a list of all the candidates separated by ";": {candidatesString}'
            },
            {
                'role': 'assistant',
                'content': f'Awesome, I have identified {len(candidates)} candidates, from now on I will only answer with a possible candidate e.g. "{candidates[0]}"'
            },
            {
                'role': 'user',
                'content': f'What candidate fits best for: {raw}'
            },
        ]
    )['choices'][0]['message']['content']


def best_matches(raw, candidates):
    candidatesString = ';'.join(candidates)
    if len(candidates) < 2:
        return candidates[0]
    return openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {
                'role': 'system',
                'content': 'You are a classifying system, you will receive a an expression or word and pick the best matches from a list of possible answers. You can select however many matches you think make sense. keep in mind the input may be contextual as "everything but X" which should return everything but that X.'
            },
            {
                'role': 'user',
                'content': f'Here are a list of all the candidates separated by ";": {candidatesString}'
            },
            {
                'role': 'assistant',
                'content': f'Awesome, I have identified {len(candidates)} candidates, from now on I will only answer with a possible candidates in a comma-separated list (if more matches are identified) e.g. "{candidates[0]}" or "{candidates[0]},{candidates[1]}".'
            },
            {
                'role': 'user',
                'content': f'What candidate fits best for: {candidates[0]}ss'
            },
            {
                'role': 'assistant',
                'content': candidates[0]
            },
            {
                'role': 'user',
                'content': f'What candidate fits best for: {raw}'
            },
        ]
    )['choices'][0]['message']['content'].split(',')


def extract_json_into_template(raw, template):
    print(json.dumps(raw, indent=2))
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {
                'role': 'system',
                'content': 'You are a system that takes a json object and populates variables within a template with the relevant data'
            },
            {
                'role': 'user',
                'content': 'Let us start with a simple example: INPUT: {"firstName": "Peter", "age": 14} TEMPLATE: Hi {name}'
            },
            {
                'role': 'assistant',
                'content': 'Hi Peter'
            },
            {
                'role': 'user',
                'content': f'perfect, another one INPUT: {json.dumps(raw)} TEMPLATE: {template}'
            },
        ]
    )['choices'][0]['message']['content']

    return response


