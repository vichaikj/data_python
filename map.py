import folium, csv, branca

LATS = []
LONGS = []
VICTS = []
LV = []
with open("mass_shooting.csv", mode='r', encoding="utf8") as f:
    r = csv.reader(f, delimiter=',')
    l = list(r)

    for i in l[1:]:
        if float(i[20]) != 36.095739 and float(i[21]) != -115.171544: # coordonnées de l'attentat de Las Vegas
            LATS.append(i[20])
            LONGS.append(i[21])
            VICTS.append(int(i[6]))
        else: # on sépare les données des victimes de Las Vegas car trop élevée comparé au reste
            LV.append(i[20])
            LV.append(i[21])
            LV.append(i[6])


coords = (38.622022, -100.179212)
map = folium.Map(location=coords, tiles='OpenStreetMap', zoom_start=5)

# on place un point rouge spécifique aux victimes de Las Vegas
for i in range(len(LATS)):
    folium.CircleMarker(
        location = [LV[0], LV[1]],
        radius = 50,
        color = None,
        fill = True,
        fill_color = 'crimson',
        fill_opacity = 0.2,
        tooltip = str(LV[2])+' victims'
    ).add_to(map)


# define a colorbar between min and max values
cm = branca.colormap.LinearColormap(['yellow', 'orange', 'red'], vmin=min(VICTS), vmax=max(VICTS))
map.add_child(cm) # add this colormap on the display

f = folium.map.FeatureGroup() # create a group

for lat, lng, size, color in zip(LATS, LONGS, VICTS, VICTS):
    f.add_child( # add iteratively a CircleMarker to this group
        folium.CircleMarker(
            location = [lat, lng],
            radius = size/2,
            color = None,
            fill = True,
            fill_color = cm(color),
            fill_opacity = 0.6,
            tooltip = str(size)+' victims')
    )

map.add_child(f) # add the group to the map
map.save(outfile='map.html')
