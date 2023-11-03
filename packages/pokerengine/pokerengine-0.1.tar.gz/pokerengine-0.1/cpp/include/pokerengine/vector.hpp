//
// Created by copper_boy on 10/9/23.
//

#ifndef POKERENGINE_VECTOR_HPP
#define POKERENGINE_VECTOR_HPP

#include <stdexcept>
#include <vector>

#include "pokerengine.hpp"

namespace pokerengine {
template < typename T >
auto operator+=(std::vector< T > &lhs, const std::vector< T > &rhs) -> std::vector< T > & {
    lhs.reserve(rhs.size());
    if (lhs.size() < rhs.size()) {
        do {
            lhs.push_back(T{});
        } while (lhs.size() < rhs.size());
    }

    for (size_t i = 0; i < lhs.size(); i++) {
        lhs[i] += rhs[i];
    }

    return lhs;
}

template < typename T >
auto operator+(const std::vector< T > &lhs, const std::vector< T > &rhs) -> std::vector< T > {
    std::vector< T > result(lhs.cbegin(), lhs.cend());
    result += rhs;

    return result;
}
} // namespace pokerengine

#endif // POKERENGINE_VECTOR_HPP
