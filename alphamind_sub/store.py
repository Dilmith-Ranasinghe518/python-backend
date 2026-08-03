from typing import Dict, Any, Optional
from database import db

# MongoDB collection for AlphaMind Courses
courses_collection = db.get_collection("alphamind_courses")

def get_all_courses() -> Dict[str, Any]:
    try:
        docs = list(courses_collection.find({}, {"_id": 0}))
        res = {}
        for doc in docs:
            res[str(doc["id"])] = doc
        return res
    except Exception as e:
        print(f"MongoDB get_all_courses error: {e}")
        return {}

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
    
    # Save directly to MongoDB
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
