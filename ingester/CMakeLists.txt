
cmake_minimum_required(VERSION 3.10)
project(pdf_ingest)

set(CMAKE_CXX_STANDARD 17)

find_package(PkgConfig REQUIRED)
pkg_check_modules(POPPLER REQUIRED poppler-cpp)

include_directories(${POPPLER_INCLUDE_DIRS})
link_directories(${POPPLER_LIBRARY_DIRS})

add_executable(pdf_ingest src/main.cpp)
target_link_libraries(pdf_ingest ${POPPLER_LIBRARIES})
