"""Task priority value object."""

from enum import Enum


class TaskPriority(Enum):
    """Priority levels for tasks."""
    
    UNASSIGNED = "unassigned"
    LOW = "low"
    MEDIUM = "medium" 
    HIGH = "high"
    CRITICAL = "critical"

    def __lt__(self, other: "TaskPriority") -> bool:
        """Enable priority comparison (unassigned < low < medium < high < critical)."""
        priority_order = [
            TaskPriority.UNASSIGNED,
            TaskPriority.LOW,
            TaskPriority.MEDIUM, 
            TaskPriority.HIGH,
            TaskPriority.CRITICAL
        ]
        
        return priority_order.index(self) < priority_order.index(other)