#ifndef ENUMS_H
#define ENUMS_H

#include <string>

using namespace std;

namespace Enums {

template<typename T>
std::string enumToString(T enumValue) {
    return std::to_string(static_cast<std::underlying_type_t<T>>(enumValue));
};

}

#endif // ENUMS