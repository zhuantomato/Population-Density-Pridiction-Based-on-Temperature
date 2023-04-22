import folium
import codecs
import streamlit as st
from folium import LatLngPopup
from streamlit_folium import st_folium

m = folium.Map(location=[39.9, 116.3], zoom_start=5, control_scale=True)
m.add_child(folium.LatLngPopup())
m.save("index.html")