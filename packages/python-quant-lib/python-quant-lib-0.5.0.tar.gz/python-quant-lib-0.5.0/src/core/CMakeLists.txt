file(GLOB_RECURSE CORE_SOURCES
        **.cpp
        **.h
)

target_sources(python_quant_lib
    PRIVATE
        ${CORE_SOURCES}
)