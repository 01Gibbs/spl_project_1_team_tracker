"""Task priority value object."""

from enum import Enum


class TaskPriority(Enum):
    """Priority levels for tasks."""
    
    LOW = "low"
    MEDIUM = "medium" 
    HIGH = "high"
    URGENT = "urgent"

    def __lt__(self, other: "TaskPriority") -> bool:
        """Enable priority comparison (low < medium < high < urgent)."""
        priority_order = [
            TaskPriority.LOW,
            TaskPriority.MEDIUM, 
            TaskPriority.HIGH,
            TaskPriority.URGENT
        ]
        
        return priority_order.index(self) < priority_order.index(other)