cpu 8086

segment code
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
	jz end
	
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

; ==================================
okay:
	xor dx, dx
	mov ax, 1
	mov cx, 1
	mov di, usIn + 2 + 7
num_loop:
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
	jge num_loop
	
; process
	mov [num], dl
	
	mov si, buffer + 99	; address
	
; ======================== bin ===============

	mov di, usIn + 2 + 7
bin_loop:
	mov al, [di]
	mov byte [si], al
	dec di
	dec si
	cmp di, usIn + 2
	jge bin_loop
	
	mov byte [si], ' '

; ======================== oct ===============
	
	mov ch, 3		; shift
	mov bh, 00000111b	; mask
	mov dl, 3		; iters
	
	call convert_to_base

	dec si
	mov byte [si], ' '
	
; ======================== hex ===============
	
	mov ch, 4
	mov bh, 00001111b
	mov dl, 2
	
	call convert_to_base
	
	dec si
	mov byte [si], ' '

; ======================== bcd ===============
	cmp dh, 1
	jne notBCD
	
	mov ch, 4
	mov bh, 00001111b
	mov dl, 2
	
	call convert_to_base
	
	dec si
	mov byte [si], ' '
	
notBCD:

; ======================== dec ===============

	cmp byte [usIn + 2], '0'
	je possitive
	
	mov al, [num]
	neg al
	
	call num_to_str
	
	dec si
	mov byte [si], '-'

	dec si
	mov byte [si], ' '
	
	jmp deka1
	
possitive:
	mov al, [num]
	call num_to_str
	
	dec si
	mov byte [si], ' '

deka1:
	mov al, [num]
	call num_to_str
	
	dec si
	mov byte [si], ' '

; ======================== asc ===============

	mov ah, 0
	mov al, [num]
	
	cmp ax, '0'
	jb print
	cmp ax, '9'
	jbe is_num
	
	cmp ax, 'A'
	jb print
	cmp ax, 'Z'
	jbe is_char
	
	cmp ax, 'a'
	jb print
	cmp ax, 'z'
	jbe is_char
	
	jmp print
	
is_num:
is_char:
	dec si
	mov byte [si], al


print:
	
	cmp byte [si], ' '
	jne no_space
	
	inc si

no_space:
	mov ah, 09h
	mov dx, si
	int 21h


end:
	hlt


; functions

; Parameters:
;	num - number
;	ch - shift
;	bh - mask
;	dl - num of iters
;	si - address
convert_to_base:

	mov dh, 1	; check for isBCD / contains num >= 10

	mov byte al, [num]
	
	mov cl, 0
	
iterate_sets:
	
	mov ah, al
	shr ah, cl
	and ah, bh
	
	add cl, ch
	
	cmp ah, 10
	jge char

	add ah, '0'
	jmp ctn

char:
	add ah, 87
	mov dh, 0	; is not BCD
	
ctn:
	dec si
	mov byte [si], ah

	dec dl

	cmp dl, 0
	jg iterate_sets
	
	ret
	
; Parameters:
;	al - number
;	si - address
num_to_str:
	
	mov ah, 0

	cmp ax, 10
	jge two_digs
	
	dec si
	add al, '0'
	mov byte [si], al
	
	jmp endf
	
two_digs:
	cmp ax, 100
	jge three_digs
	
	mov bl, 10
	div bl
	
	dec si
	add ah, '0'
	mov byte [si], ah
	
	dec si
	add al, '0'
	mov byte [si], al
	
	jmp endf
	
three_digs:
	mov bl, 10
	div bl
	
	dec si
	add ah, '0'
	mov byte [si], ah
	
	mov ah, 0
	div bl
	
	dec si
	add ah, '0'
	mov byte [si], ah
	
	dec si
	add al, '0'
	mov byte [si], al
	
endf:
	ret

	

segment data
usIn 	db 255, ?
	resb 255

error   db 'Chybný vstup', 0Dh, 0Ah, '$'
	
num 	db 0

buffer	resb 100
ending	db 0Dh, 0Ah, '$'


segment stack
	resb 32
dno: 	db ?