# Install script for directory: /home/mareike/Code/ecc_python/EpipolarConsistency/code/LibEpipolarConsistency

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "../export")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/LibEpipolarConsistency" TYPE FILE FILES
    "/home/mareike/Code/ecc_python/EpipolarConsistency/code/LibEpipolarConsistency/EpipolarConsistencyCommon.hxx"
    "/home/mareike/Code/ecc_python/EpipolarConsistency/code/LibEpipolarConsistency/EpipolarConsistency.h"
    "/home/mareike/Code/ecc_python/EpipolarConsistency/code/LibEpipolarConsistency/EpipolarConsistencyDirect.h"
    "/home/mareike/Code/ecc_python/EpipolarConsistency/code/LibEpipolarConsistency/RectifiedFBCC.h"
    "/home/mareike/Code/ecc_python/EpipolarConsistency/code/LibEpipolarConsistency/RadonIntermediate.h"
    "/home/mareike/Code/ecc_python/EpipolarConsistency/code/LibEpipolarConsistency/EpipolarConsistencyRadonIntermediate.h"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE STATIC_LIBRARY FILES "/home/mareike/Code/ecc_python/EpipolarConsistency/build/LibEpipolarConsistency/libLibEpipolarConsistency.a")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/cmake/LibEpipolarConsistency-targets.cmake")
    file(DIFFERENT EXPORT_FILE_CHANGED FILES
         "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/cmake/LibEpipolarConsistency-targets.cmake"
         "/home/mareike/Code/ecc_python/EpipolarConsistency/build/LibEpipolarConsistency/CMakeFiles/Export/cmake/LibEpipolarConsistency-targets.cmake")
    if(EXPORT_FILE_CHANGED)
      file(GLOB OLD_CONFIG_FILES "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/cmake/LibEpipolarConsistency-targets-*.cmake")
      if(OLD_CONFIG_FILES)
        message(STATUS "Old export file \"$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/cmake/LibEpipolarConsistency-targets.cmake\" will be replaced.  Removing files [${OLD_CONFIG_FILES}].")
        file(REMOVE ${OLD_CONFIG_FILES})
      endif()
    endif()
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/cmake" TYPE FILE FILES "/home/mareike/Code/ecc_python/EpipolarConsistency/build/LibEpipolarConsistency/CMakeFiles/Export/cmake/LibEpipolarConsistency-targets.cmake")
  if("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^()$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/cmake" TYPE FILE FILES "/home/mareike/Code/ecc_python/EpipolarConsistency/build/LibEpipolarConsistency/CMakeFiles/Export/cmake/LibEpipolarConsistency-targets-noconfig.cmake")
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/LibEpipolarConsistency/Gui" TYPE FILE FILES
    "/home/mareike/Code/ecc_python/EpipolarConsistency/code/LibEpipolarConsistency/Gui/PreProccess.h"
    "/home/mareike/Code/ecc_python/EpipolarConsistency/code/LibEpipolarConsistency/Gui/ComputeRadonIntermediate.hxx"
    "/home/mareike/Code/ecc_python/EpipolarConsistency/code/LibEpipolarConsistency/Gui/Visualization.h"
    "/home/mareike/Code/ecc_python/EpipolarConsistency/code/LibEpipolarConsistency/Gui/DisplayGeometry.hxx"
    "/home/mareike/Code/ecc_python/EpipolarConsistency/code/LibEpipolarConsistency/Gui/SingleImageMotion.hxx"
    "/home/mareike/Code/ecc_python/EpipolarConsistency/code/LibEpipolarConsistency/Gui/FDCTMotionCorrection.hxx"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE STATIC_LIBRARY FILES "/home/mareike/Code/ecc_python/EpipolarConsistency/build/LibEpipolarConsistency/libLibEpipolarConsistencyGui.a")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/cmake/LibEpipolarConsistencyGui-targets.cmake")
    file(DIFFERENT EXPORT_FILE_CHANGED FILES
         "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/cmake/LibEpipolarConsistencyGui-targets.cmake"
         "/home/mareike/Code/ecc_python/EpipolarConsistency/build/LibEpipolarConsistency/CMakeFiles/Export/cmake/LibEpipolarConsistencyGui-targets.cmake")
    if(EXPORT_FILE_CHANGED)
      file(GLOB OLD_CONFIG_FILES "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/cmake/LibEpipolarConsistencyGui-targets-*.cmake")
      if(OLD_CONFIG_FILES)
        message(STATUS "Old export file \"$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/cmake/LibEpipolarConsistencyGui-targets.cmake\" will be replaced.  Removing files [${OLD_CONFIG_FILES}].")
        file(REMOVE ${OLD_CONFIG_FILES})
      endif()
    endif()
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/cmake" TYPE FILE FILES "/home/mareike/Code/ecc_python/EpipolarConsistency/build/LibEpipolarConsistency/CMakeFiles/Export/cmake/LibEpipolarConsistencyGui-targets.cmake")
  if("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^()$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/cmake" TYPE FILE FILES "/home/mareike/Code/ecc_python/EpipolarConsistency/build/LibEpipolarConsistency/CMakeFiles/Export/cmake/LibEpipolarConsistencyGui-targets-noconfig.cmake")
  endif()
endif()

