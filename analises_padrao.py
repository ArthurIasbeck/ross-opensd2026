import ross as rs
import numpy as np
from ross import Q_, Probe


def main():
    # Constrói rotor
    rotor = rs.compressor_example()
    rotor.plot_rotor(nodes=999).show()

    # Análise modal
    speed_rpm = 1000
    speed_rad_s = speed_rpm * (np.pi / 30)

    modal_results = rotor.run_modal(speed=speed_rad_s)

    wn_hz = modal_results.wn / (2 * np.pi)
    wd_hz = modal_results.wd / (2 * np.pi)
    log_dec = modal_results.log_dec

    print("Frequências naturais (Hz):", wn_hz)
    print("Frequências naturais amortecidas (Hz):", wd_hz)
    print("Decremento logaritmico:", log_dec)

    # Construção dos gráficos dos modos
    for mode_idx in range(4):
        modal_results.plot_mode_2d(mode=mode_idx).show()

    for mode_idx in range(4):
        modal_results.plot_mode_3d(mode=mode_idx).show()

    # Campbell
    speed_rpm = np.linspace(0, 6000, 100)
    speed_rad_s = speed_rpm * (np.pi / 30)

    campbell_results = rotor.run_campbell(speed_range=speed_rad_s)

    campbell_results.plot(
        frequency_units="Hz",
        speed_units="RPM",
    ).show()

    # UCS
    ucs_results = rotor.run_ucs(
        stiffness_range=(5, 11),
        num=30,
        num_modes=16,
    )
    ucs_results.plot().show()

    # Resposta ao desbalanceamento
    unbalance_node = 3
    unbalance_mag = 0.01
    unbalance_phase = 0.0

    speed_range = np.linspace(0, 1000, 101)

    response = rotor.run_unbalance_response(
        node=unbalance_node,
        unbalance_magnitude=unbalance_mag,
        unbalance_phase=unbalance_phase,
        frequency=speed_range,
    )

    fig = response.plot(probe=[(unbalance_node, 0), (unbalance_node, 1)])
    fig.show()

    # Resposta em frequência
    speed_range = np.linspace(0, 2000, 400)
    freq_response = rotor.run_freq_response(speed_range=speed_range)
    freq_response.plot(inp=26 * 6 + 1, out=26 * 6 + 1).show()

    # Resposta temporal
    speed = 500.0
    n_steps = 1000
    t = np.linspace(0, 10, n_steps)
    F = np.zeros((n_steps, rotor.ndof))

    node_excitation = 3
    dof_x_index = rotor.number_dof * node_excitation + 0
    dof_y_index = rotor.number_dof * node_excitation + 1

    force_amplitude = 10.0
    F[:, dof_x_index] = force_amplitude * np.cos(2 * t)
    F[:, dof_y_index] = force_amplitude * np.sin(2 * t)

    results = rotor.run_time_response(speed=speed, F=F, t=t)

    probe_x = rs.Probe(node=node_excitation, angle=0.0)
    probe_y = rs.Probe(node=node_excitation, angle=np.pi / 2)

    results.plot_1d(probe=[probe_x, probe_y]).show()
    results.plot_2d(node=node_excitation).show()
    results.plot_3d().show()

    # Análise estática
    static_results = rotor.run_static()
    static_results.plot_free_body_diagram().show()
    static_results.plot_deformation().show()

    # Efeito de uma trinca
    mass_unb = [5e-6]
    phase_unb = [-np.pi / 2]
    node_unb = [12]

    t = np.arange(0, 5, 0.0001)

    results = rotor.run_crack(
        depth_ratio=0.49,  # crack depth / shaft radius
        n=18,
        speed=Q_(10000, "RPM"),
        crack_model="Gasch",
        node=node_unb,
        unbalance_magnitude=mass_unb,
        unbalance_phase=phase_unb,
        t=t,
        model_reduction={"num_modes": 10},
    )

    probe1 = Probe(14, 0)
    probe2 = Probe(22, 0)

    results.plot_1d([probe1, probe2]).show()

    results.plot_dfft(
        [probe1, probe2], frequency_range=Q_((0, 100), "Hz"), yaxis_type="log"
    ).show()


if __name__ == "__main__":
    main()
