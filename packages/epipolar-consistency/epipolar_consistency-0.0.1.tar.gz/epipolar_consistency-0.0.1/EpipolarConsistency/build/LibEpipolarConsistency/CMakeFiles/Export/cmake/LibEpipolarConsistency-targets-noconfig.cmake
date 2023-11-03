#----------------------------------------------------------------
# Generated CMake target import file.
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "LibEpipolarConsistency" for configuration ""
set_property(TARGET LibEpipolarConsistency APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(LibEpipolarConsistency PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_NOCONFIG "CXX"
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/lib/libLibEpipolarConsistency.a"
  )

list(APPEND _IMPORT_CHECK_TARGETS LibEpipolarConsistency )
list(APPEND _IMPORT_CHECK_FILES_FOR_LibEpipolarConsistency "${_IMPORT_PREFIX}/lib/libLibEpipolarConsistency.a" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
