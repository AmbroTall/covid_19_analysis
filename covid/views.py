from django.shortcuts import render
import pandas as pd


df3 = pd.read_json('https://cdn.jsdelivr.net/gh/highcharts/highcharts@v7.0.0/samples/data/world-population-density.json')
def side_bar_data(request):
  cases = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv',encoding='utf-8', na_values=None)
  barPlot=cases[['Country/Region',cases.columns[-1]]].groupby('Country/Region').sum()
  barPlot=barPlot.reset_index()
  barPlot.columns = ['Country/Region','values']
  barPlot=barPlot.sort_values(by='values',ascending=False)
  barValues = barPlot['values'].values.tolist()
  countryNames=barPlot['Country/Region'].values.tolist()
  total_cases=cases[cases.columns[-1]].sum()
  dataForMap = mapData(barPlot, countryNames)
  showMap = True

  context ={

    "total_cases": total_cases,
    "countryNames":countryNames,
    "barValues": barValues,
    "dataForMap":dataForMap,
    "showMap": showMap
  }
  return render(request, 'covid/dashboard.html', context)



def mapData(barPlot, countryNames):
  dataForMap =[]
  for i in countryNames:
    try:
      tempdf = df3[df3['name'] ==i]
      temp = {}
      temp['code3']=list(tempdf['code3'].values)[0]
      temp['name'] = i
      temp['value'] = barPlot[barPlot['Country/Region']==i]['values'].sum()
      temp['code']=list(tempdf['code'].values)[0]
      dataForMap.append(temp)
    except:
      pass
  return dataForMap


def map_bar_data(request):
  countryNameSe = request.POST.get('countryName')
  cases = pd.read_csv(
    'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv',
    encoding='utf-8', na_values=None)
  barPlot = cases[['Country/Region', cases.columns[-1]]].groupby('Country/Region').sum()
  barPlot = barPlot.reset_index()
  barPlot.columns = ['Country/Region', 'values']
  barPlot = barPlot.sort_values(by='values', ascending=False)
  barValues = barPlot['values'].values.tolist()
  countryNames = barPlot['Country/Region'].values.tolist()
  total_cases = cases[cases.columns[-1]].sum()
  showMap = False


  countryDataSpe = pd.DataFrame(cases[cases['Country/Region']==countryNameSe][cases.columns[4:-1]].sum()).reset_index()
  countryDataSpe.columns=['country','values']
  countryDataSpe['lagVal']=countryDataSpe['values'].shift(1).fillna(0)
  countryDataSpe['incrementVal']=countryDataSpe['values']-countryDataSpe['lagVal']
  countryDataSpe['rollingMean']=countryDataSpe['incrementVal'].rolling(window=4).mean()
  countryDataSpe=countryDataSpe.fillna(0)
  datasetsForLine=countryDataSpe['values'].values.tolist()
  datasetsForLine2={'label':'Rolling Mean 4 days','data':countryDataSpe['rollingMean'].values.tolist()}
  axisvalues = countryDataSpe.index.tolist()

  context = {
    "datasetsForLine2":datasetsForLine2,
    "axisvalues":axisvalues,
    "total_cases": total_cases,
    "countryNames": countryNames,
    "barValues": barValues,
    "showMap" : showMap,
    "datasetsForLine":datasetsForLine,
    "countryNameSe":countryNameSe,

  }
  return render(request, 'covid/dashboard.html', context)