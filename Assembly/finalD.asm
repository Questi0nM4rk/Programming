cpu 8086

segment	code
..start	mov bx, data
	mov ds, bx
	;
	mov bx, stack
	mov ss, bx
	mov sp, dno

read_loop:
	mov ah, 0Ah
	mov dx, usIn
	int 21h
	;
	jz end_loop
	
	mov al, [usIn + 1]	; get the len of the input
	mov cl, al
	cbw			; extends al to ax
	add ax, 2		; add 2 to skip the len and max size
	mov bx, usIn
	add bx, ax		; add the len of the string
    
	; dec bx to have the place of the last char
	dec bx
    
	; check if the line has 8 nums
	cmp cl, 8
	jb ff_go_next
	jg ff_go_next
	
	xor si, si
	add si, 2
check_0_1:
	cmp byte [usIn + si], '0'
	je next_char
	cmp byte [usIn + si], '1'
	je next_char
	;
	jmp ff_go_next
	
next_char:
	inc si
	cmp si, 8
	jbe check_0_1
	jmp okay

ff_go_next:
	mov ah, 09h
	mov dx, error
	int 21h
	hlt


okay:
	mov si, usIn + 2 + 7	; get the pos of las char
	mov byte [si + 1], 0	; clear possible CR LF
	mov byte [si + 2], 0
; print oct
	mov ax, 1
	mov cx, 1
	xor dx, dx
	mov di, si
	inc si
	mov byte [si], ' '
oct_loop:
	mov bl, [di]
	sub bl, '0'
	mov ax, cx
	mul bl
	add dx, ax
	
	cmp cx, 4
	jb contO
	
	mov cx, 1
	mov ax, 1
	add dl, '0'
	inc si
	mov byte [si], dl
	xor dx, dx

contO:
	mov ax, cx
	mov bl, 2
	mul bl
	mov cx, ax

	dec di
	cmp di, usIn + 2
	jge oct_loop
	
; add space separator
	inc si
	mov byte [si], ' '

; ============================ hex ================

; print hex
	mov ax, 1
	mov cx, 1
	xor dx, dx
	mov di, usIn + 2 + 7
hex_loop:
	mov bl, [di]
	sub bl, '0'
	mov ax, cx
	mul bl
	add dx, ax
	
	cmp cx, 8
	jb contH
	
	mov cx, 1
	mov ax, 1
	cmp dl, 10
	jb num

	add dl, 87
	jmp nx
num:
	add dl, '0'
nx:
	inc si
	mov byte [si], dl
	xor dx, dx

contH:
	mov ax, cx
	mov bl, 2
	mul bl
	mov cx, ax

	dec di
	cmp di, usIn + 2
	jge hex_loop
	
; add space separator
	inc si
	mov byte [si], ' '
	
; =========================== deka 1 ===============

; print deka1
	mov ax, 1
	mov cx, 1
	xor dx, dx
	mov di, usIn + 2 + 7
deka1_loop:			; rw
	mov bl, [di]
	sub bl, '0'
	mov ax, cx
	mul bl
	add dx, ax

	mov ax, cx
	mov bl, 2
	mul bl
	mov cx, ax

	dec di
	cmp di, usIn + 2
	jge deka1_loop		; rw
	
; write to buffer
	
	inc si		; inc si to be at place to write
	cmp dx, 10
	jge dig2
	
	add dl, '0'
	mov byte [si], dl
	jmp eD1
dig2:
	cmp dx, 100
	jge dig3
	
	mov ax, dx
	mov cx, 10
	div cx
	add al, '0'
	mov byte [si], al
	inc si
	add ah, '0'
	mov byte [si], ah
	jmp eD1
	
dig3:
	mov ax, dx
	mov cx, 100
	div cx
	add al, '0'
	mov byte [si], al
	inc si
	mov ax, dx
	mov cx, 10
	div cx
	add al, '0'
	mov byte [si], al
	inc si
	add ah, '0'
	mov byte [si], ah
	
; add space separator
eD1:
	inc si
	mov byte [si], ' '
	
; =========================== deka 2 ===============

; print deka2
	
	inc si		; inc si to be at place to write
	
; check sign
	cmp byte [usIn + 2], '0'
	je possitive
	
	mov byte [si], '-'
	inc si
	
	not dx
	add dx, 1

possitive:
	cmp dx, 10
	jge two_dig
	
	add dl, '0'
	mov byte [si], dl
	jmp eD2
	
two_dig:
	cmp dx, 100
	jge three_dig
	
	mov ax, dx
	mov cx, 10
	div cx
	add al, '0'
	mov byte [si], al
	inc si
	add ah, '0'
	mov byte [si], ah
	jmp eD2
	
three_dig:
	mov ax, dx
	mov cx, 100
	div cx
	add al, '0'
	mov byte [si], al
	inc si
	mov ax, dx
	mov cx, 10
	div cx
	add al, '0'
	mov byte [si], al
	inc si
	add ah, '0'
	mov byte [si], ah
	
; add space separator
eD2:
	inc si
	mov byte [si], ' '
	
ASCII:
	
BCD:


	inc si
	mov byte [si], '$'
	mov ah, 09h
	mov dx, usIn + 2
	int 21h

	jmp end
	
end:
	mov ah, 09h
	mov dx, ending
	int 21h
	
end_loop:
	hlt

	
segment data
usIn	db 255, ?
	resb 255
error   db 'Chybný vstup', 0Dh, 0Ah, '$'
ending	db 0Dh, 0Ah, '$'

vars 	resb 24


segment stack
	    resb 16
dno:	db ?