#include <Python.h>
#include <iostream>
#include <numpy/arrayobject.h>
#include <numpy/ndarrayobject.h>
#include <numpy/npy_common.h>

#include "HessianSegmentation.h"
#include "KrigingSegmentation.h"
#include "MRFSegmentation.h"
#include "NewCACSegmentation.h"
#include "NonLocalMeans.h"
#include "RegionGrowthSegmentation.h"

typedef unsigned jobIdType;

static char module_docstring[] = "TBA";
static char kriging_docstring[] = "TBA";
static char cac_docstring[] = "TBA";
static char mrf_docstring[] = "TBA";
static char rgs_docstring[] = "TBA";
static char hessian_docstring[] = "TBA";
static char windowedHessian_docstring[] = "TBA";
static char nlm_docstring[] = "TBA";
static char unsharp_docstring[] = "TBA";

static PyObject *kriging(PyObject *self, PyObject *args, PyObject *keywds) {
  import_array();

  PyObject *input_data_py;
  const int labels_count = 2;
  DataDescription data_descr;
  KrigingSettings krig_settings;
  krig_settings.nLlabels = labels_count;

  // npy_intp da[] = {3, 2};
  // PyObject *a = PyArray_SimpleNew(2, da, NPY_INT32);

  static char *kwlist[] = {"input", "settings", "thresholds", NULL};
  if (!PyArg_ParseTupleAndKeywords(
          args, keywds, "O(CCCi)(ii)", kwlist, &input_data_py,
          &krig_settings.VarMethod, &krig_settings.CorMethod,
          &krig_settings.OutFormat, &krig_settings.Radius,
          &krig_settings.Theshold.LowThreshold,
          &krig_settings.Theshold.HighThreshold))
    return NULL;
  // printf("%d %c %c %c, %d %d\n", krig_settings.Radius,
  // krig_settings.VarMethod, krig_settings.CorMethod,
  // krig_settings.OutFormat,krig_settings.Theshold.LowThreshold,
  // krig_settings.Theshold.HighThreshold);

  krig_settings.Theshold.ManualThresholding = true;
  krig_settings.Theshold.ThresholdMethod = ThreshodMethods::Th_Manual;

  int len = PyArray_SIZE(input_data_py);
  int dimData = PyArray_NDIM(input_data_py);
  npy_intp *dim_array = PyArray_DIMS(input_data_py);
  if (dimData >= 1)
    data_descr.W = dim_array[0];
  if (dimData >= 2)
    data_descr.H = dim_array[1];
  if (dimData >= 3)
    data_descr.D = dim_array[2];
  input_data_py = PyArray_ContiguousFromAny(input_data_py, NPY_INT32, 0, 0);

  int *PyArrayData = (int *)PyArray_DATA(input_data_py);
  std::vector<int> input_data(PyArrayData, PyArrayData + len);
  // PyThreadState *_save;
  // _save = PyEval_SaveThread();
  KrigingProcessor<int, std::vector<int>> freddy_kriger(labels_count);
  std::vector<int> output_data;
  output_data.resize(len);
  freddy_kriger.krig_driver('k', input_data, output_data, data_descr,
                            krig_settings, krig_settings.Theshold);
  PyObject *array = PyArray_SimpleNew(dimData, dim_array, NPY_INT32);
  memcpy(PyArray_DATA(array), output_data.data(), len * sizeof(int));
  // PyEval_RestoreThread(_save);
  return array;
}

