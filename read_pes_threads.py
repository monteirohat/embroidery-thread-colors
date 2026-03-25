from pyembroidery import EmbPattern

pes_file = r"drawing.pes"

pattern = EmbPattern(pes_file)

print("Threads found in PES:")
print("-" * 50)

for i, thread in enumerate(pattern.threadlist):
    print(f"Thread order: {i}")
    print(f"Description   : {getattr(thread, 'description', None)}")
    print(f"Catalog number: {getattr(thread, 'catalog_number', None)}")
    print(f"Brand         : {getattr(thread, 'brand', None)}")
    print(f"Chart         : {getattr(thread, 'chart', None)}")
    print(f"RGB           : ({getattr(thread, 'red', None)}, {getattr(thread, 'green', None)}, {getattr(thread, 'blue', None)})")
    print("-" * 50)