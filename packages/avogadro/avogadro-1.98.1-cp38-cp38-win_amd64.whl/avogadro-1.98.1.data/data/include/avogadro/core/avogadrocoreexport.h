
#ifndef AVOGADROCORE_EXPORT_H
#define AVOGADROCORE_EXPORT_H

#ifdef AVOGADROCORE_STATIC_DEFINE
#  define AVOGADROCORE_EXPORT
#  define AVOGADROCORE_NO_EXPORT
#else
#  ifndef AVOGADROCORE_EXPORT
#    ifdef Core_EXPORTS
        /* We are building this library */
#      define AVOGADROCORE_EXPORT __declspec(dllexport)
#    else
        /* We are using this library */
#      define AVOGADROCORE_EXPORT __declspec(dllimport)
#    endif
#  endif

#  ifndef AVOGADROCORE_NO_EXPORT
#    define AVOGADROCORE_NO_EXPORT 
#  endif
#endif

#ifndef AVOGADROCORE_DEPRECATED
#  define AVOGADROCORE_DEPRECATED __declspec(deprecated)
#endif

#ifndef AVOGADROCORE_DEPRECATED_EXPORT
#  define AVOGADROCORE_DEPRECATED_EXPORT AVOGADROCORE_EXPORT AVOGADROCORE_DEPRECATED
#endif

#ifndef AVOGADROCORE_DEPRECATED_NO_EXPORT
#  define AVOGADROCORE_DEPRECATED_NO_EXPORT AVOGADROCORE_NO_EXPORT AVOGADROCORE_DEPRECATED
#endif

#if 0 /* DEFINE_NO_DEPRECATED */
#  ifndef AVOGADROCORE_NO_DEPRECATED
#    define AVOGADROCORE_NO_DEPRECATED
#  endif
#endif

#endif /* AVOGADROCORE_EXPORT_H */
