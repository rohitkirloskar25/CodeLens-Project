import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class LinkedListTest {

    @Test
    void addElementsToLinkedList() {
        LinkedListDemo.LinkedList list = new LinkedListDemo.LinkedList();
        list.add(10);
        list.add(20);
        list.add(30);

        LinkedListDemo.Node head = list.head;
        assertNotNull(head);
        assertEquals(10, head.data);
        assertEquals(20, head.next.data);
        assertEquals(30, head.next.next.data);
        assertNull(head.next.next.next);
    }

    @Test
    void addSingleElementToLinkedList() {
        LinkedListDemo.LinkedList list = new LinkedListDemo.LinkedList();
        list.add(5);

        LinkedListDemo.Node head = list.head;
        assertNotNull(head);
        assertEquals(5, head.data);
        assertNull(head.next);
    }

    @Test
    void addMultipleElementsToLinkedList() {
        LinkedListDemo.LinkedList list = new LinkedListDemo.LinkedList();
        list.add(1);
        list.add(2);
        list.add(3);
        list.add(4);
        list.add(5);

        LinkedListDemo.Node head = list.head;
        assertNotNull(head);
        assertEquals(1, head.data);
        assertEquals(2, head.next.data);
        assertEquals(3, head.next.next.data);
        assertEquals(4, head.next.next.next.data);
        assertEquals(5, head.next.next.next.next.data);
        assertNull(head.next.next.next.next.next);
    }

    @Test
    void addZeroToLinkedList() {
        LinkedListDemo.LinkedList list = new LinkedListDemo.LinkedList();
        list.add(0);

        LinkedListDemo.Node head = list.head;
        assertNotNull(head);
        assertEquals(0, head.data);
        assertNull(head.next);
    }

    @Test
    void addNegativeNumberToLinkedList() {
        LinkedListDemo.LinkedList list = new LinkedListDemo.LinkedList();
        list.add(-10);

        LinkedListDemo.Node head = list.head;
        assertNotNull(head);
        assertEquals(-10, head.data);
        assertNull(head.next);
    }

    @Test
    void addManySameElementsToLinkedList() {
        LinkedListDemo.LinkedList list = new LinkedListDemo.LinkedList();
        list.add(7);
        list.add(7);
        list.add(7);

        LinkedListDemo.Node head = list.head;
        assertNotNull(head);
        assertEquals(7, head.data);
        assertEquals(7, head.next.data);
        assertEquals(7, head.next.next.data);
        assertNull(head.next.next.next);
    }

    @Test
    void checkHeadAfterAddingToEmptyList() {
        LinkedListDemo.LinkedList list = new LinkedListDemo.LinkedList();
        list.add(15);
        assertNotNull(list.head);
        assertEquals(15, list.head.data);
    }

    @Test
    void checkHeadAfterAddingMultipleElements() {
          LinkedListDemo.LinkedList list = new LinkedListDemo.LinkedList();
          list.add(15);
          list.add(25);
          assertEquals(15, list.head.data);
          assertEquals(25, list.head.next.data);
    }
}
