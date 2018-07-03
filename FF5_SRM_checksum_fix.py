"""
	Fix hacked FFV SRM files
	2017, by m06

	Usage: python FF5_SRM_checksum_fix.py /path/to/save_file.srm
"""

print "\n\tFinal Fantasy V SRM checksum fix\n"

import array
from struct import *
import sys

filename = ''

if len(sys.argv) > 1:
        filename = sys.argv[1]

if filename == '':
	print "!!! Please provide an SRM file to fix !!!\nUsage: python FF5_SRM_checksum_fix.py /PATH/TO/FILE.SRM\n"
	quit()

print "Fixing file: " + filename

with open(filename, "r+b") as f:
    for slot in range(4):
	f.seek( slot * 0x700 )
	checksum = 0
	data = array.array("H")
        data.fromfile(f, 0x300)
        for word in data:
            checksum += word
            if  checksum > 0xFFFF: # CARRY
		checksum = checksum & 0xFFFF
		checksum += 1
        f.seek( 0x1FF0 + (slot * 2) )
	f.write( pack('H', checksum) )

        print "Checksum for save slot " + str(slot+1) + ": " + hex(checksum)

print"Done!"

"""
Disassembly from MottZilla

$C2/F561 A5 F6       LDA $F6    [$00:01F6]   
$C2/F563 29 03 00    AND #$0003              
$C2/F566 0A          ASL A                   
$C2/F567 AA          TAX                     
$C2/F568 BD F8 7F    LDA $7FF8,x[$30:7FF8]   ; Check Slot In-Use Table
$C2/F56B C9 1B E4    CMP #$E41B              
$C2/F56E D0 0D       BNE $0D    [$F57D]      ; If not $E41B Skip
$C2/F570 20 88 F5    JSR $F588  [$C2:F588]   ; $F588 Returns Checksum
$C2/F573 DD F0 7F    CMP $7FF0,x[$30:7FF0]   ; Compare against Csum
$C2/F576 D0 0A       BNE $0A    [$F582]      ; table.
$C2/F578 A9 00 00    LDA #$0000              ; $0000 File Valid
$C2/F57B 80 08       BRA $08    [$F585]      
$C2/F57D A9 00 80    LDA #$8000              ; File not in Use
$C2/F580 80 03       BRA $03    [$F585]      
$C2/F582 A9 00 40    LDA #$4000              ; Bad Checksum
$C2/F585 85 E0       STA $E0    [$00:01E0]   
$C2/F587 60          RTS                     

$C2/F588 8B          PHB                     
$C2/F589 DA          PHX                     
$C2/F58A 5A          PHY                     
$C2/F58B 08          PHP                     
$C2/F58C F4 30 30    PEA $3030               
$C2/F58F AB          PLB                     
$C2/F590 AB          PLB                     
$C2/F591 C2 20       REP #$20                
$C2/F593 A6 FC       LDX $FC    [$00:01FC]   
$C2/F595 A0 00 06    LDY #$0600              ; Save File Size
$C2/F598 A5 8E       LDA $8E    [$00:018E]   
$C2/F59A 18          CLC                     
$C2/F59B 7D 00 00    ADC $0000,x[$30:0000]   
$C2/F59E E8          INX                     
$C2/F59F E8          INX                     
$C2/F5A0 88          DEY                     
$C2/F5A1 88          DEY                     
$C2/F5A2 D0 F7       BNE $F7    [$F59B]      
$C2/F5A4 28          PLP                     
$C2/F5A5 7A          PLY                     
$C2/F5A6 FA          PLX                     
$C2/F5A7 AB          PLB                     
$C2/F5A8 60          RTS   

"""
