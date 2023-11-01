#include <pythonic/core.hpp>
#include <pythonic/python/core.hpp>
#include <pythonic/types/bool.hpp>
#include <pythonic/types/int.hpp>
#ifdef _OPENMP
#include <omp.h>
#endif
#include <pythonic/include/types/int64.hpp>
#include <pythonic/include/types/ndarray.hpp>
#include <pythonic/include/types/float64.hpp>
#include <pythonic/types/int64.hpp>
#include <pythonic/types/ndarray.hpp>
#include <pythonic/types/float64.hpp>
#include <pythonic/include/builtins/TypeError.hpp>
#include <pythonic/include/builtins/ValueError.hpp>
#include <pythonic/include/builtins/len.hpp>
#include <pythonic/include/builtins/pythran/is_none.hpp>
#include <pythonic/include/builtins/pythran/or_.hpp>
#include <pythonic/include/builtins/pythran/static_if.hpp>
#include <pythonic/include/builtins/tuple.hpp>
#include <pythonic/include/math/sqrt.hpp>
#include <pythonic/include/numpy/square.hpp>
#include <pythonic/include/operator_/add.hpp>
#include <pythonic/include/operator_/eq.hpp>
#include <pythonic/include/operator_/mul.hpp>
#include <pythonic/include/operator_/ne.hpp>
#include <pythonic/include/operator_/not_.hpp>
#include <pythonic/include/operator_/or_.hpp>
#include <pythonic/include/operator_/sub.hpp>
#include <pythonic/include/types/str.hpp>
#include <pythonic/builtins/TypeError.hpp>
#include <pythonic/builtins/ValueError.hpp>
#include <pythonic/builtins/len.hpp>
#include <pythonic/builtins/pythran/is_none.hpp>
#include <pythonic/builtins/pythran/or_.hpp>
#include <pythonic/builtins/pythran/static_if.hpp>
#include <pythonic/builtins/tuple.hpp>
#include <pythonic/math/sqrt.hpp>
#include <pythonic/numpy/square.hpp>
#include <pythonic/operator_/add.hpp>
#include <pythonic/operator_/eq.hpp>
#include <pythonic/operator_/mul.hpp>
#include <pythonic/operator_/ne.hpp>
#include <pythonic/operator_/not_.hpp>
#include <pythonic/operator_/or_.hpp>
#include <pythonic/operator_/sub.hpp>
#include <pythonic/types/str.hpp>
namespace 
{
  namespace __pythran_euclidean_transonic
  {
    struct __for_method__EuclideanTransonic__estimate_cost_to_goal_compare0
    {
      typedef void callable;
      typedef void pure;
      template <typename argument_type0 , typename argument_type1 >
      struct type
      {
        typedef bool __type0;
        typedef typename pythonic::returnable<__type0>::type __type1;
        typedef __type1 result_type;
      }  
      ;
      template <typename argument_type0 , typename argument_type1 >
      inline
      typename type<argument_type0, argument_type1>::result_type operator()(argument_type0 current_point, argument_type1 goal_point) const
      ;
    }  ;
    struct $isstatic1
    {
      typedef void callable;
      typedef void pure;
      template <typename argument_type0 , typename argument_type1 >
      struct type
      {
        typedef decltype(pythonic::types::make_tuple()) __type0;
        typedef typename pythonic::returnable<__type0>::type __type1;
        typedef __type1 result_type;
      }  
      ;
      template <typename argument_type0 , typename argument_type1 >
      inline
      typename type<argument_type0, argument_type1>::result_type operator()(argument_type0 current_point, argument_type1 goal_point) const
      ;
    }  ;
    struct $isstatic0
    {
      typedef void callable;
      typedef void pure;
      template <typename argument_type0 , typename argument_type1 >
      struct type
      {
        typedef decltype(pythonic::types::make_tuple()) __type0;
        typedef typename pythonic::returnable<__type0>::type __type1;
        typedef __type1 result_type;
      }  
      ;
      template <typename argument_type0 , typename argument_type1 >
      inline
      typename type<argument_type0, argument_type1>::result_type operator()(argument_type0 current_point, argument_type1 goal_point) const
      ;
    }  ;
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
    struct __code_new_method__EuclideanTransonic__estimate_cost_to_goal
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
    struct __for_method__EuclideanTransonic__estimate_cost_to_goal
    {
      typedef void callable;
      ;
      template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 >
      struct type
      {
        typedef typename std::remove_cv<typename std::remove_reference<argument_type3>::type>::type __type0;
        typedef __type0 __type1;
        typedef decltype(pythonic::types::as_const(std::declval<__type1>())) __type2;
        typedef typename std::tuple_element<1,typename std::remove_reference<__type2>::type>::type __type3;
        typedef typename std::tuple_element<0,typename std::remove_reference<__type2>::type>::type __type6;
        typedef long __type7;
        typedef decltype(pythonic::types::make_tuple(std::declval<__type3>(), std::declval<__type6>(), std::declval<__type7>())) __type8;
        typedef typename pythonic::assignable<__type8>::type __type9;
        typedef __type9 __type10;
        typedef decltype(pythonic::types::as_const(std::declval<__type10>())) __type11;
        typedef typename std::tuple_element<0,typename std::remove_reference<__type11>::type>::type __type12;
        typedef __type12 __type13;
        typedef typename std::tuple_element<1,typename std::remove_reference<__type11>::type>::type __type14;
        typedef __type14 __type15;
        typedef typename std::remove_cv<typename std::remove_reference<argument_type4>::type>::type __type16;
        typedef __type16 __type17;
        typedef decltype(pythonic::types::as_const(std::declval<__type17>())) __type18;
        typedef typename std::tuple_element<1,typename std::remove_reference<__type18>::type>::type __type19;
        typedef typename std::tuple_element<0,typename std::remove_reference<__type18>::type>::type __type22;
        typedef decltype(pythonic::types::make_tuple(std::declval<__type19>(), std::declval<__type22>(), std::declval<__type7>())) __type23;
        typedef typename pythonic::assignable<__type23>::type __type24;
        typedef __type24 __type25;
        typedef decltype(pythonic::types::as_const(std::declval<__type25>())) __type26;
        typedef typename std::tuple_element<0,typename std::remove_reference<__type26>::type>::type __type27;
        typedef __type27 __type28;
        typedef typename std::tuple_element<1,typename std::remove_reference<__type26>::type>::type __type29;
        typedef __type29 __type30;
        typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::math::functor::sqrt{})>::type>::type __type31;
        typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::square{})>::type>::type __type32;
        typedef typename pythonic::lazy<__type27>::type __type33;
        typedef std::integral_constant<long,1> __type34;
        typedef indexable_container<__type34, typename std::remove_reference<__type27>::type> __type35;
        typedef std::integral_constant<long,0> __type36;
        typedef indexable_container<__type36, typename std::remove_reference<__type29>::type> __type37;
        typedef typename __combined<__type16,__type35,__type37>::type __type38;
        typedef __type38 __type39;
        typedef decltype(pythonic::types::as_const(std::declval<__type39>())) __type40;
        typedef typename std::tuple_element<0,typename std::remove_reference<__type40>::type>::type __type41;
        typedef typename std::tuple_element<1,typename std::remove_reference<__type40>::type>::type __type44;
        typedef typename std::tuple_element<2,typename std::remove_reference<__type40>::type>::type __type47;
        typedef decltype(pythonic::types::make_tuple(std::declval<__type41>(), std::declval<__type44>(), std::declval<__type47>())) __type48;
        typedef typename pythonic::assignable<__type48>::type __type49;
        typedef __type49 __type50;
        typedef decltype(pythonic::types::as_const(std::declval<__type50>())) __type51;
        typedef typename std::tuple_element<2,typename std::remove_reference<__type51>::type>::type __type52;
        typedef typename pythonic::lazy<__type52>::type __type53;
        typedef typename __combined<__type33,__type53>::type __type54;
        typedef __type54 __type55;
        typedef typename pythonic::lazy<__type12>::type __type56;
        typedef indexable_container<__type34, typename std::remove_reference<__type12>::type> __type57;
        typedef indexable_container<__type36, typename std::remove_reference<__type14>::type> __type58;
        typedef typename __combined<__type0,__type57,__type58>::type __type59;
        typedef __type59 __type60;
        typedef decltype(pythonic::types::as_const(std::declval<__type60>())) __type61;
        typedef typename std::tuple_element<0,typename std::remove_reference<__type61>::type>::type __type62;
        typedef typename std::tuple_element<1,typename std::remove_reference<__type61>::type>::type __type65;
        typedef typename std::tuple_element<2,typename std::remove_reference<__type61>::type>::type __type68;
        typedef decltype(pythonic::types::make_tuple(std::declval<__type62>(), std::declval<__type65>(), std::declval<__type68>())) __type69;
        typedef typename pythonic::assignable<__type69>::type __type70;
        typedef __type70 __type71;
        typedef decltype(pythonic::types::as_const(std::declval<__type71>())) __type72;
        typedef typename std::tuple_element<2,typename std::remove_reference<__type72>::type>::type __type73;
        typedef typename pythonic::lazy<__type73>::type __type74;
        typedef typename __combined<__type56,__type74>::type __type75;
        typedef __type75 __type76;
        typedef decltype(pythonic::operator_::sub(std::declval<__type55>(), std::declval<__type76>())) __type77;
        typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type78;
        typedef __type78 __type79;
        typedef decltype(pythonic::operator_::mul(std::declval<__type77>(), std::declval<__type79>())) __type80;
        typedef decltype(std::declval<__type32>()(std::declval<__type80>())) __type81;
        typedef typename pythonic::lazy<__type29>::type __type82;
        typedef typename std::tuple_element<1,typename std::remove_reference<__type51>::type>::type __type83;
        typedef typename pythonic::lazy<__type83>::type __type84;
        typedef typename __combined<__type82,__type84>::type __type85;
        typedef __type85 __type86;
        typedef typename pythonic::lazy<__type14>::type __type87;
        typedef typename std::tuple_element<1,typename std::remove_reference<__type72>::type>::type __type88;
        typedef typename pythonic::lazy<__type88>::type __type89;
        typedef typename __combined<__type87,__type89>::type __type90;
        typedef __type90 __type91;
        typedef decltype(pythonic::operator_::sub(std::declval<__type86>(), std::declval<__type91>())) __type92;
        typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type93;
        typedef __type93 __type94;
        typedef decltype(pythonic::operator_::mul(std::declval<__type92>(), std::declval<__type94>())) __type95;
        typedef decltype(std::declval<__type32>()(std::declval<__type95>())) __type96;
        typedef decltype(pythonic::operator_::add(std::declval<__type81>(), std::declval<__type96>())) __type97;
        typedef typename std::tuple_element<2,typename std::remove_reference<__type26>::type>::type __type98;
        typedef typename pythonic::lazy<__type98>::type __type99;
        typedef typename std::tuple_element<0,typename std::remove_reference<__type51>::type>::type __type100;
        typedef typename pythonic::lazy<__type100>::type __type101;
        typedef typename __combined<__type99,__type101>::type __type102;
        typedef __type102 __type103;
        typedef typename std::tuple_element<2,typename std::remove_reference<__type11>::type>::type __type104;
        typedef typename pythonic::lazy<__type104>::type __type105;
        typedef typename std::tuple_element<0,typename std::remove_reference<__type72>::type>::type __type106;
        typedef typename pythonic::lazy<__type106>::type __type107;
        typedef typename __combined<__type105,__type107>::type __type108;
        typedef __type108 __type109;
        typedef decltype(pythonic::operator_::sub(std::declval<__type103>(), std::declval<__type109>())) __type110;
        typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type111;
        typedef __type111 __type112;
        typedef decltype(pythonic::operator_::mul(std::declval<__type110>(), std::declval<__type112>())) __type113;
        typedef decltype(std::declval<__type32>()(std::declval<__type113>())) __type114;
        typedef decltype(pythonic::operator_::add(std::declval<__type97>(), std::declval<__type114>())) __type115;
        typedef decltype(std::declval<__type31>()(std::declval<__type115>())) __type116;
        typedef typename pythonic::returnable<__type116>::type __type117;
        typedef __type13 __ptype0;
        typedef __type15 __ptype1;
        typedef __type28 __ptype2;
        typedef __type30 __ptype3;
        typedef __type117 result_type;
      }  
      ;
      template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 >
      inline
      typename type<argument_type0, argument_type1, argument_type2, argument_type3, argument_type4>::result_type operator()(argument_type0 self_scale_x, argument_type1 self_scale_y, argument_type2 self_scale_z, argument_type3 current_point, argument_type4 goal_point) const
      ;
    }  ;
    template <typename argument_type0 , typename argument_type1 >
    inline
    typename __for_method__EuclideanTransonic__estimate_cost_to_goal_compare0::type<argument_type0, argument_type1>::result_type __for_method__EuclideanTransonic__estimate_cost_to_goal_compare0::operator()(argument_type0 current_point, argument_type1 goal_point) const
    {
      typename pythonic::assignable_noescape<decltype(pythonic::builtins::functor::len{}(goal_point))>::type $1 = pythonic::builtins::functor::len{}(goal_point);
      if (pythonic::operator_::not_(pythonic::operator_::eq(pythonic::builtins::functor::len{}(current_point), $1)))
      {
        return false;
      }
      if (pythonic::operator_::not_(pythonic::operator_::eq($1, 3L)))
      {
        return false;
      }
      return true;
    }
    template <typename argument_type0 , typename argument_type1 >
    inline
    typename $isstatic1::type<argument_type0, argument_type1>::result_type $isstatic1::operator()(argument_type0 current_point, argument_type1 goal_point) const
    {
      return pythonic::types::make_tuple();
    }
    template <typename argument_type0 , typename argument_type1 >
    inline
    typename $isstatic0::type<argument_type0, argument_type1>::result_type $isstatic0::operator()(argument_type0 current_point, argument_type1 goal_point) const
    {
      throw pythonic::builtins::functor::TypeError{};
      return pythonic::types::make_tuple();
    }
    inline
    typename __transonic__::type::result_type __transonic__::operator()() const
    {
      {
        static typename __transonic__::type::result_type tmp_global = pythonic::types::make_tuple(pythonic::types::str("0.5.3"));
        return tmp_global;
      }
    }
    inline
    typename __code_new_method__EuclideanTransonic__estimate_cost_to_goal::type::result_type __code_new_method__EuclideanTransonic__estimate_cost_to_goal::operator()() const
    {
      {
        static typename __code_new_method__EuclideanTransonic__estimate_cost_to_goal::type::result_type tmp_global = pythonic::types::str("\n\ndef new_method(self, current_point, goal_point):\n    return backend_func(self.scale_x, self.scale_y, self.scale_z, current_point, goal_point)\n\n");
        return tmp_global;
      }
    }
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 >
    inline
    typename __for_method__EuclideanTransonic__estimate_cost_to_goal::type<argument_type0, argument_type1, argument_type2, argument_type3, argument_type4>::result_type __for_method__EuclideanTransonic__estimate_cost_to_goal::operator()(argument_type0 self_scale_x, argument_type1 self_scale_y, argument_type2 self_scale_z, argument_type3 current_point, argument_type4 goal_point) const
    {
      typedef typename std::remove_cv<typename std::remove_reference<argument_type3>::type>::type __type0;
      typedef __type0 __type1;
      typedef decltype(pythonic::types::as_const(std::declval<__type1>())) __type2;
      typedef typename std::tuple_element<1,typename std::remove_reference<__type2>::type>::type __type3;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type2>::type>::type __type6;
      typedef long __type7;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type3>(), std::declval<__type6>(), std::declval<__type7>())) __type8;
      typedef typename pythonic::assignable<__type8>::type __type9;
      typedef __type9 __type10;
      typedef decltype(pythonic::types::as_const(std::declval<__type10>())) __type11;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type11>::type>::type __type12;
      typedef typename pythonic::lazy<__type12>::type __type13;
      typedef std::integral_constant<long,1> __type14;
      typedef indexable_container<__type14, typename std::remove_reference<__type12>::type> __type15;
      typedef std::integral_constant<long,0> __type16;
      typedef typename std::tuple_element<1,typename std::remove_reference<__type11>::type>::type __type17;
      typedef indexable_container<__type16, typename std::remove_reference<__type17>::type> __type18;
      typedef typename __combined<__type0,__type15,__type18>::type __type19;
      typedef __type19 __type20;
      typedef decltype(pythonic::types::as_const(std::declval<__type20>())) __type21;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type21>::type>::type __type22;
      typedef typename std::tuple_element<1,typename std::remove_reference<__type21>::type>::type __type25;
      typedef typename std::tuple_element<2,typename std::remove_reference<__type21>::type>::type __type28;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type22>(), std::declval<__type25>(), std::declval<__type28>())) __type29;
      typedef typename pythonic::assignable<__type29>::type __type30;
      typedef __type30 __type31;
      typedef decltype(pythonic::types::as_const(std::declval<__type31>())) __type32;
      typedef typename std::tuple_element<2,typename std::remove_reference<__type32>::type>::type __type33;
      typedef typename pythonic::lazy<__type33>::type __type34;
      typedef typename __combined<__type13,__type34>::type __type35;
      typedef typename pythonic::lazy<__type35>::type __type36;
      typedef typename pythonic::lazy<__type17>::type __type37;
      typedef typename std::tuple_element<1,typename std::remove_reference<__type32>::type>::type __type38;
      typedef typename pythonic::lazy<__type38>::type __type39;
      typedef typename __combined<__type37,__type39>::type __type40;
      typedef typename pythonic::lazy<__type40>::type __type41;
      typedef typename std::tuple_element<2,typename std::remove_reference<__type11>::type>::type __type42;
      typedef typename pythonic::lazy<__type42>::type __type43;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type32>::type>::type __type44;
      typedef typename pythonic::lazy<__type44>::type __type45;
      typedef typename __combined<__type43,__type45>::type __type46;
      typedef typename pythonic::lazy<__type46>::type __type47;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type4>::type>::type __type48;
      typedef __type48 __type49;
      typedef decltype(pythonic::types::as_const(std::declval<__type49>())) __type50;
      typedef typename std::tuple_element<1,typename std::remove_reference<__type50>::type>::type __type51;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type50>::type>::type __type54;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type51>(), std::declval<__type54>(), std::declval<__type7>())) __type55;
      typedef typename pythonic::assignable<__type55>::type __type56;
      typedef __type56 __type57;
      typedef decltype(pythonic::types::as_const(std::declval<__type57>())) __type58;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type58>::type>::type __type59;
      typedef typename pythonic::lazy<__type59>::type __type60;
      typedef indexable_container<__type14, typename std::remove_reference<__type59>::type> __type61;
      typedef typename std::tuple_element<1,typename std::remove_reference<__type58>::type>::type __type62;
      typedef indexable_container<__type16, typename std::remove_reference<__type62>::type> __type63;
      typedef typename __combined<__type48,__type61,__type63>::type __type64;
      typedef __type64 __type65;
      typedef decltype(pythonic::types::as_const(std::declval<__type65>())) __type66;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type66>::type>::type __type67;
      typedef typename std::tuple_element<1,typename std::remove_reference<__type66>::type>::type __type70;
      typedef typename std::tuple_element<2,typename std::remove_reference<__type66>::type>::type __type73;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type67>(), std::declval<__type70>(), std::declval<__type73>())) __type74;
      typedef typename pythonic::assignable<__type74>::type __type75;
      typedef __type75 __type76;
      typedef decltype(pythonic::types::as_const(std::declval<__type76>())) __type77;
      typedef typename std::tuple_element<2,typename std::remove_reference<__type77>::type>::type __type78;
      typedef typename pythonic::lazy<__type78>::type __type79;
      typedef typename __combined<__type60,__type79>::type __type80;
      typedef typename pythonic::lazy<__type80>::type __type81;
      typedef typename pythonic::lazy<__type62>::type __type82;
      typedef typename std::tuple_element<1,typename std::remove_reference<__type77>::type>::type __type83;
      typedef typename pythonic::lazy<__type83>::type __type84;
      typedef typename __combined<__type82,__type84>::type __type85;
      typedef typename pythonic::lazy<__type85>::type __type86;
      typedef typename std::tuple_element<2,typename std::remove_reference<__type58>::type>::type __type87;
      typedef typename pythonic::lazy<__type87>::type __type88;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type77>::type>::type __type89;
      typedef typename pythonic::lazy<__type89>::type __type90;
      typedef typename __combined<__type88,__type90>::type __type91;
      typedef typename pythonic::lazy<__type91>::type __type92;
      pythonic::builtins::pythran::functor::static_if{}(pythonic::operator_::or_(pythonic::builtins::pythran::functor::is_none{}(current_point), pythonic::builtins::pythran::functor::is_none{}(goal_point)), $isstatic0(), $isstatic1())(current_point, goal_point);
      if (pythonic::builtins::pythran::or_([&] () { return pythonic::builtins::pythran::or_([&] () { return pythonic::operator_::eq(pythonic::builtins::functor::len{}(current_point), 0L); }, [&] () { return pythonic::operator_::eq(pythonic::builtins::functor::len{}(goal_point), 0L); }); }, [&] () { return pythonic::operator_::ne(pythonic::builtins::functor::len{}(current_point), pythonic::builtins::functor::len{}(goal_point)); }))
      {
        throw pythonic::builtins::functor::ValueError{};
      }
      typename pythonic::assignable_noescape<decltype(pythonic::types::make_tuple(std::get<1>(pythonic::types::as_const(current_point)), std::get<0>(pythonic::types::as_const(current_point)), 0L))>::type __tuple0 = pythonic::types::make_tuple(std::get<1>(pythonic::types::as_const(current_point)), std::get<0>(pythonic::types::as_const(current_point)), 0L);
      __type36 current_x = std::get<0>(pythonic::types::as_const(__tuple0));
      __type41 current_y = std::get<1>(pythonic::types::as_const(__tuple0));
      __type47 current_z = std::get<2>(pythonic::types::as_const(__tuple0));
      typename pythonic::assignable_noescape<decltype(pythonic::types::make_tuple(std::get<1>(pythonic::types::as_const(goal_point)), std::get<0>(pythonic::types::as_const(goal_point)), 0L))>::type __tuple1 = pythonic::types::make_tuple(std::get<1>(pythonic::types::as_const(goal_point)), std::get<0>(pythonic::types::as_const(goal_point)), 0L);
      __type81 goal_x = std::get<0>(pythonic::types::as_const(__tuple1));
      __type86 goal_y = std::get<1>(pythonic::types::as_const(__tuple1));
      __type92 goal_z = std::get<2>(pythonic::types::as_const(__tuple1));
      if (pythonic::types::call(__for_method__EuclideanTransonic__estimate_cost_to_goal_compare0(), current_point, goal_point))
      {
        typename pythonic::assignable_noescape<decltype(pythonic::types::make_tuple(std::get<0>(pythonic::types::as_const(current_point)), std::get<1>(pythonic::types::as_const(current_point)), std::get<2>(pythonic::types::as_const(current_point))))>::type __tuple2 = pythonic::types::make_tuple(std::get<0>(pythonic::types::as_const(current_point)), std::get<1>(pythonic::types::as_const(current_point)), std::get<2>(pythonic::types::as_const(current_point)));
        current_z = std::get<0>(pythonic::types::as_const(__tuple2));
        current_y = std::get<1>(pythonic::types::as_const(__tuple2));
        current_x = std::get<2>(pythonic::types::as_const(__tuple2));
        typename pythonic::assignable_noescape<decltype(pythonic::types::make_tuple(std::get<0>(pythonic::types::as_const(goal_point)), std::get<1>(pythonic::types::as_const(goal_point)), std::get<2>(pythonic::types::as_const(goal_point))))>::type __tuple3 = pythonic::types::make_tuple(std::get<0>(pythonic::types::as_const(goal_point)), std::get<1>(pythonic::types::as_const(goal_point)), std::get<2>(pythonic::types::as_const(goal_point)));
        goal_z = std::get<0>(pythonic::types::as_const(__tuple3));
        goal_y = std::get<1>(pythonic::types::as_const(__tuple3));
        goal_x = std::get<2>(pythonic::types::as_const(__tuple3));
      }
      return pythonic::math::functor::sqrt{}(pythonic::operator_::add(pythonic::operator_::add(pythonic::numpy::functor::square{}(pythonic::operator_::mul(pythonic::operator_::sub(goal_x, current_x), self_scale_x)), pythonic::numpy::functor::square{}(pythonic::operator_::mul(pythonic::operator_::sub(goal_y, current_y), self_scale_y))), pythonic::numpy::functor::square{}(pythonic::operator_::mul(pythonic::operator_::sub(goal_z, current_z), self_scale_z))));
    }
  }
}
#include <pythonic/python/exception_handler.hpp>
#ifdef ENABLE_PYTHON_MODULE
static PyObject* __transonic__ = to_python(__pythran_euclidean_transonic::__transonic__()());
static PyObject* __code_new_method__EuclideanTransonic__estimate_cost_to_goal = to_python(__pythran_euclidean_transonic::__code_new_method__EuclideanTransonic__estimate_cost_to_goal()());
inline
typename __pythran_euclidean_transonic::__for_method__EuclideanTransonic__estimate_cost_to_goal::type<double, double, double, pythonic::types::ndarray<npy_int64,pythonic::types::pshape<long>>, pythonic::types::ndarray<npy_int64,pythonic::types::pshape<long>>>::result_type __for_method__EuclideanTransonic__estimate_cost_to_goal0(double&& self_scale_x, double&& self_scale_y, double&& self_scale_z, pythonic::types::ndarray<npy_int64,pythonic::types::pshape<long>>&& current_point, pythonic::types::ndarray<npy_int64,pythonic::types::pshape<long>>&& goal_point) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_euclidean_transonic::__for_method__EuclideanTransonic__estimate_cost_to_goal()(self_scale_x, self_scale_y, self_scale_z, current_point, goal_point);
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
__pythran_wrap___for_method__EuclideanTransonic__estimate_cost_to_goal0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[5+1];
    
    char const* keywords[] = {"self_scale_x", "self_scale_y", "self_scale_z", "current_point", "goal_point",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4]))
        return nullptr;
    if(is_convertible<double>(args_obj[0]) && is_convertible<double>(args_obj[1]) && is_convertible<double>(args_obj[2]) && is_convertible<pythonic::types::ndarray<npy_int64,pythonic::types::pshape<long>>>(args_obj[3]) && is_convertible<pythonic::types::ndarray<npy_int64,pythonic::types::pshape<long>>>(args_obj[4]))
        return to_python(__for_method__EuclideanTransonic__estimate_cost_to_goal0(from_python<double>(args_obj[0]), from_python<double>(args_obj[1]), from_python<double>(args_obj[2]), from_python<pythonic::types::ndarray<npy_int64,pythonic::types::pshape<long>>>(args_obj[3]), from_python<pythonic::types::ndarray<npy_int64,pythonic::types::pshape<long>>>(args_obj[4])));
    else {
        return nullptr;
    }
}

            static PyObject *
            __pythran_wrapall___for_method__EuclideanTransonic__estimate_cost_to_goal(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap___for_method__EuclideanTransonic__estimate_cost_to_goal0(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "__for_method__EuclideanTransonic__estimate_cost_to_goal", "\n""    - __for_method__EuclideanTransonic__estimate_cost_to_goal(float64, float64, float64, int64[:], int64[:])", args, kw);
                });
            }


