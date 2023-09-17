#pragma once

// includes

#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <memory>

// aliases

template <typename U>
using uptr = std::unique_ptr<U>;

template <typename S>
using sptr = std::shared_ptr<S>;

// struct

struct Node
{
    int data;
    Node* next;
    Node* prev;

    Node(int val) : data(val), next(nullptr), prev(nullptr) {}
};

class DoublyLinkedList
{
private:
    Node* head = nullptr;
    Node* tail = nullptr;
    int size = 0;

public:
    
    DoublyLinkedList() : head(nullptr), tail(nullptr), size(0) {}

    Node* addNodeStart(const int &val); //done C

    Node* addNodeEnd(const int &val);   //done C

    Node* insertNode(const int &pos, const int &val);   //done C

    Node* getNodeByVal(const int &val);  //done C-find

    Node* getNodeByPos(const int &pos);  //done

    Node* getHead() const;  //done

    Node* getTail() const;  //done

    uptr<Node> popNodeByVal(const int &val); //done C-find
   
    uptr<Node> popNodeByPos(const int &pos); //done

    uptr<Node> popNode(Node* node); //done

    std::vector<int> toArray() const; //done C

    bool remNodeByVal(const int &val);   //done C

    bool remNodeByPos(const int &pos);   //done

    bool remNode(Node* node);   //done C

    bool clearList();   //done C

    bool isEmpty() const;   //done

    bool swapNodesByVal(const int &val1, const int &val2); //done

    bool swapNodesByPos(const int &pos1, const int &pos2); //done

    bool swapNodes(Node* node1, Node* node2);   //done C

    int getSize() const;  //done

    void printList() const;   //done

    void printListBack() const;   //done
    
    void reverseList(); //done C

    ~DoublyLinkedList();    //done C

};



