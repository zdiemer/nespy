"""This module defines the behavior of the NES Central Processing Unit, an
   offshoot of the Ricoh 2A03. It is fully implemented in this class."""

from ctypes import c_uint8
import constants as const
import memory as mem

def create_cpu():
    """Returns a new instance of a CPU for use outside of this module."""
    return CPU()

class CPU(object):
    """This class defines the Ricoh 2A03."""

    def __init__(self):
        self.name = const.CPU_NAME
        self.memory = mem.initialize_memory(const.TYPE_CPU)

        ### Registers ###

        # Program Counter
        self.pc = 0x0000

        # Stack Pointer -- offset from the stack
        self.sp = 0x00fd

        # Accumulator
        self.a = 0x0000

        # Index Register x
        self.x = 0x0000

        # Index Register Y
        self.y = 0x0000

        # Processor Status
        self.p = 0b00110100

        # Opcodes
        self.opcodes = {
            0x69: self.adc, 0x65: self.adc, 0x75: self.adc,
            0x6d: self.adc, 0x7d: self.adc, 0x79: self.adc,
            0x61: self.adc, 0x71: self.adc, 0x29: self._and,
            0x25: self._and, 0x35: self._and, 0x2d: self._and,
            0x3d: self._and, 0x39: self._and, 0x21: self._and,
            0x31: self._and, 0x0a: self.asl, 0x06: self.asl,
            0x16: self.asl, 0x0e: self.asl, 0x1e: self.asl,
            0x90: self.bcc, 0xb0: self.bcs, 0xf0: self.beq,
            0x24: self.bit, 0x2c: self.bit, 0x30: self.bmi,
            0xd0: self.bne, 0x10: self.bpl, 0x00: self.brk,
            0x50: self.bvc, 0x70: self.bvs, 0x18: self.clc,
            0xd8: self.cld, 0x58: self.cli, 0xb8: self.clv,
            0xc9: self._cmp, 0xc5: self._cmp, 0xd5: self._cmp,
            0xcd: self._cmp, 0xdd: self._cmp, 0xd9: self._cmp,
            0xc1: self._cmp, 0xd1: self._cmp, 0xe0: self.cpx,
            0xe4: self.cpx, 0xec: self.cpx, 0xc0: self.cpy,
            0xc4: self.cpy, 0xcc: self.cpy, 0xc6: self.dec,
            0xd6: self.dec, 0xce: self.dec, 0xde: self.dec,
            0xca: self.dex, 0x88: self.dey, 0x49: self.eor,
            0x45: self.eor, 0x55: self.eor, 0x4d: self.eor,
            0x5d: self.eor, 0x59: self.eor, 0x41: self.eor,
            0x51: self.eor, 0xe6: self.inc, 0xf6: self.inc,
            0xee: self.inc, 0xfe: self.inc, 0xe8: self.inx,
            0xc8: self.iny, 0x4c: self.jmp, 0x6c: self.jmp,
            0x20: self.jsr, 0xa9: self.lda, 0xa5: self.lda,
            0xb5: self.lda, 0xad: self.lda, 0xbd: self.lda,
            0xb9: self.lda, 0xa1: self.lda, 0xb1: self.lda,
            0xa2: self.ldx, 0xa6: self.ldx, 0xb6: self.ldx,
            0xae: self.ldx, 0xbe: self.ldx, 0xa0: self.ldy,
            0xa4: self.ldy, 0xb4: self.ldy, 0xac: self.ldy,
            0xbc: self.ldy, 0x4a: self.lsr, 0x46: self.lsr,
            0x56: self.lsr, 0x4e: self.lsr, 0x5e: self.lsr,
            0xea: self.nop, 0x09: self.ora, 0x05: self.ora,
            0x15: self.ora, 0x0d: self.ora, 0x1d: self.ora,
            0x19: self.ora, 0x01: self.ora, 0x11: self.ora,
            0x48: self.pha, 0x08: self.php, 0x68: self.pla,
            0x28: self.plp, 0x2a: self.rol, 0x26: self.rol,
            0x36: self.rol, 0x2e: self.rol, 0x3e: self.rol,
            0x6a: self.ror, 0x66: self.ror, 0x76: self.ror,
            0x6e: self.ror, 0x7e: self.ror, 0x40: self.rti,
            0x60: self.rts, 0xe9: self.sbc, 0xe5: self.sbc,
            0xf5: self.sbc, 0xed: self.sbc, 0xfd: self.sbc,
            0xf9: self.sbc, 0xe1: self.sbc, 0xf1: self.sbc,
            0x38: self.sec, 0xf8: self.sed, 0x78: self.sei,
            0x85: self.sta, 0x95: self.sta, 0x8d: self.sta,
            0x9d: self.sta, 0x99: self.sta, 0x81: self.sta,
            0x91: self.sta, 0x86: self.stx, 0x96: self.stx,
            0x8e: self.stx, 0x84: self.sty, 0x94: self.sty,
            0x8c: self.sty, 0xaa: self.tax, 0xa8: self.tay,
            0xba: self.tsx, 0x8a: self.txa, 0x9a: self.txs,
            0x98: self.tya
        }

    def initialize_cpu(self):
        """Initialize CPU and begin execution"""

        self.pc = self.memory.read(0xfffc) << 8 | self.memory.read(0xfffd)

    def set_z(self, value):
        """Sets the zero flag if appropriate"""

        # set the zero register if value is zero
        self.p &= ~(const.FLAG_ZERO)
        self.p |= const.FLAG_ZERO if value == 0b0 else 0b0

    def set_n(self, value):
        """Sets the negative flag if appropriate"""

        # set the negative register if greater than 0x80
        self.p &= ~(const.FLAG_NEGATIVE)
        self.p |= const.FLAG_NEGATIVE if value >= 0x80 else 0b0

    def set_zn(self, value):
        """Shortcut to set both zero and negative flags--happens frequently"""
        self.set_z(value)
        self.set_n(value)

    def inc_sp(self):
        """Increment stack pointer"""

        # not intuitive to *DECREMENT* here, but stack is in reverse order.
        # additionally, no such thing as stack overflow. only loops.
        self.sp = c_uint8(self.sp - 1).value

    def dec_sp(self):
        """Decrement stack pointer"""

        # similar to above
        self.sp = c_uint8(self.sp + 1).value

    def push_stack(self, data):
        """Push a byte to the stack"""

        self.memory.write(0x0100 + self.sp, data)
        self.dec_sp()

    def push_pc(self):
        """Push PC to the stack"""

        self.push_stack((self.pc & 0b1111111100000000) >> 8)
        self.push_stack(self.pc & 0b11111111)

    def adc(self, arg):
        """Add with Carry"""

        # add A register + argument + carry bit
        result = self.a + arg + (self.p & 0b1)
        uint_result = c_uint8(result).value

        # set carry bit if the result is greater than 255
        self.p &= ~(const.FLAG_CARRY)
        self.p |= result > 0xff

        # set the overflow register if the sign has flipped
        sign_flipped = ~(self.a ^ arg) & (self.a ^ result) & 0x80 == 0x80
        self.p |= const.FLAG_OVERFLOW if sign_flipped else 0b0

        # set zero and/or negative flags
        self.set_zn(uint_result)

        # save the result to the A register, as a uint8
        self.a = uint_result

    def _and(self, arg):
        """Logical AND"""

        # logical AND between A register and argument
        result = self.a & arg

        # set zero and/or negative flags
        self.set_zn(result)

        # save the result to the A register
        self.a = result

    def asl(self, arg):
        """Arithmetic Shift Left"""

        # bit shift the argument left
        result = arg << 1

        # set the carry bit to the value of bit 7
        self.p &= ~(const.FLAG_CARRY)
        self.p |= 0b10000000 & arg > 0

        # set zero and/or negative flags
        self.set_zn(result)

        #save the result to the A register
        self.a = result

    def bcc(self, arg):
        """Branch if Carry Clear"""

        self.pc += arg if not self.p & const.FLAG_CARRY else 0

    def bcs(self, arg):
        """Branch if Carry Set"""

        self.pc += arg if self.p & const.FLAG_CARRY else 0

    def beq(self, arg):
        """Branch if Equal"""

        self.pc += arg if self.p & const.FLAG_ZERO else 0

    def bit(self, arg):
        """Bit Test"""

        # perform a logical AND between A & M
        result = self.a & arg
        self.set_z(result)

        # set bits 6 and 7 in the status register to bits 6 and 7 of memory
        self.p &= 0b11111100
        self.p |= (arg & 0b11)

    def bmi(self, arg):
        """Branch if Minus"""

        self.pc += arg if self.p & const.FLAG_NEGATIVE else 0

    def bne(self, arg):
        """Branch if Not Equal"""

        self.pc += arg if not self.p & const.FLAG_ZERO else 0

    def bpl(self, arg):
        """Branch if Positive"""

        self.pc += arg if not self.p & const.FLAG_NEGATIVE else 0

    def brk(self):
        """Break"""

        # write PC and status to the stack
        self.memory.write(self.sp, (self.pc & 0b1111111100000000) >> 8)
        self.inc_sp()

        self.memory.write(self.sp, self.pc & 0b11111111)
        self.inc_sp()

        self.memory.write(self.sp, self.p)
        self.inc_sp()

    def bvc(self, arg):
        """Branch if Overflow Clear"""

        self.pc += arg if not self.p & const.FLAG_OVERFLOW else 0

    def bvs(self, arg):
        """Branch if Overflow Set"""

        self.pc += arg if self.p & const.FLAG_OVERFLOW else 0

    def clc(self):
        """Clear Carry Flag"""
        self.p &= ~(const.FLAG_CARRY)

    def cld(self):
        """Clear Decimal Mode"""
        self.p &= ~(const.FLAG_DECIMAL)

    def cli(self):
        """Clear Interrupt Disable"""
        self.p &= ~(const.FLAG_INTERRUPT)

    def clv(self):
        """Clear Overflow Flag"""
        self.p &= ~(const.FLAG_OVERFLOW)

    def _cmp(self, arg):
        """Compare"""

        # do in place subtraction, not saving the result
        result = self.a - arg
        uint_result = c_uint8(result)

        # set carry flag if A >= arg
        self.p &= ~(const.FLAG_CARRY)
        self.p |= result > 0

        # set zero flag if A = M
        self.p &= ~(const.FLAG_ZERO)
        self.p |= const.FLAG_ZERO if not result else 0b0

        # set negative flag if result is negative
        self.p &= ~(const.FLAG_NEGATIVE)
        self.p |= const.FLAG_NEGATIVE if uint_result >= 0x80 else 0b0

    def cpx(self, arg):
        """Compare X Register"""

        # do in place subtraction, not saving the result
        result = self.x - arg
        uint_result = c_uint8(result)

        # set carry flag if X >= arg
        self.p &= ~(const.FLAG_CARRY)
        self.p |= result > 0

        # set zero flag if X = M
        self.p &= ~(const.FLAG_ZERO)
        self.p |= const.FLAG_ZERO if not result else 0b0

        # set negative flag if result is negative
        self.p &= ~(const.FLAG_NEGATIVE)
        self.p |= const.FLAG_NEGATIVE if uint_result >= 0x80 else 0b0

    def cpy(self, arg):
        """Compare Y Register"""

        # do in place subtraction, not saving the result
        result = self.y - arg
        uint_result = c_uint8(result)

        # set carry flag if Y >= arg
        self.p &= ~(const.FLAG_CARRY)
        self.p |= result > 0

        # set zero flag if Y = M
        self.p &= ~(const.FLAG_ZERO)
        self.p |= const.FLAG_ZERO if not result else 0b0

        # set negative flag if result is negative
        self.p &= ~(const.FLAG_NEGATIVE)
        self.p |= const.FLAG_NEGATIVE if uint_result >= 0x80 else 0b0

    def dec(self, arg):
        """Decrement Memory"""

        # TODO: Write the DEC operation
        print arg

    def dex(self):
        """Decrement X Register"""

        result = self.x - 1
        uint_result = c_uint8(result)

        self.set_zn(uint_result)
        self.x = uint_result

    def dey(self):
        """Decrement X Register"""

        result = self.x - 1
        uint_result = c_uint8(result)

        self.set_zn(uint_result)
        self.x = uint_result

    def eor(self, arg):
        """Exclusive OR"""

        result = self.a ^ arg
        self.set_zn(result)
        self.a = result

    def inc(self, arg):
        """Increment Memory"""

        # TODO: Implement INC operation
        print arg

    def inx(self):
        """Increment X Register"""

        result = self.x + 1
        uint_result = c_uint8(result)

        self.set_zn(uint_result)
        self.x = uint_result

    def iny(self):
        """Increment Y Register"""

        result = self.y + 1
        uint_result = c_uint8(result)

        self.set_zn(uint_result)
        self.y = uint_result

    def jmp(self, arg):
        """Jump"""

        # TODO: push current PC onto the stack (?)
        # assign PC to equal arg
        self.pc = arg

    def jsr(self, arg):
        """Jump to Subroutine"""

        # TODO: implement JSR operation
        print arg

    def lda(self, arg):
        """Load Accumulator"""

        self.a = arg
        self.set_zn(self.a)

    def ldx(self, arg):
        """Load X Register"""

        self.x = arg
        self.set_zn(self.x)

    def ldy(self, arg):
        """Load Y Register"""

        self.y = arg
        self.set_zn(self.y)

    def lsr(self, arg):
        """Logical Shift Right"""

        # bit shift right
        result = arg >> 1

        # set the carry bit to the previous value of bit 0
        self.p &= ~(const.FLAG_CARRY)
        self.p |= 0b1 & arg > 0

        # set zero and/or negative flags
        self.set_zn(result)

        #save the result to the A register
        self.a = result

    def nop(self):
        """No Operation"""

        # do nothing!
        return

    def ora(self, arg):
        """Logical Inclusive OR"""

        result = self.a | arg
        self.set_zn(result)
        self.a = result

    def pha(self):
        """Push Accumulator"""

        self.memory.write(self.sp, self.a)
        self.inc_sp()

    def php(self):
        """Push Processor Status"""

        self.memory.write(self.sp, self.p)
        self.inc_sp()

    def pla(self):
        """Pull Accumulator"""

        self.a = self.memory.read(self.sp)
        self.dec_sp()

    def plp(self):
        """Pull Processor Status"""

        self.p = self.memory.read(self.sp)
        self.dec_sp()

    def rol(self, arg):
        """Rotate Left"""

        self.asl(arg)

    def ror(self, arg):
        """Rotate Right"""

        self.lsr(arg)

    def rti(self):
        """Return from Interrupt"""

        self.p = self.memory.read(self.sp)
        self.dec_sp()

        # TODO: PC is 16 bits, this needs to be re-written, or write function modified?
        self.pc = self.memory.read(self.sp)
        self.dec_sp()

    def rts(self):
        """Return from Subroutine"""

        # TODO: PC is 16 bits, this needs to be re-written, or write function modified?
        self.pc = self.memory.read(self.sp) - 1
        self.dec_sp()

    def sbc(self, arg):
        """Subtract with Carry"""

        # pass the inverse to ADC... easy peasy!
        self.adc(~arg)

    def sec(self):
        """Set Carry Flag"""

        self.p |= const.FLAG_CARRY

    def sed(self):
        """Set Decimal Flag"""

        self.p |= const.FLAG_DECIMAL

    def sei(self):
        """Set Interrupt Disable"""

        self.p |= const.FLAG_INTERRUPT

    def sta(self, arg):
        """Store Accumulator"""

        self.memory.write(arg, self.a)

    def stx(self, arg):
        """Store X Register"""

        self.memory.write(arg, self.x)

    def sty(self, arg):
        """Store Y Register"""

        self.memory.write(arg, self.y)

    def tax(self):
        """Transfer Accumulator to X"""

        self.x = self.a
        self.set_zn(self.x)

    def tay(self):
        """Transfer Accumulator to Y"""

        self.y = self.a
        self.set_zn(self.y)

    def tsx(self):
        """Transfer Stack Pointer to X"""

        self.x = self.sp
        self.set_zn(self.x)

    def txa(self):
        """Transfer X to Accumulator"""

        self.a = self.x
        self.set_zn(self.a)

    def txs(self):
        """Transfer X to Stack Pointer"""

        self.sp = self.x

    def tya(self):
        """Transfer Y to Accumulator"""

        self.a = self.y
        self.set_zn(self.a)

if __name__ == "__main__":
    CPU = create_cpu()
