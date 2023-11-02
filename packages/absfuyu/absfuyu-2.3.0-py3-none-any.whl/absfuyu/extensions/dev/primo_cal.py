"""
Intertwined Fate Calculator
---
Note: Missing 60 primos in the monthly checkin app
"""



# Library
##############################################################
import math as __math
from datetime import datetime
from dateutil.relativedelta import relativedelta

try:
    # from rich.jupyter import print
    # from rich.panel import Panel
    # from IPython.display import clear_output, display
    import ipywidgets as widgets
except:
    raise SystemExit





# Function
##############################################################

# Core
########################################
def __div_down(big_num: int, small_num: int):
    """Round down divided number
    """
    return __math.floor(big_num / small_num)


def fate_result(
        primogem: int = 0,
        intertwined_fate: int = 0,
        include_extra_fates_from_shop: bool = True,
        masterless_starglitter: int = 0,
        date_to_calculate_to:str = "",
        include_abyss: bool = False,
        abyss_star: int = 0,
        include_extra_glitters_from_rolls: bool = False,
        include_extra_primogem: bool = False,
        extra_primogem: int = 0,
        have_welkin: bool = False,
        welkin_date_end: str = "",
        include_genesis_crystal: bool = False,
        genesis_crystal: int = 0,
        debug: bool = False
    ):
    """Calculate intertwined fates
    """

    # Constant variables
    DAILY_GEM = 60
    WELKIN_GEM = 90
    ABYSS_GEM = 50
    PRIMO_PER_FATE = 160
    GLITTER_PER_FATE = 5
    IFATE_MONTHLY_SHOP = 5
    ABYSS_CHAMBER_PER_FLOOR = 3
    ABYSS_INTERVAL = 14 # days
    # TODAY = datetime.now()
    DATE_FORMAT = "%Y-%m-%d"

    # Error check
    if date_to_calculate_to == "":
        date_to_calculate_to = str(datetime.now().date() + relativedelta(days=1))
    if welkin_date_end == "":
        welkin_date_end = date_to_calculate_to

    # Primogem
    _primo_day = datetime.strptime(date_to_calculate_to, DATE_FORMAT) - datetime.now()
    _primo = _primo_day.days * DAILY_GEM
    _base_primo = _primo + primogem
    _total_primo = _base_primo

    # Abyss
    _ab_time = __div_down(_primo_day.days, ABYSS_INTERVAL)
    _ab_gem = __div_down(abyss_star, ABYSS_CHAMBER_PER_FLOOR) * ABYSS_GEM *_ab_time

    # Welkin
    _w_day = datetime.strptime(welkin_date_end, DATE_FORMAT) - datetime.now()
    _w_primo = _w_day.days * WELKIN_GEM
  
    # Primogem Final
    _total_primo = _base_primo + _ab_gem*int(include_abyss) + _w_primo*int(have_welkin) +\
         genesis_crystal*int(include_genesis_crystal) + extra_primogem*int(include_extra_primogem)

    # Intertwined Fate
    _if1 = __div_down(_total_primo, PRIMO_PER_FATE) # Primogem
    _if2 = __div_down(masterless_starglitter, GLITTER_PER_FATE) # Glitter
    _if3 = 0 # Extra fates from monthly shop
    if _primo_day.days >= 30:
        _if3 = __div_down(_primo_day.days, 30) * IFATE_MONTHLY_SHOP
    _base_if = intertwined_fate + _if1 + _if2 + _if3*int(include_extra_fates_from_shop)

    # Intertwined Fate - Extra glitters from rolls (worst case)
    _ex_gl = __div_down(_base_if, 10) * 2
    _ex_if = __div_down(_ex_gl, GLITTER_PER_FATE)

    # Intertwined Fate Final
    _total_if = _base_if + _ex_if*int(include_extra_glitters_from_rolls)

    # Output
    output = {
        "Total Primogems": _total_primo,
        "Total Intertwined Fates": _total_if,
        "5-star character (worst case)": __div_down(_total_if, 90),
        "5-star weapon (worst case)": __div_down(_total_if, 80),
    }
    # Output debug
    output_d = {
        "Primogems": {
            "Current": _total_primo,
            "Base": {
                "Days to chosen date": _primo_day.days,
                "Days to Primogem": _primo,
                "Total Primogems": _base_primo,
            },
            "Abyss": {
                "Abyss time": _ab_time,
                "Abyss stars": abyss_star,
                "Abyss stars to Primogem": __div_down(abyss_star, ABYSS_CHAMBER_PER_FLOOR) * ABYSS_GEM,
                "Abyss Primogem": _ab_gem,
                "Total Primogems": _base_primo + _ab_gem,
            },
            "Welkin": {
                "Welkin days to chosen date": _w_day.days,
                "Welkin to Primogems": _w_primo,
                "Total Primogems": _base_primo + _w_primo,
            },
            "Genesis Crystal": {
                "Genesis Crystal at disposal": genesis_crystal,
                "Total Primogems": _base_primo + genesis_crystal,
            },
            "Extra": {
                "Extra Primgogems": extra_primogem,
                "Total Primogems": _base_primo + extra_primogem,
            },
            "Final": {
                "Additional Primogems": _ab_gem + _w_primo + genesis_crystal + extra_primogem,
                "Total Primogems (no welkin)": _base_primo + _ab_gem + genesis_crystal + extra_primogem,
                "Total Primogems": _base_primo + _ab_gem + _w_primo + genesis_crystal + extra_primogem
            }
        },
        "Intertwined Fates": {
            "Current": _total_if,
            "Base": {
                "Base": intertwined_fate,
                "From Primogems (base)": __div_down(_base_primo, PRIMO_PER_FATE),
                "From Glitters": _if2,
                "Extra from monthly shop": _if3,
                "Total Intertwined Fates (no shop)": intertwined_fate + __div_down(_base_primo, PRIMO_PER_FATE) + _if2,
                "Total Intertwined Fates": intertwined_fate + __div_down(_base_primo, PRIMO_PER_FATE) + _if2 + _if3,
            },
            "Extra Glitters from rolls": {
                "Extra Glitters from rolls": _ex_gl,
                "Extra Glitters from rolls to Fates": _ex_if,
                "Current fates and extra": _base_if + _ex_if
            },
            "Intertwined Fates to Primogems": _total_if * 160
        }
    }

    if debug:
        return output_d
    else:
        # return output
        return f"""
        [b]From [/][i]{datetime.now().date()}[/] [b]to[/] [i]{date_to_calculate_to}[/]

        [b]Intertwined Fate(s) gain (approx.): [cyan]{output["Total Intertwined Fates"]:,.0f}[/][/]
        [i]Which is:
        - Around [bold cyan]{output["Total Intertwined Fates"]*160:,.0f}[/] primogems
        - Around [bold cyan]{output["5-star character (worst case)"]:,.0f}[/] 5-star character(s) (worst case)
        - Around [bold cyan]{output["5-star weapon (worst case)"]:,.0f}[/] 5-star weapon(s) (worst case)
        [/]"""



