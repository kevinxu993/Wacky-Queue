"""
# Copyright Nick Cheng, 2018
# Copyright Xinzheng Xu, 2018
# Distributed under the terms of the GNU General Public License.
#
# This file is part of Assignment 1, CSCA48, Winter 2018
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file.  If not, see <http://www.gnu.org/licenses/>.
"""

from wackynode import WackyNode

# Do not add import statements or change the one above.
# Write your WackyQueue class code below.


class EmptyQueueError(Exception):
    '''An error to raise when queue is empty'''


class WackyQueue:
    def __init__(self):
        '''(WackyQueue) -> NoneType
        constructs an empty queue
        '''
        # Representation invariant:
        self._head1 = WackyNode(None, None)
        self._head2 = WackyNode(None, None)

    def __str__(self):
        '''(WackyQueue) -> str
        returns a string representing this queue
        '''
        result = ""
        if self._head1.get_next() is None:
            result = "None"
        else:
            curr1 = self._head1
            curr2 = self._head2
            while curr1.get_next() is not None:
                result = result + str(curr1.get_next().get_item()) + " -> "
                curr1 = curr1.get_next()
                if curr2.get_next() is not None:
                    result = result + str(curr2.get_next().get_item()) + " -> "
                    curr2 = curr2.get_next()
        return result

    def insert(self, obj, pri):
        '''(WackyQueue, obj, int) -> NoneType
        insert an object to queue, whose priority = pri and item = obj
        REQ: priority >= 0
        '''
        # create a node
        new_node = WackyNode(obj, pri)
        # set 3 pointers that point to 2 head nodes and the 1st node
        prev = self._head1
        curr = self._head2
        next = self._head1.get_next()
        # find the right place for insertion by comparing the priority of
        # the current object and the objects that are already in the queue
        while (next is not None) and (next.get_priority() >= pri):
            # move to the next node
            now = next
            next = curr.get_next()
            prev = curr
            curr = now
        # when find the right place
        # insert the new node after the prev node
        prev.set_next(new_node)
        # if the curr node has a _next node
        if (curr.get_next() is not None):
            # set this node to be the _next of the new node
            new_node.set_next(curr.get_next())
        # set next node to be the _next of the curr node
        curr.set_next(next)

    def extracthigh(self):
        '''(WackyQueue) -> Obj
        Remove and return the first item in the wacky queue.
        REQ: The wacky queue is not empty.
        '''
        # if the queue is empty
        if self.isempty():
            # raise error
            raise EmptyQueueError("The queue is empty!")
        # otherwise
        else:
            # find the first node in the queue
            result = self._head1.get_next()
            # set the previous second node to be the current first node
            self._head1.set_next(self._head2.get_next())
            # set the previous third node to be the current second node
            self._head2.set_next(result.get_next())
            # return the item in the node
            return result.get_item()

    def isempty(self):
        '''(WackyQueue) -> bool
        returns true if the queue is empty
        '''
        # return whether the queue is empty by checking if the head1._next is
        # None
        return self._head1.get_next() is None

    def changepriority(self, obj, pri):
        '''(WackyQueue, obj, int) -> NoneType
        Change the priority of the first copy of object obj to pri.
        The wacky queue is unchanged if obj is not in it or already has
        priority pri.
        If the priority of obj is changed, then the insertion time of obj is
        taken to be the time of the changepriority operation.
        '''
        # set 3 pointers that point to 2 head nodes and the 1st node
        prev = self._head1
        curr = self._head2
        next = self._head1.get_next()
        # check if the obj already exists by comparing the obj and the objects
        # already in the queue
        while (next is not None) and (next.get_item() != obj):
            # move to the next node
            now = next
            next = curr.get_next()
            prev = curr
            curr = now
        # if the obj already exists and it doesn't have priority pri
        if (next is not None) and (next.get_priority() != pri):
            # set the _next of curr node to be the _next of the prev node
            prev.set_next(curr.get_next())
            # set the _next of changing node to be the _next of the curr node
            curr.set_next(next.get_next())
            # insert the pri-changed node
            self.insert(obj, pri)

    def negateall(self):
        '''(WackyNode) -> NoneType
        Negate the priority of every object in the wacky queue.
        The order of insertion times of objects in the wacky queue is reversed.
        Thus the order of objects with equal priority is also reversed.
        '''
        # create pointers to the None's, 2 heads, first and second nodes
        prev1 = None
        prev2 = None
        curr1 = self._head1
        curr2 = self._head2
        next1 = curr1.get_next()
        end1 = next1
        next2 = curr2.get_next()
        end2 = next2
        # create a int to count the number of nodes
        num = 0

        # check the linked list of the odd nodes
        while curr1 is not None:
            # reverse the nodes
            curr1.set_next(prev1)
            # move to the next node
            prev1 = curr1
            curr1 = next1
            # if next1 is a node
            if next1 is not None:
                # negate its priority
                next1.set_priority(-next1.get_priority())
                # move to the next node
                next1 = next1.get_next()
                # add 1 to the number of nodes
                num = num + 1
        # update self._head1
        self._head1.set_next(prev1)
        end1.set_next(None)

        # check the linked list of the even nodes
        while curr2 is not None:
            # reverse the nodes
            curr2.set_next(prev2)
            # move to the next node
            prev2 = curr2
            curr2 = next2
            # if next2 is a node
            if next2 is not None:
                # negate its priority
                next2.set_priority(-next2.get_priority())
                # move to the next node
                next2 = next2.get_next()
                # add 1 to the number of nodes
                num = num + 1
        # update self._head2
        self._head2.set_next(prev2)
        end2.set_next(None)

        # if the number of nodes is even
        if (num % 2) == 0:
            # exchange the two heads
            head = self._head1
            self._head1 = self._head2
            self._head2 = head

    def getoddlist(self):
        '''(WackyNode) -> WackyNode or NoneType
        Return a pointer to a linked list of WackyNodes containing every
        other object in the wacky queue, starting with the first object.
        If there is no first object, then an empty list is returned.
        '''
        # return the pointer to the linked list of odd nodes
        return self._head1.get_next()

    def getevenlist(self):
        '''(WackyNode) -> WackyNode or NoneType
        Return a pointer to a linked list of WackyNodes containing every other
        object in the wacky queue, starting with the second object.
        If there is no second object, then an empty list is returned.
        '''
        # return the pointer to the linked list of even nodes
        return self._head2.get_next()

if __name__ == '__main__':
    wq = WackyQueue()
    wq.insert('6',6)
    wq.insert('6',6)
    wq.insert('A',1)
    wq.insert('A',0)
    wq.insert('A',1)
    wq.insert('A',0)
    wq.insert('B',0)
    wq.insert('B',0)
    wq.insert('Z',-2)
    wq.insert('P',-2)
    print(wq)

    print(wq.isempty())
    wq.changepriority('B',-100)
    wq.changepriority('6',4)
    wq.insert('5',5)
    print(wq)

    wq.negateall()
    print(wq)

    wq.changepriority('A',100)
    wq.insert('C',-1)
    print("---")
    print(wq)
    wq.negateall()
    print(wq)
    wq.changepriority('P',-0.5)
    wq.changepriority('KYLE',100)
    wq.negateall()
    print(wq)

    print(wq.extracthigh())
    print(wq.extracthigh())
    print(wq.extracthigh())
    print(wq.extracthigh())
    print(wq.extracthigh())
    print(wq.extracthigh())
    print(wq.extracthigh())
    print(wq.extracthigh())
    print(wq.extracthigh())
    print(wq.extracthigh())
    print(wq.extracthigh())
    print(wq.extracthigh())

    print(wq.isempty())