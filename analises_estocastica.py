import numpy as np
import plotly.io as pio
import ross as rs
import ross.stochastic as srs
from ross.probe import Probe
from ross.materials import steel


def main():
    # Configura o Plotly para abrir os gráficos em abas do navegador
    pio.renderers.default = "browser"

    print("Iniciando a configuração dos elementos estocásticos...")
    var_size = 5

    # Materiais
    E = np.random.uniform(208e9, 211e9, var_size)
    rho = np.random.uniform(7780, 7850, var_size)
    G_s = np.random.uniform(79.8e9, 81.5e9, var_size)
    rand_mat = srs.ST_Material(name="Steel", rho=rho, E=E, G_s=G_s)

    # Elementos de eixo
    # Criando um elemento cilíndrico
    o_d_cyl = np.random.uniform(0.04, 0.06, var_size)
    r_s0 = srs.ST_ShaftElement(
        L=0.25,
        idl=0.0,
        odl=o_d_cyl,
        material=rand_mat,
        shear_effects=True,
        rotary_inertia=True,
        gyroscopic=True,
        is_random=["odl", "material"],
    )

    # Criando um elemento cônico
    odl_con = np.random.uniform(0.04, 0.06, var_size)
    odr_con = np.random.uniform(0.06, 0.07, var_size)
    r_s1 = srs.ST_ShaftElement(
        L=0.25,
        idl=0.0,
        odl=odl_con,
        idr=0.0,
        odr=odr_con,
        material=rand_mat,
        shear_effects=True,
        rotary_inertia=True,
        gyroscopic=True,
        is_random=["odl", "odr", "material"],
    )

    # Construção do rotor
    # Criando os elementos base do eixo
    L_val = 0.25
    N_elements = 4
    shaft_elements = [
        rs.ShaftElement(
            L=L_val,
            idl=0.0,
            odl=0.05,
            material=steel,
            shear_effects=True,
            rotary_inertia=True,
            gyroscopic=True,
        )
        for _ in range(N_elements)
    ]

    # Inserindo o elemento aleatório na lista
    shaft_elements.insert(2, r_s0)

    # Discos
    m_disk0 = np.random.uniform(32.0, 33.0, var_size)
    Id_disk0 = np.random.uniform(0.17, 0.18, var_size)
    Ip_disk0 = np.random.uniform(0.32, 0.33, var_size)
    disk0 = srs.ST_DiskElement(
        n=2, m=m_disk0, Id=Id_disk0, Ip=Ip_disk0, is_random=["m", "Id", "Ip"]
    )

    i_d_disk1 = np.random.uniform(0.05, 0.06, var_size)
    o_d_disk1 = np.random.uniform(0.35, 0.39, var_size)
    disk1 = srs.ST_DiskElement.from_geometry(
        n=3,
        material=steel,
        width=0.07,
        i_d=i_d_disk1,
        o_d=o_d_disk1,
        is_random=["i_d", "o_d"],
    )

    # Mancais
    kxx_brg = np.random.uniform(1e6, 2e6, var_size)
    cxx_brg = np.random.uniform(1e3, 2e3, var_size)
    brg0 = srs.ST_BearingElement(
        n=0,
        kxx=kxx_brg,
        cxx=cxx_brg,
        is_random=["kxx", "cxx"],
    )

    brg1 = srs.ST_BearingElement(
        n=5,
        kxx=kxx_brg,
        cxx=cxx_brg,
        is_random=["kxx", "cxx"],
    )

    # Montagem do rotor estocástico
    print("Montando o modelo do rotor...")
    rotor1 = srs.ST_Rotor(
        shaft_elements,
        [disk0, disk1],
        [brg0, brg1],
    )

    # Análises
    print("Executando Análise de Campbell...")
    speed_range_camp = np.linspace(0, 500, 31)
    camp = rotor1.run_campbell(speed_range_camp, frequencies=7)
    fig1 = camp.plot_nat_freq(conf_interval=[90])
    fig1.show()

    print("Executando Resposta em Frequência...")
    speed_range_freq = np.linspace(0, 500, 301)
    inp = 3 * rotor1.number_dof + 1
    out = 2 * rotor1.number_dof + 1
    freqresp = rotor1.run_freq_response(inp, out, speed_range_freq)
    fig2 = freqresp.plot(conf_interval=[90], mag_kwargs=dict(yaxis=dict(type="log")))
    fig2.show()

    print("Executando Resposta ao Desbalanceamento...")
    freq_range_unb = np.linspace(0, 500, 201)
    n_unb = 3
    m_unb = np.random.uniform(0.001, 0.002, 10)
    p_unb = 0.0
    results_unb = rotor1.run_unbalance_response(n_unb, m_unb, p_unb, freq_range_unb)
    fig3 = results_unb.plot(
        probe=[Probe(3, np.pi / 2)],
        conf_interval=[90],
        mag_kwargs=dict(yaxis=dict(type="log")),
    )
    fig3.show()

    print("Executando Resposta no Tempo...")
    size = 1000
    ndof = rotor1.ndof
    node = 3  # nó onde a força é aplicada
    speed = 100.0

    t = np.linspace(0, 10, size)
    F = np.zeros((size, ndof))
    F[:, node * rotor1.number_dof + 0] = 10 * np.cos(2 * t)
    F[:, node * rotor1.number_dof + 1] = 10 * np.sin(2 * t)
    results_time = rotor1.run_time_response(speed, F, t)

    fig4 = results_time.plot_1d(probe=[Probe(3, np.pi / 2)], conf_interval=[90])
    fig4.show()

    fig5 = results_time.plot_2d(node=node, conf_interval=[90])
    fig5.show()

    fig6 = results_time.plot_3d(conf_interval=[90])
    fig6.show()

    print("Análises finalizadas com sucesso!")


if __name__ == "__main__":
    main()
