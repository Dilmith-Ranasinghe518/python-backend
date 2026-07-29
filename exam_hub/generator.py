from datetime import datetime
from typing import Dict, List, Any

def fallback_paper_markdown(subject: str, year: int, language: str) -> str:
    safe_subject = (subject or "Subject").strip() or "Subject"
    safe_year = year if isinstance(year, int) and year > 0 else datetime.now().year
    lang = (language or "English").strip() or "English"
    return f"""# G.C.E. O/L — {safe_subject} (Practice Paper)

**Year:** {safe_year} (Practice)  
**Language:** {lang}  
**Time:** 1 Hour 30 Minutes  
**Instructions:** Answer all questions. This is an ORIGINAL practice paper created for study purposes (not an official past paper).

---

## Section B — Structured (1 × 20 = 20 marks)
1. (a) Define a key term related to {safe_subject}. (4)  
   (b) Explain a process or concept with clear steps. (6)  
   (c) Describe an experiment or real-world application. (4)  
   (d) State safety/precautions or common mistakes. (6)

---

## Section C — Essay (1 × 40 = 40 marks)
1. Discuss an important topic in {safe_subject}.  
   Include key points, explanations, and examples."""

def fallback_mcq(subject: str) -> tuple[List[Dict[str, Any]], Dict[str, str]]:
    s = (subject or "Science").lower()
    is_physics = "phys" in s
    is_chem = "chem" in s
    
    if is_physics:
        mcq = [
            {"q": "The SI unit of force is:", "options": ["Joule", "Newton", "Watt", "Pascal"]},
            {"q": "In a series circuit, the current is:", "options": ["Different", "Same", "Zero", "Only in battery"]},
            {"q": "A scalar quantity is:", "options": ["Velocity", "Acceleration", "Force", "Mass"]},
            {"q": "Device to measure current:", "options": ["Voltmeter", "Ammeter", "Ohmmeter", "Thermometer"]},
            {"q": "Power formula is:", "options": ["P = VI", "P = V/I", "P = I/V", "P = V + I"]}
        ]
    elif is_chem:
        mcq = [
            {"q": "Which particle has a positive charge?", "options": ["Electron", "Proton", "Neutron", "Atom"]},
            {"q": "pH of a neutral solution at 25°C is:", "options": ["0", "7", "14", "1"]},
            {"q": "Which is a compound?", "options": ["O₂", "N₂", "H₂O", "He"]},
            {"q": "Same group elements have same:", "options": ["Protons", "Neutrons", "Shells", "Valence electrons"]},
            {"q": "Separate sand from water:", "options": ["Filtration", "Distillation", "Chromatography", "Evaporation only"]}
        ]
    else:
        mcq = [
            {"q": "Which is a renewable energy source?", "options": ["Coal", "Solar", "Diesel", "Gasoline"]},
            {"q": "The closest planet to the Sun is:", "options": ["Earth", "Venus", "Mercury", "Mars"]},
            {"q": "Water freezes at:", "options": ["0°C", "10°C", "50°C", "100°C"]},
            {"q": "A triangle has how many sides?", "options": ["2", "3", "4", "5"]},
            {"q": "Speed is:", "options": ["distance/time", "time/distance", "distance×time", "distance+time"]}
        ]

    key = {"0": "B", "1": "B", "2": "D", "3": "B", "4": "A"}
    return mcq, key

def generate_practice_paper(subject: str, year: int, language: str, provider: str = "template") -> Dict[str, Any]:
    content_markdown = fallback_paper_markdown(subject, year, language)
    mcq, key = fallback_mcq(subject)
    return {
        "content_markdown": content_markdown,
        "mcq": mcq,
        "mcq_answer_key": key,
        "source": provider if provider else "template"
    }
