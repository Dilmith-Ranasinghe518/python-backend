import os
import json
from typing import Dict, Any, Optional
from database import db

# MongoDB collection for AlphaMind Courses
courses_collection = db.get_collection("alphamind_courses")
JSON_STORE_PATH = os.path.join(os.path.dirname(__file__), "alphamind_courses.json")

def load_initial_json_courses() -> Dict[str, Any]:
    if os.path.exists(JSON_STORE_PATH):
        try:
            with open(JSON_STORE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                if data:
                    return data
        except Exception as e:
            print(f"Error loading initial JSON store: {e}")
    return {}

def seed_mongodb_from_json_if_empty() -> None:
    try:
        if courses_collection.count_documents({}) == 0:
            initial_data = load_initial_json_courses()
            if initial_data:
                for cid, cdata in initial_data.items():
                    courses_collection.update_one(
                        {"id": cdata["id"]},
                        {"$set": cdata},
                        upsert=True
                    )
                print("Seeded MongoDB alphamind_courses collection with initial course data.")
    except Exception as e:
        print(f"MongoDB seeding check error: {e}")

# Run seed check on module load
seed_mongodb_from_json_if_empty()

def get_all_courses() -> Dict[str, Any]:
    try:
        docs = list(courses_collection.find({}, {"_id": 0}))
        if docs:
            res = {}
            for doc in docs:
                res[str(doc["id"])] = doc
            return res
        else:
            # Fallback to initial JSON if database is empty
            seed_mongodb_from_json_if_empty()
            docs = list(courses_collection.find({}, {"_id": 0}))
            res = {}
            for doc in docs:
                res[str(doc["id"])] = doc
            return res
    except Exception as e:
        print(f"MongoDB get_all_courses error: {e}")
        return load_initial_json_courses()

def get_course_by_id(course_id: int) -> Optional[Dict[str, Any]]:
    try:
        doc = courses_collection.find_one({"id": course_id}, {"_id": 0})
        if doc:
            return doc
    except Exception as e:
        print(f"MongoDB get_course_by_id error: {e}")
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
    
    # Save exclusively to MongoDB
    try:
        courses_collection.update_one(
            {"id": course_data["id"]},
            {"$set": course_data},
            upsert=True
        )
        print(f"Successfully saved/updated Course #{course_data['id']} in MongoDB")
    except Exception as e:
        print(f"MongoDB update error: {e}")
        raise e
            
    return course_data

def delete_course_by_id(course_id: int) -> bool:
    try:
        result = courses_collection.delete_one({"id": course_id})
        if result.deleted_count > 0:
            print(f"Successfully deleted Course #{course_id} from MongoDB")
            return True
    except Exception as e:
        print(f"MongoDB delete error: {e}")
        
    return False
