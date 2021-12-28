
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html

from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

################
# Logo
################
SGS_LOGO = "https://www.switchdoc.com/smartgarden3.png"



################
# Navbar
################
def Navbar():
    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("SG3 Status", href="/status_page")),
            dbc.NavItem(dbc.NavLink("SG3 Cameras", href="/camera_page")),
            dbc.NavItem(dbc.NavLink("Hydroponics", href="/hydroponics_page")),
            dbc.NavItem(dbc.NavLink("Valve Graphs", href="/valve_graphs")),
            dbc.NavItem(dbc.NavLink("Bluetooth Temp/Moisture Sensor Graphs", href="/bluetoothTM_page")),
            dbc.NavItem(dbc.NavLink("Bluetooth Light/Conductivity Sensor Graphs", href="/bluetoothLC_page")),
            #dbc.NavItem(dbc.NavLink("Wired Moisture Sensors", href="/wired_page")),
            dbc.NavItem(dbc.NavLink("Next Events", href="/valves_scheduled")),
            dbc.NavItem(dbc.NavLink("P/V Programming", href="/p_v_programming")),
            dbc.NavItem(dbc.NavLink("Alarm Programming", href="/alarm_page")),
            dbc.NavItem(dbc.NavLink("Bluetooth Sensor Status", href="/bluetooth_status_page")),
            dbc.NavItem(dbc.NavLink("Manual Control", href="/manual_page")),
            dbc.NavItem(dbc.NavLink("Logs", href="/log_page")),
                ],
                id='navbar',
                brand="SmartGarden3",
                brand_href="#",
                color="primary",
                dark=True,

    )
    return navbar

def Logo():
    logo = html.Img(src=SGS_LOGO, height=100, style={'margin' :'20px'})
    return logo



