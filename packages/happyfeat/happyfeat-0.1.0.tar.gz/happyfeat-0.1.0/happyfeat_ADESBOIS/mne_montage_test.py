import mne
import pandas as pd
import matplotlib
from pathlib import Path

df = pd.read_csv('channel_example.txt')
ch_names = df.name.to_list()

pos = df[['x', 'y', 'z']].values
dig_ch_pos = dict(zip(ch_names, pos))
montage = mne.channels.make_dig_montage(ch_pos=dig_ch_pos)
fig = montage.plot()


easycap_montage = mne.channels.make_standard_montage("easycap-M1")
easycap_montage.plot()  # 2D
fig = easycap_montage.plot(kind="3d", show=False)  # 3D
fig = fig.gca().view_init(azim=70, elev=15)  # set view angle for tutorial

a = 0