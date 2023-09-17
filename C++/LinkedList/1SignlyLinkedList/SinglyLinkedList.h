#pragma once

//includes

#include "../../basic.h"

//aliases
template <typename U>
using uptr = std::unique_ptr<U>;

// the list

struct Node {
    int data;
    std::unique_ptr<Node> next;

    Node(int val) : data(val), next(nullptr) {}
};

class SinglyLinkedList {
private:
    uptr<Node> head = nullptr;
    Node* tail = nullptr;
    int size = 0;

public:
    SinglyLinkedList() : head(nullptr), tail(nullptr), size(0) {}

    Node* addNodeStart(const int &val); //done

    Node* addNodeEnd(const int &val);   //done

    Node* insertNode(const int &pos, const int &val);   //done

    Node* getNodeByVal(const int &val);  //done

    Node* getNodeByPos(const int &pos);  //done

    Node* getHead() const;  //done

    Node* getTail() const;  //done

    uptr<Node> popNodeByVal(const int &val); //done
   
    uptr<Node> popNodeByPos(const int &pos); //done

    uptr<Node> popNode(Node* node); //done

    std::vector<int> toArray() const; //done

    bool remNodeByVal(const int &val);   //done

    bool remNodeByPos(const int &pos);   //done

    bool remNode(Node* node);   //done

    bool clearList();   //done

    bool isEmpty() const;   //done

    bool swapNodesByVal(const int &val1, const int &val2); //done

    bool swapNodesByPos(const int &pos1, const int &pos2); //done

    bool swapNodes(Node* node1, Node* node2);   //done

    int getSize() const;  //done

    void printList() const;   //done
    
    void reverseList(); //done

    ~SinglyLinkedList();    //done
};