#include "./DoublyLinkedList.h"

int main() {
    
    DoublyLinkedList DLL;

    for (int i = 5; i > 0; i--) {
        DLL.addNodeStart(i);
    }

    std::cout << std::endl;

    DLL.printList();
    
    
    return EXIT_SUCCESS;
}