"""Análisis agregado del abandono bancario, sin exportar registros individuales."""

from pathlib import Path
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from .common import configure_plots, save_json, provenance, save_figure

REQUIRED = [
    "customer_id",
    "credit_score",
    "country",
    "gender",
    "age",
    "tenure",
    "balance",
    "products_number",
    "credit_card",
    "active_member",
    "estimated_salary",
    "churn",
]


def load_data(path):
    data = pd.read_csv(path)
    missing = sorted(set(REQUIRED) - set(data.columns))
    if missing:
        raise ValueError(f"Faltan columnas: {missing}")
    if data.empty or data[REQUIRED].isna().any().any():
        raise ValueError(
            "Se requieren registros completos; revise el informe de origen."
        )
    if data.customer_id.duplicated().any():
        raise ValueError(
            "customer_id debe ser único; no se eliminan clientes silenciosamente."
        )
    for col in ["credit_card", "active_member", "churn"]:
        if not data[col].isin([0, 1]).all():
            raise ValueError(f"{col} debe contener solo 0 y 1.")
    numeric = [c for c in REQUIRED if c not in ["customer_id", "country", "gender"]]
    for col in numeric:
        data[col] = pd.to_numeric(data[col], errors="raise")
    if not np.isfinite(data[numeric].to_numpy()).all():
        raise ValueError("Las variables numéricas deben ser finitas.")
    if (data.age < 18).any() or (data.age > 110).any() or (data.balance < 0).any():
        raise ValueError("Edad o saldo fuera del dominio esperado.")
    # El identificador se utiliza únicamente para validar unicidad.
    return data.drop(columns="customer_id")


def wilson_interval(successes, total, z=1.96):
    p = successes / total
    denominator = 1 + z * z / total
    center = (p + z * z / (2 * total)) / denominator
    margin = (
        z * np.sqrt(p * (1 - p) / total + z * z / (4 * total * total)) / denominator
    )
    # Evitar errores de redondeo en tasas exactamente iguales a 0 o 1.
    return np.maximum(0, np.minimum(p, center - margin)), np.minimum(
        1, np.maximum(p, center + margin)
    )


def segment_rates(data, column, min_size=30):
    table = data.groupby(column, observed=True)["churn"].agg(n="size", abandonos="sum")
    table = table.loc[table.n >= min_size].copy()
    table["tasa"] = table.abandonos / table.n
    table["ic95_inferior"], table["ic95_superior"] = wilson_interval(
        table.abandonos, table.n
    )
    table.index = table.index.astype(str)
    return (
        table.reset_index().rename(columns={column: "segmento"}).assign(variable=column)
    )


def run(data_path, output_dir="reports"):
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    configure_plots()
    data = load_data(data_path)
    data["grupo_edad"] = pd.cut(
        data.age,
        [17, 29, 39, 49, 59, 110],
        labels=["18–29", "30–39", "40–49", "50–59", "60+"],
    )
    variables = ["country", "gender", "grupo_edad", "active_member", "products_number"]
    segments = pd.concat([segment_rates(data, c) for c in variables], ignore_index=True)
    segments.to_csv(output / "segmentos.csv", index=False)
    numeric = data.select_dtypes(include="number").drop(columns=["churn"])
    numeric.describe().T.to_csv(output / "resumen_numerico.csv", index_label="variable")
    low, high = wilson_interval(int(data.churn.sum()), len(data))
    summary = {
        "n_clientes": len(data),
        "abandonos": int(data.churn.sum()),
        "tasa_abandono": float(data.churn.mean()),
        "ic95": [float(low), float(high)],
        "minimo_clientes_por_segmento": 30,
        "segmentos": segments.to_dict(orient="records"),
        "fuente": provenance(data_path),
        "filas_individuales_exportadas": 0,
    }
    save_json(output / "metrics.json", summary)

    fig, axes = plt.subplots(2, 2, figsize=(13, 9), layout="constrained")
    for ax, column, title in zip(
        axes.flat,
        ["country", "grupo_edad", "active_member", "products_number"],
        [
            "Abandono por país",
            "Abandono por grupo de edad",
            "Abandono según actividad",
            "Abandono por productos",
        ],
    ):
        s = segments.loc[segments.variable == column]
        labels = s.segmento.tolist()
        if column == "active_member":
            labels = ["Inactivo" if x == "0" else "Activo" for x in labels]
        x = np.arange(len(s))
        ax.bar(x, s.tasa * 100, color="#23788e", width=0.65)
        ax.errorbar(
            x,
            s.tasa * 100,
            yerr=[(s.tasa - s.ic95_inferior) * 100, (s.ic95_superior - s.tasa) * 100],
            fmt="none",
            ecolor="#172b4d",
            capsize=4,
        )
        ax.set_xticks(x, [f"{a}\nn={b:,}" for a, b in zip(labels, s.n)])
        ax.axhline(
            data.churn.mean() * 100,
            color="#d66a38",
            linestyle="--",
            label="Media global",
        )
        ax.set(title=title, ylabel="Clientes que abandonaron (%)", ylim=(0, 105))
        ax.legend(fontsize=8)
    fig.suptitle(
        f"Abandono bancario | {len(data):,} clientes · tasa global {data.churn.mean():.1%}",
        fontsize=17,
    )
    save_figure(fig, output / "segmentos.png")

    corr = (
        data.select_dtypes(include="number")
        .drop(columns=["grupo_edad"], errors="ignore")
        .corr()
    )
    fig, ax = plt.subplots(figsize=(10, 8), layout="constrained")
    im = ax.imshow(corr, vmin=-1, vmax=1, cmap="RdBu_r")
    ax.set_xticks(range(len(corr)), corr.columns, rotation=70, ha="right")
    ax.set_yticks(range(len(corr)), corr.columns)
    for i in range(len(corr)):
        for j in range(len(corr)):
            ax.text(
                j,
                i,
                f"{corr.iloc[i,j]:.2f}",
                ha="center",
                va="center",
                fontsize=8,
                color="white" if abs(corr.iloc[i, j]) > 0.6 else "#172b4d",
            )
    ax.set_title(
        "Correlaciones de las variables originales\nAsociación descriptiva; no causalidad"
    )
    fig.colorbar(im, ax=ax, shrink=0.7)
    save_figure(fig, output / "correlaciones.png")
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default="data/Bank Customer Churn Prediction.csv")
    parser.add_argument("--output", default="reports")
    args = parser.parse_args()
    result = run(args.data, args.output)
    print(
        f"Clientes: {result['n_clientes']:,}; abandono: {result['tasa_abandono']:.2%}"
    )
