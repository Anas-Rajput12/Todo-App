from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import Optional, Dict, Any
import re
import uuid
from datetime import datetime

from ..database import get_session
from ..models.task import Task, TaskCreate, TaskUpdate, TaskStatus
from ..models.user import UserRead
from ..services.task_service import (
    create_task, get_tasks, get_task, update_task, delete_task, toggle_task_completion
)
from ..middleware.auth import JWTBearer
from ..utils.logging_config import setup_logging

# Set up logging
logger = setup_logging()

router = APIRouter()


class ChatbotSession:
    """Simple in-memory session storage for chatbot conversations."""
    
    def __init__(self):
        self.sessions: Dict[str, Dict[str, Any]] = {}
    
    def get_or_create_session(self, session_id: Optional[str] = None) -> str:
        """Get existing session or create a new one."""
        if session_id and session_id in self.sessions:
            return session_id
        
        new_session_id = str(uuid.uuid4())
        self.sessions[new_session_id] = {
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "is_active": True,
            "message_count": 0
        }
        return new_session_id
    
    def update_session(self, session_id: str):
        """Update session timestamp and message count."""
        if session_id in self.sessions:
            self.sessions[session_id]["updated_at"] = datetime.utcnow()
            self.sessions[session_id]["message_count"] += 1
    
    def get_session_info(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session information."""
        if session_id in self.sessions:
            return {
                "id": session_id,
                **self.sessions[session_id]
            }
        return None
    
    def get_all_sessions(self) -> list:
        """Get all sessions."""
        return [
            {"id": sid, **info}
            for sid, info in self.sessions.items()
        ]


# Global session store
session_store = ChatbotSession()


def parse_intent(message: str) -> Dict[str, Any]:
    """
    Parse natural language message to determine intent.
    
    Returns a dict with:
    - intent: The detected intent
    - entities: Extracted entities (task_id, title, etc.)
    - confidence: Confidence level (high, medium, low)
    """
    message_lower = message.lower().strip()
    
    # List tasks
    list_patterns = [
        r'\b(list|show|get|view|display|my tasks|all tasks)\b',
        r'\bwhat.*task\b',
        r'\bdo.*task\b',
        r'\bhave.*task\b',
    ]
    
    # Create task
    create_patterns = [
        r'\b(add|create|new|make)\s+(a\s+)?task\b',
        r'\b(add|create)\s+.*\b(to|for)\b',
        r'\b(i want|i need|please)\s+(add|create)\b',
        r'\b(remember|remind me)\s+to\b',
    ]
    
    # Delete task
    delete_patterns = [
        r'\b(delete|remove|erase)\b.*\btask\b',
        r'\b(delete|remove)\s+(the\s+)?task\b',
        r'\btask\s+(delete|remove)\b',
        r'\b(get rid of|throw away)\s+task\b',
    ]
    
    # Update task
    update_patterns = [
        r'\b(update|edit|change|modify)\b.*\btask\b',
        r'\b(change|update)\s+(the\s+)?task\b',
        r'\b(rename|set)\s+task\b',
    ]
    
    # Complete task
    complete_patterns = [
        r'\b(complete|finish|done|check)\b.*\btask\b',
        r'\b(mark as )?(completed|done|finished)\b',
        r'\b(task ).*(completed|done|finished)\b',
    ]
    
    # Help
    help_patterns = [
        r'\b(help|what can you do|commands|how to)\b',
    ]
    
    # Check for specific intents
    def check_patterns(patterns):
        for pattern in patterns:
            if re.search(pattern, message_lower):
                return True
        return False
    
    # Extract task ID if mentioned
    task_id_match = re.search(r'\b([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})\b', message_lower)
    task_id = task_id_match.group(0) if task_id_match else None
    
    # Extract task number (e.g., "task 1", "first task")
    task_number_match = re.search(r'\btask\s*(\d+)|(\d+)(st|nd|rd|th)\s+task\b', message_lower)
    task_number = None
    if task_number_match:
        task_number = int(task_number_match.group(1) or task_number_match.group(2))
    
    # Extract title from message (text after "add task" or similar)
    title_match = re.search(r'(?:add|create|new)\s+(?:a\s+)?task\s+(?:to\s+)?(.+)', message_lower)
    title = title_match.group(1).strip() if title_match else None
    
    # Determine intent
    if check_patterns(list_patterns):
        return {
            "intent": "list_tasks",
            "entities": {},
            "confidence": "high"
        }
    
    if check_patterns(delete_patterns):
        return {
            "intent": "delete_task",
            "entities": {"task_id": task_id, "task_number": task_number},
            "confidence": "high" if task_id or task_number else "medium"
        }
    
    if check_patterns(create_patterns):
        return {
            "intent": "create_task",
            "entities": {"title": title},
            "confidence": "high" if title else "medium"
        }
    
    if check_patterns(update_patterns):
        return {
            "intent": "update_task",
            "entities": {"task_id": task_id, "task_number": task_number, "title": title},
            "confidence": "medium"
        }
    
    if check_patterns(complete_patterns):
        return {
            "intent": "complete_task",
            "entities": {"task_id": task_id, "task_number": task_number},
            "confidence": "high" if task_id or task_number else "medium"
        }
    
    if check_patterns(help_patterns):
        return {
            "intent": "help",
            "entities": {},
            "confidence": "high"
        }
    
    # Unknown intent
    return {
        "intent": "unknown",
        "entities": {},
        "confidence": "low"
    }


async def execute_intent(
    intent: str,
    entities: Dict[str, Any],
    session: Session,
    user_id: str
) -> Dict[str, Any]:
    """Execute the detected intent and return result."""
    
    try:
        if intent == "list_tasks":
            tasks = get_tasks(session, user_id)
            if not tasks:
                return {
                    "response": "You don't have any tasks yet. Would you like me to add one?",
                    "action_result": {"tasks": []},
                    "requires_confirmation": False
                }
            
            task_list = "\n".join([
                f"{i+1}. {t.title} - {t.status.value}"
                for i, t in enumerate(tasks)
            ])
            return {
                "response": f"Here are your tasks:\n\n{task_list}",
                "action_result": {"tasks": [t.model_dump() for t in tasks]},
                "requires_confirmation": False
            }
        
        elif intent == "create_task":
            title = entities.get("title")
            if not title:
                return {
                    "response": "What would you like me to add as a task? Please provide the task description.",
                    "action_result": None,
                    "requires_confirmation": False
                }
            
            task_create = TaskCreate(title=title, description="")
            created_task = create_task(session, task_create, user_id)
            return {
                "response": f"✓ Task created: \"{created_task.title}\"",
                "action_result": {"task": created_task.model_dump()},
                "requires_confirmation": False
            }
        
        elif intent == "delete_task":
            task_id = entities.get("task_id")
            task_number = entities.get("task_number")
            
            if not task_id and not task_number:
                return {
                    "response": "Which task would you like to delete? Please provide the task ID or number (e.g., 'delete task 1').",
                    "action_result": None,
                    "requires_confirmation": False
                }
            
            # If task number provided, get the task
            if task_number:
                tasks = get_tasks(session, user_id)
                if task_number < 1 or task_number > len(tasks):
                    return {
                        "response": f"Task #{task_number} not found. You have {len(tasks)} task(s).",
                        "action_result": None,
                        "requires_confirmation": False
                    }
                task_id = str(tasks[task_number - 1].id)
            
            # Get task first to verify it exists
            task = get_task(session, task_id, user_id)
            task_title = task.title
            
            # Delete the task
            delete_task(session, task_id, user_id)
            return {
                "response": f"✓ Task deleted: \"{task_title}\"",
                "action_result": {"deleted_task_id": task_id},
                "requires_confirmation": False
            }
        
        elif intent == "complete_task":
            task_id = entities.get("task_id")
            task_number = entities.get("task_number")
            
            if not task_id and not task_number:
                return {
                    "response": "Which task would you like to mark as complete? Please provide the task ID or number.",
                    "action_result": None,
                    "requires_confirmation": False
                }
            
            # If task number provided, get the task
            if task_number:
                tasks = get_tasks(session, user_id)
                if task_number < 1 or task_number > len(tasks):
                    return {
                        "response": f"Task #{task_number} not found. You have {len(tasks)} task(s).",
                        "action_result": None,
                        "requires_confirmation": False
                    }
                task_id = str(tasks[task_number - 1].id)
            
            # Toggle completion
            task = toggle_task_completion(session, task_id, True, user_id)
            return {
                "response": f"✓ Task marked as complete: \"{task.title}\"",
                "action_result": {"task": task.model_dump()},
                "requires_confirmation": False
            }
        
        elif intent == "update_task":
            return {
                "response": "I can help you update a task. Please tell me which task to update and what changes to make.",
                "action_result": None,
                "requires_confirmation": False
            }
        
        elif intent == "help":
            return {
                "response": """I can help you manage your tasks! Try these commands:

• **List tasks**: "Show my tasks" or "List all tasks"
• **Add task**: "Add a task to buy groceries"
• **Delete task**: "Delete task 1" or "Remove the task with ID xxx"
• **Complete task**: "Mark task 1 as complete"
• **Help**: "What can you do?"

Just type naturally and I'll understand!""",
                "action_result": None,
                "requires_confirmation": False
            }
        
        else:
            return {
                "response": """I'm not sure I understand. I can help you with:
• Listing tasks ("show my tasks")
• Adding tasks ("add a task to...")
• Deleting tasks ("delete task 1")
• Completing tasks ("mark task 1 as done")

Try one of these commands!""",
                "action_result": None,
                "requires_confirmation": False
            }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error executing intent {intent}: {str(e)}")
        return {
            "response": f"Sorry, I encountered an error: {str(e)}. Please try again.",
            "action_result": None,
            "requires_confirmation": False
        }


