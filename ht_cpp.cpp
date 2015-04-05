#include <vector>
#include <limits>

extern "C" {
#include <Python.h>
}

namespace ht_cpp {	
	typedef std::vector<double>  row_t;
	typedef std::vector<row_t>   matrix_t;

	static matrix_t dot(const matrix_t &a)
	{
		const double infinity = std::numeric_limits<double>::infinity();
		matrix_t result = a;
		for (size_t k=0; k<a.size(); k++) {
			for (size_t i=0; i<a.size(); i++) {
				for (size_t j=0; j<a.size(); j++) {
					double temp1 = result[i][j];
					double temp2 = result[i][k] + result[k][j];
					if (temp1*temp2 == 0)
					{
						result[i][j] = 0;
					}
					else
					{
						if ((1/temp1 + 1/temp2)==0)
						{
							result[i][j] = infinity;
						}
						else
							result[i][j] = 1/(1/temp1 + 1/temp2);
					}
				}
			}
		}
		return result;
	}
}

static ht_cpp::matrix_t pyobject_to_cxx(PyObject * py_matrix)
{
	ht_cpp::matrix_t result;
	result.resize(PyObject_Length(py_matrix));
	for (size_t i=0; i<result.size(); ++i) {
		PyObject * py_row = PyList_GetItem(py_matrix, i);
		ht_cpp::row_t & row = result[i];
		row.resize(PyObject_Length(py_row));
		for (size_t j=0; j<row.size(); ++j) {
			PyObject * py_elem = PyList_GetItem(py_row, j);
			const double elem = PyFloat_AsDouble(py_elem);
			row[j] = elem;
		}
	}
	return result;
}

static PyObject * cxx_to_pyobject(const ht_cpp::matrix_t &matrix)
{
	PyObject * result = PyList_New(matrix.size());
	for (size_t i=0; i<matrix.size(); ++i) {
		const ht_cpp::row_t & row = matrix[i];
		PyObject * py_row = PyList_New(row.size());
		PyList_SetItem(result, i, py_row);
		for (size_t j=0; j<row.size(); ++j) {
			const double elem = row[j];
			PyObject * py_elem = PyFloat_FromDouble(elem);
			PyList_SetItem(py_row, j, py_elem);
		}
	}
	return result;
}

static PyObject * matrixops_faster_dot(PyObject * module, PyObject * args)
{
	PyObject * py_a = PyTuple_GetItem(args, 0);

	/* Convert to C++ structure */
	const ht_cpp::matrix_t a = pyobject_to_cxx(py_a);

	/* Perform calculations */
	const ht_cpp::matrix_t result = ht_cpp::dot(a);

	/* Convert back to Python object */
	PyObject * py_result = cxx_to_pyobject(result);
	return py_result;
}

PyMODINIT_FUNC PyInit_matrixops()
{
	static PyMethodDef ModuleMethods[] = {
		{ "faster_dot", matrixops_faster_dot, METH_VARARGS, "Fater matrix production" },
		{ NULL, NULL, 0, NULL }
	};
	static PyModuleDef ModuleDef = {
		PyModuleDef_HEAD_INIT,
		"ht_cpp",
		"Matrix operations",
		-1, ModuleMethods, 
		NULL, NULL, NULL, NULL
	};
	PyObject * module = PyModule_Create(&ModuleDef);
	return module;
}
