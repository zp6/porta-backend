"""Bounties Module for Porta Backend.
Addresses issue #1: Develop Bounties Module
"""

from datetime import datetime
from typing import Optional, List
from dataclasses import dataclass, field
from enum import Enum


class BountyStatus(Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    UNDER_REVIEW = "under_review"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


@dataclass
class Bounty:
    id: str
    title: str
    description: str
    amount: float
    currency: str = "USD"
    creator_id: str = ""
    assignee_id: Optional[str] = None
    status: BountyStatus = BountyStatus.OPEN
    created_at: datetime = field(default_factory=datetime.now)
    deadline: Optional[datetime] = None
    tags: List[str] = field(default_factory=list)


class BountiesService:
    def __init__(self):
        self._bounties: dict[str, Bounty] = {}

    def create_bounty(self, title: str, description: str, amount: float,
                      creator_id: str, currency: str = "USD",
                      deadline: Optional[datetime] = None, tags: Optional[List[str]] = None) -> Bounty:
        bounty_id = f"bounty_{len(self._bounties) + 1}"
        bounty = Bounty(
            id=bounty_id, title=title, description=description,
            amount=amount, currency=currency, creator_id=creator_id,
            deadline=deadline, tags=tags or [],
        )
        self._bounties[bounty_id] = bounty
        return bounty

    def get_bounty(self, bounty_id: str) -> Optional[Bounty]:
        return self._bounties.get(bounty_id)

    def list_bounties(self, status: Optional[BountyStatus] = None) -> List[Bounty]:
        bounties = list(self._bounties.values())
        if status:
            bounties = [b for b in bounties if b.status == status]
        return sorted(bounties, key=lambda b: b.created_at, reverse=True)

    def assign_bounty(self, bounty_id: str, assignee_id: str) -> Bounty:
        bounty = self._bounties.get(bounty_id)
        if not bounty:
            raise ValueError(f"Bounty {bounty_id} not found")
        if bounty.status != BountyStatus.OPEN:
            raise ValueError(f"Bounty is not open for assignment")
        bounty.assignee_id = assignee_id
        bounty.status = BountyStatus.IN_PROGRESS
        return bounty

    def complete_bounty(self, bounty_id: str) -> Bounty:
        bounty = self._bounties.get(bounty_id)
        if not bounty:
            raise ValueError(f"Bounty {bounty_id} not found")
        bounty.status = BountyStatus.COMPLETED
        return bounty

    def cancel_bounty(self, bounty_id: str) -> Bounty:
        bounty = self._bounties.get(bounty_id)
        if not bounty:
            raise ValueError(f"Bounty {bounty_id} not found")
        bounty.status = BountyStatus.CANCELLED
        return bounty
