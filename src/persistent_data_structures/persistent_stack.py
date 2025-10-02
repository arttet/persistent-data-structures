from dataclasses import dataclass
from typing import Generic, TypeVar, final

T = TypeVar("T")


@final
@dataclass(frozen=True, slots=True)
class Node(Generic[T]):
    """
    A node in the persistent stack.
    """

    value: T
    previous: "Node[T] | None" = None


@final
@dataclass(frozen=True, slots=True)
class PersistentStack(Generic[T]):
    """
    An immutable (persistent) stack implemented as a linked list.

    All operations return new instances, leaving the original unchanged.
    """

    top: Node[T] | None = None

    def push(self, value: T) -> "PersistentStack[T]":
        """
        Takes a PersistentStack and an element, and returns a new stack with the element added on top.

        Time complexity: O(1)
        Space complexity: O(1) — creates one new Node
        """
        return PersistentStack(Node(value, self.top))

    def pop(self) -> tuple["PersistentStack[T]", T | None]:
        """
        Takes a PersistentStack and returns a pair consisting of the stack without its top element and the removed element.
        If the stack is empty, it returns a pair of the empty stack and nil.

        Time complexity: O(1)
        Space complexity: O(1) — reuses existing structure (structural sharing)
        """

        if self.top is None:
            return PersistentStack(), None

        return (PersistentStack(self.top.previous), self.top.value)

    def peek(self) -> T | None:
        """
        Returns the top value without modifying the stack.
        If the stack is empty, returns None.

        Time complexity: O(1)
        Space complexity: O(1)
        """
        return self.top.value if self.top is not None else None

    def is_empty(self) -> bool:
        """
        Returns True if the stack contains no elements.

        Time complexity: O(1)
        Space complexity: O(1)
        """
        return self.top is None
