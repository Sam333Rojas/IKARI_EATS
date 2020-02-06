from time import time

from django.shortcuts import render

from project_test.models import TestObject, TestObjectSerializer


class Node:
    def __init__(self, data=None, next_node=None):
        self.data = data
        self.next_node = next_node


class MyLinkedList:
    def __init__(self):
        self.head = None

    def add_at_front(self, data):
        self.head = Node(data=data, next_node=self.head)

    def is_empty(self):
        return self.head is None

    def add_at_end(self, data):
        if not self.head:
            self.head = Node(data=data)
            return
        curr = self.head
        while curr.next_node:
            curr = curr.next_node
        curr.next_node = Node(data=data)

    def delete_node(self, key):
        curr = self.head
        prev = None
        while curr and curr.data != key:
            prev = curr
            curr = curr.next_node
        if prev is None:
            self.head = curr.next_node
        elif curr:
            prev.next_node = curr.next_node
            curr.next_node = None

    def search_node(self, key):
        curr = self.head
        prev = None
        index = None
        while curr and curr.data != key:
            prev = curr
            curr = curr.next_node
            index = index + 1
        if curr.data == key:
            return index
        else:
            return -1

    def get_last_node(self):
        temp = self.head
        while temp.next_node is not None:
            temp = temp.next_node
        return temp.data

    def print_list(self):
        node = self.head
        while node is not None:
            print(node.data, end=' => ')
            node = node.next_node


def linked_list_test(request, n):
    results = {
        'title': 'Test with {} numbers in a List'.format(n)
    }
    python_list = []

    initial_time = time()
    for i in range(n):
        python_list.append(i)
    t_final = time()
    t_total = t_final - initial_time
    results['python_list_insertion'] = t_total

    initial_time1 = time()
    for i in range(n):
        python_list.pop()
    t_final1 = time()
    t_total1 = t_final1 - initial_time1
    results['python_list_delete'] = t_total1

    my_list = MyLinkedList()

    initial_time2 = time()
    for i in range(n):
        my_list.add_at_end(i)
    t_final2 = time()
    t_total2 = t_final2 - initial_time2
    results['my_list_insertion'] = t_total2

    initial_time3 = time()
    for i in range(n):
        my_list.delete_node(i)
    t_final3 = time()
    t_total3 = t_final3 - initial_time3
    results['my_list_delete'] = t_total3

    return render(request, 'tests.html', results)


def python_list_test(request, n):
    results = {
        'title': 'Test with {} numbers in a List'.format(n)
    }
    python_list = []

    initial_time = time()
    for i in range(n):
        python_list.append(i)
    t_final = time()
    t_total = t_final - initial_time
    results['python_list_insertion'] = t_total

    initial_time1 = time()
    for i in range(n):
        python_list.pop()
    t_final1 = time()
    t_total1 = t_final1 - initial_time1
    results['python_list_delete'] = t_total1

    return render(request, 'test_2.html', results)


def heap_test(request):
    for i in range(10):
        my_object = TestObject.objects.create()
        my_object.time = i + 50
        my_object.save()

    my_objects = TestObject.objects.all()
    my_objects_serializer = TestObjectSerializer(my_objects, many=True)
    results = {'group_objects': my_objects_serializer.data}
    return render(request, 'heap_test.html', results)