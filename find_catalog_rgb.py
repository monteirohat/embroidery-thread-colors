from pyembroidery.EmbThreadPec import get_thread_set

target_catalog = "1653"  # troque para o índice encontrado no seu PES

threads = get_thread_set()

found = False

for i, thread in enumerate(threads):
    catalog = getattr(thread, "catalog_number", None)
    if str(catalog) == str(target_catalog):
        print("Match found:")
        print(f"List index     : {i}")
        print(f"Description    : {getattr(thread, 'description', None)}")
        print(f"Catalog number : {catalog}")
        print(f"Brand          : {getattr(thread, 'brand', None)}")
        print(f"Chart          : {getattr(thread, 'chart', None)}")
        print(f"RGB            : ({getattr(thread, 'red', None)}, {getattr(thread, 'green', None)}, {getattr(thread, 'blue', None)})")
        found = True
        break

if not found:
    print(f"Catalog {target_catalog} not found.")