
#ifndef AVOGADROIO_EXPORT_H
#define AVOGADROIO_EXPORT_H

#ifdef AVOGADROIO_STATIC_DEFINE
#  define AVOGADROIO_EXPORT
#  define AVOGADROIO_NO_EXPORT
#else
#  ifndef AVOGADROIO_EXPORT
#    ifdef IO_EXPORTS
        /* We are building this library */
#      define AVOGADROIO_EXPORT __declspec(dllexport)
#    else
        /* We are using this library */
#      define AVOGADROIO_EXPORT __declspec(dllimport)
#    endif
#  endif

#  ifndef AVOGADROIO_NO_EXPORT
#    define AVOGADROIO_NO_EXPORT 
#  endif
#endif

#ifndef AVOGADROIO_DEPRECATED
#  define AVOGADROIO_DEPRECATED __declspec(deprecated)
#endif

#ifndef AVOGADROIO_DEPRECATED_EXPORT
#  define AVOGADROIO_DEPRECATED_EXPORT AVOGADROIO_EXPORT AVOGADROIO_DEPRECATED
#endif

#ifndef AVOGADROIO_DEPRECATED_NO_EXPORT
#  define AVOGADROIO_DEPRECATED_NO_EXPORT AVOGADROIO_NO_EXPORT AVOGADROIO_DEPRECATED
#endif

#if 0 /* DEFINE_NO_DEPRECATED */
#  ifndef AVOGADROIO_NO_DEPRECATED
#    define AVOGADROIO_NO_DEPRECATED
#  endif
#endif

#endif /* AVOGADROIO_EXPORT_H */
