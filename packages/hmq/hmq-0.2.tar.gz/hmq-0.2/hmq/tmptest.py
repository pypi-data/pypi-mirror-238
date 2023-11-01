# %%
import os
os.chdir("/home/ferchault/wrk/hummingqueue/src/user")
import hmq
import numpy as np

# %%
@hmq.task
def dimer_energy(distance: float):
    from pyscf import scf
    from pyscf import gto
    mol = gto.M(atom = f'O 0 0 0; C 0 0 {distance}', basis = 'cc-pVDZ', verbose=0)
    mf = scf.RHF(mol)
    mf.kernel()
    return mf.e_tot

ds = np.linspace(0.5, 2.0, 1000)
for d in ds:
    dimer_energy(d)

tag = dimer_energy.submit(
    tag="tagme",
    ncores=2,
    datacenters="Kassel",
    packages="pyscf,numpy,scipy".split(","),
)
#%%
tag.pull()
#tag.results

#%%
@hmq.task
def mul(a, b):
    import time
    time.sleep(10)
    return a * b

for i in range(500):
    mul(i, 1)
tag2 = mul.submit(
    tag="tagme2",
    ncores=2,
    packages="numpy,scipy".split(","),
)
# py-3.10,nc-2,dc-Kassel
# py-3.10,nc-2,dc-any
#%%
import matplotlib.pyplot as plt
plt.plot(ds, tag.results)
# # %%


# mols = (1,2,3)
# for i in mols:
#     divide(mols, 1)

# #%%
# for i in mols:
#     divide(mols, 1)

# #%%


# %%
@hmq.task
def sleep(n):
    import time

    time.sleep(1)
    return n


for i in range(10000):
    sleep(2)
tag = sleep.submit(tag="tagme")
# %%
# get results
tag.pull()
# %%
tag.pull()
# %%
tag.to_file("test.hmq")
# %%
tag = hmq.Tag.from_file("test.hmq")
# %%
tag.pull()
# %%
import numpy as np
np.abs(np.random.normal(loc=0, scale=1.48, size=10000)).mean()
# %%
