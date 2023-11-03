#----------------------------------------------------------------
# Generated CMake target import file.
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "LibProjectiveGeometry" for configuration ""
set_property(TARGET LibProjectiveGeometry APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(LibProjectiveGeometry PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_NOCONFIG "CXX"
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/lib/libLibProjectiveGeometry.a"
  )

list(APPEND _IMPORT_CHECK_TARGETS LibProjectiveGeometry )
list(APPEND _IMPORT_CHECK_FILES_FOR_LibProjectiveGeometry "${_IMPORT_PREFIX}/lib/libLibProjectiveGeometry.a" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
