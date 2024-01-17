cpu 8086

segment	code
..start	mov bx, data
	mov ds, bx
	;
	mov bx, stack
	mov ss, bx
	mov sp, dno
	; Init the row counter
	mov di, 0

read_loop:
	mov ah, 0Ah
	mov dx, usIn
	int 21h
	;
	jz end_loop
	
	; si the iterator and count of ' '
	xor si, si
	
check_space:
	mov al, [usIn + 2 + si]
	cmp al, ' '
	jne check_hashtag
	inc si
	jmp check_space
	; loop
	
check_hashtag:
	; check for '#'
	mov al, [usIn + 2 + si]
	cmp al, '#'
	je read_loop
	
continue:
	mov al, [usIn + 1]	; get the len of the input
	mov cl, al
	cbw			; extends al to ax
	add ax, 2		; add 2 to skip the len and max size
	mov bx, usIn
	add bx, ax		; add the len of the string
	
	; check for empty line
	cmp cl, 0
	je print_no_num
	
	; inc counter and check if > 99
	inc di
	cmp di, 100
	jne not_100
	mov di, 0
	
not_100:
	; check if di is >= 10, has 2 nums
	cmp di, 10
	jge more_equal_10
	
; less than 10 - di < 10
	mov ax, di
	add ax, 30h		; convert to ASCII for < 10
	mov byte [nums], ' '
	mov byte [nums + 1], al
	jmp print
	
more_equal_10:
	mov ax, di
	mov bl, 10
	div bl
	add ax, 3030h
	xchg ah, al
	mov byte [nums], ah
	mov byte [nums + 1], al

print:
	mov ah, 09h
	mov dx, nums
	int 21h
	;
	mov cx, -1

print_no_num:
	mov byte [bx], 0Dh	; CR
	inc bx
	mov byte [bx], 0Ah	; LF
	inc bx
	mov byte [bx], '$'	; terminator
	;
	mov ah, 09h
	mov dx, usIn
	add dx, 2
	add dx, si		; add num of spaces to skip
	int 21h
	;
	jmp read_loop
	; loop
	
end_loop:
	hlt
	
	
segment data
usIn	db 255, ?
	resb 255
nums	db ' ', '0', '.', ' ', '$'
vars 	db 16
	
segment stack
	resb 16
dno:	db ?
