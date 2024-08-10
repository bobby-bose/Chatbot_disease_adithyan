import json
import random


def load_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def find_matching_prognosis(prompt, data):
    keywords = [
        'acidity', 'indigestion', 'headache', 'blurred_and_distorted_vision',
        'excessive_hunger', 'muscle_weakness', 'stiff_neck', 'swelling_joints',
        'movement_stiffness', 'depression', 'irritability', 'visual_disturbances',
        'painful_walking', 'abdominal_pain', 'nausea', 'vomiting', 'blood_in_mucus',
        'Fatigue', 'Fever', 'Dehydration', 'loss_of_appetite', 'cramping',
        'blood_in_stool', 'gnawing', 'upper_abdomain_pain', 'fullness_feeling',
        'hiccups', 'abdominal_bloating', 'heartburn', 'belching', 'burning_ache'
    ]

    symptoms = prompt.split(", ")

    max_count = 0
    matching_prognosis = None
    matching_drug = None
    for entry in data:
        count = sum(1 for keyword in keywords if entry[keyword] == 1 and keyword in symptoms)
        if count > max_count:
            max_count = count
            matching_prognosis = entry["prognosis"]
            matching_drug = entry["drug"]

    return matching_prognosis, matching_drug


# Load data from output.json
data = load_data("output.json")

# Sample prompt
prompt = "nausea"

matching_prognosis, matching_drug = find_matching_prognosis(prompt, data)
print("Matching Prognosis:", matching_prognosis)
print("Matching Drug:", matching_drug)
