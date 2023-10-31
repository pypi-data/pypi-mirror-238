# GridCal
# Copyright (C) 2015 - 2023 Santiago Peñate Vera
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.


import numpy as np
import time

from GridCalEngine.Core.Devices.multi_circuit import MultiCircuit
from GridCalEngine.Simulations.NTC.ntc_opf import get_inter_areas_branches, run_linear_ntc_opf_ts
from GridCalEngine.Core.DataStructures.numerical_circuit import compile_numerical_circuit_at, NumericalCircuit
from GridCalEngine.Simulations.driver_types import SimulationTypes
from GridCalEngine.Simulations.driver_template import DriverTemplate
from GridCalEngine.Simulations.ATC.available_transfer_capacity_driver import compute_alpha
from GridCalEngine.Simulations.NTC.ntc_options import OptimalNetTransferCapacityOptions
from GridCalEngine.Simulations.NTC.ntc_results import OptimalNetTransferCapacityResults
from GridCalEngine.Simulations.ContingencyAnalysis.contingency_analysis_driver import ContingencyAnalysisDriver, \
    ContingencyAnalysisOptions
from GridCalEngine.Simulations.LinearFactors.linear_analysis import LinearAnalysis, LinearMultiContingencies
from GridCalEngine.basic_structures import SolverType
from GridCalEngine.basic_structures import Logger



