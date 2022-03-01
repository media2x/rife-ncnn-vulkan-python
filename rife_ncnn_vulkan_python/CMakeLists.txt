cmake_policy(SET CMP0091 NEW)
set(CMAKE_POLICY_DEFAULT_CMP0091 NEW)
set(CMAKE_MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>")

project(rife-ncnn-vulkan-python)

cmake_minimum_required(VERSION 3.9)

set(CMAKE_BUILD_TYPE Release)

option(USE_SYSTEM_NCNN "build with system libncnn" OFF)
option(USE_STATIC_MOLTENVK "link moltenvk static library" OFF)

find_package(Threads)
find_package(OpenMP)
find_package(Vulkan REQUIRED)

# Python
if(${CMAKE_VERSION} VERSION_LESS "3.15")
  find_package(Python REQUIRED)
else()
  find_package(Python REQUIRED COMPONENTS Development)
endif()

# SWIG
find_package(SWIG REQUIRED COMPONENTS python)
if(SWIG_FOUND)
  message("SWIG found: ${SWIG_EXECUTABLE}")
  include(${SWIG_USE_FILE})
endif()

macro(rife_add_shader SHADER_SRC)
  get_filename_component(SHADER_SRC_NAME_WE ${SHADER_SRC} NAME_WE)
  set(SHADER_COMP_HEADER
      ${CMAKE_CURRENT_BINARY_DIR}/rife-ncnn-vulkan/src/${SHADER_SRC_NAME_WE}.comp.hex.h
  )

  add_custom_command(
    OUTPUT ${SHADER_COMP_HEADER}
    COMMAND
      ${CMAKE_COMMAND}
      -DSHADER_SRC=${CMAKE_CURRENT_SOURCE_DIR}/rife-ncnn-vulkan/src/${SHADER_SRC}
      -DSHADER_COMP_HEADER=${SHADER_COMP_HEADER} -P
      "${CMAKE_CURRENT_SOURCE_DIR}/rife-ncnn-vulkan/src/generate_shader_comp_header.cmake"
    DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/rife-ncnn-vulkan/src/${SHADER_SRC}
    COMMENT "Preprocessing shader source ${SHADER_SRC_NAME_WE}.comp"
    VERBATIM)
  set_source_files_properties(${SHADER_COMP_HEADER} PROPERTIES GENERATED TRUE)

  list(APPEND SHADER_SPV_HEX_FILES ${SHADER_COMP_HEADER})
endmacro()

include_directories(${CMAKE_CURRENT_BINARY_DIR}/rife-ncnn-vulkan/src)
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/rife-ncnn-vulkan/src)
include_directories(.)

if(OPENMP_FOUND)
  set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
  set(CMAKE_EXE_LINKER_FLAGS
      "${CMAKE_EXE_LINKER_FLAGS} ${OpenMP_EXE_LINKER_FLAGS}")
endif()

# enable global link time optimization
cmake_policy(SET CMP0069 NEW)
set(CMAKE_POLICY_DEFAULT_CMP0069 NEW)
include(CheckIPOSupported)
check_ipo_supported(RESULT ipo_supported OUTPUT ipo_supported_output)
if(ipo_supported)
  set(CMAKE_INTERPROCEDURAL_OPTIMIZATION TRUE)
else()
  message(WARNING "IPO is not supported: ${ipo_supported_output}")
endif()

