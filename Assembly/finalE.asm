cpu 8086

segment	code
..start	mov bx, data
	mov ds, bx
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
	xor bx, bx
	
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
	
	; dec bx to have the place of the last char
	dec bx
	
	; check for empty line
	cmp cl, 0
	je print_no_num
	
	; inc counter and check if > 99
	inc di
	cmp di, 100
	jb not_100
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
	jmp init_encrypt
	
more_equal_10:
	mov ax, di
	mov dl, 10
	div dl
	add ax, 3030h
	xchg ah, al
	mov byte [nums], ah
	mov byte [nums + 1], al
	
init_encrypt:
	xor ax, ax
	mov word [vars + 1], di
	xor di, di
	add di, si	; add spaces
	add di, 2	; include max len, len
	;
	mov cx, -1
	
encrypt_loop:
	mov al, [usIn + di]
	;
	cmp al, 'A'
	jb next_char
	cmp al, 'Z'
	jbe is_uppercase
	;
	cmp al, 'a'
	jb next_char
	cmp al, 'z'
	jbe is_lowercase
	;
	jmp next_char
	
is_lowercase:
	add al, cl
	neg cx
	;
	cmp al, 'a'
	jb add_26
	;
	cmp al, 'z'
	jg sub_26
	;
	jmp next_char

is_uppercase:
	add al, cl
	neg cx
	;
	cmp al, 'A'
	jb add_26
	;
	cmp al, 'Z'
	jg sub_26
	;
	jmp next_char
	
add_26:
	add al, 26
	jmp next_char
sub_26:
	sub al, 26
	jmp next_char

next_char:
	mov [usIn + di], al
	inc di
	cmp di, bx
	jbe encrypt_loop
	jmp end_enc
	
end_enc:
	mov di, word [vars + 1]

print_with_nums:
	mov ah, 09h
	mov dx, nums
	int 21h

print_no_num:
	inc bx
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
vars 	db 20
	
segment stack
	resb 16
dno:	db ?

