fn main:
027F.0000: ADD     RV, PC, 0xFFE7 ; Put address of `Email: ` string to first param
0284.0000: FCR     0xFEAD ; Print email prompt

0287.0000: SUB     SP, 0x1E
; Allocate stack space for email input
; SP = FAE2
028B.0000: MOV     RV, SP ; Set stack buf as first param
028D.0000: MOV     R3, 0x1E ; Amount of input to read
0291.0000: FCR     0xFE6C ; Get email input
; SP = FAE2

0294.0000: CMP     RV,  0x1E ; Lengh must be equal to 0x1E (30)
0298.0000: BRR.NE  0x12

; R3 = 001E
; SP = FAE2
029B.0000: ADD     R3, SP, 0x1D
; R3 = FAFF = SP + 0x1D
; R3 now points to the last character in the email buf

02A0.0000: LDB     R4, [R3] ; R4 set to zero (null byte?)
02A2.0000: AND     ZERO, R4, 0x80; This instruction does nothing except set the Z flag?
02A7.0000: BRR.EQ  0x3 ; Z is set, so we jumped over the next call
02AA.0000: FCR     0xFEA7

02AD.0000: ADD     RV, PC, 0xFFC0 ; Jumped here from 02A7
; Put address of `License key: ` string to first param
02B2.0000: FCR     0xFE7F ; Print license key prompt

02B5.0000: SUB     SP, 0x1E
02B9.0000: MOV     RV, SP
02BB.0000: MOV     R3, 0x1E
02BF.0000: FCR     0xFE3E ; Get license key
; SP = FAC4

02C2.0000: CMP     RV,  0x1E ; Must be 30 bytes
02C6.0000: BRR.NE  0x12

02C9.0000: ADD     R3, SP, 0x1D ; R3 points to last char again (detect overflow?)
02CE.0000: LDB     R4, [R3] ; R4 is zeroed again
02D0.0000: AND     ZERO, R4, 0x80
02D5.0000: BRR.EQ  0x3
02D8.0000: FCR     0xFE79 ; Jump over this

02DB.0000: MOV     RV, SP ; Set stack pointer to first param
02DD.0000: MOV     R3, 0x8 ; Set second param to 0x8
02E1.0000: MOV     R4, RV ; Set third param to first param (stack pointer)
; R2 = FAC4
; R3 = 8
; R4 = FAC4
02E3.0000: FCR     0xFF34 ; Jumps to fn_021A (fn check_license_key)
02E6.0000: MOV     RV, RV ; If returned 0, then we fail
02E8.0000: FCR.EQ  0xFE69 ; Jump to weird failure place

02EB.0000: MOV     R3, SP ; Second param points to license buf buf
02ED.0000: ADD     RV, R3, 0x1E ; First param points to email buf
02F2.0000: FCR     0xFE86 ; Jump to 0x017B (fn check_email)

02F5.0000: MOV     RV, RV
02F7.0000: FCR.EQ  0xFE52 ; Jump to 0x014C (this is what we want)
02FA.0000: FCR     0xFE57 ; Jump to 0x0154 (weird failure)
02FD.0000: HLT
02FE.0000: ADD.EQ  ZERO, ZERO

---

fn recv_str(char* buf, int n):
0100.0000: MOV     R4, ZERO
0102.0000: MOV     R6, ZERO
0104.0000: BRR     0x1A ; Jump to 0x0121

0107.0000: CMP     R5,  0xA
; Jump from 0x0128
; If R5 == '\n': [RV] = 0, return
010B.0000: STB.EQ  [RV], R6 ; Assign [RV] = Last value
010D.0000: BRR.EQ  0x20

0110.0000: MOV     R4, R4
0112.0000: BRR.EQ  0x8 ; If R4 == 0, jump to 0x11d
; If we're on the first byte, skip storing it for now

0115.0000: ORR     R6, 0x80 ; For some reason all inputs are OR'd with 0x80
0119.0000: STB     [RV], R6
011B.0000: INC     RV, 1

011D.0000: MOV     R6, R5 ; Jump from 0x0112
011F.0000: INC     R4, 1

0121.0000: CMP     R4,  R3 ; Jump from 0x0104
0123.0000: BRR.GE  0xA ; if (i >= n): Jump to return
0126.0000: RDB     R5, (0) ; Read byte into R5
0128.0000: BRR.LT  0xFFDC; Jump to 0x0107

