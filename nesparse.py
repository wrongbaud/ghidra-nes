import os
import struct
import logging
import sys

logging.basicConfig(level=logging.INFO)

prg_bank_size = 0x2000

class PRGArea:
    def __init__(self,data):
        self.data = data

class CHRArea:
    def __init__(self,data):
        self.data = data

def get_byte(val):
    return struct.unpack('b',val)[0]

def get_short(val):
    return struct.unpack('H',val)[0]

class NESRom:

    def __init__(self,data,header=None):
        if header:
            self.header = True
            self.ines = data.read(16)
            self.data = data.read()
        else:
            self.ines = header
        self.chr_pages = []
        self.prg_pages = []


    def parse_ines(self):
        self.prg_rom_size = get_byte(self.ines[4]) * 0x4000
        self.prg_rom_banks = self.prg_rom_size/0x2000
        self.chr_rom_size = get_byte(self.ines[5]) * 8  * 1024
        self.mapper = get_short(self.ines[6:8])
        self.prg_ram = get_byte(self.ines[8])
        self.tv_system = get_byte(self.ines[9])
        self.tv_system_prg_ram = get_byte(self.ines[10])
        self.mapper_number = (get_byte(self.ines[6]) >> 4 ) | (get_byte(self.ines[7]) & 0xF0 )

    def print_mapper(self):
        logging.info("Mapper Information")
        logging.info("PRG ROM Size: {:X} bytes".format(self.prg_rom_size))
        logging.info("Total 8k PRG Rom Banks: {:X}".format(self.prg_rom_banks))
        logging.info("CHR ROM Size: {:X} bytes".format(self.chr_rom_size))
        logging.info("Mapper Code: {:X}".format(self.mapper))
        logging.info("PRG RAM: {:X}".format(self.prg_ram))
        logging.info("Mapper Number: {:X}".format(self.mapper_number))
        logging.info("Reset Vector: {:X}".format(self.reset_addr))
        logging.info("NMI Vector: {:X}".format(self.nmi_addr))
        logging.info("IRQ Vector: {:X}".format(self.irq_addr))
    
    def get_chr_area(self):
        self.chr_area = self.data[self.prg_rom_size:self.chr_rom_size + self.prg_rom_size]

    def get_prg_area(self):
        self.prg_area = self.data[0:self.prg_rom_size]

    def get_interrupt_vectors(self):
        self.reset_addr = get_short(self.prg_area[0x200A:0x200C]) 
        self.nmi_addr = get_short(self.prg_area[0x200C:0x200E])
        self.irq_addr = get_short(self.prg_area[0x200E:0x2010]) 

    '''
    #Export the CHR file to a PNG to be viewed
    def print_chr(self):

    # Find the pallete in use?
    def get_pallete(self):

    # Update the pallete in use
    def update_pallete(self):
    '''

if __name__ == "__main__":
    romfile = open(sys.argv[1],'rb')
    rom = NESRom(romfile,True)
    rom.parse_ines()
    rom.get_prg_area()
    rom.get_chr_area()
    rom.get_interrupt_vectors()
    rom.print_mapper()

