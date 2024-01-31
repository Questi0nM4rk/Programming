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
	
; ================================= OCT =========
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
	jb multO
	
	mov cx, 1
	mov ax, 1
	add dl, '0'
	inc si
	mov byte [si], dl
	xor dx, dx
	
	jmp contO

multO:
	mov ax, cx
	mov bl, 2
	mul bl
	mov cx, ax
	
contO:
	dec di
	cmp di, usIn + 2
	jge oct_loop

; add two last bits
	add dl, '0'
	inc si
	mov byte [si], dl

; reverse
	mov dl, byte [si]
	mov dh, byte [si - 2]
	mov byte [si], dh
	mov byte [si - 2], dl

; add space separator
	inc si
	mov byte [si], ' '

; ============================ hex ================
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
	jb multH
	
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
	jmp contH

multH:
	mov ax, cx
	mov bl, 2
	mul bl
	mov cx, ax

contH:
	dec di
	cmp di, usIn + 2
	jge hex_loop
	
; reverse
	mov dl, byte [si]
	mov dh, byte [si - 1]
	mov byte [si], dh
	mov byte [si - 1], dl

; add space separator
endH:
	inc si
	mov byte [si], ' '
	
; =========================== deka 1 ===============

; count deka1
	mov ax, 1
	mov cx, 1
	xor dx, dx
	mov di, usIn + 2 + 7
deka1_loop:
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
	jge deka1_loop
	
; skip function
	jmp eD1

; Parameters:
;   dx - the number to check
;   si - the address to save the result
count_n:
	push dx
	
	; Check the number of digits
	cmp dx, 10
	jge two_digits

	; One digit
	add dl, '0'
	mov [si], dl
	jmp end_check

two_digits:
	cmp dx, 100
	jge three_digits
	
	; Two digits
	mov ax, dx
	mov cx, 10
	div cl
	add al, '0'
	mov byte [si], al
	inc si
	add ah, '0'
	mov byte [si], ah
	jmp end_check

three_digits:
	; Three digits
	mov ax, dx
	mov cx, 100
	div cl
	add al, '0'
	mov [si], al
	inc si
	mov ax, dx
	mov cx, 10
	div cl
	add al, '0'
	mov [si], al
	inc si
	add ah, '0'
	mov [si], ah
    
end_check:
	pop dx
	ret

; write to buffer
eD1:
	
; print deka1
	inc si
	call count_n
	; adds deka1 to buffer
	
	; add the ' ' separator
	inc si
	mov byte [si], ' '
	
	; check for deka2 sign
	cmp byte [usIn + 2], '0'
	je possitive
	
; prints deka2 if negative
	neg dx
	inc si
	mov byte [si], '-'
	inc si
	call count_n
	neg dx
	jmp ASCII
	
possitive:
	mov byte [si], ' '
	inc si
	call count_n
	; prints deka2 if possitive

; ====================================== ASCII ===========

ASCII:
	cmp dx, 'a'
	jb BCD
	cmp dx, 'z'
	jbe is_char
	
	cmp dx, 'A'
	jb BCD
	cmp dx, 'Z'
	jbe is_char
	
	jmp BCD
	
is_char:
	inc si
	mov byte [si], ' '
	inc si
	mov byte [si], dl
	
; ===================================== BCD ==============

BCD:
	inc si
	mov byte [si], ' '
	
	mov ax, 1
	mov cx, 1
	xor dx, dx
	mov di, usIn + 2 + 7
bcd_loop:
	mov bl, [di]
	sub bl, '0'
	mov ax, cx
	mul bl
	add dx, ax
	
	cmp cx, 8
	jb multB
	
	mov cx, 1
	mov ax, 1
	cmp dl, 10
	jge end_rem
	
	add dl, '0'
	inc si
	mov byte [si], dl
	xor dx, dx
	jmp contB

multB:
	mov ax, cx
	mov bl, 2
	mul bl
	mov cx, ax

contB:
	dec di
	cmp di, usIn + 2
	jge bcd_loop

; reverse
	mov dl, byte [si]
	mov dh, byte [si - 1]
	mov byte [si], dh
	mov byte [si - 1], dl
	jmp end

; remove the separating space when bin isnt BCD
end_rem:
	cmp byte [si], ' '
	jne o1
	
	dec si
	jmp end

o1:
	cmp byte [si - 1], ' '
	jne o2
	
	sub si, 2
	jmp end

o2:
	sub si, 3
	jmp end

end:
	inc si
	mov byte [si], '$'
	mov ah, 09h
	mov dx, usIn + 2
	int 21h

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


segment stack
	    resb 32
dno:	db ?