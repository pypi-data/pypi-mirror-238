#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <stdio.h>
#include <linux/uinput.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>

int _close_fd(int fd) {
    if (ioctl(fd, UI_DEV_DESTROY) < 0) {
        close(fd);
        return -1;
    }

    return close(fd);
}

static PyObject* open_device(PyObject *self, PyObject *args) {
    const char* dev_node;

    int ret = PyArg_ParseTuple(args, "s", &dev_node);
    if (!ret) {
        return NULL;
    }

    int fd = open(dev_node, O_RDWR | O_NONBLOCK);
    if (fd < 0) {
        PyErr_SetString(PyExc_IOError, "Error opening uinput device in write mode");
        return NULL;
    }

    return Py_BuildValue("i", fd);
}

static PyObject* close_device(PyObject *self, PyObject *args) {
    int fd;

    int ret = PyArg_ParseTuple(args, "i", &fd);
    if (!ret) {
        PyErr_SetString(PyExc_Exception, "Invalid arguments");
        return NULL;
    }

    if (_close_fd(fd) < 0) {
        PyErr_SetString(PyExc_Exception, "Error destroying uinput device");
        return NULL;
    }

    Py_RETURN_NONE;
}

static PyObject* setup_device(PyObject *self, PyObject *args) {
    int fd;
    uint16_t vendor_id, product_id, version_id;
    const char* name;

    int ret = PyArg_ParseTuple(args, "ishhi", &fd, &name, &vendor_id, &product_id, &version_id);
    if (!ret) {
        PyErr_SetString(PyExc_Exception, "Invalid arguments");
        return NULL;
    }

    struct uinput_setup u_setup;

    memset(&u_setup, 0, sizeof(u_setup));
    snprintf(u_setup.name, UINPUT_MAX_NAME_SIZE, "%s", name);
    u_setup.id.bustype = BUS_USB;
    u_setup.id.vendor = vendor_id;
    u_setup.id.product = product_id;
    u_setup.id.version = version_id;
    u_setup.ff_effects_max = 0;

    if (ioctl(fd, UI_DEV_SETUP, &u_setup) < 0) {
        _close_fd(fd);
        PyErr_SetString(PyExc_IOError, "Error setting up uinput device");
        return NULL;
    }

    if (ioctl(fd, UI_DEV_CREATE) < 0) {
        _close_fd(fd);
        PyErr_SetString(PyExc_IOError, "Error creating up uinput device");
        return NULL;
    }

    Py_RETURN_NONE;
}

static PyObject* enable_events(PyObject *self, PyObject *args) {
    int fd;
    uint16_t type, code;
    unsigned long req;

    int ret = PyArg_ParseTuple(args, "ihh", &fd, &type, &code);
    if (!ret) {
        PyErr_SetString(PyExc_Exception, "Invalid arguments");
        return NULL;
    }

    switch (type) {
        case EV_KEY:
            req = UI_SET_KEYBIT;
            break;
        case EV_LED:
            req = UI_SET_LEDBIT;
            break;
        default:
            PyErr_SetString(PyExc_Exception, "Invalid event type");
            return NULL;
    }

    if (ioctl(fd, UI_SET_EVBIT, type) < 0) {
        _close_fd(fd);
        PyErr_SetString(PyExc_IOError, "Error enabling events for uinput device");
        return NULL;
    }

    if (ioctl(fd, req, code) < 0) {
        _close_fd(fd);
        PyErr_SetString(PyExc_IOError, "Error enabling events for uinput device");
        return NULL;
    }

    Py_RETURN_NONE;
}

static PyObject* write_event(PyObject *self, PyObject *args) {
    int fd, type, code, value;
    if (!PyArg_ParseTuple(args, "iiii", &fd, &type, &code, &value)) {
        PyErr_SetString(PyExc_Exception, "Invalid arguments");
        return NULL;
    }

    struct input_event ie;
    memset(&ie, 0, sizeof(ie));

    struct timeval teval;
    gettimeofday(&teval, 0);

    ie.time.tv_usec = teval.tv_usec;
    ie.time.tv_sec = teval.tv_sec;
    ie.type = type;
    ie.code = code;
    ie.value = value;

    if(write(fd, &ie, sizeof(ie)) != sizeof(ie)) {
        PyErr_SetString(PyExc_IOError, "Error sending key event");
        return NULL;
    }

    Py_RETURN_NONE;
}

static PyMethodDef UInputMethods[] = {
    {"open_device", (PyCFunction) open_device, METH_VARARGS, "Open uinput device"},
    {"close_device", (PyCFunction) close_device, METH_VARARGS, "Destroy uinput device"},
    {"setup_device", (PyCFunction) setup_device, METH_VARARGS, "Setup uinput device"},
    {"enable_events", (PyCFunction) enable_events, METH_VARARGS, "Enable events for uinput device"},
    {"write_event", (PyCFunction) write_event, METH_VARARGS, "Write event to uinput device"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef _uinput = {
    PyModuleDef_HEAD_INIT,
    "_uinput",
    "Python minimal keyboard bindings for uinput",
    -1,
    UInputMethods
};

PyMODINIT_FUNC PyInit__uinput(void) {
    return PyModule_Create(&_uinput);
}
