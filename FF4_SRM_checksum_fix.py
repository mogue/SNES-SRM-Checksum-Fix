"""
	Fix hacked FFIV SRM files
	2017, by m06

	Usage: python FF4_SRM_checksum_fix.py /path/to/save_file.srm
"""

print "\n\tFinal Fantasy IV SRM checksum fix\n"

import array
from struct import *
import sys

filename = ''

if len(sys.argv) > 1:
        filename = sys.argv[1]

if filename == '':
	print "!!! Please provide an SRM file to fix !!!\nUsage: python FF4_SRM_checksum_fix.py /PATH/TO/FILE.SRM\n"
	quit()

print "Fixing file: " + filename

with open(filename, "r+b") as f:
    for slot in range(4):
	f.seek( slot * 0x800 )
	checksum = 0
	data = array.array("B")
        data.fromfile(f, 0x7FA)
        lastbyte = None
        for byte in data:
            if  lastbyte is None:
		lastbyte = byte
		continue
            word = (byte << 8) + lastbyte
            checksum += word
            lastbyte = byte
            if  checksum > 0xFFFF: # CARRY
		checksum = checksum & 0xFFFF
		checksum += 1
        f.seek( ( (slot+1) * 0x800) - 4 )
	f.write( pack('H', checksum) )

        print "Checksum for save slot " + str(slot+1) + ": " + hex(checksum)

print"Done!"

"""
Disassembly by me:

01CC5F     85 4E         STA $4E          ; Save slot index
01CC61     0A            ASL a            ; Multiply by 2
01CC62     65 4E         ADC $4E          ; Multiply by 3
01CC64     20 B4 87      JSR $87B4        ; TAX through $43
01CC67     BF 86 CC 01   LDA $01CC86.l,x  ; High byte of pointer to save slot
01CC6B     85 4E         STA $4E          ; store it
01CC6D     C2 20         REP #$20         ; 16-bit A
01CC6F     BF 87 CC 01   LDA $01CC87.l,x  ; Low 2 bytes of pointer
01CC73     85 4F         STA $4F          ; store it
01CC75     A5 41         LDA $41
01CC77     A0 FA 07      LDY #$07FA       ; Size of save slot
01CC7A     18            CLC              ; Carry clear
01CC7B     67 4E         ADC [$4E]        ; Add next byte and carry
01CC7D     E6 4E         INC $4E          ; next byte
01CC7F     88            DEY              ; decrease size left
01CC80     D0 F9         BNE $CC7B        ; Loop for all bytes
01CC82     AA            TAX              ; Set checksum to X
01CC83     E2 20         SEP #$20         ; 8-bit A
01CC85     60            RTS              ; Return

"""