if(USE_SYSTEM_NCNN)
  set(GLSLANG_TARGET_DIR
      "GLSLANG-NOTFOUND"
      CACHE PATH "Absolute path to glslangTargets.cmake directory")
  if(NOT GLSLANG_TARGET_DIR AND NOT DEFINED ENV{GLSLANG_TARGET_DIR})
    message(
      WARNING
        "GLSLANG_TARGET_DIR must be defined! USE_SYSTEM_NCNN will be turned off."
    )
    set(USE_SYSTEM_NCNN OFF)
  else()
    message(STATUS "Using glslang install located at ${GLSLANG_TARGET_DIR}")

    find_package(Threads)

    include("${GLSLANG_TARGET_DIR}/OSDependentTargets.cmake")
    include("${GLSLANG_TARGET_DIR}/OGLCompilerTargets.cmake")
    if(EXISTS "${GLSLANG_TARGET_DIR}/HLSLTargets.cmake")
      # hlsl support can be optional
      include("${GLSLANG_TARGET_DIR}/HLSLTargets.cmake")
    endif()
    include("${GLSLANG_TARGET_DIR}/glslangTargets.cmake")
    include("${GLSLANG_TARGET_DIR}/SPIRVTargets.cmake")

    if(NOT TARGET glslang OR NOT TARGET SPIRV)
      message(
        WARNING
          "glslang or SPIRV target not found! USE_SYSTEM_NCNN will be turned off."
      )
      set(USE_SYSTEM_NCNN OFF)
    endif()
  endif()
endif()

if(USE_SYSTEM_NCNN)
  find_package(ncnn)
  if(NOT TARGET ncnn)
    message(
      WARNING "ncnn target not found! USE_SYSTEM_NCNN will be turned off.")
    set(USE_SYSTEM_NCNN OFF)
  endif()
endif()

if(NOT USE_SYSTEM_NCNN)
  # build ncnn library
  if(NOT EXISTS
     "${CMAKE_CURRENT_SOURCE_DIR}/rife-ncnn-vulkan/src/ncnn/CMakeLists.txt")
    message(
      FATAL_ERROR
        "The submodules were not downloaded! Please update submodules with \"git submodule update --init --recursive\" and try again."
    )
  endif()

  option(NCNN_INSTALL_SDK "" OFF)
  option(NCNN_PIXEL_ROTATE "" OFF)
  option(NCNN_PIXEL_AFFINE "" OFF)
  option(NCNN_PIXEL_DRAWING "" OFF)
  option(NCNN_VULKAN "" ON)
  option(NCNN_VULKAN_ONLINE_SPIRV "" ON)
  option(NCNN_BUILD_BENCHMARK "" OFF)
  option(NCNN_BUILD_TESTS "" OFF)
  option(NCNN_BUILD_TOOLS "" OFF)
  option(NCNN_BUILD_EXAMPLES "" OFF)
  option(NCNN_DISABLE_RTTI "" ON)
  option(NCNN_DISABLE_EXCEPTION "" ON)
  option(NCNN_INT8 "" OFF)

  option(WITH_LAYER_absval "" OFF)
  option(WITH_LAYER_argmax "" OFF)
  option(WITH_LAYER_batchnorm "" OFF)
  option(WITH_LAYER_bias "" OFF)
  option(WITH_LAYER_bnll "" OFF)
  option(WITH_LAYER_concat "" ON)
  option(WITH_LAYER_convolution "" ON)
  option(WITH_LAYER_crop "" ON)
  option(WITH_LAYER_deconvolution "" ON)
  option(WITH_LAYER_dropout "" OFF)
  option(WITH_LAYER_eltwise "" OFF)
  option(WITH_LAYER_elu "" OFF)
  option(WITH_LAYER_embed "" OFF)
  option(WITH_LAYER_exp "" OFF)
  option(WITH_LAYER_flatten "" ON)
  option(WITH_LAYER_innerproduct "" ON)
  option(WITH_LAYER_input "" ON)
  option(WITH_LAYER_log "" OFF)
  option(WITH_LAYER_lrn "" OFF)
  option(WITH_LAYER_memorydata "" OFF)
  option(WITH_LAYER_mvn "" OFF)
  option(WITH_LAYER_pooling "" ON)
  option(WITH_LAYER_power "" OFF)
  option(WITH_LAYER_prelu "" ON)
  option(WITH_LAYER_proposal "" OFF)
  option(WITH_LAYER_reduction "" OFF)
  option(WITH_LAYER_relu "" ON)
  option(WITH_LAYER_reshape "" OFF)
  option(WITH_LAYER_roipooling "" OFF)
  option(WITH_LAYER_scale "" OFF)
  option(WITH_LAYER_sigmoid "" ON)
  option(WITH_LAYER_slice "" ON)
  option(WITH_LAYER_softmax "" OFF)
  option(WITH_LAYER_split "" ON)
  option(WITH_LAYER_spp "" OFF)
  option(WITH_LAYER_tanh "" OFF)
  option(WITH_LAYER_threshold "" OFF)
  option(WITH_LAYER_tile "" OFF)
  option(WITH_LAYER_rnn "" OFF)
  option(WITH_LAYER_lstm "" OFF)
  option(WITH_LAYER_binaryop "" ON)
  option(WITH_LAYER_unaryop "" ON)
  option(WITH_LAYER_convolutiondepthwise "" OFF)
  option(WITH_LAYER_padding "" ON)
  option(WITH_LAYER_squeeze "" OFF)
  option(WITH_LAYER_expanddims "" OFF)
  option(WITH_LAYER_normalize "" OFF)
  option(WITH_LAYER_permute "" OFF)
  option(WITH_LAYER_priorbox "" OFF)
  option(WITH_LAYER_detectionoutput "" OFF)
  option(WITH_LAYER_interp "" ON)
  option(WITH_LAYER_deconvolutiondepthwise "" OFF)
  option(WITH_LAYER_shufflechannel "" OFF)
  option(WITH_LAYER_instancenorm "" OFF)
  option(WITH_LAYER_clip "" ON)
  option(WITH_LAYER_reorg "" OFF)
  option(WITH_LAYER_yolodetectionoutput "" OFF)
  option(WITH_LAYER_quantize "" OFF)
  option(WITH_LAYER_dequantize "" OFF)
  option(WITH_LAYER_yolov3detectionoutput "" OFF)
  option(WITH_LAYER_psroipooling "" OFF)
  option(WITH_LAYER_roialign "" OFF)
  option(WITH_LAYER_packing "" ON)
  option(WITH_LAYER_requantize "" OFF)
  option(WITH_LAYER_cast "" ON)
  option(WITH_LAYER_hardsigmoid "" OFF)
  option(WITH_LAYER_selu "" OFF)
  option(WITH_LAYER_hardswish "" OFF)
  option(WITH_LAYER_noop "" OFF)
  option(WITH_LAYER_pixelshuffle "" ON)
  option(WITH_LAYER_deepcopy "" OFF)
  option(WITH_LAYER_mish "" OFF)
  option(WITH_LAYER_statisticspooling "" OFF)
  option(WITH_LAYER_swish "" OFF)
  option(WITH_LAYER_gemm "" OFF)
  option(WITH_LAYER_groupnorm "" OFF)
  option(WITH_LAYER_layernorm "" OFF)
  option(WITH_LAYER_softplus "" OFF)
  option(WITH_LAYER_gru "" OFF)
  option(WITH_LAYER_multiheadattention "" OFF)
  option(WITH_LAYER_gelu "" OFF)

  add_subdirectory("rife-ncnn-vulkan/src/ncnn")
