import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

nltk.download('punkt')
nltk.download('stopwords')

class NLPModule:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.disease_responses = {
    'cancer': "It is stage 5. It is incurable.",
    'tuberculosis': "You should go and consult a doctor.",
    'pain': "You should go and take a painkiller.",
    'influenza': "Rest and stay hydrated. If symptoms persist, consult a doctor.",
    'diabetes': "Maintain a healthy lifestyle and follow your doctor's advice for managing blood sugar levels.",
    'hypertension': "Monitor your blood pressure regularly and follow a low-sodium diet. Consult a doctor for medication if necessary.",
    'asthma': "Use your inhaler as prescribed by your doctor. Seek medical attention if you experience severe symptoms.",
    'arthritis': "Engage in regular physical activity and consider medication prescribed by your doctor for pain management.",
    'migraine': "Rest in a quiet, dark room. Consider taking medication prescribed by your doctor.",
    'depression': "Seek support from friends, family, or a mental health professional. Consider therapy or medication.",
    'anxiety': "Practice relaxation techniques and seek support from a therapist. Medication may be prescribed by a doctor if necessary.",
    'obesity': "Adopt a healthy diet and exercise regularly. Consult a doctor for personalized advice and support.",
    'stroke': "Seek emergency medical attention immediately. Time is crucial for treatment.",
    'heartdisease': "Follow a heart-healthy diet and exercise regularly. Consult a cardiologist for personalized advice.",
    'kidneydisease': "Monitor your kidney function regularly and follow a low-protein diet. Consult a nephrologist for personalized advice.",
    'liverdisease': "Avoid alcohol and follow a healthy diet. Consult a hepatologist for personalized advice and treatment.",
    'osteoporosis': "Ensure an adequate intake of calcium and vitamin D. Consult a doctor for medication if necessary.",
    'bronchitis': "Rest, drink fluids, and use a humidifier. Consult a doctor if symptoms worsen or persist.",
    'pneumonia': "Get plenty of rest and stay hydrated. Antibiotics may be prescribed by a doctor if the cause is bacterial.",
    'gastritis': "Avoid spicy and acidic foods. Eat smaller, more frequent meals. Consult a gastroenterologist for personalized advice.",
    'gout': "Follow a low-purine diet and stay hydrated. Medication may be prescribed by a doctor to manage symptoms.",
    'fibromyalgia': "Engage in gentle exercise and practice stress-management techniques. Medication may be prescribed for pain relief.",
    'chronicfatiguesyndrome': "Practice pacing and energy conservation. Cognitive behavioral therapy may be helpful. Consult a doctor for management strategies.",
    'Alzheimerdisease': "Create a supportive environment and consider medication prescribed by a neurologist. Seek support from caregivers.",
    'Parkinsondisease': "Engage in regular exercise and follow medication regimens prescribed by a neurologist. Seek support from caregivers.",
    'schizophrenia': "Stay on medication as prescribed by a psychiatrist. Engage in therapy and seek support from loved ones.",
    'endometriosis': "Consult a gynecologist for personalized treatment options, which may include medication or surgery.",
    'anemia': "Eat a diet rich in iron and take iron supplements if prescribed by a doctor. Consult a hematologist for personalized advice.",
    'fibroids': "Consult a gynecologist for personalized treatment options, which may include medication or surgery.",
    'PCOS': "Maintain a healthy weight and consider medication prescribed by a gynecologist. Lifestyle changes may help manage symptoms.",
    'menopause': "Consult a gynecologist for personalized advice on managing symptoms, which may include hormone therapy or lifestyle changes.",
    'infertility': "Consult a fertility specialist for personalized treatment options, which may include medication or assisted reproductive technologies.",
    'pregnancy': "Attend regular prenatal check-ups and follow your doctor's advice for a healthy pregnancy.",
    'miscarriage': "Seek emotional support and follow your doctor's advice for physical recovery. Consider counseling if needed.",
    'menstrualcramps': "Apply heat to the abdomen and consider over-the-counter pain relievers. Consult a gynecologist for severe or persistent pain.",
    'yeast infection': "Use over-the-counter antifungal treatments or consult a gynecologist for prescription medication.",
    'UTI': "Drink plenty of water and cranberry juice. Consult a doctor for antibiotics if necessary.",
    'STDs': "Practice safe Sex",
    'HIV/AIDS': "Consult a doctor for antiretroviral therapy and follow-up care.",
    'HPV': "Get vaccinated and attend regular screenings. Consult a doctor for treatment options if necessary.",
    'herpes': "Use antiviral medications as prescribed by a doctor",
    'chlamydia': "Consult a doctor for antibiotics and follow-up testing. Practice",
    'gonorrhea': "Consult a doctor for antibiotics and follow-up testing. Practice",
    'syphilis': "Consult a doctor for antibiotics and follow-up testing. Practice",
    'hepatitis': "Consult a doctor for antiviral medications and follow-up care.",
    'COVID-19': "Follow public health guidelines, wear a mask, practice social distancing, and get vaccinated when eligible.",
    'common cold': "Rest, drink fluids, and consider over-the-counter remedies for symptom relief.",
    'flu': "Rest, drink fluids, and consider antiviral medications if prescribed by a doctor.",
    'allergies': "Avoid triggers, use antihistamines, and consider allergy shots for long-term management.",
    'asthma': "Use inhalers as prescribed, avoid triggers, and seek medical attention for severe symptoms.",
    'eczema': "Moisturize regularly, avoid irritants, and use topical steroids as prescribed by a doctor.",
    'psoriasis': "Moisturize, avoid triggers, and use topical treatments or medications as prescribed by a dermatologist.",
    'acne': "Use gentle cleansers, avoid picking or squeezing, and consider topical or oral medications prescribed by a dermatologist.",
    'rosacea': "Avoid triggers like spicy foods and alcohol, use gentle skincare products, and consider prescription medications.",
    'hives': "Avoid triggers, use antihistamines, and seek medical attention for severe or persistent hives.",
    'sunburn': "Apply aloe vera or moisturizer, stay hydrated, and avoid further sun exposure.",
    'frostbite': "Gradually warm the affected area, avoid rubbing, and seek medical attention for severe frostbite.",
    'heatexhaustion': "Move to a cool place, drink fluids, and rest. Seek medical attention if symptoms worsen.",
    'concussion': "Rest and avoid physical or mental exertion. Seek medical attention for severe symptoms.",
    'sprain': "Rest, ice, compress, and elevate the affected area. Consider physical therapy for recovery.",
    'fracture': "Immobilize the affected area, seek medical attention, and follow the doctor's advice for recovery.",
    'burns': "Cool the burn with running water, cover with a clean cloth, and seek medical attention for severe burns.",
    'cuts': "Clean the wound, apply pressure to stop bleeding, and seek medical attention for deep or severe cuts.",
    'bites': "Clean the bite, apply antiseptic, and seek medical attention for animal or severe bites.",
    'stings': "Remove the stinger, clean the area, and apply ice or antihistamines for relief.",
    'poisoning': "Call poison control, follow their advice, and seek medical attention if necessary.",
    'choking': "Perform the Heimlich maneuver, call emergency services, and follow their instructions.",
    'heart attack': "Call emergency services, chew aspirin if available, and wait for medical help to arrive.",
    'stroke': "Remember FAST (Face drooping, Arm weakness, Speech difficulty, Time to call 911) and seek immediate medical attention.",
    'seizure': "Clear the area, protect the person from injury, and stay with them until the seizure ends.",
    'diabetic emergency': "Give sugar or glucose tablets, call emergency services, and follow their instructions.",
    'anaphylaxis': "Use an epinephrine auto-injector if available, call emergency services, and seek medical attention.",
    'drowning': "Remove from water, perform CPR if trained, and call emergency services.",
    'hypothermia': "Gradually warm the person, remove wet clothing, and seek medical attention for severe cases.",
    'heatstroke': "Move to a cool place, apply cool cloths, and seek medical attention for severe symptoms.",
    'dehydration': "Drink fluids, rest, and seek medical attention if symptoms persist.",
    'foodpoisoning': "Stay hydrated, rest, and seek medical attention if symptoms worsen or persist.",
    'motionsickness': "Sit in the front seat, focus on the horizon, and consider medication for prevention.",





}


    def process_input(self, input_text):
        tokens = word_tokenize(input_text.lower())
        # Remove stop words
        tokens = [word for word in tokens if word not in self.stop_words]
        return tokens

    def generate_response(self, tokens):
        if 'hello' in tokens:
            return "Hi"
        elif 'how' in tokens and 'are' in tokens and 'you' in tokens:
            return "I'm doing well, thank you!"
        else:
            # Check if any disease name is mentioned
            for word in tokens:
                if word in self.disease_responses:
                    return self.disease_responses[word]
            return "I'm sorry, I didn't understand that."

# Example usage:
nlp = NLPModule()
input_text = "Hello, how are you?"
tokens = nlp.process_input(input_text)
response = nlp.generate_response(tokens)
print(response)

# Example usage for disease:
input_text = "I have cancer."
tokens = nlp.process_input(input_text)
response = nlp.generate_response(tokens)
print(response)
