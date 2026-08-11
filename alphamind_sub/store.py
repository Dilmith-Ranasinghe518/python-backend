from typing import Dict, Any, Optional, List
from database import db

# MongoDB collections
courses_collection = db.get_collection("alphamind_courses")
courses_page_collection = db.get_collection("alphamind_courses_page")
books_page_collection = db.get_collection("alphamind_books_page")
short_notes_page_collection = db.get_collection("alphamind_short_notes_page")
revision_page_collection = db.get_collection("alphamind_revision_page")
auth_config_collection = db.get_collection("alphamind_auth_config")
users_collection = db.get_collection("alphamind_users")

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

DEFAULT_SHORT_NOTES_PAGE_DATA = {
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
            "id": "cnt-sn1",
            "subjectId": "slide-1",
            "title": "Introduction",
            "subcontents": [
                {
                    "id": "sub-sn1",
                    "title": "What is Generative AI?",
                    "duration": "5m 23s video",
                    "completed": False,
                    "videoUrl": "https://www.youtube.com/watch?v=1ukSR1GRtMU",
                    "description": "Understand the fundamentals of generative artificial intelligence and its applications.",
                    "resources": [],
                    "studyMaterials": ["/images/Poster1.jpg"]
                },
                {
                    "id": "sub-sn2",
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
            "id": "r1-1",
            "subcontentId": "sub-sn1",
            "title": "Deadpool 2",
            "subtitle": "Short Note Summary",
            "description": "Comprehensive short notes on key principles.",
            "image": "https://images.unsplash.com/photo-1534447677768-be436bb09401?w=400&q=80",
            "badge": "Popular",
            "learners": "133,854",
            "rating": "8.1",
            "pill": "Free with Plus",
            "price": "520",
            "ratingValue": "8.1",
            "year": "2018"
        },
        {
            "id": "r1-2",
            "subcontentId": "sub-sn2",
            "title": "October",
            "subtitle": "Short Note Summary",
            "description": "Essential revision notes.",
            "image": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=400&q=80",
            "badge": "Best seller",
            "learners": "136,041",
            "rating": "8.0",
            "pill": "Free with Plus",
            "price": "550",
            "ratingValue": "8.0",
            "year": "2018"
        },
        {
            "id": "r1-3",
            "subcontentId": "sub-sn1",
            "title": "The Meg",
            "subtitle": "Short Note Summary",
            "description": "Quick overview and study material.",
            "image": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?w=400&q=80",
            "badge": "New",
            "learners": "140,210",
            "rating": "6.4",
            "pill": "Free with Plus",
            "price": "490",
            "ratingValue": "6.4",
            "year": "2018"
        }
    ]
}

def get_short_notes_page_data() -> Dict[str, Any]:
    try:
        doc = short_notes_page_collection.find_one({"pageId": "short_notes_page"}, {"_id": 0})
        if doc:
            return doc
        else:
            # Seed initial page data
            data = {"pageId": "short_notes_page", **DEFAULT_SHORT_NOTES_PAGE_DATA}
            short_notes_page_collection.update_one(
                {"pageId": "short_notes_page"},
                {"$set": data},
                upsert=True
            )
            return data
    except Exception as e:
        print(f"MongoDB get_short_notes_page_data error: {e}")
        return {"pageId": "short_notes_page", **DEFAULT_SHORT_NOTES_PAGE_DATA}

def save_short_notes_page_data(data: Dict[str, Any]) -> Dict[str, Any]:
    data["pageId"] = "short_notes_page"
    try:
        short_notes_page_collection.update_one(
            {"pageId": "short_notes_page"},
            {"$set": data},
            upsert=True
        )
        print("Successfully saved ShortNotesPageData in MongoDB")
    except Exception as e:
        print(f"MongoDB save_short_notes_page_data error: {e}")
        raise e
    return data

DEFAULT_REVISION_PAGE_DATA = {
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
            "id": "cnt-r1",
            "subjectId": "slide-1",
            "title": "Introduction",
            "subcontents": [
                {
                    "id": "sub-r1",
                    "title": "What is Generative AI?",
                    "duration": "5m 23s video",
                    "completed": False,
                    "videoUrl": "https://www.youtube.com/watch?v=1ukSR1GRtMU",
                    "description": "Understand the fundamentals of generative artificial intelligence and its applications.",
                    "resources": [],
                    "studyMaterials": ["/images/Poster1.jpg"]
                },
                {
                    "id": "sub-r2",
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
            "id": "rev-1",
            "subcontentId": "sub-r1",
            "title": "The Sales Program",
            "subtitle": "Taught by Best-Selling Author Jeffrey Gitomer.",
            "description": "You cannot succeed in business without knowing how to sell. In this program, Jeffrey Gitomer will teach you the ins and outs of sales...",
            "image": "https://images.unsplash.com/photo-1560250097-0b93528c311a?w=800&q=80",
            "badge": "HOT",
            "learners": "300+ student reviews",
            "rating": "4.6",
            "pill": "Free with Plus",
            "price": "520",
            "ratingValue": "4.6"
        },
        {
            "id": "rev-2",
            "subcontentId": "sub-r2",
            "title": "Foundation Models Masterclass",
            "subtitle": "Taught by Industry Experts.",
            "description": "Deep dive into model fine-tuning, prompt engineering, and real-world AI deployment techniques.",
            "image": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=800&q=80",
            "badge": "NEW",
            "learners": "450+ student reviews",
            "rating": "4.8",
            "pill": "Free with Plus",
            "price": "580",
            "ratingValue": "4.8"
        }
    ]
}

