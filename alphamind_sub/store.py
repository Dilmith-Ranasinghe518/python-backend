from typing import Dict, Any, Optional, List
from database import db

# MongoDB collections
courses_collection = db.get_collection("alphamind_courses")
courses_page_collection = db.get_collection("alphamind_courses_page")
books_page_collection = db.get_collection("alphamind_books_page")

DEFAULT_COURSES_PAGE_DATA = {
    "heroImage": "/images/Poster1.jpg",
    "carouselItems": [
        {
            "id": "subj-1",
            "name": "What is Generative AI?",
            "image": "/images/Poster1.jpg",
            "badge": "Best seller",
            "pill": "Free with Plus"
        },
        {
            "id": "subj-2",
            "name": "Understanding Foundation Models",
            "image": "/images/Poster3.jpg",
            "badge": "New",
            "pill": "Free with Plus"
        },
        {
            "id": "subj-3",
            "name": "Generative AI Use Cases",
            "image": "/images/Poster5.jpg",
            "badge": "Best seller",
            "pill": "Free with Plus"
        },
        {
            "id": "subj-4",
            "name": "Model Capabilities and Limits",
            "image": "/images/Poster7.jpg",
            "badge": "New",
            "pill": "Free with Plus"
        },
        {
            "id": "subj-5",
            "name": "Getting Started Toolkit",
            "image": "/images/Poster8.jpg",
            "badge": "Best seller",
            "pill": "Free with Plus"
        },
        {
            "id": "subj-6",
            "name": "Training AI Models",
            "image": "/images/Poster9.jpg",
            "badge": "New",
            "pill": "Free with Plus"
        }
    ],
    "contents": [
        {
            "id": "cnt-1",
            "subjectId": "subj-1",
            "title": "Introduction",
            "subcontents": [
                {
                    "id": "sub-1",
                    "title": "What is Generative AI?",
                    "duration": "5m 23s video",
                    "completed": False,
                    "videoUrl": "https://www.youtube.com/watch?v=1ukSR1GRtMU",
                    "description": "Understand the fundamentals of generative artificial intelligence and its applications.",
                    "resources": [],
                    "studyMaterials": ["/images/Poster1.jpg"]
                },
                {
                    "id": "sub-2",
                    "title": "Understanding Foundation Models",
                    "duration": "8m 45s video",
                    "completed": False,
                    "videoUrl": "https://www.youtube.com/watch?v=bKueYVtV0eA",
                    "description": "Explore foundation models and their role as the building blocks of modern GenAI.",
                    "resources": [],
                    "studyMaterials": ["/images/Poster3.jpg"]
                },
                {
                    "id": "sub-3",
                    "title": "Generative AI Use Cases",
                    "duration": "7m 12s video",
                    "completed": False,
                    "videoUrl": "https://www.youtube.com/watch?v=LtlsX_lCfK4",
                    "description": "Explore practical generative AI deployments.",
                    "resources": [],
                    "studyMaterials": ["/images/Poster5.jpg"]
                }
            ]
        },
        {
            "id": "cnt-2",
            "subjectId": "subj-1",
            "title": "Core Concepts",
            "subcontents": [
                {
                    "id": "sub-4",
                    "title": "Training AI Models",
                    "duration": "12m 30s video",
                    "completed": False,
                    "videoUrl": "https://www.youtube.com/watch?v=1ukSR1GRtMU",
                    "description": "Deep dive into model pre-training and fine-tuning.",
                    "resources": [],
                    "studyMaterials": ["/images/Poster9.jpg"]
                }
            ]
        }
    ],
    "contentCards": [
        {
            "id": "card-1",
            "subcontentId": "sub-1",
            "title": "What is Generative AI?",
            "subtitle": "A course by Pinar Seyhan Demirdag",
            "description": "Understand the fundamentals of generative artificial intelligence and its applications across various fields.",
            "image": "/images/Poster1.jpg",
            "badge": "BEST SELLER",
            "learners": "133,854",
            "rating": "95% (2.65K)",
            "pill": "FREE WITH PLUS"
        },
        {
            "id": "card-2",
            "subcontentId": "sub-2",
            "title": "Understanding Foundation Models",
            "subtitle": "A course by Pinar Seyhan Demirdag",
            "description": "Explore the concept of foundation models and their role as the building blocks of modern GenAI systems.",
            "image": "/images/Poster3.jpg",
            "badge": "NEW",
            "learners": "136,041",
            "rating": "94% (2.54K)",
            "pill": "FREE WITH PLUS"
        }
    ]
}

def get_courses_page_data() -> Dict[str, Any]:
    try:
        doc = courses_page_collection.find_one({"pageId": "courses_page"}, {"_id": 0})
        if doc:
            return doc
        else:
            # Seed initial page data
            data = {"pageId": "courses_page", **DEFAULT_COURSES_PAGE_DATA}
            courses_page_collection.update_one(
                {"pageId": "courses_page"},
                {"$set": data},
                upsert=True
            )
            return data
    except Exception as e:
        print(f"MongoDB get_courses_page_data error: {e}")
        return {"pageId": "courses_page", **DEFAULT_COURSES_PAGE_DATA}

