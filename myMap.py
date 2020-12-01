import folium
import json
import pandas as pd

def buildMap(db):
    #carrega as fronteiras dos municipios
    #https://github.com/tbrugz/geodata-br
    municipios_sp = "./static/datasets/geojs-35-mun.json"
    geo_json_data = json.load(open(municipios_sp,encoding='utf-8'))
    
    #carrega valores latitude e longitude por municipio do BR
    #https://github.com/kelvins/Municipios-Brasileiros/blob/main/csv/municipios.csv

    data_collection= db['beneficioDataAPI']
    documents = data_collection.find()

    df=pd.DataFrame()
    COLUNAS = [
        'nomeIBGE',
        'latitude',
        'longitude',
        'MaxBeneficiados']
    df=pd.DataFrame(columns=COLUNAS)

    lis_mes=[]
    for x in range(1,13):
        if x <10:
            lis_mes.append('m0'+str(x))
        else:
            lis_mes.append('m'+str(x))

    lis_dict=[]
    if(documents != None):
        for document in documents:
            max_benef=[]
            for i in lis_mes:
                max_benef.append(document['mesRef'][i]['quantidadeBeneficiados'])
            var_max= max(max_benef)

            row_dict={
                'nomeIBGE':document['nomeIBGE'],
                'latitude': document['latitude'],
                'longitude': document['longitude'],
                'MaxBeneficiados':var_max}

            lis_dict.append(row_dict)
    df=pd.DataFrame(lis_dict)

    #df=pd.read_csv("./static/datasets/muni_lat_long.csv", delimiter=',')
    
    #reduzimos apenas para SP == 35
    #df=df[df['codigo_uf']==35]

    latitude = df['latitude']
    longitude = df['longitude']

    mapa = folium.Map(location=[-22.449, -48.6388], 
                    zoom_start=6.5)

    folium.GeoJson(geo_json_data, style_function=lambda feature: {'fillColor': 'green',
                                                                  'color': 'green','weight': 0.4,}).add_to(mapa)

    nome=df['nomeIBGE']
    beneficiados=df['MaxBeneficiados']
    for lat, lon, nom, benf in zip(latitude, longitude, nome,beneficiados):
        folium.Marker(location=[float(lat), float(lon)], popup=nom+'\n'+str(benf), icon=folium.Icon(color='orange')).add_to(mapa)
        
    mapa.save('templates/map.html')

        

        

        

        

        

        

        

        

        

        

        

        

        

        

