#include <pythonic/core.hpp>
#include <pythonic/python/core.hpp>
#include <pythonic/types/bool.hpp>
#include <pythonic/types/int.hpp>
#ifdef _OPENMP
#include <omp.h>
#endif
#include <pythonic/include/types/float64.hpp>
#include <pythonic/types/float64.hpp>
#include <pythonic/include/builtins/ValueError.hpp>
#include <pythonic/include/builtins/tuple.hpp>
#include <pythonic/include/operator_/div.hpp>
#include <pythonic/include/operator_/gt.hpp>
#include <pythonic/include/operator_/lt.hpp>
#include <pythonic/include/operator_/mul.hpp>
#include <pythonic/include/operator_/sub.hpp>
#include <pythonic/include/types/str.hpp>
#include <pythonic/builtins/ValueError.hpp>
#include <pythonic/builtins/tuple.hpp>
#include <pythonic/operator_/div.hpp>
#include <pythonic/operator_/gt.hpp>
#include <pythonic/operator_/lt.hpp>
#include <pythonic/operator_/mul.hpp>
#include <pythonic/operator_/sub.hpp>
#include <pythonic/types/str.hpp>
namespace 
{
  namespace __pythran_reciprocal_transonic
  {
    struct __transonic__
    {
      typedef void callable;
      typedef void pure;
      struct type
      {
        typedef pythonic::types::str __type0;
        typedef decltype(pythonic::types::make_tuple(std::declval<__type0>())) __type1;
        typedef typename pythonic::returnable<__type1>::type __type2;
        typedef __type2 result_type;
      }  ;
      inline
      typename type::result_type operator()() const;
      ;
    }  ;
    struct __code_new_method__ReciprocalTransonic__minimum_step_cost
    {
      typedef void callable;
      typedef void pure;
      struct type
      {
        typedef pythonic::types::str __type0;
        typedef typename pythonic::returnable<__type0>::type __type1;
        typedef __type1 result_type;
      }  ;
      inline
      typename type::result_type operator()() const;
      ;
    }  ;
    struct __for_method__ReciprocalTransonic__minimum_step_cost
    {
      typedef void callable;
      typedef void pure;
      template <typename argument_type0 >
      struct type
      {
        typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type0;
        typedef __type0 __type1;
        typedef typename pythonic::returnable<__type1>::type __type2;
        typedef __type2 result_type;
      }  
      ;
      template <typename argument_type0 >
      inline
      typename type<argument_type0>::result_type operator()(argument_type0 self__min_step_cost) const
      ;
    }  ;
    struct __code_new_method__ReciprocalTransonic__cost_of_moving_to
    {
      typedef void callable;
      typedef void pure;
      struct type
      {
        typedef pythonic::types::str __type0;
        typedef typename pythonic::returnable<__type0>::type __type1;
        typedef __type1 result_type;
      }  ;
      inline
      typename type::result_type operator()() const;
      ;
    }  ;
    struct __for_method__ReciprocalTransonic__cost_of_moving_to
    {
      typedef void callable;
      typedef void pure;
      template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 >
      struct type
      {
        typedef typename std::remove_cv<typename std::remove_reference<argument_type4>::type>::type __type0;
        typedef __type0 __type1;
        typedef __type1 __type2;
        typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type3;
        typedef __type3 __type4;
        typedef __type4 __type5;
        typedef double __type6;
        typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type7;
        typedef __type7 __type8;
        typedef typename pythonic::assignable<__type1>::type __type9;
        typedef __type9 __type10;
        typedef typename std::remove_cv<typename std::remove_reference<argument_type3>::type>::type __type11;
        typedef __type11 __type12;
        typedef decltype(pythonic::operator_::sub(std::declval<__type10>(), std::declval<__type12>())) __type13;
        typedef decltype(pythonic::operator_::mul(std::declval<__type8>(), std::declval<__type13>())) __type14;
        typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type15;
        typedef __type15 __type16;
        typedef decltype(pythonic::operator_::sub(std::declval<__type16>(), std::declval<__type12>())) __type18;
        typedef decltype(pythonic::operator_::div(std::declval<__type14>(), std::declval<__type18>())) __type19;
        typedef typename pythonic::assignable<__type19>::type __type20;
        typedef typename pythonic::assignable<__type4>::type __type21;
        typedef typename __combined<__type20,__type21>::type __type22;
        typedef __type22 __type23;
        typedef decltype(pythonic::operator_::div(std::declval<__type6>(), std::declval<__type23>())) __type24;
        typedef typename pythonic::returnable<__type24>::type __type25;
        typedef __type2 __ptype0;
        typedef __type5 __ptype1;
        typedef __type25 result_type;
      }  
      ;
      template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 >
      inline
      typename type<argument_type0, argument_type1, argument_type2, argument_type3, argument_type4>::result_type operator()(argument_type0 self_RECIPROCAL_MAX, argument_type1 self_RECIPROCAL_MIN, argument_type2 self_max_intensity, argument_type3 self_min_intensity, argument_type4 intensity_at_new_point) const
      ;
    }  ;
    inline
    typename __transonic__::type::result_type __transonic__::operator()() const
    {
      {
        static typename __transonic__::type::result_type tmp_global = pythonic::types::make_tuple(pythonic::types::str("0.5.3"));
        return tmp_global;
      }
    }
    inline
    typename __code_new_method__ReciprocalTransonic__minimum_step_cost::type::result_type __code_new_method__ReciprocalTransonic__minimum_step_cost::operator()() const
    {
      {
        static typename __code_new_method__ReciprocalTransonic__minimum_step_cost::type::result_type tmp_global = pythonic::types::str("\n\ndef new_method(self, ):\n    return backend_func(self._min_step_cost, )\n\n");
        return tmp_global;
      }
    }
    template <typename argument_type0 >
    inline
    typename __for_method__ReciprocalTransonic__minimum_step_cost::type<argument_type0>::result_type __for_method__ReciprocalTransonic__minimum_step_cost::operator()(argument_type0 self__min_step_cost) const
    {
      return self__min_step_cost;
    }
    inline
    typename __code_new_method__ReciprocalTransonic__cost_of_moving_to::type::result_type __code_new_method__ReciprocalTransonic__cost_of_moving_to::operator()() const
    {
      {
        static typename __code_new_method__ReciprocalTransonic__cost_of_moving_to::type::result_type tmp_global = pythonic::types::str("\n\ndef new_method(self, intensity_at_new_point):\n    return backend_func(self.RECIPROCAL_MAX, self.RECIPROCAL_MIN, self.max_intensity, self.min_intensity, intensity_at_new_point)\n\n");
        return tmp_global;
      }
    }
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 >
    inline
    typename __for_method__ReciprocalTransonic__cost_of_moving_to::type<argument_type0, argument_type1, argument_type2, argument_type3, argument_type4>::result_type __for_method__ReciprocalTransonic__cost_of_moving_to::operator()(argument_type0 self_RECIPROCAL_MAX, argument_type1 self_RECIPROCAL_MIN, argument_type2 self_max_intensity, argument_type3 self_min_intensity, argument_type4 intensity_at_new_point) const
    {
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type0;
      typedef __type0 __type1;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type4>::type>::type __type2;
      typedef __type2 __type3;
      typedef typename pythonic::assignable<__type3>::type __type4;
      typedef __type4 __type5;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type3>::type>::type __type6;
      typedef __type6 __type7;
      typedef decltype(pythonic::operator_::sub(std::declval<__type5>(), std::declval<__type7>())) __type8;
      typedef decltype(pythonic::operator_::mul(std::declval<__type1>(), std::declval<__type8>())) __type9;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type10;
      typedef __type10 __type11;
      typedef decltype(pythonic::operator_::sub(std::declval<__type11>(), std::declval<__type7>())) __type13;
      typedef decltype(pythonic::operator_::div(std::declval<__type9>(), std::declval<__type13>())) __type14;
      typedef typename pythonic::assignable<__type14>::type __type15;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type16;
      typedef __type16 __type17;
      typedef typename pythonic::assignable<__type17>::type __type18;
      typedef typename __combined<__type15,__type18>::type __type19;
      typedef typename pythonic::assignable<__type19>::type __type20;
      typename pythonic::assignable_noescape<decltype(intensity_at_new_point)>::type intensity_at_new_point_ = intensity_at_new_point;
      if (pythonic::operator_::gt(intensity_at_new_point_, self_max_intensity))
      {
        throw pythonic::builtins::functor::ValueError{};
      }
      __type20 intensity_at_new_point__ = pythonic::operator_::div(pythonic::operator_::mul(self_RECIPROCAL_MAX, pythonic::operator_::sub(intensity_at_new_point_, self_min_intensity)), pythonic::operator_::sub(self_max_intensity, self_min_intensity));
      if (pythonic::operator_::lt(intensity_at_new_point__, self_RECIPROCAL_MIN))
      {
        intensity_at_new_point__ = self_RECIPROCAL_MIN;
      }
      return pythonic::operator_::div(1.0, intensity_at_new_point__);
    }
  }
}
#include <pythonic/python/exception_handler.hpp>
#ifdef ENABLE_PYTHON_MODULE
static PyObject* __transonic__ = to_python(__pythran_reciprocal_transonic::__transonic__()());
static PyObject* __code_new_method__ReciprocalTransonic__minimum_step_cost = to_python(__pythran_reciprocal_transonic::__code_new_method__ReciprocalTransonic__minimum_step_cost()());
inline
typename __pythran_reciprocal_transonic::__for_method__ReciprocalTransonic__minimum_step_cost::type<double>::result_type __for_method__ReciprocalTransonic__minimum_step_cost0(double&& self__min_step_cost) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_reciprocal_transonic::__for_method__ReciprocalTransonic__minimum_step_cost()(self__min_step_cost);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
static PyObject* __code_new_method__ReciprocalTransonic__cost_of_moving_to = to_python(__pythran_reciprocal_transonic::__code_new_method__ReciprocalTransonic__cost_of_moving_to()());
inline
typename __pythran_reciprocal_transonic::__for_method__ReciprocalTransonic__cost_of_moving_to::type<double, double, double, double, double>::result_type __for_method__ReciprocalTransonic__cost_of_moving_to0(double&& self_RECIPROCAL_MAX, double&& self_RECIPROCAL_MIN, double&& self_max_intensity, double&& self_min_intensity, double&& intensity_at_new_point) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_reciprocal_transonic::__for_method__ReciprocalTransonic__cost_of_moving_to()(self_RECIPROCAL_MAX, self_RECIPROCAL_MIN, self_max_intensity, self_min_intensity, intensity_at_new_point);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}