# ipywidgets
########################################
def get_layout(layout: str, border: str = None):
    """
    List of pre-made layout
    """

    # Layout
    width_auto_layout = widgets.Layout(
        width="auto",
        border=border,
    )
    hbox_layout = widgets.Layout(
        width="auto",
        align_items="stretch",
        border=border, # "solid 1px"
        display="flex",
        flex_flow="row",
        justify_content="space-between"
    )
    vbox_layout = widgets.Layout(
        width="auto",
        align_items="stretch",
        border=border,
        display="flex",
        flex_flow="column",
        justify_content="space-between"
    )
    header_layout = widgets.Layout(
        width="auto",
        border="solid 2px",
        display="flex",
        justify_content="center",
    )

    # Output dict
    output = {
        "autow": width_auto_layout,
        "hbox": hbox_layout,
        "vbox": vbox_layout,
        "header": header_layout
    }

    # Error check & output
    try:
        return output[layout]
    except:
        raise SyntaxError(f"List of layout: {list(output.keys())}")


def make_header(value: str = "Header"):
    """Create quick header"""
    return widgets.Label(value=value, layout=get_layout("header"))


def make_intbox(label: str, value: int,
                is_bounded:bool = False, min:int = 0, max:int = 1000000):
    """Make IntBox
    """
  
    if is_bounded:
        init_box = widgets.IntText(
            value=value,
            layout=get_layout("autow")
        )
    else:
        init_box = widgets.BoundedIntText(
            value=value,
            min=min,
            max=max,
            step=1,
            layout=get_layout("autow")
        )
  
    final_box = widgets.HBox(
        [widgets.Label(value=label), init_box],
        layout=get_layout("hbox")
    )

    return final_box


