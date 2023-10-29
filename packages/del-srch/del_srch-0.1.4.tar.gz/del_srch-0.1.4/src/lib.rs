use numpy::{PyReadonlyArray1, PyReadonlyArray2, PyArray1, PyArray2, PyArray3, IntoPyArray};
use pyo3::prelude::*;
use pyo3::{pymodule, pyfunction, pyclass, types::PyModule, PyResult, Python, wrap_pyfunction};
use del_misc;

fn squared_dist(p0: &[f32], p1: &[f32]) -> f32 {
    (p0[0] - p1[0]) * (p0[0] - p1[0])
        + (p0[1] - p1[1]) * (p0[1] - p1[1])
        + (p0[2] - p1[2]) * (p0[2] - p1[2])
}

#[pyfunction]
fn first_intersection_ray_meshtri3<'a>(
    py: Python<'a>,
    src: PyReadonlyArray1<'a, f32>,
    dir: PyReadonlyArray1<'a, f32>,
    vtx2xyz: PyReadonlyArray2<'a, f32>,
    tri2vtx: PyReadonlyArray2<'a, usize>) -> (&'a PyArray1<f32>, i64)
{
    use crate::del_misc::srch_bruteforce;
    let res = srch_bruteforce::intersection_meshtri3(
        src.as_slice().unwrap(),
        dir.as_slice().unwrap(),
        vtx2xyz.as_slice().unwrap(),
        tri2vtx.as_slice().unwrap());
    match res {
        None => {
            let a = PyArray1::<f32>::zeros(py, 3, true);
            return (a, -1);
        }
        Some(postri) => {
            let a = PyArray1::<f32>::from_slice(py, &postri.0);
            return (a, postri.1 as i64);
        }
    }
}

#[pyfunction]
fn pick_vertex_meshtri3<'a>(
    src: PyReadonlyArray1<'a, f32>,
    dir: PyReadonlyArray1<'a, f32>,
    vtx2xyz: PyReadonlyArray2<'a, f32>,
    tri2vtx: PyReadonlyArray2<'a, usize>) -> i64
{
    use crate::del_misc::srch_bruteforce;
    let res = srch_bruteforce::intersection_meshtri3(
        src.as_slice().unwrap(),
        dir.as_slice().unwrap(),
        vtx2xyz.as_slice().unwrap(),
        tri2vtx.as_slice().unwrap());
    match res {
        None => {
            return -1;
        }
        Some(postri) => {
            let pos = postri.0;
            let idx_tri = postri.1;
            let i0 = tri2vtx.get([idx_tri, 0]).unwrap();
            let i1 = tri2vtx.get([idx_tri, 1]).unwrap();
            let i2 = tri2vtx.get([idx_tri, 2]).unwrap();
            let q0 = &vtx2xyz.as_slice().unwrap()[i0 * 3..i0 * 3 + 3];
            let q1 = &vtx2xyz.as_slice().unwrap()[i1 * 3..i1 * 3 + 3];
            let q2 = &vtx2xyz.as_slice().unwrap()[i2 * 3..i2 * 3 + 3];
            let d0 = squared_dist(&pos, q0);
            let d1 = squared_dist(&pos, q1);
            let d2 = squared_dist(&pos, q2);
            if d0 <= d1 && d0 <= d2 { return *i0 as i64; }
            if d1 <= d2 && d1 <= d0 { return *i1 as i64; }
            if d2 <= d0 && d2 <= d1 { return *i2 as i64; }
            return -1;
        }
    }
}


#[pyclass]
struct MyClass {
    tree: del_geo::kdtree2::KdTree2<f32>,
}

#[pymethods]
impl MyClass {
    #[new]
    fn new<'a>(vtx2xy: PyReadonlyArray2<'a, f32>) -> Self {
        let slice = vtx2xy.as_slice().unwrap();
        let points_ = nalgebra::Matrix2xX::<f32>::from_column_slice(slice);
        let tree = del_geo::kdtree2::KdTree2::from_matrix(&points_);
        vtx2xy.as_slice().unwrap();
        MyClass {
            tree: tree
        }
    }

    fn edges<'a>(&self, py: Python<'a>) -> &'a PyArray3<f32> {
        let e = self.tree.edges();
        numpy::ndarray::Array3::<f32>::from_shape_vec(
            (e.len() /4, 2, 2), e).unwrap().into_pyarray(py)
    }
}


/// A Python module implemented in Rust.
#[pymodule]
fn del_srch(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(first_intersection_ray_meshtri3, m)?)?;
    m.add_function(wrap_pyfunction!(pick_vertex_meshtri3, m)?)?;
    m.add_class::<MyClass>()?;
    Ok(())
}