"""
	Fix hacked Harvest Moon SRM files
	2023, by m06

	Usage: python HarvestMoon_SRM_checksum_fix.py /path/to/save_file.srm
"""

print "\n\tHarvest Moon SRM checksum fix\n"

import array
from struct import *
import sys

filename = ''

if len(sys.argv) > 1:
        filename = sys.argv[1]

if filename == '':
	print "!!! Please provide an SRM file to fix !!!\nUsage: python HarvestMoon_SRM_checksum_fix.py /PATH/TO/FILE.SRM\n"
	quit()

print "Fixing file: " + filename

with open(filename, "r+b") as f:
    for slot in range(2):
        f.seek( 0x2F + (slot * 0x1000) )
        f.write( pack('H', 0x0000 ) ) # clear old checksum

        f.seek( 0x0 + (slot * 0x1000) )
        checksum = 0
        data = array.array("H")
        data.fromfile(f, 0x800) # 0x1000 bytes as words
        for word in data:
            checksum += word
            checksum &= 0xFFFF

        f.seek( 0x2F + (slot * 0x1000) )
        f.write( pack('H', checksum ) )

        print "Checksum for save slot " + str(slot+1) + ": " + hex(checksum)

print"Done!"

"""
Disassembly by denim: http://www.romhacking.net/forum/index.php?topic=18307.0

0You have two save games in harvest moon. The first uses the 16bit checksum of the first $1000 bytes, i.e., 4096 bytes. The result is stored in the word at offset $002f for the first save and $102f for the second save. The second save uses the checksum of words from $1001-$2000. Important to say that the checksum word can't be added to the result. The game stores a zero in it before evaluate the checksum.

$83/BB28 A0 2F 00    LDY #$002F              A:0000 X:057C Y:002E D:0000 DB:00 S:1EFD P:envmxdIZC HC:0144 VC:255 FC:55 I:00
$83/BB2B B7 72       LDA [$72],y[$70:002F]   A:0000 X:057C Y:002F D:0000 DB:00 S:1EFD P:envmxdIzC HC:0192 VC:255 FC:55 I:00  ;the checksum
$83/BB2D 85 7E       STA $7E    [$00:007E]   A:5D9B X:057C Y:002F D:0000 DB:00 S:1EFD P:envmxdIzC HC:0250 VC:255 FC:55 I:00
$83/BB2F A9 00 00    LDA #$0000              A:5D9B X:057C Y:002F D:0000 DB:00 S:1EFD P:envmxdIzC HC:0284 VC:255 FC:55 I:00
$83/BB32 97 72       STA [$72],y[$70:002F]   A:0000 X:057C Y:002F D:0000 DB:00 S:1EFD P:envmxdIZC HC:0332 VC:255 FC:55 I:00 ;store 0000 in the checksum offset
$83/BB34 A0 00 00    LDY #$0000              A:0000 X:057C Y:002F D:0000 DB:00 S:1EFD P:envmxdIZC HC:0390 VC:255 FC:55 I:00
$83/BB37 64 80       STZ $80    [$00:0080]   A:0000 X:057C Y:0000 D:0000 DB:00 S:1EFD P:envmxdIZC HC:0414 VC:255 FC:55 I:00
$83/BB39 B7 72       LDA [$72],y[$70:0000]   A:0000 X:057C Y:0000 D:0000 DB:00 S:1EFD P:envmxdIZC HC:0472 VC:255 FC:55 I:00 ;start to sum all words from save block
$83/BB3B 18          CLC                     A:0200 X:057C Y:0000 D:0000 DB:00 S:1EFD P:envmxdIzC HC:0530 VC:255 FC:55 I:00
$83/BB3C 65 80       ADC $80    [$00:0080]   A:0200 X:057C Y:0000 D:0000 DB:00 S:1EFD P:envmxdIzc HC:0588 VC:255 FC:55 I:00
$83/BB3E 85 80       STA $80    [$00:0080]   A:0200 X:057C Y:0000 D:0000 DB:00 S:1EFD P:envmxdIzc HC:0622 VC:255 FC:55 I:00
$83/BB40 C8          INY                     A:0200 X:057C Y:0000 D:0000 DB:00 S:1EFD P:envmxdIzc HC:0656 VC:255 FC:55 I:00
$83/BB41 C8          INY                     A:0200 X:057C Y:0001 D:0000 DB:00 S:1EFD P:envmxdIzc HC:0674 VC:255 FC:55 I:00
$83/BB42 C0 00 10    CPY #$1000              A:0200 X:057C Y:0002 D:0000 DB:00 S:1EFD P:envmxdIzc HC:0692 VC:255 FC:55 I:00 ;$1000 bytes loop
$83/BB45 D0 F2       BNE $F2    [$BB39]      A:0200 X:057C Y:0002 D:0000 DB:00 S:1EFD P:eNvmxdIzc HC:0716 VC:255 FC:55 I:00
$83/BB47 C2 30       REP #$30                A:5D9B X:057C Y:1000 D:0000 DB:00 S:1EFD P:enVmxdIZC HC:0182 VC:121 FC:57 I:00 ;here we have the final result
$83/BB49 A5 7E       LDA $7E    [$00:007E]   A:5D9B X:057C Y:1000 D:0000 DB:00 S:1EFD P:enVmxdIZC HC:0206 VC:121 FC:57 I:00
$83/BB4B C5 80       CMP $80    [$00:0080]   A:5D9B X:057C Y:1000 D:0000 DB:00 S:1EFD P:enVmxdIzC HC:0240 VC:121 FC:57 I:00 ;compares with the value stores
$83/BB4D D0 12       BNE $12    [$BB61]      A:5D9B X:057C Y:1000 D:0000 DB:00 S:1EFD P:enVmxdIZC HC:0274 VC:121 FC:57 I:00 ;reset block if checksum is wrong
"""
