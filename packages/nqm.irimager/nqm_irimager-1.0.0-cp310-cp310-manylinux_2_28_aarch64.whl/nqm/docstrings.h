/*
  This file contains docstrings for use in the Python bindings.
  Do not edit! They were automatically extracted by pybind11_mkdoc.
 */

#define __EXPAND(x)                                      x
#define __COUNT(_1, _2, _3, _4, _5, _6, _7, COUNT, ...)  COUNT
#define __VA_SIZE(...)                                   __EXPAND(__COUNT(__VA_ARGS__, 7, 6, 5, 4, 3, 2, 1, 0))
#define __CAT1(a, b)                                     a ## b
#define __CAT2(a, b)                                     __CAT1(a, b)
#define __DOC1(n1)                                       __doc_##n1
#define __DOC2(n1, n2)                                   __doc_##n1##_##n2
#define __DOC3(n1, n2, n3)                               __doc_##n1##_##n2##_##n3
#define __DOC4(n1, n2, n3, n4)                           __doc_##n1##_##n2##_##n3##_##n4
#define __DOC5(n1, n2, n3, n4, n5)                       __doc_##n1##_##n2##_##n3##_##n4##_##n5
#define __DOC6(n1, n2, n3, n4, n5, n6)                   __doc_##n1##_##n2##_##n3##_##n4##_##n5##_##n6
#define __DOC7(n1, n2, n3, n4, n5, n6, n7)               __doc_##n1##_##n2##_##n3##_##n4##_##n5##_##n6##_##n7
#define DOC(...)                                         __EXPAND(__EXPAND(__CAT2(__DOC, __VA_SIZE(__VA_ARGS__)))(__VA_ARGS__))

#if defined(__GNUG__)
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wunused-variable"
#endif


static const char *__doc_IRImager = R"doc(IRImager object - interfaces with a camera.)doc";

static const char *__doc_IRImagerMock =
R"doc(Mocked version of IRImager.

This class can be used to return dummy data when there isn't a camera
connected (e.g. for testing).)doc";

static const char *__doc_IRImagerMock_IRImagerMock = R"doc()doc";

static const char *__doc_IRImagerMock_IRImagerMock_2 = R"doc()doc";

static const char *__doc_IRImager_IRImager = R"doc(Copies and existing IRImager object.)doc";

static const char *__doc_IRImager_IRImager_2 = R"doc(Moves an existing IRImager object into the new stack location.)doc";

static const char *__doc_IRImager_IRImager_3 =
R"doc(Loads the configuration for an IR Camera from the given XML file

Throws:
    std::runtime_error if the XML file could not be read.)doc";

static const char *__doc_IRImager_IRImager_4 = R"doc()doc";

static const char *__doc_IRImager_IRImager_5 = R"doc(Uninitialized constructor, should only be used in inheritance.)doc";

static const char *__doc_IRImager_get_frame =
R"doc(Return a frame.

If the shutter is down (normally done automatically by the thermal
camera for calibration), this function will wait until the shutter is
back up, before returning (usually around ~1s).

Throws:
    RuntimeError if a frame cannot be loaded, e.g. if the camera isn't
    streaming.

Returns:
    A tuple containing: 1. A 2-D matrix containing the image. This
    must be adjusted by :py:meth:`~IRImager.get_temp_range_decimal` to
    get the actual temperature in degrees Celcius, offset from -100 ℃.
    2. The time the image was taken.)doc";

static const char *__doc_IRImager_get_library_version =
R"doc(Get the version of the libirimager library.

Returns:
    the version of the libirmager library, or "MOCKED" if the library
    has been mocked.)doc";

static const char *__doc_IRImager_get_temp_range_decimal =
R"doc(The number of decimal places in the thermal data

For example, if :py:meth:`~IRImager.get_frame` returns 19000, you can
divide this number by 10 to the power of the result of
:py:meth:`~IRImager.get_temp_range_decimal`, then subtract 100, to get
the actual temperature in degrees Celcius.)doc";

static const char *__doc_IRImager_impl = R"doc(pImpl implementation)doc";

static const char *__doc_IRImager_pImpl = R"doc()doc";

static const char *__doc_IRImager_start_streaming =
R"doc(Start video grabbing

Prefer using `with irimager: ...` to automatically start/stop
streaming on errors.

Throws:
    RuntimeError if streaming cannot be started, e.g. if the camera is
    not connected.)doc";

static const char *__doc_IRImager_stop_streaming = R"doc(Stop video grabbing)doc";

static const char *__doc_Logger =
R"doc(Handles converting C++ logs to Python :py:class:`logging.Logger`.

After you instantiate an object of this class, all spdlogs will no
longer be printed to ``stderr``. Instead, they'll go to callback
you've defined, or a :py:class:`logging.Logger`.

Additionally, evo::IRLogger logs will also be captured.

Only a single instance of this object can exist at a time. You must
destroy existing instances to create a new instance.)doc";

static const char *__doc_Logger_Logger = R"doc(Creates a new logger with a custom logging callback.)doc";

static const char *__doc_Logger_Logger_2 =
R"doc(Creates a new logger using a custom Python :py:class:`logging.Logger`
object)doc";

static const char *__doc_Logger_Logger_3 =
R"doc(Creates a new logger using the default Python
:py:class:`logging.Logger`)doc";

static const char *__doc_Logger_impl = R"doc(pImpl implementation)doc";

static const char *__doc_Logger_pImpl = R"doc()doc";

#if defined(__GNUG__)
#pragma GCC diagnostic pop
#endif

