# Automatic medical report generation

## Datenintegration

1. Recherche welche Datensätze für Aufgabenstellung geeignet sind
   - Huggingface, ncbi/Open-Patients (https://huggingface.co/datasets/ncbi/Open-Patients)
   - ~180k patient descriptions 
2. Recherche welches Modell geeignet und wie integrieren?
   - Nutzen von Hugingface Inference API mittels python lib huggingface_hub
   - Modell: https://huggingface.co/mistralai/Mistral-Nemo-Instruct-2407
  
## Erste Ergebnisse
- Using prompt: "Please create a medical report including sections about Patient History, Clinical Findings and Treatment Options based on this Patient description: 
- Example patient description: "A 58-year-old nonsmoker white female with mild exertional dyspnea and occasional cough is found to have a left lung mass on chest x-ray. She is otherwise asymptomatic. A neurologic examination is unremarkable, but a CT scan of the head shows a solitary mass in the right frontal lobe."
- Output: 
   ```console 
      The patient has no significant medical history and is not taking any medications.

      Patient History:
      - Age: 58 years old
      - Gender: Female
      - Race: White
      - Smoking status: Nonsmoker
      - Occupation: Not specified
      - Family history: Not specified
      - Medical history:
      - Mild exertional dyspnea (shortness of breath with physical activity)
      - Occasional cough
      - No other significant medical history mentioned
      - Medications: None
      - Allergies: Not specified
      - Immunizations: Not specified
      - Social history: Not specified (other than smoking status)

      Clinical Findings:
      - Chest X-ray: Left lung mass identified
      - CT scan of the head: Solitary mass in the right frontal lobe
      - Neurologic examination: Unremarkable (no abnormalities detected)
      - Other diagnostic tests: Not specified

      Treatment Options:
      1. **Pulmonary mass (left lung):**
         - Further imaging studies (e.g., PET scan, MRI) to determine the nature and extent of the mass.
         - Biopsy (e.g., CT-guided, bronchoscopic, or surgical) to obtain a tissue diagnosis.
         - Surgical resection (e.g., lobectomy, pneumonectomy) if the mass is deemed resectable and the patient is a suitable candidate for surgery.
         - Adjuvant therapy (e.g., chemotherapy, radiation therapy) based on the biopsy results and stage of the disease.
         - Palliative care if the mass is unresectable or the patient is not a suitable candidate for curative intent treatment.

      2. **Brain mass (right frontal lobe):**
         - Further imaging studies (e.g., MRI with contrast, functional MRI, or PET scan) to better characterize the mass and its relationship to surrounding structures.
         - Neurosurgical consultation for consideration of biopsy or resection, depending on the mass's location, size, and nature.
         - Stereotactic radiosurgery or radiation therapy as an alternative or adjunct to surgical intervention, depending on the mass's characteristics and the patient's overall health.
         - Neuro-oncologic consultation for management of potential metastases or primary brain tumors, including consideration of systemic therapy (e.g., chemotherapy, targeted therapy) based on the biopsy results.
         - Palliative care and supportive measures to manage symptoms and improve quality of life.

      Given the patient's asymptomatic presentation and the presence of both a pulmonary and a brain mass, a multidisciplinary approach involving pulmonary medicine, neurosurgery, medical oncology, and radiation oncology is recommended to optimize patient care and treatment planning.
   ```

## Verbesserungen
- Es wurde bei manchen reports beobachtet, dass das Modell halluziniert und Punkte in den Bericht hinzufügt, die überhaupt nicht genannt werden. 
   --> Um dies zu verhindern wurde der Prompt etwas verändert:
   ```console
   Please create a short medical report only including sections about Patient History, Clinical Findings + Diagnosis and Treatment Options based on this Patient description: 
   ```