static PyObject *cac(PyObject *self, PyObject *args, PyObject *keywds) {
  import_array();

  // npy_intp da[] = {3, 2};
  // PyObject *a = PyArray_SimpleNew(2, da, NPY_INT32);

  PyObject *input_data_py;
  DataDescription data_descr;
  CACSettings cac_settings;
  ThresholdSettings thr_settings;

  static char *kwlist[] = {"input", "settings", "thresholds", NULL};

  if (!PyArg_ParseTupleAndKeywords(
          args, keywds, "O(ddd)(ii)", kwlist, &input_data_py,
          &cac_settings.AlphaG, &cac_settings.AlphaI, &cac_settings.G0,
          //&cac_settings.UnsharpMaskStrength,
          //&cac_settings.nlm_iterations,
          //&cac_settings.nlm_search_radius,
          &thr_settings.LowThreshold, &thr_settings.HighThreshold))
    return NULL;

  thr_settings.ManualThresholding = true;
  thr_settings.ThresholdMethod = ThreshodMethods::Th_Manual;

  int len = PyArray_SIZE(input_data_py);

  int dimData = PyArray_NDIM(input_data_py);
  const npy_intp *dim_array = PyArray_DIMS(input_data_py);
  if (dimData >= 1)
    data_descr.W = dim_array[0];
  if (dimData >= 2)
    data_descr.H = dim_array[1];
  if (dimData >= 3)
    data_descr.D = dim_array[2];

  input_data_py = PyArray_ContiguousFromAny(input_data_py, NPY_INT32, 0, 0);

  int *PyArrayData = (int *)PyArray_DATA(input_data_py);
  std::vector<int> input_data(PyArrayData, PyArrayData + len);

  PyThreadState *_save;
  _save = PyEval_SaveThread();
  Threshold<int, std::vector<int>> thresholder;
  thresholder.Setup(thr_settings);

  std::vector<int> output_data;
  output_data.resize(len);

  NewCACSegmentation cac_segmenter;
  cac_segmenter.Perform(input_data, output_data, thresholder, cac_settings,
                        data_descr.W, data_descr.H, data_descr.D);

  PyObject *array = nullptr;
  array = PyArray_SimpleNew(dimData, dim_array, NPY_INT32);
  memcpy(PyArray_DATA(array), output_data.data(), len * sizeof(int));
  PyEval_RestoreThread(_save);
  return array;
}

static PyObject *mrf(PyObject *self, PyObject *args, PyObject *keywds) {
  import_array();

  PyObject *input_data_py;
  const int labels_count = 2;
  DataDescription data_descr;
  MRFSettings mrf_settings;
  ThresholdSettings thr_settings;
  mrf_settings.nLabels = labels_count;
  // npy_intp da[] = {3, 2};
  // PyObject *a = PyArray_SimpleNew(2, da, NPY_INT32);

  int method_code = 0;
  static char *kwlist[] = {"input", "settings", "thresholds", NULL};
  if (!PyArg_ParseTupleAndKeywords(
          args, keywds, "O(ddidddi)(ii)", kwlist, &input_data_py,
          &mrf_settings.Beta, &mrf_settings.FreezingSpeed, &method_code,
          &mrf_settings.TStart, &mrf_settings.Alpha,
          &mrf_settings.EnergyThreshold, &mrf_settings.MaxIterations,
          &thr_settings.LowThreshold, &thr_settings.HighThreshold))
    return NULL;

  switch (method_code) {
  case 0:
    mrf_settings.Method = MRFMethods::MRF_ModifiedMetropolis;
    break;
  case 1:
    mrf_settings.Method = MRFMethods::MRF_ICM;
    break;
  default:
    mrf_settings.Method = MRFMethods::MRF_Undefined;
    break;
  }

  thr_settings.ManualThresholding = true;
  thr_settings.ThresholdMethod = ThreshodMethods::Th_Manual;

  int len = PyArray_SIZE(input_data_py);

  int dimData = PyArray_NDIM(input_data_py);
  npy_intp *dim_array = PyArray_DIMS(input_data_py);
  if (dimData >= 1)
    data_descr.W = dim_array[0];
  if (dimData >= 2)
    data_descr.H = dim_array[1];
  if (dimData >= 3)
    data_descr.D = dim_array[2];

  input_data_py = PyArray_ContiguousFromAny(input_data_py, NPY_INT32, 0, 0);

  int *PyArrayData = (int *)PyArray_DATA(input_data_py);
  std::vector<int> input_data(PyArrayData, PyArrayData + len);

  // PyThreadState *_save;
  // _save = PyEval_SaveThread();
  Threshold<int, std::vector<int>> thresholder;
  thresholder.Setup(thr_settings);
  std::vector<int> output_data;
  output_data.resize(len);

  MRFSegmentation<int, std::vector<int>, 3> mrf_segmenter(mrf_settings);
  mrf_segmenter.Perform(input_data, output_data, thresholder, data_descr.W,
                        data_descr.H, data_descr.D);
  PyObject *array = PyArray_SimpleNew(dimData, dim_array, NPY_INT32);
  memcpy(PyArray_DATA(array), output_data.data(), len * sizeof(int));
  // PyEval_RestoreThread(_save);
  return array;
}

