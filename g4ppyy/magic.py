"""
G4PPYY.magic : Registers Geant4 Specific Jupyter Magic
=============

Python based helper tools to register Jupyter magic if ran inside
a Jupyter cell.

Author: Patrick Stowell
Date: 2024-12-06
License: MIT
"""

try:

    # Main Jupyter Load Check    
    from IPython.core.magic import register_cell_magic

    # System Imports
    import os
    import hashlib

    # G4PPYY Imports
    from . import _lazy_loader as _lzl
    from . import run as _run
    from . macros import macro

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

    # Define the magic command
    @register_cell_magic
    def g4_macro(filename, cell):
        """
        Magic function that saves the content of a cell to a file and calls my_function with the filename.
        Usage: %%save_and_call filename
        """
        macro(cell)

    # print("Jupyter Magic : g4_k3d g4_compile")

except:

    pass