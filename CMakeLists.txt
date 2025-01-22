cmake_minimum_required(VERSION 3.29)
project(testfile)

set(CMAKE_CXX_STANDARD 20)

add_executable(testfile main.cpp
        testheader.h)
