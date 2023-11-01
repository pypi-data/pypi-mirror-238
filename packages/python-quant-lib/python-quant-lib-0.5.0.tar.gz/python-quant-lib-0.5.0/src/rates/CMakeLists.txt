file(GLOB_RECURSE RATES_SOURCES
        **.cpp
        **.h
)

target_sources(python_quant_lib
    PRIVATE
        ${RATES_SOURCES}
)