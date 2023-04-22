import GUI
from streamlit_folium import folium_static
import folium

def execute_code_on_map_interaction(map):
    lat, lng = map['last_clicked']['lat'], map['last_clicked']['lng']
    print(lat, lng)



# f = open('index.html', 'r')

# map = st_folium(m, height=350, width=700)
# data = map['last_clicked']['lat'], map['last_clicked']['lng']
# data = get_pos(map['last_clicked']['lat'],map['last_clicked']['lng'])
# if data is not None:
#    st.write(data)
# print(data)
# f.close()
