# Sets up basic memory regions for the NES

#@menupath File.Run.NESLoad
#@toolbar NES.jpeg
#@category ghidra-nes

from ghidra.program.model.address.Address import *

addrFactory = currentProgram.getAddressFactory()

INTERNAL_RAM = addrFactory.getAddress(0)

print "NES Load Testing!"
NES_MEM = {
    "Internal Ram":[0,0x7FF],
    "RAM Mirror 1":[0x800,0xFFF],
    "RAM Mirror 2":[0x1000,0x17FF],
    "RAM Mirror 3":[0x1800,0x1FFF],
    "PPU": [0x2000,0x3FFF],
    "APU-IO":[0x4000,0x401F],
}
for region in NES_MEM:
    print "Creating Region: {}".format(region)
    createMemoryBlock(region,NES_MEM[region][0],None,NES_MEM[region][1] - NES_MEM[region][0],False)
