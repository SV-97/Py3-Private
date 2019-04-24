extern crate pyo3;
extern crate num;

use pyo3::prelude::*;
use pyo3::wrap_pyfunction;
use pyo3::ObjectProtocol;
use pyo3::types::PyTuple;

macro_rules! call1 {
    ( $f:ident, $py:ident, $( $arg:expr ),* ) => {
        $f.call1($py, PyTuple::new($py, &[$( $arg, )*]))
    }
}

#[pyfunction]
fn external_call(obj: PyObject) -> PyResult<()> {
    let gil = Python::acquire_gil();
    let py = gil.python();
    obj.call0(py);
    Ok(())
}

#[pyfunction]
fn ext_call_ret(obj: PyObject) -> PyResult<PyObject> {
    let gil = Python::acquire_gil();
    let py = gil.python();
    match obj.call0(py) {
        Ok(val) => Ok(val),
        Err(e) => Err(e)
    }
}

#[pyfunction]
fn ext_call_arg(obj: PyObject, s: String) -> PyResult<()> {
    let gil = Python::acquire_gil();
    let py = gil.python();
    obj.call1(py, PyTuple::new(py, &[s]));
    Ok(())
}

#[pyfunction]
fn ext_add(a: isize, b: isize) -> PyResult<isize> {
    Ok(a + b)
}

#[pyfunction]
fn composite_simpsons(f: PyObject, a: f64, b:f64, n: u64) -> PyResult<f64> {
    let gil = Python::acquire_gil();
    let py = gil.python();

    let step_size = (b - a) / n as f64;
    let mut x_k;
    let mut x_k1;
    let mut integral = 0.0;
    for i in 0..n {
        let k = &(i as f64);
        x_k = a + k * step_size;
        x_k1 = a + (k + 1.) * step_size;
        let f_1 = call1!(f, py, x_k.clone());
        let f_2 = call1!(f, py, (x_k + x_k1) / 2. );
        let f_3 = call1!(f, py, x_k1);
        let (f_1, f_2, f_3): (f64, f64, f64) = match (f_1, f_2, f_3) {
            (Err(e), _, _)|
            (_, Err(e), _)|
            (_, _, Err(e)) => return Err(e),
            (Ok(f_1), Ok(f_2), Ok(f_3)) => (f_1.extract(py)?, f_2.extract(py)?, f_3.extract(py)?) 
        };
        let simpson = step_size / 6. * (f_1 + 4. * f_2 + f_3);
        integral += simpson;
    }
    Ok(integral)
}

#[pyfunction]
/// Alternative implementation where the gil is acquired and dropped each iteration
fn alternative_composite_simpsons(f: PyObject, a: f64, b:f64, n: u64) -> PyResult<f64> {
    let step_size = (b - a) / n as f64;
    let mut x_k;
    let mut x_k1;
    let mut integral = 0.0;
    for i in 0..n {
        let k = &(i as f64);
        x_k = a + k * step_size;
        x_k1 = a + (k + 1.) * step_size;
        let gil = Python::acquire_gil();
        let py = gil.python();
        let f_1 = call1!(f, py, x_k.clone());
        let f_2 = call1!(f, py, (x_k + x_k1) / 2. );
        let f_3 = call1!(f, py, x_k1);
        let (f_1, f_2, f_3): (f64, f64, f64) = match (f_1, f_2, f_3) {
            (Err(e), _, _)|
            (_, Err(e), _)|
            (_, _, Err(e)) => return Err(e),
            (Ok(f_1), Ok(f_2), Ok(f_3)) => (f_1.extract(py)?, f_2.extract(py)?, f_3.extract(py)?) 
        };
        let simpson = step_size / 6. * (f_1 + 4. * f_2 + f_3);
        integral += simpson;
    }
    Ok(integral)
}

#[pymodule]
fn rusty_integration(py: Python, m: &PyModule) -> PyResult<()> {
    m.add_wrapped(wrap_pyfunction!(external_call))?;
    m.add_wrapped(wrap_pyfunction!(ext_call_ret))?;
    m.add_wrapped(wrap_pyfunction!(ext_call_arg))?;
    m.add_wrapped(wrap_pyfunction!(ext_add))?;
    m.add_wrapped(wrap_pyfunction!(composite_simpsons))?;
    m.add_wrapped(wrap_pyfunction!(alternative_composite_simpsons))?;

    Ok(())
}