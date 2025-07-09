# echo_memory.py - Memory Core for Toneform Storage and Retrieval with Lineage Handlers

class EchoMemory:
    def __init__(self):
        self.memory = {}

    def store_toneform(self, lineage, toneform):
        if lineage not in self.memory:
            self.memory[lineage] = []
        self.memory[lineage].append(toneform)

    def retrieve_toneforms(self, lineage):
        if lineage in self.memory:
            return self.memory[lineage]
        else:
            return None

# Example Usage:
# memory_core = EchoMemory()
# memory_core.store_toneform("Ancient", "Echo of Wisdom")
# memory_core.store_toneform("Ancient", "Echo of Power")
# memory_core.store_toneform("Ethereal", "Echo of Serenity")
# print(memory_core.retrieve_toneforms("Ancient"))
