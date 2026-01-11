import re
from typing import List, Dict

class ClinicalExtractor:
    def __init__(self):
        self.medications = [
            'aspirin', 'metformin', 'albuterol', 'prednisone', 'lisinopril',
            'amoxicillin', 'nitrofurantoin', 'ibuprofen', 'amlodipine',
            'levothyroxine', 'pantoprazole', 'nitro', 'duoneb'
        ]
    
    def extract_vitals_meds(self, text: str) -> Dict[str, List[str]]:
        cleaned = re.sub(r'[\n\r\t]+', ' ', text.strip().lower())
        
        # Precise vitals regex
        vitals = re.findall(r'(bp|hr|rr|spo2|temp|o2)[:\s]*(\d+/?\d*)', cleaned)
        vitals_list = [f"{v[0].upper()}:{v[1]}" for v in vitals]
        
        # Medication extraction
        meds_found = [m for m in self.medications if m in cleaned]
        meds_list = [f"{m.title()} prescribed" for m in set(meds_found)]
        
        return {"vitals": vitals_list, "medications": meds_list}
