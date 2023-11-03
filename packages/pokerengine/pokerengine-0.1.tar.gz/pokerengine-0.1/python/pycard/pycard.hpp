//
// Created by copper_boy on 10/31/23.
//
#ifndef POKERENGINE_PYCARD_HPP
#define POKERENGINE_PYCARD_HPP

#include <pybind11/operators.h>

#include "card/card.hpp"

#include "python.hpp"

namespace python {
auto setup_pycard(py::module_ &module_) -> void {
    auto card = module_.def_submodule("card");

    py::class_< pokerengine::rank_abc >(card, "_RankRepresentationABC", py::module_local()); // NOLINT
    py::class_< pokerengine::rank, pokerengine::rank_abc >(card, "Rank", py::module_local())
                    .def(py::init< pokerengine::enums::rank_t >(), py::arg("value"))
                    .def(py::init< char >(), py::arg("value"))
                    .def(py::self == py::self) // NOLINT
                    .def(py::self != py::self) // NOLINT
                    .def(py::self > py::self)  // NOLINT
                    .def(py::self < py::self)  // NOLINT
                    .def("as_string", &pokerengine::rank::as_string)
                    .def("as_string_long", &pokerengine::rank::as_string_long)
                    .def("as_bitset", &pokerengine::rank::as_bitset)
                    .def_property_readonly("rank", &pokerengine::rank::get_value);

    py::class_< pokerengine::suit_abc >(card, "_SuitRepresentationABC", py::module_local()); // NOLINT
    py::class_< pokerengine::suit >(card, "Suit", py::module_local())
                    .def(py::init< pokerengine::enums::suit_t >(), py::arg("value"))
                    .def(py::init< char >(), py::arg("value"))
                    .def(py::self == py::self) // NOLINT
                    .def(py::self != py::self) // NOLINT
                    .def(py::self > py::self)  // NOLINT
                    .def(py::self < py::self)  // NOLINT
                    .def("as_string", &pokerengine::suit::as_string)
                    .def("as_string_pretty", &pokerengine::suit::as_string_pretty)
                    .def("as_string_long", &pokerengine::suit::as_string_long)
                    .def("as_bitset", &pokerengine::suit::as_bitset)
                    .def_property_readonly("suit", &pokerengine::suit::get_value);

    py::class_< pokerengine::card >(card, "Card", py::module_local())
                    .def(py::init< const pokerengine::rank &, const pokerengine::suit & >())
                    .def(py::init< pokerengine::enums::rank_t, pokerengine::enums::suit_t >())
                    .def(py::init< uint8_t >())
                    .def(py::init< std::string_view >())
                    .def(py::self == py::self) // NOLINT
                    .def(py::self != py::self) // NOLINT
                    .def(py::self > py::self)  // NOLINT
                    .def(py::self < py::self)  // NOLINT
                    .def("as_bitset", &pokerengine::card::as_bitset)
                    .def("as_string", &pokerengine::card::as_string)
                    .def_property_readonly("card", &pokerengine::card::get_card)
                    .def_property_readonly("rank", &pokerengine::card::get_rank)
                    .def_property_readonly("suit", &pokerengine::card::get_suit);

    py::class_< pokerengine::card_set >(card, "CardSet", py::module_local())
                    .def(py::init())
                    .def(py::init< const std::initializer_list< const pokerengine::card > & >())
                    .def(py::init< uint64_t >())
                    .def(py::init< const std::span< const pokerengine::card > & >())
                    .def(py::init< std::string_view >())
                    .def("__len__", &pokerengine::card_set::size)
                    .def("__contains__",
                         [](pokerengine::card_set &self, const pokerengine::card &v) -> bool {
                             return self.contains(v);
                         })
                    .def("__contains__",
                         [](pokerengine::card_set &self, const pokerengine::card_set &v) -> bool {
                             return self.contains(v);
                         })
                    .def("combine",
                         [](pokerengine::card_set &self,
                            const pokerengine::card &v) -> pokerengine::card_set {
                        return self.combine(v);
                    })
                    .def("combine",
                         [](pokerengine::card_set &self, const pokerengine::card_set &v)
                                         -> pokerengine::card_set {
                        return self.combine(v);
                    })
                    .def("clear", &pokerengine::card_set::clear)
                    .def("fill", &pokerengine::card_set::fill)
                    .def("insert", &pokerengine::card_set::insert)
                    .def("join", &pokerengine::card_set::join)

                    .def("remove",
                         [](pokerengine::card_set &self, const pokerengine::card_set &v) -> void {
                             self.remove(v);
                         })
                    .def("remove",
                         [](pokerengine::card_set &self, const pokerengine::card_set &v) -> void {
                             self.remove(v);
                         })
                    .def_property("cards", &pokerengine::card_set::get_cards, &pokerengine::card_set::set_cards);

    py::class_< pokerengine::card_generator >(card, "CardGenerator", py::module_local())
                    .def(py::init< uint16_t >())
                    .def("generate", &pokerengine::card_generator::generate)
                    .def("generate_v", &pokerengine::card_generator::generate_v);
}
} // namespace python

#endif //POKERENGINE_PYCARD_HPP