from presets import run_preset

presets = [
    "quality_compounder",
    "value_pick",
    "growth_accelerator",
    "dividend_champion",
    "debt_free_bluechip",
    "turnaround_watch"
]

for p in presets:

    df = run_preset(p)

    print(
        p,
        len(df)
    )