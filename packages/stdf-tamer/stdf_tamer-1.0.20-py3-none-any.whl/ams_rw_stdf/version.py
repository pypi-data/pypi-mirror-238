try:
    from importlib.metadata import version
except:
    from importlib_metadata import version


version = version("stdf-tamer")