def make_date_select(label: str = "Date to calculate to:"):
    date_s = widgets.DatePicker(
        value=datetime.now().date() + relativedelta(days=1),
        layout=get_layout("autow")
    )
    date_select = widgets.HBox(
        [widgets.Label(value=label), date_s],
        layout=get_layout("hbox")
    )
    return date_select


def make_bool_box(value: bool = False, desc: str = None, disabled: bool = False,
                  button_style: str = "", tooltip: str = None, border: str = None):
    bool_box = widgets.ToggleButton(
        value=value,
        description=desc,
        disabled=disabled,
        button_style=button_style, # 'success', 'info', 'warning', 'danger' or ''
        tooltip=tooltip,
        layout=get_layout("autow", border=border)
    )
    return bool_box


def make_gui():
    """Make GUI
    """

    # Make primogem int input box
    pg_int = make_intbox("Primogem:", 0)

    # Make intertwined fate int input box
    if_int = make_intbox("Intertwined Fate:", 0)

    # Make masterless starglitter int input box
    mg_int = make_intbox("Masterless Starglitter:", 0)

    # Make date select
    date_s = make_date_select()

    # Make option box
    option_box = widgets.VBox([
        make_bool_box(
            value=True,
            desc="Include Fates from shop",
            tooltip="Add Primogems from monthly shop reset",
            border="solid 1px"
        ),
        make_bool_box(
            value=True,
            desc="Include Glitters from rolls",
            tooltip="Add Primogems from extra masterless glitters when gacha",
            border="solid 1px"
        )
    ], layout=get_layout("vbox"))

    # Make base box
    base_box = widgets.HBox([
        widgets.VBox([pg_int, if_int], layout=get_layout("vbox")),
        widgets.VBox([mg_int, date_s], layout=get_layout("vbox")),
        option_box
    ], layout=get_layout("autow"))

    # Make Abyss box
    ab_box = widgets.VBox([
        make_bool_box(desc="Include abyss",
                        tooltip="Add Primogems obtained by abyss"),
        make_intbox("Star:", 0, 1, 0, 36)
    ], layout=get_layout("vbox","solid 1px"))

    # Make Genesis Crystal box
    genesis_box = widgets.VBox([
        make_bool_box(desc="Include Genesis Crystal",
                        tooltip="Add Primogems when converting Genesis Crystals"),
        make_intbox("Genesis Crystal:", 0)
    ], layout=get_layout("vbox","solid 1px"))

    # Make welkin box
    welkin_box = widgets.VBox([
        make_bool_box(desc="Include Welkin",
                        tooltip="Add Primogems when having Welkin"),
        make_date_select()
    ], layout=get_layout("vbox","solid 1px"))

    # Make extra box
    extra_box = widgets.VBox([
        make_bool_box(desc="Include extra Primogem",
                        tooltip="Add extra Primogems"),
        make_intbox("Extra:", 0)
    ], layout=get_layout("vbox","solid 1px"))

    # Make option2 box
    option_box2 = widgets.HBox(
        [ab_box, extra_box, welkin_box, genesis_box],
        layout=get_layout("autow")
    )

    # # Make Calculate button
    # cal_butt = widgets.Button(
    #     description="Calculate!",
    #     tooltip="Calculate number of Intertwined Fate"
    # )

    # Make GUI
    final_box = widgets.VBox(
        [base_box, option_box2],
        layout=get_layout("vbox")
    )

    # Return GUI
    return final_box


