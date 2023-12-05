cpu 8086

segment segm
    resb 1024

segment code
..start mov bx, data
       mov ds, bx
       mov bx, stack
       mov ss, bx
       mov sp, dno
       mov bx, segm
       mov es, bx

       mov bx, code
       mov cs, bx

       mov es:[16], word into85
       mov es:[18], cs

       mov bx, 0

loop:
    mov dl, [data188+bx]
    add dl, [data288+bx]
    into
    inc bx
    cmp bx, [delka4f]
    jne loop
    hlt

into85:
    mov ax, 0
    push ax
    push dx
    mov ax, bx ; Move the counter i to ax

    ; Print the "overflow " part of the mesg string
    mov dx, mesg
    mov ah, 9
    int 21h

    ; Convert the high byte of bx to two hexadecimal digits
    mov al, bh
    mov cl, 4
    shr al, cl
    call ascii
    mov al, bh
    and al, 0Fh
    call ascii

    ; Convert the low byte of bx to two hexadecimal digits
    mov al, bl
    mov cl, 4
    shr al, cl
    call ascii
    mov al, bl
    and al, 0Fh
    call ascii

    ; Print a carriage return and line feed
    mov dx, enter
    mov ah, 9
    int 21h

    pop dx
    pop ax
    iret ; Return from interrupt

ascii:
    and al, 0Fh
    cmp al, 9
    jbe next
    add al, 7
next:
    add al, 30h
    mov AH, 2
    mov DL, al
    int 21h
    ret

segment data
delka4f dw 5

data188 db -100 
    	db -22
    	db -100
    	db 100
    	db 7
    	resb 10000

data288 db -100 
    	db -22
    	db -100
    	db 100
    	db 7
    	resb 10000

mesg db "overflow ", '$'
enter db 13, 10, '$'

segment stack
    resb 16
dno: db ?
