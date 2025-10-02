from dataclasses import dataclass, field
from typing import Generic, TypeVar, final

from persistent_data_structures.persistent_stack import PersistentStack

T = TypeVar("T")


@final
@dataclass(frozen=True, slots=True)
class PersistentQueue(Generic[T]):
    """
    An immutable (persistent) queue with amortized O(1*) enqueue and dequeue.
    """

    _inbox: "PersistentStack[T]" = field(default_factory=PersistentStack)
    _outbox: "PersistentStack[T]" = field(default_factory=PersistentStack)

    def enqueue(self, value: T) -> "PersistentQueue[T]":
        """
        Adds an element to the end of the queue.

        Time complexity: O(1)
        Space complexity: O(1)
        """
        return PersistentQueue(self._inbox.push(value), self._outbox)

    def dequeue(self) -> tuple["PersistentQueue[T]", T | None]:
        """
        Removes and returns the front element and the new queue.
        If the queue is empty, returns (empty_queue, None).

        Time complexity: O(1*) amortized
        Space complexity: O(1*) amortized
        """

        balanced = self._balance()
        if balanced._outbox.is_empty():
            return PersistentQueue(), None

        new_outbox, value = balanced._outbox.pop()
        return PersistentQueue(balanced._inbox, new_outbox), value

    def peek(self) -> T | None:
        """
        Returns the front element without modifying the queue.
        Returns None if the queue is empty.

        Time complexity: O(1*) amortized
        Space complexity: O(1*) amortized
        """
        balanced = self._balance()
        return balanced._outbox.peek()

    def is_empty(self) -> bool:
        """
        Returns True if the queue contains no elements.

        Time complexity: O(1)
        Space complexity: O(1)
        """

        return self._inbox.is_empty() and self._outbox.is_empty()

    def _balance(self) -> "PersistentQueue[T]":
        """
        Transfers all elements from inbox to outbox (reversing order).

        Time complexity: O(n), where n = len(inbox)
        Space complexity: O(n)
        """

        if not self._outbox.is_empty():
            return self

        outbox = PersistentStack()
        inbox = self._inbox

        while not inbox.is_empty():
            inbox, val = inbox.pop()
            outbox = outbox.push(val)

        return PersistentQueue(PersistentStack(), outbox)
