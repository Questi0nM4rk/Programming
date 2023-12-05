CPU 8086

SEGMENT ivt
    DW div91, 0 ; Interrupt 0 (division by zero)
    RESB 1020    ; Reserve space for the rest of the IVT

SEGMENT code
..start:
    ; Set up data segment
    MOV AX, data
    MOV DS, AX

    ; Set up stack segment
    MOV AX, stack
    MOV SS, AX
    MOV SP, dno

    ; Set up ivt segment
    MOV AX, ivt
    MOV ES, AX
    
    ; Get the div91 offset
    LEA BX, div91
    MOV [ES:0*4], BX 		; Point interrupt 0 to the div91
    MOV [ES:0*4+2], CS

    ; Cause division by zero
    XOR AX, AX
    DIV AL
    XOR AX, AX
    DIV AL
    XOR AX, AX
    DIV AL
    
konec39	HLT
    
div91:
    ; Print "division by zero"
    MOV DX, mesg
    MOV AH, 9
    INT 21H

    ; Adjust return address
    POP AX       		; Pop IP
    ADD AX, 2 			; Length of DIV instruction
    PUSH AX 			; Push back adjusted IP

    IRET

SEGMENT data
mesg    DB 'Division by zero', 13, 10, '$'

SEGMENT stack
    RESB 16
dno:    DB ?