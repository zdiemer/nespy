import cpu as CPU
import unittest


class CpuTest(unittest.TestCase):

    def test_cpu_init(self):

        # get a CPU
        cpu = CPU.create_cpu()

        # check program counter
        self.assertEqual(cpu.pc, 0x0000)

        # check the stack pointer
        self.assertEqual(cpu.sp, 0x00ff)

        # check the acc
        self.assertEqual(cpu.a, 0x0000)

        # check reg x
        self.assertEqual(cpu.x, 0x0000)

        # check reg y
        self.assertEqual(cpu.y, 0x0000)

        # check the processor status
        self.assertEqual(cpu.p, 0b00110100)

        
if __name__ == 'main':
    unittest.main()
