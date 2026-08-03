import os
import json
from typing import Dict, Any, List, Optional
try:
    from database import db
    courses_collection = db.get_collection("alphamind_courses")
except Exception as e:
    courses_collection = None

JSON_STORE_PATH = os.path.join(os.path.dirname(__file__), "alphamind_courses.json")

def load_courses_from_json() -> Dict[str, Any]:
    if os.path.exists(JSON_STORE_PATH):
        try:
            with open(JSON_STORE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                if data:
                    return data
        except Exception as e:
            print(f"Error loading JSON store: {e}")
    return {}

def save_courses_to_json(courses: Dict[str, Any]) -> None:
    try:
        with open(JSON_STORE_PATH, "w", encoding="utf-8") as f:
            json.dump(courses, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving to JSON store: {e}")

def get_all_courses() -> Dict[str, Any]:
    json_courses = load_courses_from_json()
    
    if courses_collection is not None:
        try:
            docs = list(courses_collection.find({}, {"_id": 0}))
            if docs:
                res = {}
                for doc in docs:
                    res[str(doc["id"])] = doc
                return res
            elif json_courses:
                # Seed MongoDB from json_courses if MongoDB collection is empty
                for cid, cdata in json_courses.items():
                    courses_collection.update_one(
                        {"id": cdata["id"]},
                        {"$set": cdata},
                        upsert=True
                    )
        except Exception as e:
            print(f"MongoDB query failed, using JSON fallback: {e}")
    
    return json_courses

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