@router.post("/message")
async def chatbot_message(
    request: Dict[str, Any],
    current_user: UserRead = Depends(JWTBearer()),
    session: Session = Depends(get_session)
):
    """
    Process a chatbot message and return appropriate response.
    
    The chatbot understands natural language commands for task management:
    - List tasks: "show my tasks", "list all tasks"
    - Create task: "add a task to buy groceries"
    - Delete task: "delete task 1", "remove task with ID xxx"
    - Complete task: "mark task 1 as complete"
    - Help: "what can you do?"
    """
    message = request.get("message", "")
    session_id = request.get("sessionId")
    
    if not message:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message is required"
        )
    
    logger.info(f"Processing chatbot message from user {current_user.id}: {message}")
    
    # Get or create session
    new_session_id = session_store.get_or_create_session(session_id)
    session_store.update_session(new_session_id)
    
    # Parse intent
    parsed = parse_intent(message)
    logger.info(f"Parsed intent: {parsed['intent']} (confidence: {parsed['confidence']})")
    
    # Execute intent
    result = await execute_intent(
        parsed["intent"],
        parsed["entities"],
        session,
        str(current_user.id)
    )
    
    response_data = {
        "sessionId": new_session_id,
        "response": result["response"],
        "intent": parsed["intent"],
        "actionResult": result["action_result"],
        "requiresConfirmation": result["requires_confirmation"],
        "timestamp": datetime.utcnow().isoformat()
    }
    
    logger.info(f"Chatbot response: {result['response'][:100]}...")
    return response_data


@router.get("/sessions")
async def get_chatbot_sessions(
    current_user: UserRead = Depends(JWTBearer())
):
    """Get all chatbot sessions for the current user."""
    sessions = session_store.get_all_sessions()
    return {"sessions": sessions}