static PyObject *
__pythran_wrap___for_method__ReciprocalTransonic__minimum_step_cost0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[1+1];
    
    char const* keywords[] = {"self__min_step_cost",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "O",
                                     (char**)keywords , &args_obj[0]))
        return nullptr;
    if(is_convertible<double>(args_obj[0]))
        return to_python(__for_method__ReciprocalTransonic__minimum_step_cost0(from_python<double>(args_obj[0])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap___for_method__ReciprocalTransonic__cost_of_moving_to0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[5+1];
    
    char const* keywords[] = {"self_RECIPROCAL_MAX", "self_RECIPROCAL_MIN", "self_max_intensity", "self_min_intensity", "intensity_at_new_point",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4]))
        return nullptr;
    if(is_convertible<double>(args_obj[0]) && is_convertible<double>(args_obj[1]) && is_convertible<double>(args_obj[2]) && is_convertible<double>(args_obj[3]) && is_convertible<double>(args_obj[4]))
        return to_python(__for_method__ReciprocalTransonic__cost_of_moving_to0(from_python<double>(args_obj[0]), from_python<double>(args_obj[1]), from_python<double>(args_obj[2]), from_python<double>(args_obj[3]), from_python<double>(args_obj[4])));
    else {
        return nullptr;
    }
}

            static PyObject *
            __pythran_wrapall___for_method__ReciprocalTransonic__minimum_step_cost(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap___for_method__ReciprocalTransonic__minimum_step_cost0(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "__for_method__ReciprocalTransonic__minimum_step_cost", "\n""    - __for_method__ReciprocalTransonic__minimum_step_cost(float64)", args, kw);
                });
            }


            static PyObject *
            __pythran_wrapall___for_method__ReciprocalTransonic__cost_of_moving_to(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap___for_method__ReciprocalTransonic__cost_of_moving_to0(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "__for_method__ReciprocalTransonic__cost_of_moving_to", "\n""    - __for_method__ReciprocalTransonic__cost_of_moving_to(float64, float64, float64, float64, float64)", args, kw);
                });
            }