static PyObject *rgs(PyObject *self, PyObject *args, PyObject *keywds) {
  import_array();

  PyObject *input_data_py;
  const int labels_count = 2;
  DataDescription data_descr;
  ThresholdSettings thr_settings;

  // npy_intp da[] = {3, 2};
  // PyObject *a = PyArray_SimpleNew(2, da, NPY_INT32);

  static char *kwlist[] = {"input", "thresholds", NULL};
  if (!PyArg_ParseTupleAndKeywords(args, keywds, "O(ii)", kwlist,
                                   &input_data_py, &thr_settings.LowThreshold,
                                   &thr_settings.HighThreshold))
    return NULL;

  thr_settings.ManualThresholding = true;
  thr_settings.ThresholdMethod = ThreshodMethods::Th_Manual;

  int len = PyArray_SIZE(input_data_py);

  int dimData = PyArray_NDIM(input_data_py);
  const npy_intp *dim_array = PyArray_DIMS(input_data_py);
  if (dimData >= 1)
    data_descr.W = dim_array[0];
  if (dimData >= 2)
    data_descr.H = dim_array[1];
  if (dimData >= 3)
    data_descr.D = dim_array[2];

  input_data_py = PyArray_ContiguousFromAny(input_data_py, NPY_INT32, 0, 0);

  int *PyArrayData = (int *)PyArray_DATA(input_data_py);
  std::vector<int> input_data(PyArrayData, PyArrayData + len);

  // PyThreadState *_save;
  // _save = PyEval_SaveThread();
  Threshold<int, std::vector<int>> thresholder;
  thresholder.Setup(thr_settings);

  std::vector<int> output_data;
  output_data.resize(len);

  RegionGrowthSegmentation rgs_segmenter(labels_count);
  rgs_segmenter.Perform(input_data, output_data, thresholder, data_descr.W,
                        data_descr.H, data_descr.D, thr_settings);

  PyObject *array = nullptr;
  array = PyArray_SimpleNew(dimData, dim_array, NPY_INT32);
  memcpy(PyArray_DATA(array), output_data.data(), len * sizeof(int));
  // PyEval_RestoreThread(_save);
  return array;
}

static PyObject *hessian(PyObject *self, PyObject *args, PyObject *keywds) {
  import_array();

  // npy_intp da[] = {3, 2};
  // PyObject *a = PyArray_SimpleNew(2, da, NPY_INT32);

  PyObject *input_data_py;
  const int labels_count = 2;

  DataDescription data_descr;
  HessianSettings hess_settings;
  hess_settings.nPhases = labels_count;

  static char *kwlist[] = {"input", "settings", NULL};

  if (!PyArg_ParseTupleAndKeywords(
          args, keywds, "O(iidiipp)", kwlist, &input_data_py,
          &hess_settings.Order, &hess_settings.Threshold, &hess_settings.Gain,
          &hess_settings.Sgn, &hess_settings.nScales, &hess_settings.IsAuto,
          &hess_settings.UseScales))
    return NULL;

  hess_settings.nPhases = 2;

  int len = PyArray_SIZE(input_data_py);

  int dimData = PyArray_NDIM(input_data_py);
  const npy_intp *dim_array = PyArray_DIMS(input_data_py);
  if (dimData >= 1)
    data_descr.W = dim_array[0];
  if (dimData >= 2)
    data_descr.H = dim_array[1];
  if (dimData >= 3)
    data_descr.D = dim_array[2];

  input_data_py = PyArray_ContiguousFromAny(input_data_py, NPY_UINT8, 0, 0);

  unsigned char *PyArrayData = (unsigned char *)PyArray_DATA(input_data_py);
  DynamicArray<unsigned char> input_data(PyArrayData, PyArrayData + len);

  // PyThreadState *_save;
  // _save = PyEval_SaveThread();
  DynamicArray<unsigned char> output_data;
  output_data.resize(len);

  HessianSegmentation hessian_segmenter;
  hessian_segmenter.Perform(input_data, output_data, hess_settings,
                            data_descr.W, data_descr.H, data_descr.D);

  PyObject *array = nullptr;
  array = PyArray_SimpleNew(dimData, dim_array, NPY_UINT8);
  memcpy(PyArray_DATA(array), output_data.data(), len * sizeof(unsigned char));
  // PyEval_RestoreThread(_save);
  return array;
}

