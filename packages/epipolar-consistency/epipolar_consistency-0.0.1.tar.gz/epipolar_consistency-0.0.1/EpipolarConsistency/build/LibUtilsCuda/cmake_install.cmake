# Install script for directory: /home/mareike/Code/ecc_python/EpipolarConsistency/code/LibUtilsCuda

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
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/LibUtilsCuda" TYPE FILE FILES
    "/home/mareike/Code/ecc_python/EpipolarConsistency/code/LibUtilsCuda/UtilsCuda.hxx"
    "/home/mareike/Code/ecc_python/EpipolarConsistency/code/LibUtilsCuda/CudaTextureArray.hxx"
    "/home/mareike/Code/ecc_python/EpipolarConsistency/code/LibUtilsCuda/CudaMemory.h"
    "/home/mareike/Code/ecc_python/EpipolarConsistency/code/LibUtilsCuda/CudaAlgorithms.h"
    "/home/mareike/Code/ecc_python/EpipolarConsistency/code/LibUtilsCuda/CudaBindlessTexture.h"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE STATIC_LIBRARY FILES "/home/mareike/Code/ecc_python/EpipolarConsistency/build/LibUtilsCuda/libLibUtilsCuda.a")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/cmake/LibUtilsCuda-targets.cmake")
    file(DIFFERENT EXPORT_FILE_CHANGED FILES
         "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/cmake/LibUtilsCuda-targets.cmake"
         "/home/mareike/Code/ecc_python/EpipolarConsistency/build/LibUtilsCuda/CMakeFiles/Export/cmake/LibUtilsCuda-targets.cmake")
    if(EXPORT_FILE_CHANGED)
      file(GLOB OLD_CONFIG_FILES "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/cmake/LibUtilsCuda-targets-*.cmake")
      if(OLD_CONFIG_FILES)
        message(STATUS "Old export file \"$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/cmake/LibUtilsCuda-targets.cmake\" will be replaced.  Removing files [${OLD_CONFIG_FILES}].")
        file(REMOVE ${OLD_CONFIG_FILES})
      endif()
    endif()
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/cmake" TYPE FILE FILES "/home/mareike/Code/ecc_python/EpipolarConsistency/build/LibUtilsCuda/CMakeFiles/Export/cmake/LibUtilsCuda-targets.cmake")
  if("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^()$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/cmake" TYPE FILE FILES "/home/mareike/Code/ecc_python/EpipolarConsistency/build/LibUtilsCuda/CMakeFiles/Export/cmake/LibUtilsCuda-targets-noconfig.cmake")
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/LibUtilsCuda/culaut" TYPE FILE FILES
    "/home/mareike/Code/ecc_python/EpipolarConsistency/code/LibUtilsCuda/culaut/culaut.hxx"
    "/home/mareike/Code/ecc_python/EpipolarConsistency/code/LibUtilsCuda/culaut/xgeinv.hxx"
    "/home/mareike/Code/ecc_python/EpipolarConsistency/code/LibUtilsCuda/culaut/xprojectionmatrix.hxx"
    )
endif()

