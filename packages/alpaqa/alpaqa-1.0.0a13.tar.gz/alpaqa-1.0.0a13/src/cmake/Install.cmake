include(GNUInstallDirs)
include(${PROJECT_SOURCE_DIR}/cmake/Debug.cmake)

set(ALPAQA_INSTALL_CMAKEDIR "${CMAKE_INSTALL_LIBDIR}/cmake/alpaqa"
    CACHE STRING "Installation directory for CMake configuration files")
set(ALPAQA_INSTALL_BINDIR "${CMAKE_INSTALL_BINDIR}"
    CACHE STRING "Installation directory for binaries and DLLs")
set(ALPAQA_INSTALL_LIBDIR "${CMAKE_INSTALL_LIBDIR}"
    CACHE STRING "Installation directory for archives and libraries")
set(ALPAQA_INSTALL_INCLUDEDIR "${CMAKE_INSTALL_INCLUDEDIR}"
    CACHE STRING "Installation directory for headers")

# Set the runtime linker/loader search paths to make alpaqa stand-alone
if (ALPAQA_STANDALONE)
    cmake_path(RELATIVE_PATH ALPAQA_INSTALL_LIBDIR
               BASE_DIRECTORY ALPAQA_INSTALL_BINDIR
               OUTPUT_VARIABLE ALPAQA_INSTALL_LIBRELBINDIR)
    foreach (TGT IN LISTS ALPAQA_INSTALL_TARGETS ALPAQA_INSTALL_EXE)
        set_target_properties(${TGT} PROPERTIES
            INSTALL_RPATH "$ORIGIN;$ORIGIN/${ALPAQA_INSTALL_LIBRELBINDIR}")
    endforeach()
endif()

# Add the alpaqa library to the "export-set", install the library files
message(STATUS "Targets to install: ${ALPAQA_INSTALL_TARGETS};${ALPAQA_INSTALL_EXE}")
install(TARGETS ${ALPAQA_INSTALL_TARGETS} warnings
    EXPORT alpaqaTargets
    RUNTIME DESTINATION "${ALPAQA_INSTALL_BINDIR}"
        COMPONENT shlib
    LIBRARY DESTINATION "${ALPAQA_INSTALL_LIBDIR}"
        COMPONENT shlib
        NAMELINK_COMPONENT dev
    ARCHIVE DESTINATION "${ALPAQA_INSTALL_LIBDIR}" 
        COMPONENT dev)
# Executables
install(TARGETS ${ALPAQA_INSTALL_EXE}
    EXPORT alpaqaTargets
    RUNTIME DESTINATION "${ALPAQA_INSTALL_BINDIR}"
        COMPONENT bin)

# Install the header files
install(FILES "${PROJECT_BINARY_DIR}/include/alpaqa-version.h"
    DESTINATION "${ALPAQA_INSTALL_INCLUDEDIR}"
        COMPONENT dev)
install(DIRECTORY "${PROJECT_SOURCE_DIR}/src/alpaqa/include/"
    DESTINATION "${ALPAQA_INSTALL_INCLUDEDIR}"
        COMPONENT dev
    FILES_MATCHING REGEX "/.*\.(h|[hti]pp)$")
install(DIRECTORY "${PROJECT_SOURCE_DIR}/src/interop/casadi/include/"
    DESTINATION "${ALPAQA_INSTALL_INCLUDEDIR}"
        COMPONENT dev
    FILES_MATCHING REGEX "/.*\.(h|[hti]pp)$")
install(DIRECTORY "${PROJECT_SOURCE_DIR}/src/interop/ipopt/include/"
    DESTINATION "${ALPAQA_INSTALL_INCLUDEDIR}"
        COMPONENT dev
    FILES_MATCHING REGEX "/.*\.(h|[hti]pp)$")
install(DIRECTORY "${PROJECT_SOURCE_DIR}/src/interop/lbfgsb/include/"
    DESTINATION "${ALPAQA_INSTALL_INCLUDEDIR}"
        COMPONENT dev
    FILES_MATCHING REGEX "/.*\.(h|[hti]pp)$")
install(DIRECTORY "${PROJECT_SOURCE_DIR}/src/interop/dl/include/"
    DESTINATION "${ALPAQA_INSTALL_INCLUDEDIR}"
        COMPONENT dev
    FILES_MATCHING REGEX "/.*\.(h|[hti]pp)$")
install(DIRECTORY "${PROJECT_SOURCE_DIR}/src/interop/dl-api/include/"
    DESTINATION "${ALPAQA_INSTALL_INCLUDEDIR}"
        COMPONENT dl_dev
    FILES_MATCHING REGEX "/.*\.(h|[hti]pp)$")
install(DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}/export/alpaqa"
    DESTINATION "${ALPAQA_INSTALL_INCLUDEDIR}"
        COMPONENT dev
    FILES_MATCHING REGEX "/.*\.(h|[hti]pp)$")

# Install the debug files
foreach(target IN LISTS ALPAQA_INSTALL_TARGETS ALPAQA_INSTALL_EXE)
    get_target_property(target_type ${target} TYPE)
    if (${target_type} STREQUAL "SHARED_LIBRARY")
        alpaqa_install_debug_syms(${target} debug
                                  ${ALPAQA_INSTALL_LIBDIR}
                                  ${ALPAQA_INSTALL_BINDIR})
    elseif (${target_type} STREQUAL "EXECUTABLE")
        alpaqa_install_debug_syms(${target} debug
                                  ${ALPAQA_INSTALL_BINDIR}
                                  ${ALPAQA_INSTALL_BINDIR})
    endif()
endforeach()

# Install the export set for use with the install tree
install(EXPORT alpaqaTargets 
    FILE alpaqaTargets.cmake
    DESTINATION "${ALPAQA_INSTALL_CMAKEDIR}" 
        COMPONENT dev
    NAMESPACE alpaqa::)

# Generate the config file that includes the exports
include(CMakePackageConfigHelpers)
configure_package_config_file(
    "${CMAKE_CURRENT_SOURCE_DIR}/cmake/Config.cmake.in"
    "${PROJECT_BINARY_DIR}/alpaqaConfig.cmake"
    INSTALL_DESTINATION "${ALPAQA_INSTALL_CMAKEDIR}"
    NO_SET_AND_CHECK_MACRO
    NO_CHECK_REQUIRED_COMPONENTS_MACRO)
write_basic_package_version_file(
    "${PROJECT_BINARY_DIR}/alpaqaConfigVersion.cmake"
    VERSION "${PROJECT_VERSION}"
    COMPATIBILITY SameMajorVersion)

# Install the alpaqaConfig.cmake and alpaqaConfigVersion.cmake
install(FILES
    "${PROJECT_BINARY_DIR}/alpaqaConfig.cmake"
    "${PROJECT_BINARY_DIR}/alpaqaConfigVersion.cmake"
    DESTINATION "${ALPAQA_INSTALL_CMAKEDIR}" 
        COMPONENT dev)

# Add all targets to the build tree export set
export(EXPORT alpaqaTargets
    FILE "${PROJECT_BINARY_DIR}/alpaqaTargets.cmake"
    NAMESPACE alpaqa::)