def get_value(gui):
    """Get value from GUI
    """

    # Extract data
    # Pt. 01
    sector1 = gui.children[0] # primo, fate, glit, date, shop, roll
    s1b1 = sector1.children[0] # primo, fate
    prim = s1b1.children[0].children[1].value # primo
    ifate = s1b1.children[1].children[1].value # fate

    s1b2 = sector1.children[1] # glit, date
    mglit = s1b2.children[0].children[1].value # glit
    ndate = str(s1b2.children[1].children[1].value) # date

    s1b3 = sector1.children[2] # shop, roll
    shop = s1b3.children[0].value # shop
    roll = s1b3.children[1].value # roll

    # Pt. 02
    sector2 = gui.children[1] # abyss, extra, welkin, genesis
    s2b1 = sector2.children[0] # abyss
    ab_butt = s2b1.children[0].value # bool
    ab_star = s2b1.children[1].children[1].value # star
    if ab_star > 36: ab_star = 36

    s2b2 = sector2.children[1] # extra
    ex_butt = s2b2.children[0].value # bool
    extragem = s2b2.children[1].children[1].value # extra

    s2b3 = sector2.children[2] # welkin
    we_butt = s2b3.children[0].value # bool
    wdate = str(s2b3.children[1].children[1].value) # welkin date

    s2b4 = sector2.children[3] # genesis
    ge_butt = s2b4.children[0].value # bool
    genee = s2b4.children[1].children[1].value # genesis

    # Output
    output = {
        "primo": prim,
        "ifate": ifate,
        "glit": mglit,
        "date": ndate,
        "inl_fate": shop,
        "inl_glit": roll,
        "inl_ab": ab_butt,
        "star": ab_star,
        "inl_ex": ex_butt,
        "ex": extragem,
        "inl_wel": we_butt,
        "wdate": wdate,
        "inl_gen": ge_butt,
        "gen": genee
    }

    return output



def if_cal(gui):
    """Calculate from get_value(data)
    """
    data = get_value(gui)

    result = fate_result(
        primogem = data["primo"],
        intertwined_fate = data["ifate"],
        include_extra_fates_from_shop = data["inl_fate"],
        masterless_starglitter = data["glit"],
        date_to_calculate_to = data["date"],
        include_abyss = data["inl_ab"],
        abyss_star = data["star"],
        include_extra_glitters_from_rolls = data["inl_glit"],
        include_extra_primogem = data["inl_ex"],
        extra_primogem = data["ex"],
        have_welkin = data["inl_wel"],
        welkin_date_end = data["wdate"],
        include_genesis_crystal = data["inl_gen"],
        genesis_crystal = data["gen"],
    )

    return result



def example(option:int = 2):
    """
    Provide code tutorial to make this works
    """

    OPTION1 = """\
#@title **Intertwined Fate Calculator** {run: "auto", vertical-output: true, display-mode: "form"}

# Install Packages
!pip install -U -q absfuyu[rich]
!pip install -U -q rich[jupyter]

# Import
from absfuyu.extensions.dev.primo_cal import (
    clear_output, display,
    Panel, make_gui, if_cal, widgets
)
from rich.jupyter import print
clear_output(wait=True)

# Make GUI
calculator = make_gui()

# Make Calculate button
cal_butt = widgets.Button(
    description="Calculate!",
    tooltip="Calculate number of Intertwined Fate"
)

def on_button_clicked(b):
    result = if_cal(calculator)
    with output:
        clear_output(wait=True)
        print(Panel(result, title="[b]Result[/]"))

cal_butt.on_click(on_button_clicked)

# Output
output = widgets.Output()

# Final
display(calculator, cal_butt, output)
"""
    # Short ver
    OPTION2 = """\
#@title **Intertwined Fate Calculator** {run: "auto", vertical-output: true, display-mode: "form"}

!pip install -U -q absfuyu[rich]
!pip install -U -q rich[jupyter]

from absfuyu.extensions.dev.primo_cal import (
    clear_output, display,
    Panel, make_gui, if_cal, widgets
)
from rich.jupyter import print
clear_output(wait=True)

calculator = make_gui()
cal_butt = widgets.Button(description="Calculate!")
def on_button_clicked(b):
    result = if_cal(calculator)
    with output:
        clear_output(wait=True)
        print(Panel(result, title="[b]Result[/]"))
cal_butt.on_click(on_button_clicked)

output = widgets.Output()
display(calculator, cal_butt, output)
"""
    if option == 1:
        return OPTION1
    elif option == 2:
        return OPTION2
    else:
        return OPTION2
