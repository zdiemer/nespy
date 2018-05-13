import memory as mem
import sys
from exceptions.memoryexceptions import MemoryLocationError
import constants
import unittest


class MemoryTest(unittest.TestCase):

    def test_mem_init(self):

        memory = mem.initialize_memory(constants.TYPE_CPU)

        self.assertEqual(memory.read(0x0000), 0)

    def test_write_memory(self):

        memory = mem.initialize_memory(constants.TYPE_CPU)

        self.assertEqual(memory.read(0x0000), 0)

        memory.write(0x0000, 1)

        self.assertEqual(memory.read(0x0000), 1)

        memory.write(0x0000, 0)

        self.assertEqual(memory.read(0x0000), 0)

    def test_mem_read_out_of_bounds(self):

        memory = mem.initialize_memory(constants.TYPE_CPU)

        with self.assertRaises(MemoryLocationError):
            memory.read(-1)

        with self.assertRaises(MemoryLocationError):
            memory.read(memory.size + 1)


if __name__ == "__main__":
    unittest.main()