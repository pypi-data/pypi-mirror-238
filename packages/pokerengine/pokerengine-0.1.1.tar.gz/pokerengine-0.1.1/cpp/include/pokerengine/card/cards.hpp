//
// Created by copper_boy on 7/4/23.
//

#ifndef POKERENGINE_CARDS_HPP
#define POKERENGINE_CARDS_HPP

#include <compare>
#include <set>
#include <span>
#include <stdexcept>
#include <string>
#include <type_traits>
#include <vector>

#include "card/card.hpp"
#include "card/hand.hpp"
#include "pokerengine.hpp"

namespace pokerengine {
namespace constants {
uint8_t BOARD_SIZE = 5;
} // namespace constants

class cards {
public:
    cards() = delete;

    cards(const std::vector< std::string > &board, const std::vector< std::string > &hands)
            : board_(board.begin(), board.end()), hands_(hands.begin(), hands.end()) {
        if (board_.size() > constants::BOARD_SIZE) {
            throw std::length_error{ "Board size in texas holdem poker must be less or equal than 5" };
        }

        if (board_.size() + hands_.size() !=
            std::set(board_.cbegin(), board_.cend()).size() + std::set(hands_.cbegin(), hands_.cend()).size()) {
            throw std::logic_error{ "Cards not unique" };
        }
    }

    auto operator<=>(const cards &other) const noexcept -> std::strong_ordering = default;

    [[nodiscard]] auto get_board_n(uint8_t n) -> std::span< card > {
        if (n > constants::BOARD_SIZE) {
            throw std::runtime_error{ "Index greater than " + std::to_string(constants::BOARD_SIZE) +
                                      " i.e. the board size" };
        }

        return std::span< card >{ board_.data(), n };
    }

    [[nodiscard]] auto get_board() const noexcept -> std::vector< card > {
        return board_;
    }

    [[nodiscard]] auto get_hands() const noexcept -> std::vector< hand > {
        return hands_;
    }

private:
    std::vector< card > board_;
    std::vector< hand > hands_;
};
} // namespace pokerengine

#endif // POKERENGINE_CARDS_HPP
