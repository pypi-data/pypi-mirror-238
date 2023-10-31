#include "dominx/flow.h"

static int
dmxPy_Flow_traverse(dmxPy_FlowObject *self, visitproc visit, void *arg)
{
    Py_VISIT(self->hook);
    return 0;
}

static int
dmxPy_Flow_clear(dmxPy_FlowObject *self)
{
    Py_CLEAR(self->hook);
    return 0;
}

static void
dmxPy_Flow_dealloc(dmxPy_FlowObject *self)
{
    PyObject_GC_UnTrack(self);
    dmxPy_Flow_clear(self);
    Py_TYPE(self)->tp_free((PyObject *)self);
}

static PyObject *
dmxPy_Flow_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    dmxPy_FlowObject *self;
    self = (dmxPy_FlowObject *)type->tp_alloc(type, 0);

    return (PyObject *)self;
}

static int
dmxPy_Flow_init(dmxPy_FlowObject *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"hook", NULL};
    PyObject *hook = NULL;
    PyObject *tmp;

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "O:Flow.__init__", kwlist, &hook))
        return -1;

    if (!PyCallable_Check(hook)) {
        char *msg;
        stringf(&msg, "'%s' object is not callable", Py_TYPE(hook)->tp_name);

        PyErr_SetString(PyExc_TypeError, msg);
        return -1;
    }

    tmp = self->hook;
    Py_INCREF(hook);
    self->hook = hook;
    Py_XDECREF(tmp);

    return 0;
}

static PyObject *
dmxPy_Flow_call(dmxPy_FlowObject *self, PyObject *args, PyObject *kwds)
{
    return PyObject_Call((PyObject *)self->hook, args, kwds);
}

static PyObject *
dmxPy_Flow_gethook(dmxPy_FlowObject *self, void *closure)
{
    Py_INCREF(self->hook);
    return self->hook;
}

static int
dmxPy_Flow_sethook(dmxPy_FlowObject *self, PyObject *value, void *closure)
{
    if (value == NULL) {
        char *msg;
        stringf(&msg, "'%s' object has no attribute 'hook'", Py_TYPE(self)->tp_name);

        PyErr_SetString(PyExc_AttributeError, msg);
        return -1;
    }
    if (!PyCallable_Check(value)) {
        char *msg;
        stringf(&msg, "'%s' object is not callable", Py_TYPE(value)->tp_name);

        PyErr_SetString(PyExc_TypeError, msg);
        return -1;
    }

    PyObject *tmp = self->hook;
    Py_INCREF(value);
    self->hook = value;
    Py_DECREF(tmp);

    return 0;
}

PyMODINIT_FUNC
PyInit_flow(void)
{
    PyObject *m;

    if (PyType_Ready(&dmxPy_FlowType) < 0)
        return NULL;

    m = PyModule_Create(&dmxPy_module_flow);
    if (m == NULL)
        return NULL;

    Py_INCREF(&dmxPy_FlowType);
    if (PyModule_AddObject(m, "Flow", (PyObject *)&dmxPy_FlowType) < 0) {
        Py_DECREF(&dmxPy_FlowType);
        Py_DECREF(m);
        return NULL;
    }

    return m;
}
