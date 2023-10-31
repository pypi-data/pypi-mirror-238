#include "dominx/stream.h"

static int
dmxPy_Stream_traverse(dmxPy_StreamObject *self, visitproc visit, void *arg)
{
    return 0;
}

static int
dmxPy_Stream_clear(dmxPy_StreamObject *self)
{
    return 0;
}

static void
dmxPy_Stream_dealloc(dmxPy_StreamObject *self)
{
    PyObject_GC_UnTrack(self);
    dmxPy_Stream_clear(self);
    Py_TYPE(self)->tp_free((PyObject *)self);
}

static PyObject *
dmxPy_Stream_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    dmxPy_StreamObject *self;
    self = (dmxPy_StreamObject *)type->tp_alloc(type, 0);

    return (PyObject *)self;
}

static int
dmxPy_Stream_init(dmxPy_StreamObject *self, PyObject *args, PyObject *kwds)
{
    return 0;
}

PyMODINIT_FUNC
PyInit_stream(void)
{
    PyObject *m;

    if (PyType_Ready(&dmxPy_StreamType) < 0)
        return NULL;

    m = PyModule_Create(&dmxPy_module_stream);
    if (m == NULL)
        return NULL;

    Py_INCREF(&dmxPy_StreamType);
    if (PyModule_AddObject(m, "Stream", (PyObject *)&dmxPy_StreamType) < 0) {
        Py_DECREF(&dmxPy_StreamType);
        Py_DECREF(m);
        return NULL;
    }

    return m;
}
