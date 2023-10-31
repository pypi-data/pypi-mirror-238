NAME

::

   LIBOBJ - object library


DESCRIPTION

::

   LIBOBJ is a python3 library that is based around a JSON on disk
   object.

   LIBOBJ is a contribution back to society and is Public Domain.


SYNOPSIS

::

   >>> from obj.spec import *
   >>> o = Object()
   >>> o.a = "b"
   >>> write(o, "test")
   >>> oo = Object()
   >>> read(oo, "test")
   >>> oo
   {"a": "b"}  


INSTALL

::

   $ pip install libobj


AUTHOR

::

  libbot <libbotx@gmail.com>


COPYRIGHT

::

   LIBOBJ is placed in the Public Domain.
