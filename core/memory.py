"""This module is a reusable module for the memory structures of both the
   CPU and the PPU. Each use a similar layout."""

import constants as const

def initialize_memory(mem_type):
    """Initializes memory based on the type of struct required"""
    mem = Memory(mem_type)

    if mem_type == const.TYPE_CPU:
        ranges = [
            {
                "start": 0x0000,
                "end": 0x00ff,
                "title": const.ZERO_PAGE
            }, {
                "start": 0x0100,
                "end": 0x01ff,
                "title": const.STACK
            }, {
                "start": 0x0200,
                "end": 0x07ff,
                "title": const.RAM
            }, {
                # This section mirrors everything from 0x0000 to 0x07ff,
                # just add "0x0800" to the value to get its mirrored location.
                "start": 0x0800,
                "end": 0x1fff,
                "title": const.MIRRORS_0X0000_0X07FF
            }, {
                "start": 0x2000,
                "end": 0x2007,
                "title": const.IO_REGISTERS
            }, {
                # For this section of mirrors, 0x2000 - 0x2007 is repeated every
                # 8 bytes, then the remaining I/O registers follow afterwards.
                "start": 0x2008,
                "end": 0x3fff,
                "title": const.MIRRORS_0X2000_0X2007
            }, {
                "start": 0x4000,
                "end": 0x401f,
                "title": const.REMAINING_IO_REGISTERS
            }, {
                "start": 0x4020,
                "end": 0x5fff,
                "title": const.EXPANSION_ROM
            }, {
                "start": 0x6000,
                "end": 0x7fff,
                "title": const.SRAM
            }, {
                "start": 0x8000,
                "end": 0xbfff,
                "title": const.PRGROM_LOW
            }, {
                "start": 0xc000,
                "end": 0xffff,
                "title": const.PRGROM_UP
            }
        ]

        mem.define_ranges(ranges)
    else:
        return ""

    return mem

class Memory(object):
    """This class defines a memory bank to be used by either the CPU or PPU."""

    def __init__(self, mem_type):
        # Size in kibibytes
        self.size = 65536
        self.mem_bank = [0x00] * self.size
        self.ranges = []
        self.mem_type = mem_type

    def define_ranges(self, ranges):
        """Defines how to segment memory"""
        self.ranges = ranges

    def write(self, loc, data):
        """Writes to a memory location given location and data"""
        if self.mem_type == const.TYPE_CPU:
            # Check if in mirrored ranges
            if loc in range(0x0000, 0x0800):
                cp_loc = loc + 0x0800

                # copy RAM data to 3 mirrors
                while cp_loc < 0x2000:
                    self.mem_bank[cp_loc] = data
                    cp_loc += 0x0800
            elif loc in range(0x2000, 0x2008):
                cp_loc = loc + 0x0008

                # copy IO Registers every 8 bytes
                while cp_loc < 0x4000:
                    self.mem_bank[cp_loc] = data
                    cp_loc += 0x0008

        self.mem_bank[loc] = data

    def read(self, loc):
        """Reads from a range of memory"""
        if loc >= self.size:
            # TODO: Throw an error here
            return
        elif loc < 0:
            # TODO: Throw an error here
            return

        return self.mem_bank[loc]

    def delete(self, loc):
        """Zeroes out a specified memory location"""
        if loc >= self.size:
            # TODO: Throw an error here
            return
        elif loc < 0:
            # TODO: Throw an error here
            return

        self.ranges[loc] = 0x00
