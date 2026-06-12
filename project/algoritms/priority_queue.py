from typing import Any, List, Tuple, Optional


class PriorityQueue:
    """
    Реализация очереди с приоритетами на основе бинарной кучи.
    Чем МЕНЬШЕ число priority, тем ВЫШЕ приоритет выполнения.
    """

    def __init__(self) -> None:
        self._heap: List[Tuple[float, int, Any]] = []
        self._counter: int = 0  # Гарантирует стабильность при равных приоритетах

    def push(self, item: Any, priority: float) -> None:
        """Добавляет элемент с заданным приоритетом. Сложность: O(log N)"""
        entry = (priority, self._counter, item)
        self._counter += 1
        self._heap.append(entry)
        self._sift_up(len(self._heap) - 1)

    def pop(self) -> Any:
        """Извлекает элемент с наивысшим приоритетом. Сложность: O(log N)"""
        if not self._heap:
            raise IndexError("pop from empty priority queue")

        if len(self._heap) == 1:
            return self._heap.pop()[2]

        # Меняем корень с последним элементом и удаляем корень
        self._swap(0, len(self._heap) - 1)
        item = self._heap.pop()[2]
        self._sift_down(0)
        return item

    def peek(self) -> Optional[Any]:
        """Возвращает элемент с наивысшим приоритетом без удаления. O(1)"""
        return self._heap[0][2] if self._heap else None

    def is_empty(self) -> bool:
        return len(self._heap) == 0

    def __len__(self) -> int:
        return len(self._heap)

    # 🔽 Внутренние методы поддержания структуры кучи
    def _parent(self, i: int) -> int:
        return (i - 1) // 2

    def _left(self, i: int) -> int:
        return 2 * i + 1

    def _right(self, i: int) -> int:
        return 2 * i + 2

    def _sift_up(self, i: int) -> None:
        """Поднимает элемент вверх, пока не восстановится свойство кучи."""
        while i > 0:
            p = self._parent(i)
            if self._heap[i] < self._heap[p]:
                self._swap(i, p)
                i = p
            else:
                break

    def _sift_down(self, i: int) -> None:
        """Опускает элемент вниз, пока не восстановится свойство кучи."""
        size = len(self._heap)
        while True:
            smallest = i
            l, r = self._left(i), self._right(i)

            if l < size and self._heap[l] < self._heap[smallest]:
                smallest = l
            if r < size and self._heap[r] < self._heap[smallest]:
                smallest = r

            if smallest != i:
                self._swap(i, smallest)
                i = smallest
            else:
                break

    def _swap(self, i: int, j: int) -> None:
        self._heap[i], self._heap[j] = self._heap[j], self._heap[i]
