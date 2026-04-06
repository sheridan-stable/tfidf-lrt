import numpy as np
import pandas as pd
from plotnine import (
    ggplot, aes, geom_histogram, labs, theme_minimal, 
    scale_fill_manual, scale_x_log10, theme, element_blank
)
from mizani.transforms import log_trans

def main():
    try:
        df = pd.read_csv("../reports/r8-bb-params-mle.csv")
    except FileNotFoundError:
        print("Error: 'r8-bb-params-mle.csv' not found.")
        return
    
    df_melted = df.melt(
        value_vars=['alpha_i', 'alpha_not_i'],
        var_name='Parameter',
        value_name='Value'
    )

    df_melted['Parameter'] = df_melted['Parameter'].replace({
        'alpha_i': r'$\alpha_i$',
        'alpha_not_i': r'$\alpha_{\neg i}$'
    })

    p = (
        ggplot(df_melted, aes(x='Value', fill='Parameter'))
        + geom_histogram(bins=80, alpha=0.90, position='identity')
        + scale_x_log10(trans=log_trans(base=np.e),
            breaks=lambda x: [10**i for i in range(-5, 5)],
            labels=lambda x: [f"{val:.0f}" if val < 0.0001 else f"{val:.4f}" if val < 0.001 else f"{val:.3f}" if val < 0.01 else f"{val:.2f}" if val < 0.1 else f"{val:.1f}" if val < 1 else f"{val:.0f}" for val in x]
        )
        + labs(
            x='Parameter value',
            y='Frequency',
            title=r'Empirical distributions of $\alpha_i$ and $\alpha_{\neg i}$',
            fill='Parameter'
        )
        + scale_fill_manual(values={
            r'$\alpha_i$': '#619CFF',
            r'$\alpha_{\neg i}$': '#FDB863'
        })
        + theme_minimal()
        + theme(
            legend_position=(0.98, 0.83),   
            legend_justification=(1, 0),    
            legend_background=element_blank(),
            legend_key=element_blank()
        )
    )

    p.save("../plots/parameter-distribution-r8.pdf", width=10, height=6, dpi=300)
    print("Plot saved successfully.")

if __name__ == "__main__":
    main()