static PyObject *windowedHessian(PyObject *self, PyObject *args,
                                 PyObject *keywds) {
  import_array();

  // npy_intp da[] = {3, 2};
  // PyObject *a = PyArray_SimpleNew(2, da, NPY_INT32);

  PyObject *input_data_py;
  const int labels_count = 2;
  DataDescription data_descr;
  HessianSettings hess_settings;
  HWSSettings hws_settings;
  ThresholdSettings thr_settings;

  static char *kwlist[] = {"input", "settings", "settings2", "thresholds",
                           NULL};

  if (!PyArg_ParseTupleAndKeywords(
          args, keywds, "O(iidiipp)(diiiid)(ii)", kwlist, &input_data_py,
          &hess_settings.Order, &hess_settings.Threshold, &hess_settings.Gain,
          &hess_settings.Sgn, &hess_settings.nScales, &hess_settings.IsAuto,
          &hess_settings.UseScales,

          &hws_settings.FreezingSpeed, &hws_settings.HessianOrder,
          &hws_settings.nSteps, &hws_settings.Radius, &hws_settings.Strength,
          &hws_settings.TStart,

          &thr_settings.LowThreshold, &thr_settings.HighThreshold))
    return NULL;

  hws_settings.nLabels = 2;
  hws_settings.nPhases = 2;

  thr_settings.ManualThresholding = true;
  thr_settings.ThresholdMethod = ThreshodMethods::Th_Manual;

  int len = PyArray_SIZE(input_data_py);

  int dimData = PyArray_NDIM(input_data_py);
  const npy_intp *dim_array = PyArray_DIMS(input_data_py);
  if (dimData >= 1)
    data_descr.W = dim_array[0];
  if (dimData >= 2)
    data_descr.H = dim_array[1];
  if (dimData >= 3)
    data_descr.D = dim_array[2];

  input_data_py = PyArray_ContiguousFromAny(input_data_py, NPY_INT32, 0, 0);

  int *PyArrayData = (int *)PyArray_DATA(input_data_py);
  DynamicArray<int> input_data(PyArrayData, PyArrayData + len);

  // PyThreadState *_save;
  // _save = PyEval_SaveThread();
  HessianWindowedSegmantation<int, DynamicArray<int>, 3> wnd_hess_segmenter(
      labels_count);
  Threshold<int, DynamicArray<int>> thresholder;
  thresholder.Setup(thr_settings);

  DynamicArray<int> output_data;
  output_data.resize(len);

  DynamicArray<int> window_image;
  DynamicArray<int> hessian_image;
  wnd_hess_segmenter.Perform(input_data, output_data, window_image, thresholder,
                             hessian_image, data_descr.W, data_descr.H,
                             data_descr.D, hess_settings, hws_settings);

  PyObject *array = nullptr;
  array = PyArray_SimpleNew(dimData, dim_array, NPY_INT32);
  memcpy(PyArray_DATA(array), output_data.data(), len * sizeof(int));
  // PyEval_RestoreThread(_save);
  return array;
}

