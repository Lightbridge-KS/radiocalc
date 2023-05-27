from shiny import App, render, ui, reactive

aspects_choices = {"caudate": "Caudate", 
                   "putamen": "Putamen",
                   "int_cap": "Internal capsule",
                   "insular": "Insular cortex",
                   "M1": "M1",
                   "M2": "M2",
                   "M3": "M3",
                   "M4": "M4",
                   "M5": "M5",
                   "M6": "M6"}


aspects_pc_choices = {
    "rt_thal": "Right thalamus",
    "lt_thal": "Left thalamus",
    "rt_occ": "Right occipital lobe",
    "lt_occ": "Left occipital lobe",
    "mb": "Midbrain",
    "pons": "Pons",
    "rt_cere": "Right hemicerebellum",
    "lt_cere": "Left hemicerebellum"
}


# UI 
stroke_ct_ui = ui.page_fluid(
        ui.row(
            ui.column(4, 
                ui.input_checkbox_group("aspects", ui.markdown("**ASPECTS**"), aspects_choices),
                
            ),
            ui.column(4, 
                ui.input_checkbox_group("aspects_pc", ui.markdown("**Pc-ASPECTS**"), aspects_pc_choices),
                
            )
        ),
        ui.row(
            ui.column(4,
                ui.output_text_verbatim("txt_aspects")
            ),
            ui.column(4,
                ui.output_text_verbatim("txt_aspects_pc")
            )

        )
)

# Server
def stroke_ct_server(input, output, session):
    
    ## ASPECT Calculation
    @reactive.Calc
    def calc_aspects():
        return 10 - len(input.aspects())

    ## ASPECT Text
    @output
    @render.text
    def txt_aspects():
        return f"ASPECTS: {calc_aspects()}"
    
    ## Pc-ASPECT Calculation
    @reactive.Calc
    def calc_aspects_pc():
        choices = input.aspects_pc()
        # Pontine or MB lesion reduce by 2
        add_pons = 1 if "pons" in choices else 0
        add_mb = 1 if "mb" in choices else 0
        return 10 - (len(choices) + add_pons + add_mb)

    
    ## Pc-ASPECT Text Output
    @output
    @render.text
    def txt_aspects_pc():
        return f"pc-ASPECTS: {calc_aspects_pc()}"



app = App(stroke_ct_ui, stroke_ct_server, debug=True)
