#include "DoublyLinkedList.h"


Node* DoublyLinkedList::addNodeStart(const int &val) {
    Node* newNode = new Node(val);
    
    if (head == nullptr) {
        head = newNode;
        
        size++;
        return head;

    } else if (tail == nullptr) {
        head->next = std::move(newNode);
        tail = head->next;
        tail->prev = head;
        
        size++;
        return tail;

    } else {
        newNode->prev = head;
        newNode->next = head->next;
        newNode->next->prev = newNode;
        head->next = std::move(newNode);
        
        size++;
        return newNode;
    }
}

Node* DoublyLinkedList::addNodeEnd(const int &val) {
    Node* newNode = new Node(val);
    
    if (head == nullptr) {
        head = newNode;

        size++;
        return head;

    } else if (tail == nullptr) {
        head->next = newNode;
        tail = head->next;
        tail->prev = head;

        size++;
        return tail;

    } else {
        newNode->prev = tail;
        tail->next = newNode;
        tail = tail->next;
        
        size++;
        return newNode;
    }
}


Node* DoublyLinkedList::insertNode(const int &pos, const int &val) {
    if (!head) {
        return nullptr;
    }

    Node* newNode = new Node(val);

    Node* nodePos = getNodeByPos(pos);

    if (!nodePos) {
        return nullptr;
    }

    newNode->next = nodePos->next;
    newNode->prev = nodePos;
    nodePos->next = newNode;

    size++;

    return nodePos->next;
}


Node* DoublyLinkedList::getNodeByVal(const int &val) {
    if (head == nullptr) {
        return nullptr;
    }

    Node* left = head;
    Node* right = tail;

    while (left->next != right && right->prev != left && left != nullptr && right != nullptr) {
        if (left->data == val) {
            return left;
        }
        if (right->data == val) {
            return right;
        }

        left = left->next;
        right = right->prev;
    }

    if (left == right && left != nullptr && left->data == val) {
        return left;
    }

    return nullptr;
}

Node* DoublyLinkedList::getNodeByPos(const int &pos) {
    if (head == nullptr) {
        return nullptr;
    }

    if (pos == 0) {
        return head;
    }

    else if (pos == size-1) {
        return tail;
    }

    Node* left = head;
    Node* right = tail;

    int leftPos = 0;
    int rightPos = size;

    while (left->next != right && right->prev != left && left != nullptr && right != nullptr) {
        if (leftPos == pos) {
            return left;
        }

        if (rightPos == pos) {
            return right;
        }

        leftPos++;
        rightPos--;
    }

    if (leftPos == 0) {
        return left;
    }

    return nullptr;
}


Node* DoublyLinkedList::getHead() const {
    return head;
}

Node* DoublyLinkedList::getTail() const {
    return tail;
}


uptr<Node> DoublyLinkedList::popNodeByVal(const int &val) {

    Node* node = getNodeByVal(val);

    return popNode(node);
}

uptr<Node> DoublyLinkedList::popNodeByPos(const int &pos) {

    Node* node = getNodeByPos(pos);

    return popNode(node);

}

uptr<Node> DoublyLinkedList::popNode(Node* node) {
    if (head == nullptr) {
        return nullptr;
    }

    if (node->next) {
        node->next->prev = node->prev;
    } else {
        tail = node->prev;
        tail->next = nullptr;
    }

    if (node->prev) {
        node->prev->next = node->next;
    } else {
        head = node->next;
        head->prev = nullptr;
    }

    size--;

    return uptr<Node>(node);

}


std::vector<int> DoublyLinkedList::toArray() const {
    std::vector<int> result;

    Node* current = head;
    while (current) {
        result.push_back(current->data);
        current = current->next;
    }

    return result;
}


bool DoublyLinkedList::remNodeByVal(const int &val) {

    Node* node = getNodeByVal(val);

    return remNode(node);

}

bool DoublyLinkedList::remNodeByPos(const int &pos) {
    
    Node* node = getNodeByPos(pos);

    return remNode(node);
    
}

bool DoublyLinkedList::remNode(Node* node) {
    if (head == nullptr) {
        return false;
    }

    if (node == nullptr) {
        return false;
    }

    popNode(node);

    size--;

    return true;
}


bool DoublyLinkedList::clearList() {
    if (head == nullptr) {
        return false;
    }

    Node* current = head;
    
    while (current) {
        Node* nextNode = current->next;
        current->prev = nullptr; 
        current->next = nullptr; 
        current = nextNode;
    }

    head = nullptr;
    tail = nullptr;

    size = 0;

    return true;
    
}

bool DoublyLinkedList::isEmpty() const {
    return head == nullptr;
}


bool DoublyLinkedList::swapNodesByVal(const int &val1, const int &val2) {
    Node* node1 = getNodeByVal(val1);
    Node* node2 = getNodeByVal(val2);

    return swapNodes(node1, node2);
}

bool DoublyLinkedList::swapNodesByPos(const int &pos1, const int &pos2) {
    Node* node1 = getNodeByPos(pos1);
    Node* node2 = getNodeByPos(pos2);

    return swapNodes(node1, node2);
}

bool DoublyLinkedList::swapNodes(Node* node1, Node* node2) {
    if (!head || !node1 || !node2) {
        return false;
    }

    Node* tmpN1next = node1->next;
    Node* tmpN1prev = node1->prev;

    node1->next = node2->next;
    node1->prev = node2->prev;

    node2->next = std::move(tmpN1next);
    node2->prev = tmpN1prev;
    
    if (node1->prev != nullptr)
        node1->prev->next = node1;  // propably this is the last thing that holds the next node, so after replacing it with the new node destroyes the second node

    if (node2->prev != nullptr)
        node2->prev->next = node2;

    if (node1->next != nullptr)
        node1->next->prev = node1;

    if (node2->next != nullptr)
        node2->next->prev = node2;

    if (node1 == head) {
        head = node2;
        tail = node1;

    } else if (node2 == head) {
        head = node1;
        tail = node2;
    }

    return true;
}


int DoublyLinkedList::getSize() const {
    return size;
}

void DoublyLinkedList::printList() const {
    Node* current = head;

    while (current) {
        std::cout << current->data;

        if (current->next) {
            std::cout << " <--> ";
        }

        current = current->next;
    }

    std::cout << std::endl;
}

void DoublyLinkedList::printListBack() const {
    Node* current = tail;

    while (current) {
        std::cout << current->data;

        if (current->prev) {
            std::cout << " <--> ";
        }

        current = current->prev;
    }

    std::cout << std::endl;
}

void DoublyLinkedList::reverseList() {
    if (!head && !head->next) {
        return;
    }

    int left = 0;
    int right = size;

    Node* leftNode = head;
    Node* rightNode = tail;
    Node* rightNodeH = nullptr;
    Node* leftNodeH = nullptr;

    int half = size/2;

    while(left < half && right > half) {
        leftNodeH = leftNode->next;
        rightNodeH = rightNode->prev;
        
        swapNodes(leftNode, rightNode);
        printList();

        leftNode = leftNodeH;
        rightNode = rightNodeH;

        left++;
        right--;
    }
    
}

DoublyLinkedList::~DoublyLinkedList() {
    clearList();
}
