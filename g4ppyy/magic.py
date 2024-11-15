try:
    
    from IPython.core.magic import register_cell_magic

    import os
    import hashlib

    from . import _lazy_loader as _lzl

    definitions = []

    # Define the magic command
    @register_cell_magic
    def g4_compile(filename, cell):
        """
        Magic function that saves the content of a cell to a file and calls my_function with the filename.
        Usage: %%save_and_call filename
        """
        # Extract the filename from the line argument
        cell_hash = hashlib.sha256(cell.encode('utf-8')).hexdigest()  # Using SHA-256 to generate a unique hash
        filename = f"./.g4magic.{cell_hash}.hh"  # File extension can be adjusted based on content type

        if cell_hash in definitions:
            print("Cell already loaded.")
            return 
                
        # Save the cell content to the file
        if not os.path.isfile(filename):
            with open(filename, 'w') as f:
                f.write(cell)
        
        # Call the local function with the filename
        _lzl.include(filename)

        definitions.append(cell_hash)



    from . import run as _run
    @register_cell_magic
    def g4_k3d(filename, cell):
        
        _run.create_visualization(None)
        _run.draw_visualization(None)

    print("Jupyter Magic : g4_k3d g4_compile")
except:
    pass