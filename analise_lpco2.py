import ross as rs
import numpy as np
from ross.units import Q_
from ross.probe import Probe
import time as time_lib

def main():
    print("Carregando o modelo do rotor...")
    rotor = rs.Rotor.load("rotor_model_lpco2.toml")

    print(f"Massa do rotor: {rotor.m}")
    print(f"Número do rotor: {rotor.ndof}")

    # Exportando a geometria do rotor
    print("Construindo representação gráfica do rotor...")
    fig_rotor = rotor.plot_rotor(nodes=999)
    fig_rotor.write_html("output/01_geometria_rotor.html")
    print("-> Salvo: 01_geometria_rotor.html")

    # --- UCS ---
    print("Calculando Undamped Critical Speeds (UCS)...")
    ucs = rotor.run_ucs(stiffness_range=(6, 10))
    fig_ucs = ucs.plot(frequency_units="rpm")
    fig_ucs.write_html("output/02_diagrama_ucs.html")
    print("-> Salvo: 02_diagrama_ucs.html")

    # --- Análise Modal ---
    print("Executando Análise Modal...")
    rotor_speed = 0  # rad/s
    modal = rotor.run_modal(rotor_speed, num_modes=24)

    fig_m2d_0 = modal.plot_mode_2d(0, orientation="x", frequency_units="rpm")
    fig_m2d_0.write_html("output/03_modo_2d_modo0.html")

    fig_m2d_2 = modal.plot_mode_2d(2, orientation="x", frequency_units="rpm")
    fig_m2d_2.write_html("output/04_modo_2d_modo2.html")

    fig_m3d_0 = modal.plot_mode_3d(0, frequency_units="rpm")
    fig_m3d_0.write_html("output/05_modo_3d_modo0.html")

    fig_m3d_2 = modal.plot_mode_3d(2, frequency_units="rpm")
    fig_m3d_2.write_html("output/06_modo_3d_modo2_animado.html")
    print("-> Salvos: Gráficos de análise modal (03 a 06)")

    # --- Resposta ao Desbalanceamento ---
    print("Calculando Resposta ao Desbalanceamento...")
    node = 24
    mass = Q_(2161.4, "g*mm")
    phase = Q_(0, "deg")
    frequency_range = Q_(np.linspace(0, 5000, 101), "RPM")

    unbalance = rotor.run_unbalance_response(node, mass, phase, frequency_range)
    probe = Probe(24, Q_(0, "deg"))  # Nó 24, orientação 0°
    fig_bode = unbalance.plot_bode(
        probe=[probe],
        frequency_units="rpm",
        amplitude_units="microm",
        phase_units="deg",
    )
    fig_bode.write_html("output/07_resposta_desbalanceamento_bode.html")
    print("-> Salvo: 07_resposta_desbalanceamento_bode.html")

    # --- Diagrama de Campbell ---
    print("Gerando Diagrama de Campbell...")
    samples = 31
    speed_range = Q_(np.linspace(0, 15000, samples), "rpm")
    campbell = rotor.run_campbell(speed_range)

    fig_campbell = campbell.plot()
    fig_campbell.write_html("output/08_diagrama_campbell.html")
    print("-> Salvo: 08_diagrama_campbell.html")

    # --- Resposta Temporal ---
    print("Calculando Resposta Temporal...")
    time_lib.sleep(1)
    time_samples = 1001
    t = np.linspace(0, 20, time_samples)
    speed = Q_(6882, "rpm")
    node = 24

    F = np.zeros((time_samples, rotor.ndof))
    # Força Harmônica na direção x
    F[:, node * rotor.number_dof + 0] = 200 * np.cos(4 * t)
    # Força Harmônica na direção y
    F[:, node * rotor.number_dof + 1] = 200 * np.sin(4 * t)

    time = rotor.run_time_response(speed, F, t)
    time_probe = Probe(24, 0)  # Nó 24, orientação 0°

    fig_t1d = time.plot_1d(probe=[time_probe])
    fig_t1d.write_html("output/10_resposta_temporal_1d.html")

    fig_t2d = time.plot_2d(node=24)
    fig_t2d.write_html("output/11_resposta_temporal_2d_orbita.html")

    fig_t3d = time.plot_3d()
    fig_t3d.write_html("output/12_resposta_temporal_3d.html")
    print("-> Salvos: Gráficos de resposta temporal (10 a 12)")

    print(
        "\nTodas as análises foram concluídas e os arquivos HTML foram gerados com sucesso!"
    )


if __name__ == "__main__":
    main()