endif()

rife_add_shader(rife_preproc.comp)
rife_add_shader(rife_postproc.comp)
rife_add_shader(rife_preproc_tta.comp)
rife_add_shader(rife_postproc_tta.comp)
rife_add_shader(rife_flow_tta_avg.comp)
rife_add_shader(rife_v2_flow_tta_avg.comp)
rife_add_shader(rife_flow_tta_temporal_avg.comp)
rife_add_shader(rife_v2_flow_tta_temporal_avg.comp)
rife_add_shader(rife_out_tta_temporal_avg.comp)
rife_add_shader(rife_v4_timestep.comp)
rife_add_shader(warp.comp)
rife_add_shader(warp_pack4.comp)
rife_add_shader(warp_pack8.comp)

add_custom_target(generate-spirv DEPENDS ${SHADER_SPV_HEX_FILES})

set(RIFE_LINK_LIBRARIES ncnn ${Vulkan_LIBRARY})

if(USE_STATIC_MOLTENVK)
  find_library(CoreFoundation NAMES CoreFoundation)
  find_library(Foundation NAMES Foundation)
  find_library(Metal NAMES Metal)
  find_library(QuartzCore NAMES QuartzCore)
  find_library(CoreGraphics NAMES CoreGraphics)
  find_library(Cocoa NAMES Cocoa)
  find_library(IOKit NAMES IOKit)
  find_library(IOSurface NAMES IOSurface)

  list(
    APPEND
    RIFE_LINK_LIBRARIES
    ${Metal}
    ${QuartzCore}
    ${CoreGraphics}
    ${Cocoa}
    ${IOKit}
    ${IOSurface}
    ${Foundation}
    ${CoreFoundation})
