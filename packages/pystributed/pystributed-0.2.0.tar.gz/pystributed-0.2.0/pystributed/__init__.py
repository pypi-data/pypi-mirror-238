
# Check if we're in an IPython or Jupyter environment
try:
    __IPYTHON__
    from .save_for_remote_magic import save_for_remote
except NameError:
    pass  # Not in IPython or Jupyter environment
