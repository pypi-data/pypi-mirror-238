
from IPython.core.magic import register_cell_magic
import tempfile
import os
import sys

# Ensuring pystributed is in the path
sys.path.append('./')  # Update this path

from pystributed.main import main

@register_cell_magic
def save_for_remote(line, cell):
    # Save the cell content to a temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
        temp_file_name = temp_file.name
        temp_file.write(cell)

    # Use pystributed's main function to run the code on the remote server
    os.rename(temp_file_name, "./temp_script.py")
    main(file_path="temp_script.py")
    


    # Clean up the temporary file
    #os.remove("/tmp/temp_script.py")
