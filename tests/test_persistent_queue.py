import pytest

from persistent_data_structures.persistent_queue import PersistentQueue


def test_empty_queue():
    q = PersistentQueue()
    assert q.is_empty()
    assert q.peek() is None

    new_q, value = q.dequeue()
    assert value is None
    assert new_q.is_empty()


def test_enqueue_creates_new_queue():
    q1 = PersistentQueue()
    q2 = q1.enqueue(42)

    assert q1.is_empty()
    assert not q2.is_empty()
    assert q2.peek() == 42


def test_fifo_order():
    q = PersistentQueue()
    q = q.enqueue(1)
    q = q.enqueue(2)
    q = q.enqueue(3)

    q, val = q.dequeue()
    assert val == 1

    q, val = q.dequeue()
    assert val == 2

    q, val = q.dequeue()
    assert val == 3

    assert q.is_empty()


def test_peek_does_not_modify_queue():
    q = PersistentQueue().enqueue("hello")
    val = q.peek()
    assert val == "hello"

    # Queue unchanged
    assert q.peek() == "hello"
    assert not q.is_empty()


def test_dequeue_returns_new_queue_and_value():
    q1 = PersistentQueue().enqueue(100)
    q2, val = q1.dequeue()

    assert val == 100
    assert q2.is_empty()

    assert q1.peek() == 100


def test_dequeue_from_empty_returns_empty_and_none():
    q = PersistentQueue()
    new_q, val = q.dequeue()
    assert val is None
    assert new_q.is_empty()


def test_is_empty():
    q = PersistentQueue()
    assert q.is_empty()

    q = q.enqueue(1)
    assert not q.is_empty()

    q, _ = q.dequeue()
    assert q.is_empty()


def test_queue_with_multiple_enqueues_and_dequeues():
    q = PersistentQueue()
    for i in range(5):
        q = q.enqueue(i)

    for i in range(3):
        q, val = q.dequeue()
        assert val == i

    q = q.enqueue(10)
    q = q.enqueue(20)

    expected = [3, 4, 10, 20]
    for exp in expected:
        q, val = q.dequeue()
        assert val == exp

    assert q.is_empty()


def test_immutability():
    q0 = PersistentQueue()
    q1 = q0.enqueue(1)
    q2 = q1.enqueue(2)

    # Dequeue from q2
    q3, val = q2.dequeue()
    assert val == 1
    assert not q3.is_empty()

    # Originals unchanged
    assert q0.is_empty()
    assert q1.peek() == 1
    assert q2.peek() == 1


def test_structural_sharing():
    q = PersistentQueue()
    q = q.enqueue(1)
    q = q.enqueue(2)
    q = q.enqueue(3)

    q_after, _ = q.dequeue()  # now outbox has [2, 3] (reversed)
    assert q_after.peek() == 2

    q_after2, _ = q_after.dequeue()
    assert q_after2.peek() == 3


@pytest.mark.parametrize("value", [42, "text", 3.14, True, None])
def test_generic_type_consistency(value):
    """
    Queue works correctly with various types.
    """

    q = PersistentQueue()
    q = q.enqueue(value)
    assert q.peek() == value

    q_after, popped = q.dequeue()
    assert popped == value
    assert q_after.is_empty()


def test_peek_after_balance():
    q = PersistentQueue()
    q = q.enqueue(10)
    q = q.enqueue(20)

    # inbox has [10, 20]
    # peek() should balance and return 10
    assert q.peek() == 10

    # Queue still has both elements
    q2, val = q.dequeue()
    assert val == 10
    assert q2.peek() == 20


def test_dequeue_after_balance():
    q = PersistentQueue()
    q = q.enqueue("A")
    q = q.enqueue("B")

    q2, val = q.dequeue()
    assert val == "A"
    assert q2.peek() == "B"

    q3, val = q2.dequeue()
    assert val == "B"
    assert q3.is_empty()
