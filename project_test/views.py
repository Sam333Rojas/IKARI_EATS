from time import time

from django.shortcuts import render


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
        'title': 'Prueba con {} usuarios'.format(n)
    }
    users = MyLinkedList()
    initial_time = time()

    for i in range(n):
        users.add_at_end(i)

    t_final = time()
    t_total = t_final - initial_time

    results['final_time'] = 'Tiempo total al insertar {} datos = {}'.format(n, t_total)

    initial_time2 = time()
    users.delete_node(n)
    t_final2 = time()
    t_elimination = t_final2 - initial_time2
    results['elimination'] = 'Tiempo total al eliminar el dato {} = {}'.format(n, t_elimination)
    return render(request, 'tests.html', results)
