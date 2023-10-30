from setuptools import Extension

import warnings
from typing import Optional


class ZigExtension(Extension):
    def __init__(
        self,
        name: str,
        sources: list[str],
        include_dirs: Optional[list[str]]=None,
        define_macros: Optional[list[tuple[str, str|None]]]=None,
        undef_macros: Optional[list[str]]=None,
        library_dirs: Optional[list[str]]=None,
        libraries: Optional[list[str]]=None,
        runtime_library_dirs: Optional[list[str]]=None,
        extra_objects: Optional[list[str]]=None,
        extra_c_compile_args: Optional[list[str]]=None,
        extra_zig_compile_args: Optional[list[str]]=None,
        extra_link_args: Optional[list[str]]=None,
        export_symbols: Optional[list[str]]=None,
        swig_opts: Optional[list[str]]=None,
        depends: Optional[list[str]]=None,
        language: Optional[str]=None,
        optional: Optional[bool]=None,
        py_limited_api: Optional[bool]=None,
        **kw  # To catch unknown keywords. Not used.
    ) -> None:

        # self.sources and self.extra_compile_args are named for compatibility with the original
        # Extension API. Naming these 'self.c_sources' and 'self.extra_c_compile_args' may break things.

        if not isinstance(name, str):
            raise AssertionError("'name' must be a string")
        if not (isinstance(sources, list) and all(isinstance(v, str) for v in sources)):
            raise AssertionError("'sources' must be a list of strings")

        self.sources = []
        self.zig_sources = []
        for s in sources:
            if s.endswith(".zig"):
                self.zig_sources += s
            else:
                self.sources += s
        
        self.name = name
        self.include_dirs = include_dirs or []
        self.define_macros = define_macros or []
        self.undef_macros = undef_macros or []
        self.library_dirs = library_dirs or []
        self.libraries = libraries or []
        self.runtime_library_dirs = runtime_library_dirs or []
        self.extra_objects = extra_objects or []
        self.extra_compile_args = extra_c_compile_args or []
        self.extra_zig_compile_args = extra_zig_compile_args or []
        self.extra_link_args = extra_link_args or []
        self.export_symbols = export_symbols or []
        self.swig_opts = swig_opts or []
        self.depends = depends or []
        self.language = language
        self.optional = optional
        self.py_limited_api = py_limited_api or False

        if len(kw) > 0:
            options = [repr(option) for option in kw]
            options = ', '.join(sorted(options))
            msg = "Unknown Extension options: %s" % options
            warnings.warn(msg)

        def __repr__(self):
            return '<{}.{}({!r}) at {:#x}>'.format(
                self.__class__.__module__,
                self.__class__.__qualname__,
                self.name,
                id(self),
            )

