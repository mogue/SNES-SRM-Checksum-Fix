"""
	Fix hacked Secret of Evermore SRM files
	2015, by m06

	Usage: python SoE_SRM_checksum_fix.py /path/to/save_file.srm

"""

print "\n\tSecret of Evermore SRM checksum fix\n"

from struct import *
import sys

filename = ''

if len(sys.argv) > 1:
        filename = sys.argv[1]

if filename == '':
	print "!!! Please provide an SRM file to fix !!!\nUsage: python SoE_SRM_checksum_fix.py /PATH/TO/FILE.SRM\n"
	quit()

print "Fixing file: " + filename

with open(filename, "r+b") as f:
    for slot in range(4):
	f.seek(4 + (slot * 0x331))
	checksum = 0x43F
	temp = checksum + unpack('B', f.read(1))[0]
        for b in f.read(0x32E):
	    temp &= 0xFF
            checksum &= 0xFF00
	    checksum |= temp
            checksum <<= 1
            if  checksum > 0xFFFF: # Carry
                checksum -= 0xFFFF
            temp = checksum + unpack('B', b)[0]

        f.seek( 2 + (slot * 0x331) )
        f.write( pack('H', checksum) )

        print "Checksum for save slot " + str(slot+1) + ": " + hex(checksum)

print"Done!"

"""
Disassembly from John David Ratliff

  $8D/B469 A0 2F 03    LDY #$032F             ; load 0x32F into counter
  $8D/B46C 22 78 B4 8D JSL $8DB478[$8D:B478]  ; jump to subroutine
  
  $8D/B478 A9 3F 04    LDA #$043F             ; a = 0x43F
  $8D/B47B E2 20       SEP #$20               ; use 8-bit accumulator
  $8D/B47D 18          CLC                    ; clear carry
  $8D/B47E 7D 00 00    ADC $0000,x[$30:6666]  ; add data[offset]
  
  $8D/B481 88          DEY                    ; y = y - 1
  $8D/B482 F0 0B       BEQ $0B    [$B48F]     ; branch if y = 0
  $8D/B484 E8          INX                    ; x = x + 1
  $8D/B485 C2 20       REP #$20               ; use 16-bit accumulator
  $8D/B487 0A          ASL A                  ; shift left
  $8D/B488 E2 20       SEP #$20               ; use 8-bit accumulator
  $8D/B48A 7D 00 00    ADC $0000,x[$30:6667]  ; add data[offset]
  $8D/B48D 80 F2       BRA $F2    [$B481]     ; branch always
  
  $8D/B48F C2 20       REP #$20               ; use 16-bit accumulator
  $8D/B491 6B          RTL                    ; return from subroutine

"""

