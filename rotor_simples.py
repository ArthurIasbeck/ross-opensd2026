import ross as rs
import numpy as np

steel = rs.Material(name="Steel", rho=7810, E=211e9, Poisson=0.3)

L = 0.2     # Comprimento do elemento
i_d = 0     # Diâmetro interno do elemento
o_d = 0.1   # Diametro externo do elemento
N_elem = 6  # Número de elementos do eixo

shaft_elements = []
for _ in range(N_elem):
    shaft_element = rs.ShaftElement(
        L=L,
        idl=i_d,
        odl=o_d,
        material=steel,
        shear_effects=True,
        rotary_inertia=True,
        gyroscopic=True,
    )
    shaft_elements.append(shaft_element)

bearing0 = rs.BearingElement(
    n=0,        # Nó onde se encontra o mancal
    kxx=1.0e6,  # Rigidez na direção x
    kyy=2.0e6,  # Rigidez na direação y
    cxx=1.0e3,  # Amortecimento na direção x
    cyy=1.0e3,  # Amortecimento na direção y
)
bearing1 = rs.BearingElement(
    n=5,
    kxx=1.0e6,
    kyy=2.0e6,
    cxx=1.0e3,
    cyy=1.0e3,
)
bearings = [bearing0, bearing1]

disk = rs.DiskElement(n=2, m=30, Ip=0.2, Id=0.3)

rotor = rs.Rotor(
    shaft_elements=shaft_elements, disk_elements=[disk], bearing_elements=bearings
)

rotor.plot_rotor().show()

campbell = rotor.run_campbell(speed_range=np.linspace(0, 1000))
campbell.plot().show()