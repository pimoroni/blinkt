%module blinkt

%include "stdint.i"
%include "carrays.i"

%{
#include "lib/blinkt.h"
%}

%include "lib/blinkt.h"

%pythoncode %{
import atexit

def clean_exit():
    stop()

if start() > 0:
    raise ImportError("Blinkt requires root.")

atexit.register(clean_exit)
%}