static PyMethodDef Methods[] = {
    {
    "__for_method__EuclideanTransonic__estimate_cost_to_goal",
    (PyCFunction)__pythran_wrapall___for_method__EuclideanTransonic__estimate_cost_to_goal,
    METH_VARARGS | METH_KEYWORDS,
    "calculates the estimated cost from current point to the goal\n""\n""        Parameters\n""        ----------\n""        current_point : numpy ndarray\n""            the coordinates of the current point\n""        goal_point : numpy ndarray\n""            the coordinates of the current point\n""\n""        Returns\n""        -------\n""        float\n""            the estimated cost to goal in the form of Euclidean distance\n""\n""        Notes\n""        -----\n""        If the image is zoomed in or out, then the scale of one of more\n""        axes will be more or less than 1.0. For example, if the image is zoomed\n""        in to twice its size then the scale of X and Y axes will be 2.0.\n""\n""        By including the scale in the calculation of distance to the goal we\n""        can get an accurate cost.\n""\n""    Supported prototypes:\n""\n""    - __for_method__EuclideanTransonic__estimate_cost_to_goal(float64, float64, float64, int64[:], int64[:])\n""\n""        - for 2D points, the order of coordinates is: (y, x)\n""        - for 3D points, the order of coordinates is: (z, x, y)\n"""},
    {NULL, NULL, 0, NULL}
};


            #if PY_MAJOR_VERSION >= 3
              static struct PyModuleDef moduledef = {
                PyModuleDef_HEAD_INIT,
                "euclidean_transonic",            /* m_name */
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
            PYTHRAN_MODULE_INIT(euclidean_transonic)(void)
            #ifndef _WIN32
            __attribute__ ((visibility("default")))
            #if defined(GNUC) && !defined(__clang__)
            __attribute__ ((externally_visible))
            #endif
            #endif
            ;
            PyMODINIT_FUNC
            PYTHRAN_MODULE_INIT(euclidean_transonic)(void) {
                import_array()
                #if PY_MAJOR_VERSION >= 3
                PyObject* theModule = PyModule_Create(&moduledef);
                #else
                PyObject* theModule = Py_InitModule3("euclidean_transonic",
                                                     Methods,
                                                     ""
                );
                #endif
                if(! theModule)
                    PYTHRAN_RETURN;
                PyObject * theDoc = Py_BuildValue("(ss)",
                                                  "0.14.0",
                                                  "23d39c0d6d81164699008af2e973691d8eabf26852941b3c0acfd14923e9cec6");
                if(! theDoc)
                    PYTHRAN_RETURN;
                PyModule_AddObject(theModule,
                                   "__pythran__",
                                   theDoc);

                PyModule_AddObject(theModule, "__transonic__", __transonic__);
PyModule_AddObject(theModule, "__code_new_method__EuclideanTransonic__estimate_cost_to_goal", __code_new_method__EuclideanTransonic__estimate_cost_to_goal);
                PYTHRAN_RETURN;
            }

#endif