static PyMethodDef Methods[] = {
    {
    "__for_method__ReciprocalTransonic__minimum_step_cost",
    (PyCFunction)__pythran_wrapall___for_method__ReciprocalTransonic__minimum_step_cost,
    METH_VARARGS | METH_KEYWORDS,
    "calculates the minimum step cost\n""\n""    Supported prototypes:\n""\n""    - __for_method__ReciprocalTransonic__minimum_step_cost(float64)\n""\n""        Returns\n""        -------\n""        float\n""            the minimum step cost\n"""},{
    "__for_method__ReciprocalTransonic__cost_of_moving_to",
    (PyCFunction)__pythran_wrapall___for_method__ReciprocalTransonic__cost_of_moving_to,
    METH_VARARGS | METH_KEYWORDS,
    "calculates the cost of moving to a point\n""\n""    Supported prototypes:\n""\n""    - __for_method__ReciprocalTransonic__cost_of_moving_to(float64, float64, float64, float64, float64)\n""\n""        Parameters\n""        ----------\n""        intensity_at_new_point : float\n""            The intensity of the new point under consideration\n""\n""        Returns\n""        -------\n""        float\n""            the cost of moving to the new point\n""\n""        Notes\n""        -----\n""        - To cope with zero intensities, RECIPROCAL_MIN is added to the intensities in the range before reciprocal calculation\n""        - We set the maximum intensity <= RECIPROCAL_MAX so that the intensity is between RECIPROCAL MIN and RECIPROCAL_MAX\n""\n"""},
    {NULL, NULL, 0, NULL}
};


            #if PY_MAJOR_VERSION >= 3
              static struct PyModuleDef moduledef = {
                PyModuleDef_HEAD_INIT,
                "reciprocal_transonic",            /* m_name */
                "",         /* m_doc */
                -1,                  /* m_size */
                Methods,             /* m_methods */
                NULL,                /* m_reload */
                NULL,                /* m_traverse */
                NULL,                /* m_clear */
                NULL,                /* m_free */
              };
            #define PYTHRAN_RETURN return theModule
            #define PYTHRAN_MODULE_INIT(s) PyInit_##s
            #else
            #define PYTHRAN_RETURN return
            #define PYTHRAN_MODULE_INIT(s) init##s
            #endif
            PyMODINIT_FUNC
            PYTHRAN_MODULE_INIT(reciprocal_transonic)(void)
            #ifndef _WIN32
            __attribute__ ((visibility("default")))
            #if defined(GNUC) && !defined(__clang__)
            __attribute__ ((externally_visible))
            #endif
            #endif
            ;
            PyMODINIT_FUNC
            PYTHRAN_MODULE_INIT(reciprocal_transonic)(void) {
                import_array()
                #if PY_MAJOR_VERSION >= 3
                PyObject* theModule = PyModule_Create(&moduledef);
                #else
                PyObject* theModule = Py_InitModule3("reciprocal_transonic",
                                                     Methods,
                                                     ""
                );
                #endif
                if(! theModule)
                    PYTHRAN_RETURN;
                PyObject * theDoc = Py_BuildValue("(ss)",
                                                  "0.14.0",
                                                  "c12fc91ebb71f094ff16824cf783aa7eee90249d13935b40a7de5ee1ba6b50e8");
                if(! theDoc)
                    PYTHRAN_RETURN;
                PyModule_AddObject(theModule,
                                   "__pythran__",
                                   theDoc);

                PyModule_AddObject(theModule, "__transonic__", __transonic__);
PyModule_AddObject(theModule, "__code_new_method__ReciprocalTransonic__minimum_step_cost", __code_new_method__ReciprocalTransonic__minimum_step_cost);
PyModule_AddObject(theModule, "__code_new_method__ReciprocalTransonic__cost_of_moving_to", __code_new_method__ReciprocalTransonic__cost_of_moving_to);
                PYTHRAN_RETURN;
            }

#endif