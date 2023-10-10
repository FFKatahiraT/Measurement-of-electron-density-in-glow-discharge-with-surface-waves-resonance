# Measurement-of-electron-density-in-glow-discharge-with-surface-waves-resonance
Raw experimental data and Comsol Multiphysics model for manuscript "Measurement of electron density in glow discharge with surface waves resonance"

The study consist of 3 parts: 
1) Comsol Multiphysics 6.1 model (Hg_glow_discharge_light.mph), 
2) Results of emission spectroscopy of Hg glow discharge (SpectrumPlotter),
3) VSWR measurements data (VSWR_exp3).

1. To open the model you need Comsol Multiphysics v. 6.1 or above (https://www.comsol.com/).
   The model requires Plasma Module. To start the simulation press Study -> compute.

2. Raw spectrum data in csv format are in Spectrum_exp3/data directory.
   You can get spectrum images using Plotter.py script. Images will be saved in "Images" directory.
   For successful executing scripts python3 with matplotlib and numpy libraires is needed.
   Then, to obtain electron temperatures you can use plot_Te.py script.

4. Raw data are in "raw" directory.
   You can make VSWR(frequency) plots and calculate electron density on power dependence using calcNe_2.py  