class OptimalNetTransferCapacityDriver(DriverTemplate):
    name = 'Optimal net transfer capacity'
    tpe = SimulationTypes.OPF_NTC_run

    def __init__(self, grid: MultiCircuit, options: OptimalNetTransferCapacityOptions, pf_options: "PowerFlowOptions"):
        """
        PowerFlowDriver class constructor
        @param grid: MultiCircuit Object
        @param options: OPF options
        """
        DriverTemplate.__init__(self, grid=grid)

        # Options to use
        self.options = options
        self.pf_options = pf_options

        self.all_solved = True

        self.logger = Logger()

    def get_steps(self):
        """
        Get time steps list of strings
        """
        return list()

    def compute_exchange_sensitivity(self, linear, numerical_circuit: NumericalCircuit, with_n1=True):

        # compute the branch exchange sensitivity (alpha)
        return compute_alpha(
            ptdf=linear.PTDF,
            lodf=linear.LODF if with_n1 else None,
            P0=numerical_circuit.Sbus.real,
            Pinstalled=numerical_circuit.bus_installed_power,
            Pgen=numerical_circuit.generator_data.get_injections_per_bus()[:, 0].real,
            Pload=numerical_circuit.load_data.get_injections_per_bus()[:, 0].real,
            idx1=self.options.area_from_bus_idx,
            idx2=self.options.area_to_bus_idx,
            dT=self.options.sensitivity_dT,
            mode=self.options.transfer_method.value,
        )

    def opf(self):
        """
        Run a power flow for every circuit
        @return: OptimalPowerFlowResults object
        """

        self.progress_text.emit('Compiling...')

        contingency_flows_list = list()
        contingency_indices_list = list()
        contingency_gen_flows_list = list()
        contingency_gen_indices_list = list()
        contingency_hvdc_flows_list = list()
        contingency_hvdc_indices_list = list()

        contingency_branch_alpha_list = list()
        contingency_generation_alpha_list = list()
        contingency_hvdc_alpha_list = list()

        numerical_circuit = compile_numerical_circuit_at(
            circuit=self.grid,
            t_idx=None,
            apply_temperature=self.pf_options.apply_temperature_correction,
            branch_tolerance_mode=self.pf_options.branch_impedance_tolerance_mode)

        self.progress_text.emit('Running linear analysis...')

        # declare the linear analysis
        linear = LinearAnalysis(
            numerical_circuit=numerical_circuit,
            distributed_slack=False,
            correct_values=False,
            with_nx=self.options.consider_nx_contingencies,
            branch_dict=self.grid.get_branches_wo_hvdc_dict(),
            contingency_group_dict=self.grid.get_contingency_group_dict(),
        )

        linear.run()

        # sensitivities
        if self.options.monitor_only_sensitive_branches or self.options.monitor_only_ntc_load_rule_branches:
            alpha, alpha_n1 = self.compute_exchange_sensitivity(
                linear=linear,
                numerical_circuit=numerical_circuit,
                with_n1=self.options.n1_consideration
            )
        else:
            alpha = np.ones(numerical_circuit.nbr)
            alpha_n1 = np.ones((numerical_circuit.nbr, numerical_circuit.nbr))

        self.progress_text.emit('Formulating NTC OPF...')

        opf_vars = run_linear_ntc_opf_ts(
            grid=self.grid,
            time_indices=[None],
            solver_type=self.options.mip_solver,
            zonal_grouping=self.options.zonal_grouping,
            skip_generation_limits=self.options.skip_generation_limits,
            consider_contingencies=self.options.consider_contingencies,
            lodf_threshold=self.options.lodf_tolerance,
            buses_areas_1=self.options.area_from_bus_idx,
            buses_areas_2=self.options.area_to_bus_idx,
            transfer_method=self.options.transfer_method,
            logger=self.logger,
            progress_text=self.progress_text.emit,
            progress_func=self.progress_signal.emit,
            export_model_fname=self.options.export_model_fname)

        self.results.voltage = np.ones((opf_vars.nt, opf_vars.nbus)) * np.exp(1j * opf_vars.bus_vars.theta)
        self.results.bus_shadow_prices = opf_vars.bus_vars.shadow_prices
        self.results.load_shedding = opf_vars.load_vars.shedding
        self.results.battery_power = opf_vars.batt_vars.p
        self.results.battery_energy = opf_vars.batt_vars.e
        self.results.generator_power = opf_vars.gen_vars.p
        self.results.Sf = opf_vars.branch_vars.flows
        self.results.St = -opf_vars.branch_vars.flows
        self.results.overloads = opf_vars.branch_vars.flow_slacks_pos - opf_vars.branch_vars.flow_slacks_neg
        self.results.loading = opf_vars.branch_vars.loading
        self.results.phase_shift = opf_vars.branch_vars.tap_angles
        # self.results.Sbus = problem.get_power_injections()
        self.results.hvdc_Pf = opf_vars.hvdc_vars.flows
        self.results.hvdc_loading = opf_vars.hvdc_vars.loading

        idx_w = np.argmax(np.abs(alpha_n1), axis=1)
        alpha_w = np.take_along_axis(alpha_n1, np.expand_dims(idx_w, axis=1), axis=1)

        # pack the results
        self.results = OptimalNetTransferCapacityResults(
            bus_names=numerical_circuit.bus_data.names,
            branch_names=numerical_circuit.branch_data.names,
            load_names=numerical_circuit.load_data.names,
            generator_names=numerical_circuit.generator_data.names,
            battery_names=numerical_circuit.battery_data.names,
            hvdc_names=numerical_circuit.hvdc_data.names,
            trm=self.options.trm,
            ntc_load_rule=self.options.ntc_load_rule,
            branch_control_modes=numerical_circuit.branch_data.control_mode,
            hvdc_control_modes=numerical_circuit.hvdc_data.control_mode,
            Sbus=problem.get_power_injections(),
            voltage=problem.get_voltage(),
            battery_power=np.zeros((numerical_circuit.nbatt, 1)),
            controlled_generation_power=problem.get_generator_power(),
            Sf=problem.get_branch_power_from(),
            loading=problem.get_loading(),
            solved=bool(solved),
            bus_types=numerical_circuit.bus_types,
            hvdc_flow=problem.get_hvdc_flow(),
            hvdc_loading=problem.get_hvdc_loading(),
            phase_shift=problem.get_phase_angles(),
            generation_delta=problem.get_generator_delta(),
            hvdc_angle_slack=problem.get_hvdc_angle_slacks(),
            inter_area_branches=problem.inter_area_branches,
            inter_area_hvdc=problem.inter_area_hvdc,
            alpha=alpha,
            alpha_n1=alpha_n1,
            alpha_w=alpha_w,
            monitor=problem.monitor,
            monitor_loading=problem.monitor_loading,
            monitor_by_sensitivity=problem.monitor_by_sensitivity,
            monitor_by_unrealistic_ntc=problem.monitor_by_unrealistic_ntc,
            monitor_by_zero_exchange=problem.monitor_by_zero_exchange,
            contingency_branch_flows_list=problem.get_contingency_flows_list(),
            contingency_branch_indices_list=problem.contingency_indices_list,
            contingency_branch_alpha_list=problem.contingency_branch_alpha_list,
            contingency_generation_flows_list=problem.get_contingency_gen_flows_list(),
            contingency_generation_indices_list=problem.contingency_gen_indices_list,
            contingency_generation_alpha_list=problem.contingency_generation_alpha_list,
            contingency_hvdc_flows_list=problem.get_contingency_hvdc_flows_list(),
            contingency_hvdc_indices_list=problem.contingency_hvdc_indices_list,
            contingency_hvdc_alpha_list=problem.contingency_hvdc_alpha_list,
            branch_ntc_load_rule=problem.get_branch_ntc_load_rule(),
            rates=numerical_circuit.branch_data.rates[:, 0],
            contingency_rates=numerical_circuit.branch_data.contingency_rates[:, 0],
            area_from_bus_idx=self.options.area_from_bus_idx,
            area_to_bus_idx=self.options.area_to_bus_idx,
            structural_ntc=problem.structural_ntc,
            sbase=numerical_circuit.Sbase,
            loading_threshold=self.options.loading_threshold_to_report,
            reversed_sort_loading=self.options.reversed_sort_loading,
        )

        self.progress_text.emit('Creating reports...')
        self.results.create_all_reports(
            loading_threshold=self.options.loading_threshold_to_report,
            reverse=self.options.reversed_sort_loading,
        )

        self.progress_text.emit('Done!')

        return self.results

    def run(self):
        """

        :return:
        """
        start = time.time()
        self.opf()
        end = time.time()
        self.elapsed = end - start