static PyObject *nlm(PyObject *self, PyObject *args, PyObject *keywds) {
  PyObject *input_data_py;
  const int labels_count = 2;

  DataDescription data_descr;
  int nlm_iters_count{0};
  int nlm_radius{0};
  bool verbose = true;

  static char *kwlist[] = {"input", "settings", NULL};

  if (!PyArg_ParseTupleAndKeywords(args, keywds, "O(ii)", kwlist,
                                   &input_data_py, &nlm_iters_count,
                                   &nlm_radius))
    return NULL;

  int len = PyArray_SIZE(input_data_py);

  int dimData = PyArray_NDIM(input_data_py);
  const npy_intp *dim_array = PyArray_DIMS(input_data_py);
  if (dimData >= 1)
    data_descr.W = dim_array[0];
  if (dimData >= 2)
    data_descr.H = dim_array[1];
  if (dimData >= 3)
    data_descr.D = dim_array[2];

  input_data_py = PyArray_ContiguousFromAny(input_data_py, NPY_INT32, 0, 0);

  int *PyArrayData = (int *)PyArray_DATA(input_data_py);
  std::vector<int> input_data(PyArrayData, PyArrayData + len);

  PyThreadState *_save;
  _save = PyEval_SaveThread();

  int shape[3] = {data_descr.W, data_descr.H, data_descr.D};

  int *denoised_data = NonLocalMeans::nlm_denoise(
      input_data.data(), shape, nlm_iters_count, nlm_radius, verbose);
  std::vector<int> denoised;
  denoised.assign(denoised_data, denoised_data + len);

  PyEval_RestoreThread(_save);

  PyObject *array = nullptr;
  array = PyArray_SimpleNew(dimData, dim_array, NPY_INT32);
  memcpy(PyArray_DATA(array), denoised.data(), len * sizeof(int));
  free(denoised_data);
  return array;
}

static PyObject *unsharp(PyObject *self, PyObject *args, PyObject *keywds) {
  PyObject *input_data_py;
  const int labels_count = 2;

  DataDescription data_descr;
  double unsharp_mask_strength{1.0};

  static char *kwlist[] = {"input", "settings", NULL};

  if (!PyArg_ParseTupleAndKeywords(args, keywds, "O(d)", kwlist, &input_data_py,
                                   &unsharp_mask_strength))
    return NULL;

  int len = PyArray_SIZE(input_data_py);

  int dimData = PyArray_NDIM(input_data_py);
  const npy_intp *dim_array = PyArray_DIMS(input_data_py);
  if (dimData >= 1)
    data_descr.W = dim_array[0];
  if (dimData >= 2)
    data_descr.H = dim_array[1];
  if (dimData >= 3)
    data_descr.D = dim_array[2];

  input_data_py = PyArray_ContiguousFromAny(input_data_py, NPY_INT32, 0, 0);

  int *PyArrayData = (int *)PyArray_DATA(input_data_py);
  std::vector<int> input_data(PyArrayData, PyArrayData + len);

  PyThreadState *_save;
  _save = PyEval_SaveThread();

  LatticeModel data_processor(2);
  std::vector<int> unsharped(len);
  data_processor.ApplyUnsharpMask(input_data, data_descr.W, data_descr.H,
                                  data_descr.D, unsharped,
                                  unsharp_mask_strength);

  PyEval_RestoreThread(_save);

  PyObject *array = nullptr;
  array = PyArray_SimpleNew(dimData, dim_array, NPY_INT32);
  memcpy(PyArray_DATA(array), unsharped.data(), len * sizeof(int));

  return array;
}

static PyMethodDef module_methods[] = {
    {"kriging", (PyCFunction)kriging, METH_VARARGS | METH_KEYWORDS,
     kriging_docstring},
    {"cac", (PyCFunction)cac, METH_VARARGS | METH_KEYWORDS, cac_docstring},
    {"mrf", (PyCFunction)mrf, METH_VARARGS | METH_KEYWORDS, mrf_docstring},
    {"rgs", (PyCFunction)rgs, METH_VARARGS | METH_KEYWORDS, rgs_docstring},
    {"hessian", (PyCFunction)hessian, METH_VARARGS | METH_KEYWORDS,
     hessian_docstring},
    {"windowedHessian", (PyCFunction)windowedHessian,
     METH_VARARGS | METH_KEYWORDS, windowedHessian_docstring},
    {"nlm", (PyCFunction)nlm, METH_VARARGS | METH_KEYWORDS, nlm_docstring},
    {"unsharp", (PyCFunction)unsharp, METH_VARARGS | METH_KEYWORDS,
     unsharp_docstring},
    {NULL, NULL, 0, NULL}};

static struct PyModuleDef moduledef = {PyModuleDef_HEAD_INIT, "mazalib",
                                       module_docstring, -1, module_methods};

PyMODINIT_FUNC PyInit_mazalib(void) {
  Py_Initialize();
  import_array();
  PyObject *module = PyModule_Create(&moduledef);
  if (!module) {
    return NULL;
  }
  import_array();
  return module;
}