cpu 8086
segment	code
..start:
    mov bx, data
    mov ds, bx
    
    mov bx, stack
    mov ss, bx
    mov sp, dno
    
    mov bx, 0xef0f
    mov es, bx
    mov bx, 0xf68d
    mov es:[bx], word 0x2eFF
    mov es:[bx+2], word doma36
    
    jmp far [mimo3b]
    
end:
    hlt

segment	data
mimo3b	dw 0xf68d
        dw 0xef0f
    
doma36	dw end, code
        dw code

segment	stack
    resb 16
dno:    db ?