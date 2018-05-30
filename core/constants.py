"""Defines constants used throughout the application"""

# CPU Name
CPU_NAME = "Ricoh 2A03"

# Memory Types
TYPE_CPU = "cpu"
TYPE_PPU = "ppu"

# CPU Memory Sections
ZERO_PAGE = "Zero Page"
STACK = "Stack"
RAM = "RAM"
MIRRORS_0X0000_0X07FF = "Mirrors 0x0000 - 0x07ff"
IO_REGISTERS = "I/O Registers"
MIRRORS_0X2000_0X2007 = "Mirrors 0x2000 - 0x2007"
REMAINING_IO_REGISTERS = "Remaining I/O Registers"
EXPANSION_ROM = "Expansion ROM"
SRAM = "SRAM"
PRGROM_LOW = "PRG-ROM Lower Bank"
PRGROM_UP = "PRG-ROM Upper Bank"

# Addressing Modes
ADDR_IMPLICIT = "Implicit"
ADDR_ACCUMULATOR = "Accumulator"
ADDR_IMMEDIATE = "Immediate"
ADDR_ZERO_PAGE = "Zero Page Addressing"
ADDR_ZERO_PAGE_X = "Zero Page X"
ADDR_ZERO_PAGE_Y = "Zero Page Y"
ADDR_RELATIVE = "Relative"
ADDR_ABSOLUTE = "Absolute"
ADDR_ABSOLUTE_X = "Absolute X"
ADDR_ABSOLUTE_Y = "Absolute Y"
ADDR_INDIRECT = "Indirect"
ADDR_INDEXED_INDIRECT = "Indexed Indirect"
ADDR_INDIRECT_INDEXED = "Indirect Indexed"

# Flags
FLAG_NEGATIVE = 0b10000000
FLAG_OVERFLOW = 0b01000000
FLAG_BREAK = 0b00010000
FLAG_DECIMAL = 0b00001000
FLAG_INTERRUPT = 0b00000100
FLAG_ZERO = 0b00000010
FLAG_CARRY = 0b00000001

# Exception Strings
EXCEPTION_MEMORY_LESS_ZERO = "The requested memory location is less than zero."
EXCEPTION_MEMORY_EXCEEDS_MAX = "The requested memory location is greater than the maximum memory size."
