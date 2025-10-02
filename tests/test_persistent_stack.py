import pytest

from persistent_data_structures.persistent_stack import PersistentStack


def test_empty_stack():
    stack = PersistentStack()
    assert stack.top is None


def test_push_creates_new_stack():
    stack1 = PersistentStack()
    stack2 = stack1.push(42)

    assert stack1.top is None

    assert stack2.top is not None
    assert stack2.top.value == 42
    assert stack2.top.previous is None


def test_push_multiple_values():
    stack = PersistentStack().push(1).push(2).push(3)

    assert stack.peek() == 3
    stack, value = stack.pop()
    assert value == 3

    assert stack.peek() == 2
    stack, value = stack.pop()
    assert value == 2

    assert stack.peek() == 1
    stack, value = stack.pop()
    assert value == 1

    assert stack.top is None


def test_peek_does_not_modify_stack():
    stack = PersistentStack().push(100)

    value = stack.peek()
    assert value == 100

    assert stack.peek() == 100


def test_pop_returns_value_and_new_stack():
    stack1 = PersistentStack().push("hello")
    stack2, value = stack1.pop()

    assert value == "hello"
    assert stack2.top is None

    assert stack1.peek() == "hello"


def test_pop_from_empty_stack_returns_empty_stack_and_none():
    stack = PersistentStack()
    new_stack, value = stack.pop()

    assert value is None
    assert new_stack.top is None
    assert isinstance(new_stack, PersistentStack)


def test_peek_from_empty_stack_returns_none():
    stack = PersistentStack()
    value = stack.peek()
    assert value is None


def test_stack_with_custom_objects():
    class Item:
        def __init__(self, name: str):
            self.name = name

        def __eq__(self, other):
            return isinstance(other, Item) and self.name == other.name

    item1 = Item("A")
    item2 = Item("B")

    stack = PersistentStack().push(item1).push(item2)
    assert stack.peek() == item2

    stack, value = stack.pop()

    assert value == item2
    assert stack.peek() == item1


def test_immutability_and_structural_sharing():
    stack0: PersistentStack[int] = PersistentStack()
    stack1: PersistentStack[int] = stack0.push(1)
    stack2: PersistentStack[int] = stack1.push(2)

    assert stack0.top is None
    assert stack1.peek() == 1

    after_pop, _ = stack2.pop()

    assert after_pop.top is not None
    assert stack1.top is not None

    assert after_pop.top.value == stack1.top.value
    assert after_pop.top.previous is stack1.top.previous


@pytest.mark.parametrize("value", [42, "text", 3.14, True, None])
def test_generic_type_consistency(value):
    """
    Smoke test: stack works with various types.
    After push and pop, the stack should be empty again.
    """
    stack = PersistentStack().push(value)
    peeked = stack.peek()

    stack_after_pop, popped = stack.pop()

    # Value consistency
    assert peeked == value
    assert popped == value

    # Stack should be empty after pop
    assert stack_after_pop.top is None
    assert stack_after_pop.peek() is None


def test_chained_operations():
    s = PersistentStack()
    s1 = s.push(10)
    s2 = s1.push(20)
    s3 = s2.push(30)

    # Pop 30 → back to s2
    s_back, val = s3.pop()
    assert val == 30
    assert s_back.peek() == 20

    # Pop 20 → back to s1
    s_back2, val = s_back.pop()
    assert val == 20
    assert s_back2.peek() == 10

    # Original s1 still works
    assert s1.peek() == 10