012B.0000: MOV     RV, R5
012D.0000: BRR     0x2 ; Jump to return

0130.0000: MOV     RV, R4 ; Jump from 0x010D
0132.0000: BRA     RD, RA ; RET

---

fn print_str(char* s):
0134.0000: MOV     RV, RV ; Jumped here from func_021A (Prints `Invalid email or license key`)
0136.0000: BRA.EQ  RD, RA
0138.0000: MOV     R5, 0x7F
013C.0000: LDB     R3, [RV]
013E.0000: INC     RV, 1
0140.0000: AND     R4, R3, R5
0143.0000: WRB     (0), R4
0145.0000: CMP     R3,  R4
0147.0000: BRR.GT  0xFFF2
014A.0000: BRA     RD, RA ; RET

014C.0000: RDB     RV, (15) ; Read a byte from port 0xF (the flag port) and print it
014E.0000: WRB.LT  (0), RV
0150.0000: BRR.LT  0xFFF9
0153.0000: HLT

fn weird_failure:
0154.0000: ADD     RV, PC, 0x4 ; We get here from 02AA, a call that never happens (?)
; What's with PC + 4? Doesn't that just point to HLT?
0159.0000: FCR     0xFFD8 ; Print out some message
015C.0000: HLT

---

fn check_email(char* email, char* license):
017B.0000: MOV     R4, RV ; R4 = email
017D.0000: MOV     R5, RV ; R5 = email

017F.0000: LDB     RV, [R5] ; RV = email[R5]
0181.0000: AND     ZERO, RV, 0x80 ; Make sure it's not 0x80
0186.0000: INC.NE  R5, 1
0188.0000: BRR.NE  0xFFF4 ; Jump to 017f
; R5 = 0xFAFF (end of the buffer)

018B.0000: MOV     R6, R5 ; R6 = R5 (end of buffer)
018D.0000: SUB     RV, R5, R4

0190.0000: CMP     RV,  if rv `<` 0xA: fail or success?
0194.0000: INC.LT  RV, 1 ;
0196.0000: BRA.LT  RD, RA ; RET 1

0198.0000: LDB     RV, [R5]
019A.0000: INC     R5, -1

019C.0000: SUB     RV, 0x72
01A0.0000: BRA.NE  RD, RA ; if rv != 0x72: fail

01A2.0000: LDB     RV, [R5] ; next char from the end
01A4.0000: INC     R5, -1

01A6.0000: XOR     RV, 0xE1 ; if rv != 0xe1: fail
01AA.0000: BRA.NE  RD, RA

01AC.0000: LDB     RV, [R5] ; next char
01AE.0000: INC     R5, -1

01B0.0000: SUB     RV, 0xE5 ; if rv != 0xe5: fail
01B4.0000: BRA.NE  RD, RA

01B6.0000: LDB     RV, [R5]
01B8.0000: INC     R5, -1

01BA.0000: XOR     RV, 0xAE
01BE.0000: BRA.NE  RD, RA

01C0.0000: LDB     RV, [R5]
01C2.0000: INC     R5, -1

01C4.0000: SUB     RV, 0xE7
01C8.0000: BRA.NE  RD, RA

01CA.0000: LDB     RV, [R5]
01CC.0000: INC     R5, -1

01CE.0000: XOR     RV, 0xE5
01D2.0000: BRA.NE  RD, RA

01D4.0000: LDB     RV, [R5]
01D6.0000: INC     R5, -1

01D8.0000: SUB     RV, 0xF0
01DC.0000: BRA.NE  RD, RA

01DE.0000: LDB     RV, [R5]
01E0.0000: INC     R5, -1

01E2.0000: XOR     RV, 0xC0
01E6.0000: BRA.NE  RD, RA

; R3 = &license[0]
; R4 = &email[0]
; R6 = &email[28]
01E8.0000: MOV     R5, R4                       ; R5 = &email[0]
01EA.0000: MOV     R7, ZERO                     ; R7 = 0
01EC.0000: AND     RV, R7, 0x7                  ; RV = R7 & 0x7 (highest bit)
01F1.0000: ADD     RV, R3 ; RV = R3 + 0x7       ; RV += R3
01F3.0000: LDB     R4, [R5]                     ; R4 = *R5
01F5.0000: LDB     TMP, [RV]                    ; TMP = *RV
01F7.0000: ADD     TMP, R4                      ; TMP += R4
01F9.0000: STB     [RV], TMP                    ; *RV = TMP
01FB.0000: INC     R5, 1                        ; R5++
01FD.0000: INC     R7, 1                        ; R7++
01FF.0000: CMP     R5,  R6                      ; if R5 > R6: break
0201.0000: BRR.LE  0xFFE8