def save_courses_page_data(data: Dict[str, Any]) -> Dict[str, Any]:
    data["pageId"] = "courses_page"
    try:
        courses_page_collection.update_one(
            {"pageId": "courses_page"},
            {"$set": data},
            upsert=True
        )
        print("Successfully saved CoursesPageData in MongoDB")
    except Exception as e:
        print(f"MongoDB save_courses_page_data error: {e}")
        raise e
    return data

DEFAULT_BOOKS_PAGE_DATA = {
    "heroImage": "/images/Poster1.jpg",
    "carouselItems": [
        {
            "id": "slide-1",
            "name": "Combined Maths",
            "image": "/images/Poster1.jpg",
            "badge": "Popular",
            "pill": "Free with Plus"
        },
        {
            "id": "slide-2",
            "name": "Physics",
            "image": "/images/Poster3.jpg",
            "badge": "Best seller",
            "pill": "Free with Plus"
        },
        {
            "id": "slide-3",
            "name": "Chemistry",
            "image": "/images/Poster5.jpg",
            "badge": "New",
            "pill": "Free with Plus"
        },
        {
            "id": "slide-4",
            "name": "Biology",
            "image": "/images/Poster7.jpg",
            "badge": "Popular",
            "pill": "Free with Plus"
        },
        {
            "id": "slide-5",
            "name": "ICT",
            "image": "/images/Poster8.jpg",
            "badge": "Best seller",
            "pill": "Free with Plus"
        },
        {
            "id": "slide-6",
            "name": "Business Studies",
            "image": "/images/Poster9.jpg",
            "badge": "New",
            "pill": "Free with Plus"
        }
    ],
    "contents": [
        {
            "id": "cnt-b1",
            "subjectId": "slide-1",
            "title": "Introduction",
            "subcontents": [
                {
                    "id": "sub-b1",
                    "title": "What is Generative AI?",
                    "duration": "5m 23s video",
                    "completed": False,
                    "videoUrl": "https://www.youtube.com/watch?v=1ukSR1GRtMU",
                    "description": "Understand the fundamentals of generative artificial intelligence and its applications.",
                    "resources": [],
                    "studyMaterials": ["/images/Poster1.jpg"]
                },
                {
                    "id": "sub-b2",
                    "title": "Understanding Foundation Models",
                    "duration": "8m 45s video",
                    "completed": False,
                    "videoUrl": "https://www.youtube.com/watch?v=bKueYVtV0eA",
                    "description": "Explore foundation models and their role as the building blocks of modern GenAI.",
                    "resources": [],
                    "studyMaterials": ["/images/Poster3.jpg"]
                }
            ]
        }
    ],
    "contentCards": [
        {
            "id": "card-b1",
            "subcontentId": "sub-b1",
            "title": "What is Generative AI?",
            "subtitle": "A course by Pinar Seyhan Demirdag",
            "description": "Understand the fundamentals of generative artificial intelligence and its applications across various fields.",
            "image": "/images/Poster1.jpg",
            "badge": "BEST SELLER",
            "learners": "133,854",
            "rating": "95% (2.65K)",
            "pill": "FREE WITH PLUS",
            "price": "520",
            "ratingValue": "4.8"
        },
        {
            "id": "card-b2",
            "subcontentId": "sub-b2",
            "title": "Understanding Foundation Models",
            "subtitle": "A course by Pinar Seyhan Demirdag",
            "description": "Explore the concept of foundation models and their role as the building blocks of modern GenAI systems.",
            "image": "/images/Poster3.jpg",
            "badge": "NEW",
            "learners": "136,041",
            "rating": "94% (2.54K)",
            "pill": "FREE WITH PLUS",
            "price": "555",
            "ratingValue": "4.7"
        }
    ]
}

def get_books_page_data() -> Dict[str, Any]:
    try:
        doc = books_page_collection.find_one({"pageId": "books_page"}, {"_id": 0})
        if doc:
            return doc
        else:
            # Seed initial page data
            data = {"pageId": "books_page", **DEFAULT_BOOKS_PAGE_DATA}
            books_page_collection.update_one(
                {"pageId": "books_page"},
                {"$set": data},
                upsert=True
            )
            return data
    except Exception as e:
        print(f"MongoDB get_books_page_data error: {e}")
        return {"pageId": "books_page", **DEFAULT_BOOKS_PAGE_DATA}

def save_books_page_data(data: Dict[str, Any]) -> Dict[str, Any]:
    data["pageId"] = "books_page"
    try:
        books_page_collection.update_one(
            {"pageId": "books_page"},
            {"$set": data},
            upsert=True
        )
        print("Successfully saved BooksPageData in MongoDB")
    except Exception as e:
        print(f"MongoDB save_books_page_data error: {e}")
        raise e
    return data

# Legacy Course functions for backward compatibility
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
        existing_ids = [int(k) for k in courses.keys() if k.isdigit()]
        new_id = max(existing_ids) + 1 if existing_ids else 1
        course_data["id"] = new_id
    else:
        course_data["id"] = int(course_data["id"])
    
    try:
        courses_collection.update_one(
            {"id": course_data["id"]},
            {"$set": course_data},
            upsert=True
        )
    except Exception as e:
        print(f"MongoDB update error: {e}")
        raise e
            
    return course_data

def delete_course_by_id(course_id: int) -> bool:
    try:
        result = courses_collection.delete_one({"id": course_id})
        if result.deleted_count > 0:
            return True
    except Exception as e:
        print(f"MongoDB delete error: {e}")
        
    return False
