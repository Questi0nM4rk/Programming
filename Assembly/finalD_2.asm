cpu 8086

segment code
..start	mov bx, data
	mov ds, bx
	;
	mov bx, stack
	mov ss, bx
	mov sp, dno


	mov ax, 1
	mov cx, 1
	mov di, usIn + 2 + 7
num_loop:
	mov bl, [di]
	sub bl, '0'
	mov ax, cx
	mul bl
	add num, ax

	mov ax, cx
	mov bl, 2
	mul bl
	mov cx, ax

	dec di
	cmp di, usIn + 2
	jge num_loop

; ======================== oct ===============



end:
	hlt


; functions

; Parameters:
;	num - number
;	cl - shift
;	si - address
convert_to_base:



segment data
usIn 	db 255, ?
	resb 255
num 	db 0

buffer	resb 100
ending	db 0Dh, 0Ah, '$'



segment stack
	restb 32
dno: 	db ?
    