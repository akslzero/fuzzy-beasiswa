import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def fuzzy_membership(x):
    # Tidak Layak
    tidak_layak = 0
    if x <= 2.0:
        tidak_layak = 1
    elif 2.0 < x < 2.75:
        tidak_layak = (2.75 - x) / (2.75 - 2.0)
    
    # Dipertimbangkan
    dipertimbangkan = 0
    if 2.5 < x <= 3.0:
        dipertimbangkan = (x - 2.5) / (3.0 - 2.5)
    elif 3.0 < x < 3.5:
        dipertimbangkan = (3.5 - x) / (3.5 - 3.0)
        
    # Layak
    layak = 0
    if 3.25 < x < 3.75:
        layak = (x - 3.25) / (3.75 - 3.25)
    elif x >= 3.75:
        layak = 1
        
    return tidak_layak, dipertimbangkan, layak

st.title("🎓 Sistem Kelayakan Beasiswa (Fuzzy Logic)")
ipk_input = st.slider("Masukkan IPK Anda:", 0.0, 4.0, 3.0, step=0.01)

mu_tidak, mu_pertimbang, mu_layak = fuzzy_membership(ipk_input)

# Menentukan Hasil Akhir
labels = ["Tidak Layak", "Dipertimbangkan", "Layak"]
values = [mu_tidak, mu_pertimbang, mu_layak]
idx_max = np.argmax(values)
status_akhir = labels[idx_max]

# --- TABEL DERAJAT KEANGGOTAAN ---
st.subheader("📊 Tabel Derajat Keanggotaan")
data_fuzzy = {
    "Himpunan Fuzzy": labels,
    "Derajat Keanggotaan (μ)": [f"{v:.4f}" for v in values]
}
st.table(pd.DataFrame(data_fuzzy))

# --- OUTPUT PERHITUNGAN ---
st.subheader("📝 Output Perhitungan")
st.write(f"Berdasarkan input IPK **{ipk_input}**, didapatkan nilai keanggotaan:")
st.latex(rf"\mu_{{\text{{Tidak Layak}}}}({ipk_input}) = {mu_tidak:.4f}")
st.latex(rf"\mu_{{\text{{Dipertimbangkan}}}}({ipk_input}) = {mu_pertimbang:.2f}")
st.latex(rf"\mu_{{\text{{Layak}}}}({ipk_input}) = {mu_layak:.4f}")

st.info(f"**Kesimpulan:** Nilai tertinggi adalah **{values[idx_max]:.4f}** pada kategori **{status_akhir}**.")

# --- GRAFIK ---
st.subheader("📈 Grafik Himpunan Fuzzy")
x_range = np.linspace(0, 4, 400)
y_plots = [ [fuzzy_membership(i)[j] for i in x_range] for j in range(3)]
colors = ['red', 'orange', 'green']

fig, ax = plt.subplots()
for y, label, color in zip(y_plots, labels, colors):
    ax.plot(x_range, y, label=label, color=color)
ax.axvline(x=ipk_input, color='blue', linestyle='--', label=f'Input: {ipk_input}')
ax.set_ylabel("Degree of Membership")
ax.legend()
st.pyplot(fig)
