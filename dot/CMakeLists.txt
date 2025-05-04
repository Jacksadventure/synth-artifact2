cmake_minimum_required(VERSION 3.18)
project(dot_parser LANGUAGES CXX)

# ---------------------------------------------------------------------------
# ① 告诉 CMake Homebrew 的 package 位置
# ---------------------------------------------------------------------------
execute_process(COMMAND brew --prefix antlr4-cpp-runtime
                OUTPUT_VARIABLE ANTLR4_PREFIX
                OUTPUT_STRIP_TRAILING_WHITESPACE
                ERROR_QUIET)
if(ANTLR4_PREFIX)
  list(APPEND CMAKE_PREFIX_PATH "${ANTLR4_PREFIX}/lib/cmake/antlr4-runtime")
endif()

# ---------------------------------------------------------------------------
# ② 读取配置文件（一定要 CONFIG）
# ---------------------------------------------------------------------------
find_package(antlr4-runtime REQUIRED CONFIG)

# Homebrew 导出的两个目标：antlr4_static / antlr4_shared
# 任选其一；这里用静态库（更便携）
set(ANTLR_TARGET antlr4_static)

# ---------------------------------------------------------------------------
# ③ 源文件
# ---------------------------------------------------------------------------
set(GENERATED_SRC
    DOTBaseListener.cpp
    DOTLexer.cpp
    DOTListener.cpp
    DOTParser.cpp
)

add_executable(dot_parser
    main.cpp
    ErrorListener.h
    ${GENERATED_SRC}
)

# ---------------------------------------------------------------------------
# ④ 传递 include 路径 + 链接库
# ---------------------------------------------------------------------------
# include 目录：<brew_prefix>/include/antlr4-runtime
target_include_directories(dot_parser PRIVATE
    "${ANTLR4_PREFIX}/include/antlr4-runtime")

target_link_libraries(dot_parser PRIVATE ${ANTLR_TARGET})
target_compile_features(dot_parser PRIVATE cxx_std_17)