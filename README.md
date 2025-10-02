# Persistent Stack

Let `PersistentStack` be a data structure with the following `API`:

* `push` takes a `PersistentStack` and an element, and returns a new stack with the element added on top,
* `pop` takes a `PersistentStack` and returns a pair consisting of the stack without its top element and the removed element; if the stack is empty, it returns a pair of the empty stack and nil.

The key point is that both functions are non-mutating: they create new entities. While each function returns a new stack, it does not rebuild the structure
from scratch but instead reuses the existing one. This ensures that both operations run in `O(1)` time.

* How can one implement `PersistentStack`?
* Can you implement a `PersistentQueue` data structure with similar properties?
* In what contexts are such data structures useful?
* Do you also know how to implement other kinds of persistent data structures?
