import os
import json
from typing import Dict, Any, List, Optional
try:
    from database import db
    courses_collection = db.get_collection("alphamind_courses")
except Exception as e:
    courses_collection = None

JSON_STORE_PATH = os.path.join(os.path.dirname(__file__), "alphamind_courses.json")

DEFAULT_COURSES = {
    "1": {
        "id": 1,
        "title": "What Is Generative Artificial Intelligence?",
        "instructor": "Pinar Seyhan Demirdag",
        "duration": "1h 3m",
        "badge": "Popular",
        "badgeColor": "bg-purple-100 text-purple-800",
        "image": "/images/Poster1.jpg",
        "preview": "Learn the fundamentals of generative AI and how it's transforming industries...",
        "category": "Generative AI",
        "chapters": [
            {
                "id": 1,
                "title": "Introduction",
                "lessons": [
                    {
                        "id": 1,
                        "title": "What is Generative AI?",
                        "duration": "5m 23s",
                        "completed": False,
                        "videoUrl": "https://www.youtube.com/watch?v=1ukSR1GRtMU",
                        "description": "Understand the fundamentals of generative artificial intelligence and its applications.",
                        "objectives": [
                            "Define generative AI and its key characteristics.",
                            "Identify common applications of generative AI."
                        ],
                        "transcript": [
                            {"timestamp": "0:00", "text": "Welcome to the Generative AI course."},
                            {"timestamp": "0:15", "text": "Generative AI creates new content like text and images."}
                        ],
                        "resources": [],
                        "studyMaterials": ["/images/Poster1.jpg", "/images/Poster2.jpg"]
                    },
                    {
                        "id": 2,
                        "title": "Understanding Foundation Models",
                        "duration": "8m 45s",
                        "completed": False,
                        "videoUrl": "https://www.youtube.com/watch?v=bKueYVtV0eA",
                        "description": "Explore foundation models and their role as the building blocks of modern GenAI.",
                        "objectives": ["Explain what a foundation model is."],
                        "transcript": [],
                        "resources": [],
                        "studyMaterials": ["/images/Poster3.jpg"]
                    }
                ]
            }
        ]
    }
}

def load_courses_from_json() -> Dict[str, Any]:
    if os.path.exists(JSON_STORE_PATH):
        try:
            with open(JSON_STORE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                if data:
                    return data
        except Exception:
            pass
    # Initialize with default
    save_courses_to_json(DEFAULT_COURSES)
    return DEFAULT_COURSES

def save_courses_to_json(courses: Dict[str, Any]) -> None:
    try:
        with open(JSON_STORE_PATH, "w", encoding="utf-8") as f:
            json.dump(courses, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving to JSON store: {e}")

def get_all_courses() -> Dict[str, Any]:
    if courses_collection is not None:
        try:
            docs = list(courses_collection.find({}, {"_id": 0}))
            if docs:
                res = {}
                for doc in docs:
                    res[str(doc["id"])] = doc
                return res
        except Exception as e:
            print(f"MongoDB query failed, using JSON fallback: {e}")
    
    return load_courses_from_json()

def get_course_by_id(course_id: int) -> Optional[Dict[str, Any]]:
    courses = get_all_courses()
    return courses.get(str(course_id))

def save_or_update_course(course_data: Dict[str, Any]) -> Dict[str, Any]:
    courses = get_all_courses()
    
    if "id" not in course_data or not course_data["id"]:
        # Generate new integer ID
        existing_ids = [int(k) for k in courses.keys() if k.isdigit()]
        new_id = max(existing_ids) + 1 if existing_ids else 1
        course_data["id"] = new_id
    else:
        course_data["id"] = int(course_data["id"])
    
    cid_str = str(course_data["id"])
    courses[cid_str] = course_data
    
    # Save to MongoDB if available
    if courses_collection is not None:
        try:
            courses_collection.update_one(
                {"id": course_data["id"]},
                {"$set": course_data},
                upsert=True
            )
        except Exception as e:
            print(f"MongoDB update failed: {e}")
            
    # Always save to local JSON file as backup
    save_courses_to_json(courses)
    return course_data

def delete_course_by_id(course_id: int) -> bool:
    courses = get_all_courses()
    cid_str = str(course_id)
    if cid_str in courses:
        del courses[cid_str]
        
        if courses_collection is not None:
            try:
                courses_collection.delete_one({"id": course_id})
            except Exception as e:
                print(f"MongoDB delete failed: {e}")
                
        save_courses_to_json(courses)
        return True
    return False
