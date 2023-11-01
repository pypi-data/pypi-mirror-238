file(GLOB_RECURSE DATE_SOURCES
        **.cpp
        **.h
)

target_sources(python_quant_lib
    PRIVATE
        ${DATE_SOURCES}
)