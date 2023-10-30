from setuptools.extension import Library
from setuptools.command.build_ext import build_ext

import os

class BuildZigExt(build_ext):
    def build_extension(self, ext):
        build_lib = self.get_finalized_command('build_py').build_lib
        self.compiler.mkpath(build_lib)
        build_ext.build_extension(self, ext)

    def run(self):
        from setuptools_ziglang.zigcompiler import ZigCompiler

        if not self.extensions:
            return
        
        if self.distribution.has_c_libraries():
            build_clib = self.get_finalized_command('build_clib')
            self.libraries.extend(build_clib.get_library_names() or [])
            self.library_dirs.append(build_clib.build_clib)

        self.compiler = ZigCompiler()
        self.compiler.set_default_flags()

        if self.include_dirs is not None:
            self.compiler.set_include_dirs(self.include_dirs)
        if self.define is not None:
            for name, value in self.define:
                self.compiler.define_macro(name, value)
        if self.undef is not None:
            for macro in self.undef:
                self.compiler.undefine_macro(macro)
        if self.libraries is not None:
            self.compiler.set_libraries(self.libraries)
        if self.library_dirs is not None:
            self.compiler.set_library_dirs(self.library_dirs)
        if self.rpath is not None:
            self.compiler.set_runtime_library_dirs(self.rpath)
        if self.link_objects is not None:
            self.compiler.set_link_objects(self.link_objects)

        self.build_extensions()


