#include "dominx/display.h"

PyMODINIT_FUNC
PyInit_display(void)
{
    PyObject *m = PyModule_Create(&dmxPy_module_display);
    return m;
}