0204.0000: MOV     RV, ZERO
0206.0000: MOV     R7, ZERO
0208.0000: ADD     R5, R3, R7
020B.0000: LDB     R5, [R5]
020D.0000: ORR     RV, R5

020F.0000: CMP     R7,  0x7
0213.0000: INC.LT  R7, 1
0215.0000: BRR.LT  0xFFF0 ; Jump to 0208
0218.0000: BRA     RD, RA ; RET

fn check_license_key:
021A.0000: MOV     R3, R3 ; When R3 reaches 0, we're done
021C.0000: MOV.EQ  RV, 0x1 ; RV = 1, Didn't execute
0220.0000: BRA.EQ  RD, RA; RD = RA, Didn't execute
0222.0000: INC     R3, -1 ; Not done, decrement R3 (8 -> 7)

0224.0000: LDB     R5, [RV] ; Load byte from RV (FAC4), now contains 0x00B1
0226.0000: AND     ZERO, R5, 0x80 ; Check if RV equals 0x80
022B.0000: MOV.EQ  RV, ZERO ; If so, then set RV = 0
022D.0000: BRA.EQ  RD, RA ; And also set RD = RA
022F.0000: INC     RV, 1 ; Increment RV (move to the next byte)

0231.0000: SUB     R5, 0xEB ; R5 = R5 - 235, R5 = FFD6
0235.0000: CMP     R5,  0xF ; Compare R5 to 0xF000
0239.0000: MOV.GT  RV, ZERO ; Greater? Then set RV = 0 (return false)
023B.0000: BRA.GT  RD, RA ; Greater? RD = RA (this kills us immediately)
; If it's signed, then being greater than 0xF means you are negative
; That means we need a value larger than 0xEB

023D.0000: LDB     R6, [RV] ; Check the next byte
023F.0000: INC     RV, 1 ; Move on to the next byte
0241.0000: AND     ZERO, R6, 0x80 ; Don't let it be 0x80 (char can't be 0)
0246.0000: MOV.EQ  R3, ZERO ; R3 = 0 if true

0248.0000: AND     R6, 0x7F ; R6 = R6 & 0x7F
024C.0000: SUB     R6, 0x41 ; R6 = R6 - 0x41
0250.0000: CMP     R6,  0xF ; R6 > 0xF?
0254.0000: MOV.GT  RV, ZERO ; If so, then we're dead
0256.0000: BRA.GT  RD, RA

0258.0000: SHL     R6, 0x4 ; R6 = R6 `<<` 4
025C.0000: ORR     R5, R6 ; R5 = R5 | R6
025E.0000: STB     [R4], R5 ; s[0] = R5
0260.0000: INC     R4, 1 ; Increment R4
0262.0000: BRR     0xFFB5 ; Jump back to the start of the function
0265.0000: MOV     RV, 0x1 ; We want to get here
0269.0000: BRA     RD, RA ; RET

$ hexdump r 0xfac4 60
fac4: 0000 0000 0000 0000 ebc1 ebc1 ebc1 ebc1  ................
fad4: ebc1 ebc1 ebc1 ebc1 ebc1 ebc1 eb00 3980  ................
fae4: 8080 8080 8080 8080 8080 f2f2 f2f2 f2f2  ................
faf4: f2f2 f2c0 f0e5 e7ae e5e1 7200            ..........r.

Post scramble
$ hexdump r 0xfac4 60
fac4: 672e 6561 f2c0 f0e5 ebc1 ebc1 ebc1 ebc1  g.ea............
fad4: ebc1 ebc1 ebc1 ebc1 ebc1 ebc1 eb00 8080  ................
fae4: 8080 8080 8080 8080 8080 8080 8080 8080  ................
faf4: 8080 80c0 f0e5 e7ae e5e1 7200            ..........r.

Expect 0, got:
ce5c cac2 e480 e0ca
