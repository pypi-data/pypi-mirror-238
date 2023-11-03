//
// Created by copper_boy on 11/2/23.
//

#ifndef POKERENGINE_PYPLAYER_HPP
#define POKERENGINE_PYPLAYER_HPP

#include <pybind11/operators.h>
#include <pybind11/stl.h>

#include "engine/player.hpp"

#include "python.hpp"

namespace python {
auto setup_pyplayer(py::module_ &module_) -> void {
    auto player = module_.def_submodule("player");

    py::class_< pokerengine::player >(player, "Player", py::module_local())
                    .def(py::init< size_t, bool, int32_t, int32_t, int32_t, int32_t, pokerengine::enums::state_t >())
                    .def(py::self == py::self) // NOLINT
                    .def_readwrite("id", &pokerengine::player::id)
                    .def_readwrite("is_left", &pokerengine::player::is_left)
                    .def_readwrite("stack", &pokerengine::player::stack)
                    .def_readwrite("behind", &pokerengine::player::behind)
                    .def_readwrite("front", &pokerengine::player::front)
                    .def_readwrite("round_bet", &pokerengine::player::round_bet)
                    .def_readwrite("state", &pokerengine::player::state);
    py::class_< pokerengine::players_set >(player, "Players", py::module_local())
                    .def(py::init())
                    .def("get_player", &pokerengine::players_set::get_player)
                    .def("set_players", &pokerengine::players_set::set_players)
                    .def("add_player", &pokerengine::players_set::add_player)
                    .def("remove_player", &pokerengine::players_set::remove_player)
                    .def_property_readonly("players", &pokerengine::players_set::get_players);
}
} // namespace python

#endif // POKERENGINE_PYPLAYER_HPP
