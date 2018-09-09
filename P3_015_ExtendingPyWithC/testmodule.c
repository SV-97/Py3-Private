#include <Python.h>

int Cfib(int n)
{
    if (n < 2)
        return n;
    else
        return Cfib(n-1)+Cfib(n-2);    
}

static PyObject* fib(PyObject* self, PyObject* args)
{
    int n;
    if (!PyArg_ParseTuple(args, "i", &n))
        return NULL;
    return Py_BuildValue("i", Cfib(n));
}

static PyObject* version(PyObject* self)
{
    return Py_BuildValue("s", "Version 1.0");
}

static PyMethodDef testmodmethods[] = {
    {"fib", fib, METH_VARARGS, "Calculate fibonacci number"},
    {"version", version, METH_NOARGS, "Return Version"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef testModule = {
    PyModuleDef_HEAD_INIT,
    "testmodule",
    "Test Module documentation",
    -1,
    testmodmethods
};

PyMODINIT_FUNC PyInit_testmodule(void)
{
    return PyModule_Create(&testModule);
}