SET(BINDINGS_NAME random_username_for_pip_package_toadharvard)

file(GLOB_RECURSE sources "*.h*" "*.cpp*")
pybind11_add_module(${BINDINGS_NAME} ${sources})
target_link_libraries(${BINDINGS_NAME} PRIVATE ${CMAKE_PROJECT_NAME}_lib)

if (PYTHON STREQUAL INSTALL)
    install(TARGETS ${BINDINGS_NAME} LIBRARY DESTINATION .)
endif()