def get_revision_page_data() -> Dict[str, Any]:
    try:
        doc = revision_page_collection.find_one({"pageId": "revision_page"}, {"_id": 0})
        if doc:
            return doc
        else:
            # Seed initial page data
            data = {"pageId": "revision_page", **DEFAULT_REVISION_PAGE_DATA}
            revision_page_collection.update_one(
                {"pageId": "revision_page"},
                {"$set": data},
                upsert=True
            )
            return data
    except Exception as e:
        print(f"MongoDB get_revision_page_data error: {e}")
        return {"pageId": "revision_page", **DEFAULT_REVISION_PAGE_DATA}

def save_revision_page_data(data: Dict[str, Any]) -> Dict[str, Any]:
    data["pageId"] = "revision_page"
    try:
        revision_page_collection.update_one(
            {"pageId": "revision_page"},
            {"$set": data},
            upsert=True
        )
        print("Successfully saved RevisionPageData in MongoDB")
    except Exception as e:
        print(f"MongoDB save_revision_page_data error: {e}")
        raise e
    return data

DEFAULT_AUTH_CONFIG_DATA = {
    "backgroundImage": "/images/login-hero.jpeg",
    "loginTitle": "Sign in to QC",
    "signupTitle": "Create your account",
    "forgotPasswordTitle": "Reset your password"
}

def get_auth_config_data() -> Dict[str, Any]:
    try:
        doc = auth_config_collection.find_one({"configId": "auth_config"}, {"_id": 0})
        if doc:
            return doc
        else:
            data = {"configId": "auth_config", **DEFAULT_AUTH_CONFIG_DATA}
            auth_config_collection.update_one(
                {"configId": "auth_config"},
                {"$set": data},
                upsert=True
            )
            return data
    except Exception as e:
        print(f"MongoDB get_auth_config_data error: {e}")
        return {"configId": "auth_config", **DEFAULT_AUTH_CONFIG_DATA}

def save_auth_config_data(data: Dict[str, Any]) -> Dict[str, Any]:
    data["configId"] = "auth_config"
    try:
        auth_config_collection.update_one(
            {"configId": "auth_config"},
            {"$set": data},
            upsert=True
        )
        print("Successfully saved AuthConfigData in MongoDB")
    except Exception as e:
        print(f"MongoDB save_auth_config_data error: {e}")
        raise e
    return data

import hashlib
import uuid

def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def register_user(full_name: str, identifier: str, password: str) -> Dict[str, Any]:
    clean_identifier = identifier.strip().lower()
    existing = users_collection.find_one({"identifier": clean_identifier})
    if existing:
        return {"success": False, "message": "User with this email/phone already exists"}

    user_id = str(uuid.uuid4())
    token = f"user-token-{uuid.uuid4().hex}"
    user_doc = {
        "userId": user_id,
        "fullName": full_name,
        "identifier": clean_identifier,
        "passwordHash": _hash_password(password),
        "createdAt": str(uuid.uuid4())
    }
    try:
        users_collection.insert_one(user_doc)
        return {
            "success": True,
            "message": "Registration successful",
            "token": token,
            "user": {"userId": user_id, "fullName": full_name, "identifier": clean_identifier}
        }
    except Exception as e:
        print(f"MongoDB register_user error: {e}")
        return {"success": False, "message": f"Registration failed: {str(e)}"}

def login_user(identifier: str, password: str) -> Dict[str, Any]:
    clean_identifier = identifier.strip().lower()
    user = users_collection.find_one({"identifier": clean_identifier})
    if not user:
        return {"success": False, "message": "User not found. Please register first."}

    if user.get("passwordHash") != _hash_password(password):
        return {"success": False, "message": "Incorrect password. Please try again."}

    token = f"user-token-{uuid.uuid4().hex}"
    return {
        "success": True,
        "message": "Login successful",
        "token": token,
        "user": {"userId": user.get("userId"), "fullName": user.get("fullName"), "identifier": clean_identifier}
    }

def forgot_password_user(identifier: str, new_password: Optional[str] = None) -> Dict[str, Any]:
    clean_identifier = identifier.strip().lower()
    user = users_collection.find_one({"identifier": clean_identifier})
    if not user:
        return {"success": False, "message": "No account found matching this identifier."}

    if new_password and new_password.strip():
        new_hash = _hash_password(new_password)
        users_collection.update_one(
            {"identifier": clean_identifier},
            {"$set": {"passwordHash": new_hash}}
        )
        return {"success": True, "message": "Password updated successfully. You can now log in."}
    else:
        return {"success": True, "message": "Account verified. Please enter your new password to reset."}

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
