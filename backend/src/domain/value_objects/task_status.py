"""Task status value object."""

from enum import Enum


class TaskStatus(Enum):
    """Valid states for a task."""
    
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress" 
    COMPLETED = "completed"

    def can_transition_to(self, new_status: "TaskStatus") -> bool:
        """Check if transition to new status is valid."""
        valid_transitions = {
            TaskStatus.NOT_STARTED: [TaskStatus.IN_PROGRESS],
            TaskStatus.IN_PROGRESS: [TaskStatus.COMPLETED],
            TaskStatus.COMPLETED: [],  # No transitions from completed
        }
        
        return new_status in valid_transitions.get(self, [])