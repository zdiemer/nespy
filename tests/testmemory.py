import memory as mem
import constants
import unittest


class MemoryTest(unittest.TestCase):

    def test_mem_init(self):

        memory = mem.initialize_memory(constants.TYPE_CPU)

        self.assertEqual(memory.read(0x0000), 0)


if __name__ == "__main__":
    unittest.main()