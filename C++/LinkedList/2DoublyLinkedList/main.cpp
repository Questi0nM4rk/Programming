#include "DoublyLinkedList.h"

int main() {
    
    DoublyLinkedList DLL;

    for (int i = 5; i > 0; i--) {
        DLL.addNodeStart(i);
    }

    std::cout << std::endl;

    DLL.printList();
    std::cout << std::endl;
    DLL.printListBack();

    std::cout << std::endl;
    
    DLL.reverseList();

    std::cout << std::endl;

    DLL.printList();
    std::cout << std::endl;
    DLL.printListBack();

    return EXIT_SUCCESS;
}