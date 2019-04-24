#![feature(proc_macro, specialization)]

extern crate pyo3;

use pyo3::prelude::*;
use pyo3::wrap_pyfunction;

#[pyfunction]
fn composite_simpsons(f: &Fn(f64) -> f64, a: f64, b:f64, n: u64) -> PyResult<f64> {
    let step_size = (b - a) / n as f64;
    let mut x_k;
    let mut x_k1;
    let mut integral = 0.0;
    for i in 0..n {
        let k = &(i as f64);
        x_k = a + k * step_size;
        x_k1 = a + (k + 1.) * step_size;

        let simpson = step_size / 6. * (f(x_k) + 4. * f((x_k + x_k1) / 2. ) + f(x_k1));
        integral += simpson;
    }
    integral
}

/// This module is a python module implemented in Rust.
#[pymodule]
fn rusty_integration(py: Python, m: &PyModule) -> PyResult<()> {
    m.add_wrapped(wrap_pyfunction!(composite_simpsons))?;

    Ok(())
}