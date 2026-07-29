import os
import json
from datetime import datetime
from typing import List, Dict, Any, Optional

# Initial Demo Papers seed
DEMO_PAPERS = [
    {
        "id": 100001,
        "title": "G.C.E. O/L Chemistry (Practice) — Demo",
        "subject": "Chemistry",
        "year": 2026,
        "language": "English",
        "source": "demo",
        "created_at": "2026-07-29T10:00:00.000Z",
        "content_markdown": """# G.C.E. O/L — Chemistry (Practice Paper)

**Time:** 1 Hour 30 Minutes  
**Instructions:** Answer all questions. This is an ORIGINAL practice paper (not an official past paper).

---

## Section B — Structured (1 × 20 = 20 marks)
1. (a) Define **isotope** and give one example. (4)  
   (b) Explain why **ionic compounds** conduct electricity when molten but not as solids. (6)  
   (c) Describe an experiment to identify **CO₂ gas**. (4)  
   (d) State two safety precautions when using acids in the lab. (6)

---

## Section C — Essay (1 × 40 = 40 marks)
1. Discuss the factors affecting the **rate of reaction**.  
   In your answer, include: concentration, temperature, surface area, catalysts, and collision theory.""",
        "mcq": [
            {"q": "Which particle has a positive charge?", "options": ["Electron", "Proton", "Neutron", "Atom"]},
            {"q": "The pH value of a neutral solution at 25°C is:", "options": ["0", "7", "14", "1"]},
            {"q": "Which of the following is a compound?", "options": ["O₂", "N₂", "H₂O", "He"]},
            {"q": "In the periodic table, elements in the same group have the same:", "options": ["Number of protons", "Number of neutrons", "Number of electron shells", "Number of valence electrons"]},
            {"q": "Which method is best to separate sand from water?", "options": ["Filtration", "Distillation", "Chromatography", "Evaporation only"]}
        ],
        "mcq_answer_key": {"0": "B", "1": "B", "2": "C", "3": "D", "4": "A"},
        "marking_rubric": "Marking guidance:\n- Structured: award marks for correct definitions, correct reasoning, and clear steps.\n- Essay: award marks for key points, explanations, and logical structure.\n"
    },
    {
        "id": 100002,
        "title": "G.C.E. O/L Physics (Practice) — Demo",
        "subject": "Physics",
        "year": 2026,
        "language": "English",
        "source": "demo",
        "created_at": "2026-07-29T10:05:00.000Z",
        "content_markdown": """# G.C.E. O/L — Physics (Practice Paper)

**Time:** 1 Hour 30 Minutes  
**Instructions:** Answer all questions. This is an ORIGINAL practice paper (not an official past paper).

---

## Section B — Structured (1 × 20 = 20 marks)
1. (a) Define **velocity** and **acceleration**. (6)  
   (b) A car accelerates uniformly from rest to 20 m/s in 5 s. Calculate the acceleration. (4)  
   (c) Explain why a seatbelt reduces injuries during a sudden stop. (4)  
   (d) State two ways to reduce friction in a moving machine. (6)

---

## Section C — Essay (1 × 40 = 40 marks)
1. Discuss how **electrical energy** is transferred and used in a household circuit.  
   Include: series vs parallel, fuses/MCBs, earthing, and power calculation (P = VI).""",
        "mcq": [
            {"q": "The SI unit of force is:", "options": ["Joule", "Newton", "Watt", "Pascal"]},
            {"q": "A speed of 10 m/s is equal to:", "options": ["10 km/h", "36 km/h", "18 km/h", "3.6 km/h"]},
            {"q": "Which is an example of a scalar quantity?", "options": ["Velocity", "Acceleration", "Force", "Mass"]},
            {"q": "In a series circuit, the current is:", "options": ["Different in each component", "Same through all components", "Always zero", "Only in the battery"]},
            {"q": "The device used to measure electric current is:", "options": ["Voltmeter", "Ammeter", "Ohmmeter", "Thermometer"]}
        ],
        "mcq_answer_key": {"0": "B", "1": "B", "2": "D", "3": "B", "4": "B"},
        "marking_rubric": "Marking guidance:\n- Structured: award marks for correct definitions, correct reasoning, and clear steps.\n- Essay: award marks for key points, explanations, and logical structure.\n"
    }
]

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
PAPERS_PATH = os.path.join(DATA_DIR, "exam-hub-papers.json")

def _ensure_data_file():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(PAPERS_PATH):
        max_id = max(p["id"] for p in DEMO_PAPERS)
        initial_store = {
            "nextId": max_id + 1,
            "papers": DEMO_PAPERS
        }
        with open(PAPERS_PATH, "w", encoding="utf-8") as f:
            json.dump(initial_store, f, indent=2)

def _read_store() -> Dict[str, Any]:
    _ensure_data_file()
    try:
        with open(PAPERS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, dict) and "papers" in data and "nextId" in data:
                return data
    except Exception:
        pass
    max_id = max(p["id"] for p in DEMO_PAPERS)
    return {"nextId": max_id + 1, "papers": DEMO_PAPERS}

def _write_store(store: Dict[str, Any]):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(PAPERS_PATH, "w", encoding="utf-8") as f:
        json.dump(store, f, indent=2)

def list_papers() -> List[Dict[str, Any]]:
    # Try MongoDB first
    try:
        from database import db
        col = db.get_collection("exam_hub_papers")
        docs = list(col.find({}, {"_id": 0, "mcq_answer_key": 0, "marking_rubric": 0}).sort("created_at", -1))
        if docs:
            return [{
                "id": d["id"],
                "title": d["title"],
                "subject": d["subject"],
                "year": d["year"],
                "language": d["language"],
                "source": d["source"],
                "created_at": d["created_at"]
            } for d in docs]
    except Exception:
        pass

    # JSON Store Fallback
    store = _read_store()
    papers = sorted(store["papers"], key=lambda p: p.get("created_at", ""), reverse=True)
    return [{
        "id": p["id"],
        "title": p["title"],
        "subject": p["subject"],
        "year": p["year"],
        "language": p["language"],
        "source": p["source"],
        "created_at": p["created_at"]
    } for p in papers]

def get_paper(paper_id: int) -> Optional[Dict[str, Any]]:
    # Try MongoDB first
    try:
        from database import db
        col = db.get_collection("exam_hub_papers")
        doc = col.find_one({"id": paper_id}, {"_id": 0})
        if doc:
            return doc
    except Exception:
        pass

    # JSON Store Fallback
    store = _read_store()
    for p in store["papers"]:
        if p["id"] == paper_id:
            return p
    return None

def create_paper(paper_input: Dict[str, Any]) -> Dict[str, Any]:
    store = _read_store()
    new_id = store["nextId"]
    store["nextId"] += 1
    created_at = datetime.utcnow().isoformat() + "Z"

    paper_record = {
        **paper_input,
        "id": new_id,
        "created_at": created_at
    }

    # Save to JSON Store
    store["papers"].insert(0, paper_record)
    _write_store(store)

    # Save to MongoDB if available
    try:
        from database import db
        col = db.get_collection("exam_hub_papers")
        col.insert_one(dict(paper_record))
    except Exception:
        pass

    return paper_record