endif()

# target_link_libraries(rife-ncnn-vulkan ${RIFE_LINK_LIBRARIES})

set(UseSWIG_TARGET_NAME_PREFERENCE STANDARD)
set_property(SOURCE rife.i PROPERTY CPLUSPLUS ON DEPENDS generate-spirv)

# set output directory for the .py file
set_property(SOURCE rife.i PROPERTY OUTFILE_DIR ${CMAKE_CURRENT_BINARY_DIR})
set_property(
  SOURCE rife.i PROPERTY OUTPUT_DIR
                         ${CMAKE_CURRENT_BINARY_DIR}/rife_ncnn_vulkan_python)

swig_add_library(
  rife_ncnn_vulkan_wrapper
  TYPE MODULE
  LANGUAGE python
  SOURCES rife.i
          rife-ncnn-vulkan/src/rife.cpp
          rife-ncnn-vulkan/src/warp.cpp
          rife_wrapped.cpp
          OUTPUT_DIR
          ${CMAKE_CURRENT_BINARY_DIR}/rife_ncnn_vulkan_python
          OUTFILE_DIR
          ${CMAKE_CURRENT_BINARY_DIR}/rife_ncnn_vulkan_python)

add_dependencies(rife_ncnn_vulkan_wrapper generate-spirv)
target_compile_options(rife_ncnn_vulkan_wrapper PUBLIC -fexceptions)

# set output directory of the .so file
if(CALL_FROM_SETUP_PY)
  set_target_properties(
    rife_ncnn_vulkan_wrapper PROPERTIES LIBRARY_OUTPUT_DIRECTORY
                                        ${CMAKE_INSTALL_PREFIX})
else()
  set_target_properties(
    rife_ncnn_vulkan_wrapper
    PROPERTIES LIBRARY_OUTPUT_DIRECTORY
               ${CMAKE_CURRENT_BINARY_DIR}/rife_ncnn_vulkan_python)
endif()

if(${CMAKE_VERSION} VERSION_LESS "3.15")
  include_directories(${PYTHON_INCLUDE_DIRS})
  target_link_libraries(rife_ncnn_vulkan_wrapper ${RIFE_LINK_LIBRARIES}
                        ${PYTHON_LIBRARIES})
else()
  target_link_libraries(rife_ncnn_vulkan_wrapper ${RIFE_LINK_LIBRARIES}
                        Python::Module)
endif()

# Get the autogenerated Python file
get_property(
  WRAPPER_PY_FILE
  TARGET rife_ncnn_vulkan_wrapper
  PROPERTY SWIG_SUPPORT_FILES)

if(CALL_FROM_SETUP_PY)
  # Install the autogenerated Python file
  install(FILES ${WRAPPER_PY_FILE} DESTINATION ${CMAKE_INSTALL_PREFIX})

  install(TARGETS rife_ncnn_vulkan_wrapper
          LIBRARY DESTINATION ${CMAKE_INSTALL_PREFIX})
  install(DIRECTORY rife-ncnn-vulkan/models DESTINATION ${CMAKE_INSTALL_PREFIX})
  install(FILES rife_ncnn_vulkan.py DESTINATION ${CMAKE_INSTALL_PREFIX})
else()
  file(COPY rife-ncnn-vulkan/models
       DESTINATION ${CMAKE_CURRENT_BINARY_DIR}/rife_ncnn_vulkan_python)
  file(COPY rife_ncnn_vulkan.py
       DESTINATION ${CMAKE_CURRENT_BINARY_DIR}/rife_ncnn_vulkan_python)
endif()
