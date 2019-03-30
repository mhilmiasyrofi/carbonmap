# electricitymap [![Slack Status](http://slack.tmrow.co/badge.svg)](http://slack.tmrow.co) [![CircleCI](https://circleci.com/gh/tmrowco/electricitymap-contrib.svg?style=shield)](https://circleci.com/gh/tmrowco/electricitymap-contrib) [![Twitter Follow](https://img.shields.io/twitter/follow/electricitymap.svg?style=social&label=Follow)](https://twitter.com/electricitymap)
A real-time visualisation of the Greenhouse Gas (in terms of CO<sub>2</sub> equivalent) footprint of electricity consumption built with [d3.js](https://d3js.org/) and [mapbox GL](https://github.com/mapbox/mapbox-gl-js/), maintained by [Tomorrow](https://www.tmrow.com). Try it out at [http://www.electricitymap.org](http://www.electricitymap.org), or download the app:

[![Get it on Google Play](https://cloud.githubusercontent.com/assets/1655848/25219122/99b446e6-25ad-11e7-934f-9491d2eb6c9b.png)](https://play.google.com/store/apps/details?id=com.tmrow.electricitymap&utm_source=github) [![Get it on the Apple Store](https://cloud.githubusercontent.com/assets/1655848/25218927/e0ec8bdc-25ac-11e7-8df8-7ab62787303e.png)](https://itunes.apple.com/us/app/electricity-map/id1224594248&utm_source=github)


![image](https://www.electricitymap.org/images/electricitymap_social_image.jpg)

You can [contribute](#contribute) by
- **[adding a new country on the map](#adding-a-new-country)**
- correcting [data sources](#data-sources) and [capacities](#updating-country-capacities)
- [translating](https://github.com/tmrowco/electricitymap-contrib/tree/master/web/locales) the map
- fixing existing [issues](https://github.com/tmrowco/electricitymap-contrib/issues)
- submitting ideas, feature requests, or bugs in the [issues](https://github.com/tmrowco/electricitymap-contrib/issues) section.

You can also see a list of missing data displayed as warnings in the developer console, or question marks in the country panel:

![image](https://cloud.githubusercontent.com/assets/1655848/16256617/9c5872fc-3853-11e6-8c84-f562679086f3.png)

Check the [contributing](#contribute) section for more details.
Join us on [Slack](https://slack.tmrow.com) if you wish to discuss development or need help to get started.

## Frequently asked questions

**How do you define real-time data?**
Real-time data is defined as a data source with an hourly (or better) frequency, delayed by less than 2hrs. It should provide a breakdown by generation type. Often fossil fuel generation (coal/gas/oil) is combined under a single heading like 'thermal' or 'conventional', this is not a problem.

**Why do you calculate the carbon intensity of *consumption*?**
In short, citizens should not be responsible for the emissions associated with all the products they export, but only for what they consume.
Consumption-based accounting (CBA) is a very important aspect of climate policy, and allows to assign responsibility to consumers instead of producers.
Furthermore, this method is robust to governments relocating dirty production to neighbouring countries in order to green their image while still importing from it.
We published our methodology [here](https://arxiv.org/abs/1812.06679).

**Why don't you show emissions per capita?**
A country that has few inhabitants but a lot of factories will appear high on CO<sub>2</sub>/capita.
This means you can "trick" the numbers by moving your factory abroad and import the produced *good* instead of the electricity itself.
That country now has a low CO<sub>2</sub>/capita number because we only count CO<sub>2</sub> for electricity (not for imported/exported goods).
The CO<sub>2</sub>/capita metric, by involving the size of the population, and by not integrating all CO<sub>2</sub> emission sources, is thus an incomplete metric.
CO<sub>2</sub> intensity on the other hand only describes where is the best place to put that factory (and when it is best to use electricity), enabling proper decisions.

**CO<sub>2</sub> emission factors look high — what do they cover exactly?**
The carbon intensity of each type of power plant takes into account emissions arising from the whole life cycle of the plant (construction, fuel production, operational emissions, and decommissioning).

**Is delayed data useful?**
While the map relies on having real-time data to work it's still useful to collect data from days/months past. This older data can be used to show past emissions and build up a better dataset. So if there's an hourly data source that lags several days behind you can still build a parser for it.

**Can scheduled/assumed generation data be used?**
The electricitymap doesn't use scheduled generation data or make assumptions about unknown fuel mixes. This is to avoid introducing extra uncertainty into emissions calculations.

**Can areas other than countries be shown?**
Yes providing there is a valid GeoJSON geometry (or another format that can be converted) for the area. As an example we already split several countries into states and grid regions.

**How can I get access to historical data or the live API?**
All this and more can be found **[here](https://api.electricitymap.org/)**.

## Data sources

### Carbon intensity calculation and data source
The carbon intensity of each country is measured from the perspective of a consumer. It represents the greenhouse gas footprint of 1 kWh consumed inside a given country. The footprint is measured in gCO<sub>2</sub>eq (grams CO<sub>2</sub> equivalent), meaning each greenhouse gas is converted to its CO<sub>2</sub> equivalent in terms of global warming potential over 100 year (for instance, 1 gram of methane emitted has the same global warming impact during 100 years as ~20 grams of CO<sub>2</sub> over the same period).

The carbon intensity of each type of power plant takes into account emissions arising from the whole life cycle of the plant (construction, fuel production, operational emissions, and decommissioning). Carbon-intensity factors used in the map are detailed in [co2eq_parameters.json](https://github.com/tmrowco/electricitymap-contrib/blob/master/config/co2eq_parameters.json). These numbers come mostly from the following scientific peer reviewed literature: IPCC (2014) Fifth Assessment Report is used as reference in most instances (see a summary in the [wikipedia entry](https://en.wikipedia.org/wiki/Life-cycle_greenhouse-gas_emissions_of_energy_sources#2014_IPCC.2C_Global_warming_potential_of_selected_electricity_sources))

Each country has a CO<sub>2</sub> mass flow that depends on neighbouring countries. In order to determine the carbon footprint of each country, the set of coupled CO<sub>2</sub> mass flow balance equations of each countries must be solved simultaneously. This is done by solving the linear system of equations defining the network of greenhouse gas exchanges. Take a look at this [notebook](https://github.com/tmrowco/electricitymap-contrib/blob/master/CO2eq%20Model%20Explanation.ipynb) for a deeper explanation. We also published our methodology [here](https://arxiv.org/abs/1812.06679).


### Real-time electricity data sources
Real-time electricity data is obtained using [parsers](https://github.com/tmrowco/electricitymap-contrib/tree/master/parsers)
&nbsp;<details><summary>Click to see the full list of sources</summary>
- Åland: [Kraftnät Åland](http://www.kraftnat.ax/text2.con?iPage=28&iLan=1)
- Argentina: [Cammesa](http://portalweb.cammesa.com/Memnet1/default.aspx)
- Aruba: [WEB Aruba](https://www.webaruba.com/renewable-energy-dashboard/aruba) ([JSON](https://www.webaruba.com/renewable-energy-dashboard/app/rest/results.json))
- Australia: [AREMI National Map](http://nationalmap.gov.au/renewables/)
  ([CSV](http://services.aremi.nationalmap.gov.au/aemo/v3/csv/all))
- Australia (Western): [AEMO](http://wa.aemo.com.au/Electricity/Wholesale-Electricity-Market-WEM/Data-dashboard)
  ([CSV](http://wa.aemo.com.au/aemo/data/wa/infographic/facility-intervals-last96.csv))
- Australia (distributed solar generation): [Australian PV Institute](http://pv-map.apvi.org.au/live)
- Australia (South Battery): [Nemwatch](https://ausrealtimefueltype.global-roam.com/expanded)
- Austria: [ENTSOE](https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html)
- Bangladesh: [PGCB](https://pgcb.org.bd/PGCB/?a=pages/operational_daily.php)
- Bosnia and Herzegovina: [ENTSOE](https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html)
- Bolivia: [CNDC](http://www.cndc.bo/media/archivos/graf/gene_hora/gweb_despdia_genera.php)
- Belgium: [ENTSOE](https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html)
- Brazil: [ONS](http://www.ons.org.br/pt/paginas/energia-agora/carga-e-geracao)
- Bulgaria: [TSO](http://tso.bg/default.aspx/page-707/bg)
- Canada (Alberta): [AESO](http://ets.aeso.ca/ets_web/ip/Market/Reports/CSDReportServlet)
- Canada (New Brunswick): [NB Power](https://tso.nbpower.com/Public/en/op/market/data.aspx)
- Canada (Nova Scotia): [Nova Scotia Power](http://www.nspower.ca/en/home/about-us/todayspower.aspx)
- Canada (Ontario): [IESO](http://www.ieso.ca/power-data)
- Canada (Prince Edward Island): [Government of PEI](https://www.princeedwardisland.ca/en/feature/pei-wind-energy/)
- Canada (Yukon): [Yukon Energy](http://www.yukonenergy.ca/energy-in-yukon/electricity-101/current-energy-consumption)
- Chile (SIC): [SIC](https://sic.coordinador.cl/informes-y-documentos/fichas/operacion-real/)
- Chile (SING): [SGER](https://sger.coordinadorelectrico.cl/Charts/AmChartCurvaCompuesta?showinfo=True)
- Czech Republic: [ENTSOE](https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html)
- Costa Rica: [ICE](https://appcenter.grupoice.com/CenceWeb/CencePosdespachoNacional.jsf)
- Croatia (Exchanges): [HOPS](https://www.hops.hr/wps/portal/hr/web)
- Cyprus : [TSO](http://www.dsm.org.cy/en/daily-system-generation-on-the-transmission-system-mw)
- Denmark: [TSO](https://www.energidataservice.dk/en/group/production-and-consumption)
- Denmark (Bornholm): [PowerlabDK](http://bornholm.powerlab.dk/)
- Dominican Republic: [OC](http://www.oc.org.do/Reportes/postdespacho.aspx)
- El Salvador: [Unidad de Transacciones](http://estadistico.ut.com.sv/OperacionDiaria.aspx)
- Estonia: [ENTSOE](https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html)
- Faroe Islands: [SEV](https://w3.sev.fo/framleidsla/)
- Finland: [ENTSOE](https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html)
- France: [RTE](https://opendata.reseaux-energies.fr)
- Germany: [ENTSOE](https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html)
- Georgia: [GSE](http://www.gse.com.ge/home)
- Great Britain: [ENTSOE](https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html)
- Great Britain (Orkney Islands): [SSEN](https://www.ssen.co.uk/ANM/)
- Greece: [ENTSOE](https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html)
- Guatemala : [AMM](http://www.amm.org.gt)
- Hungary: [ENTSOE](https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html)
- Iceland: [LANDSNET](http://amper.landsnet.is/MapData/api/measurements)
- Ireland: [ENTSOE](https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html)
- Italy: [ENTSOE](https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html)
- India: [meritindia](http://meritindia.in/)
- India (Andhra Pradesh): [CORE Dashboard](https://core.ap.gov.in/CMDashBoard/UserInterface/Power/PowerReport.aspx)
- India (Chhattisgarh): [cspc.co.in](http://117.239.199.203/csptcl/GEN.aspx)
- India (Delhi): [delhisldc](http://www.delhisldc.org/Redirect.aspx?Loc=0804)
- India (Gujarat): [sldcguj](https://www.sldcguj.com/RealTimeData/RealTimeDemand.php)
- India (Karnataka): [kptclsldc.com](http://kptclsldc.com/StateGen.aspx)
- India (Punjab): [punjabsldc](http://www.punjabsldc.org/pungenrealw.asp?pg=pbGenReal)
- India (Uttar Pradesh): [upsldc](http://www.upsldc.org/real-time-data)
- India (Uttarakhand): [uksldc](http://uksldc.in/real-time-data.php)
- Iraq: [Iraqi Power System](http://109.224.53.139:8080/IPS.php)
- Japan (Exchanges): [OCCTO](http://occtonet.occto.or.jp/public/dfw/RP11/OCCTO/SD/LOGIN_login)
- Japan (Chūbu): [Chūden](http://denki-yoho.chuden.jp/)
- Japan (Chūgoku): [Energia](http://www.energia.co.jp/jukyuu/)
- Japan (Hokkaidō): [Hokuden](http://denkiyoho.hepco.co.jp/area_forecast.html)
- Japan (Hokuriku): [Rikuden](http://www.rikuden.co.jp/denki-yoho/)
- Japan (Kansai): [Kepco](http://www.kepco.co.jp/energy_supply/supply/denkiyoho/)
- Japan (Kyūshū): [Kyūden](http://www.kyuden.co.jp/power_usages/pc.html)
- Japan (Kyūshū/Genkai NPP): [Kyūden](http://www.kyuden.co.jp/php/nuclear/genkai/rename.php?A=g_power.fdat&B=ncp_state.fdat&_=1520532904073)
- Japan (Kyūshū/Sendai NPP): [Kyūden](http://www.kyuden.co.jp/php/nuclear/sendai/rename.php?A=s_power.fdat&B=ncp_state.fdat&_=1520532401043)
- Japan (Shikoku): [Yonden](http://www.yonden.co.jp/denkiyoho/)
- Japan (Tōhoku-Niigata): [TH-EPCO](http://setsuden.tohoku-epco.co.jp/graph.html)
- Japan (Tōkyō area): [TEPCO](http://www.tepco.co.jp/forecast/html/images/juyo-j.csv)
- Latvia: [ENTSOE](https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html)
- Lithuania: [ENTSOE](https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html)
- Malaysia: [GSO](https://www.gso.org.my/LandingPage.aspx)
- Moldova: [MoldElectrica](http://www.moldelectrica.md/ro/activity/system_state)
- Montenegro: [ENTSOE](https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html)
- Namibia: [NamPower](http://www.nampower.com.na/Scada.aspx)
- Netherlands: [ENTSOE](https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html)
- New Zealand: [Transpower](https://www.transpower.co.nz/power-system-live-data)
- Nicaragua: [CNDC](http://www.cndc.org.ni/)
- Northern Ireland: [SONI](http://www.soni.ltd.uk/InformationCentre/)
- Norway: [ENTSOE](https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html)
- Panama: [CND](http://sitr.cnd.com.pa/m/pub/gen.html)
- Peru: [COES](http://www.coes.org.pe/Portal/portalinformacion/Generacion)
- Poland: [ENTSOE](https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html)
- Portugal: [ENTSOE](https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html)
- Romania: [ENTSOE](https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html)
- Russia: [SO-UPS](http://br.so-ups.ru/Public/MainPageData/BR/PowerGeneration.aspx)
- Serbia: [ENTSOE](https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html)
- Singapore: [EMC](https://www.emcsg.com)
- Singapore (Solar): [EMA](https://www.ema.gov.sg/solarmap.aspx)
- Slovakia: [ENTSOE](https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html)
- Slovenia: [ENTSOE](https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html)
- Spain: [ENTSOE](https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html)
- Spain (Canary Islands): [REE](https://demanda.ree.es/movil)
- Spain (Balearic Islands): [REE](https://demanda.ree.es/movil)
- Sweden: [SVK](https://www.svk.se/en/national-grid/the-control-room/)
- Switzerland: [ENTSOE](https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html)
- Taiwan: [TAIPOWER](http://www.taipower.com.tw/d006/loadGraph/loadGraph/genshx_.html)
- Turkey: [ytbs](https://ytbs.teias.gov.tr/ytbs/frm_login.jsf)
- Ukraine: [UKRENERGO](https://ua.energy/activity/dispatch-information/ues-operation/)
- United States of America
  - Bonneville Power Authority: [BPA](https://transmission.bpa.gov/business/operations/Wind/baltwg.txt)
  - California: [CAISO](http://www.caiso.com/Pages/default.aspx)
  - Idaho Power Company: [IPC](https://www.idahopower.com/energy/delivering-power/generation-and-demand/)
  - MISO: [MISO](https://api.misoenergy.org/MISORTWDDataBroker/DataBrokerServices.asmx?messageType=getfuelmix&returnType=json)
  - New England: [NEISO](https://www.iso-ne.com/isoexpress/)
  - New York: [NYISO](http://www.nyiso.com/public/markets_operations/market_data/graphs/index.jsp)
  - PJM: [PJM](http://www.pjm.com/markets-and-operations.aspx)
  - Southwest Power Pool: [SPP](https://marketplace.spp.org/pages/generation-mix)
  - Southwest Variable Energy Resource Initiative: [SVERI](https://sveri.energy.arizona.edu/#generation-by-fuel-type)
  - Texas: [ERCOT](http://www.ercot.com/content/cdr/html/real_time_system_conditions.html)
- Uruguay: [UTE](http://www.ute.com.uy/SgePublico/ConsPotenciaGeneracionArbolXFuente.aspx)
&nbsp;</details>

### Production capacity data sources
Production capacities are centralized in the [zones.json](https://github.com/tmrowco/electricitymap-contrib/blob/master/config/zones.json) file.
&nbsp;<details><summary>Click to see the full list of sources</summary>
- Argentina: [Cammesa](http://portalweb.cammesa.com/Documentos%20compartidos/Noticias/Informe%20Anual%202016.pdf)
- Aruba: [WEB Aruba](https://www.webaruba.com/energy-production/power-production-figures)
- Australia [wikipedia.org](https://en.wikipedia.org/wiki/Wind_power_in_Australia#Wind_power_by_state)
- Austria
  - Wind: [IGWindKraft](https://www.igwindkraft.at)
  - Other: [ENTSO-E](https://transparency.entsoe.eu/generation/r2/installedGenerationCapacityAggregation/show)
- Belarus: [belstat.gov.by](http://www.belstat.gov.by/upload/iblock/7f7/7f70938f51eb9e49abc4a6e62f831a2c.rar), [RenEn](http://director.by/zhurnal/arkhiv-zhurnala/arkhiv-nomerov-2017/375-7-2017-iyul-2017/5456-zelenaya-energetika-nabiraet-oboroty)
- Belgium: [ENTSO-E](https://transparency.entsoe.eu/generation/r2/installedGenerationCapacityAggregation/show)
- Bolivia: [CNDC](http://www.cndc.bo/agentes/generacion.php)
- Brazil: [ONS](http://www.ons.org.br/Paginas/resultados-da-operacao/historico-da-operacao/capacidade_instalada.aspx)
- Bulgaria: [wikipedia.org](https://en.wikipedia.org/wiki/Energy_in_Bulgaria)
- Canada (British Columbia, Manitoba, New Brunswick, Newfoundland and Labrador, Nova Scotia, Prince Edward Island):
    [wikipedia.org](https://en.wikipedia.org/wiki/List_of_generating_stations_in_Canada)
- Canada (Ontario): [IESO](http://www.ieso.ca/en/Power-Data/Supply-Overview/Transmission-Connected-Generation)
- Canada (Québec): [Hydro-Québec](http://www.hydroquebec.com/generation/)
- Canada (Saskatchewan): [SaskPower](http://www.saskpower.com/our-power-future/our-electricity/)
- Chile (SIC)
  - Geothermal, Hydro, Solar, Wind: [SIC](https://sic.coordinador.cl/capacidad-instalada/)
  - Other: [energiaabierta.cl](http://energiaabierta.cl/visualizaciones/capacidad-instalada/)
- Chile (SING)
  - Solar/Wind: [SGER](https://sger.coordinadorelectrico.cl/Plants/InstalledCapacity)
  - Other: [energiaabierta.cl](http://energiaabierta.cl/visualizaciones/capacidad-instalada/)
- Czech Republic: [ENTSO-E](https://transparency.entsoe.eu/generation/r2/installedGenerationCapacityAggregation/show)
- Denmark (DK1 and DK2): [ENTSO-E](https://transparency.entsoe.eu/generation/r2/installedGenerationCapacityAggregation/show)
- Denmark (Bornholm)
  - Wind: [stateofgreen.com](https://stateofgreen.com/en/profiles/regional-municipality-of-bornholm/solutions/kalby-wind-turbines)
- Dominican Republic: [Climatescope](http://global-climatescope.org/en/country/dominican-republic/#/details)
- El Salvador:
  - Thermal: [CNE](http://estadisticas.cne.gob.sv/wp-content/uploads/2016/09/Plan_indicativo_2016_2026-1.pdf)
  - Biomass, Geothermal, Hydro & Solar: [IRENA](http://resourceirena.irena.org/gateway/countrySearch/?countryCode=SLV)
- Estonia:
  - Biomass & Solar: [IRENA](http://resourceirena.irena.org/gateway/countrySearch/?countryCode=EST)
  - Other: [ENTSO-E](https://transparency.entsoe.eu/generation/r2/installedGenerationCapacityAggregation/show)
- Faroe Islands: [Johan Pauli Magnussen's Thesis, p44](https://setur.fo/uploads/tx_userpubrep/BScThesis_JohanPauliMagnussen.pdf)
- Finland: [ENTSO-E](https://transparency.entsoe.eu/generation/r2/installedGenerationCapacityAggregation/show)
- France: [RTE](http://bilan-electrique-2017.rte-france.com/production/le-parc-de-production-national/)
- Germany: [Frauenhofer ISE](https://www.energy-charts.de/power_inst.htm?year=2018&period=annual&type=power_inst)
- Georgia: [GSE](http://www.gse.com.ge/for-customers/data-from-the-power-system)
- Great Britain: [ENTSO-E](https://transparency.entsoe.eu/generation/r2/installedGenerationCapacityAggregation/show)
- Greece: [ENTSO-E](https://transparency.entsoe.eu/generation/r2/installedGenerationCapacityAggregation/show)
- Guatemala: [AMM](http://www.amm.org.gt/pdfs2/2017/Capacidad_Instalada_2017.xls)
- Hungary
  - Solar: [IRENA](http://resourceirena.irena.org/gateway/countrySearch/?countryCode=HUN)
  - Other[ENTSO-E](https://transparency.entsoe.eu/generation/r2/installedGenerationCapacityAggregation/show)
- Iceland: [Statistics Iceland](http://px.hagstofa.is/pxen/pxweb/en/Atvinnuvegir/Atvinnuvegir__orkumal/IDN02101.px)
- Ireland
  - All production types: [ENTSO-E](https://transparency.entsoe.eu/generation/r2/installedGenerationCapacityAggregation/show)
  - Biomass, Solar & Wind: [IRENA](http://resourceirena.irena.org/gateway/countrySearch/?countryCode=IRL)
- Italy
  - Wind & Solar: [IRENA](http://resourceirena.irena.org/gateway/countrySearch/?countryCode=ITA)
  - Other: [ENTSO-E](https://transparency.entsoe.eu/generation/r2/installedGenerationCapacityAggregation/show)
- India: [mercomindia](https://mercomindia.com/solar-indias-installed-power-capacity/)
- India (Andhra Pradesh): [wikipedia.org](https://en.wikipedia.org/wiki/Power_sector_of_Andhra_Pradesh)
- India (Chhattisgarh, Delhi, Gujarat, Karnataka, Punjab, Uttar Pradesh): [National Power Portal](https://npp.gov.in/dashBoard/cp-map-dashboard)
- Latvia: [ENTSO-E](https://transparency.entsoe.eu/generation/r2/installedGenerationCapacityAggregation/show)
- Lithuania: [ENTSO-E](https://transparency.entsoe.eu/generation/r2/installedGenerationCapacityAggregation/show)
- Malaysia: [GSO](https://www.gso.org.my/SystemData/PowerStation.aspx)
- Moldova: [FAS](http://en.fas.gov.ru/upload/other/National%20Agency%20for%20Energy%20Regulation%20(G.%20Pyrzy).pdf)
- Montenegro: [EPCG](http://www.epcg.com/en/about-us/production-facilities)
- Namibia
  - Coal & Oil: [NamPower](http://www.nampower.com.na/Page.aspx?p=182)
  - Hydro, solar & wind: [African Energy](https://www.africa-energy.com/database)
- Netherlands: [ENTSO-E](https://transparency.entsoe.eu/generation/r2/installedGenerationCapacityAggregation/show)
- Nicaragua: [Climatescope](http://global-climatescope.org/en/country/nicaragua/)
- Norway
  - Hydro: [NVE](https://www.nve.no/energiforsyning-og-konsesjon/vannkraft/vannkraftdatabase/)
  - Wind: [NVE](https://www.nve.no/energiforsyning-og-konsesjon/vindkraft/utbygde-vindkraftverk/)
  - Other: [ENTSO-E](https://transparency.entsoe.eu/generation/r2/installedGenerationCapacityAggregation/show)
- Northern Ireland: [EIR Grid](http://www.eirgridgroup.com/site-files/library/EirGrid/Generation_Capacity_Statement_20162025_FINAL.pdf)
- Poland: [ENTSO-E](https://transparency.entsoe.eu/generation/r2/installedGenerationCapacityAggregation/show)
- Portugal
  - Solar: [IRENA](http://resourceirena.irena.org/gateway/countrySearch/?countryCode=PTA)
  - Other: [ENTSO-E](https://transparency.entsoe.eu/generation/r2/installedGenerationCapacityAggregation/show)
- Romania:
  - Nuclear: [Nuclearelectrica](http://www.nuclearelectrica.ro/cne/)
  - Other: [ENTSO-E](https://transparency.entsoe.eu/generation/r2/installedGenerationCapacityAggregation/show)
- Russia: [Minenergo](https://minenergo.gov.ru/node/532)
- Serbia: [ENTSO-E](https://transparency.entsoe.eu/generation/r2/installedGenerationCapacityAggregation/show)
- Singapore
  - Solar: [Energy Market Authority Statistics](https://www.ema.gov.sg/statistic.aspx?sta_sid=20170711hc85chOLVvWp)
  - Other: [Energy Market Authority](https://www.ema.gov.sg/cmsmedia/Publications_and_Statistics/Publications/SES/2016/Singapore%20Energy%20Statistics%202016.pdf)
- Slovakia: [SEPS](https://www.sepsas.sk/Dokumenty/RocenkySed/ROCENKA_SED_2015.pdf)
- Slovenia: [ENTSO-E](https://transparency.entsoe.eu/generation/r2/installedGenerationCapacityAggregation/show)
- Spain:
  - Hydro: [IRENA](http://resourceirena.irena.org/gateway/countrySearch/?countryCode=ESP)
  - Other: [ENTSO-E](https://transparency.entsoe.eu/generation/r2/installedGenerationCapacityAggregation/show?name=&defaultValue=false&viewType=TABLE&areaType=BZN&atch=false&dateTime.dateTime=01.01.2017+00:00|UTC|YEAR&dateTime.endDateTime=01.01.2017+00:00|UTC|YEAR&area.values=CTY|10YES-REE------0!BZN|10YES-REE------0&productionType.values=B01&productionType.values=B02&productionType.values=B03&productionType.values=B04&productionType.values=B05&productionType.values=B06&productionType.values=B07&productionType.values=B08&productionType.values=B09&productionType.values=B10&productionType.values=B11&productionType.values=B12&productionType.values=B13&productionType.values=B14&productionType.values=B20&productionType.values=B15&productionType.values=B16&productionType.values=B17&productionType.values=B18&productionType.values=B19)
- Spain (Canary Islands)
  - Hydro storage: [goronadelviento.es](http://www.goronadelviento.es/)
  - Wind, Solar: [REE](http://www.ree.es/sites/default/files/11_PUBLICACIONES/Documentos/Renovables-2016-v3.pdf)
- Spain (Balearic Islands)
  - Coal: [wikipedia.org](https://es.wikipedia.org/wiki/Central_t%C3%A9rmica_de_Es_Murterar)
  - Wind, Solar: [REE](http://www.ree.es/sites/default/files/11_PUBLICACIONES/Documentos/Renovables-2016-v3.pdf)
- Sweden
  - Renewables: [IRENA](http://resourceirena.irena.org/gateway/countrySearch/?countryCode=SWE)
  - Other: [ENTSO-E](https://transparency.entsoe.eu/generation/r2/installedGenerationCapacityAggregation/show)
- Switzerland: [ENTSO-E](https://transparency.entsoe.eu/generation/r2/installedGenerationCapacityAggregation/show)
- Taiwan: [TAIPOWER](http://www.taipower.com.tw/d006/loadGraph/loadGraph/genshx_.html)
- Turkey: [TEİAŞ](https://www.teias.gov.tr/)
- Ukraine: [wikipedia.org](https://uk.wikipedia.org/wiki/%D0%95%D0%BB%D0%B5%D0%BA%D1%82%D1%80%D0%BE%D0%B5%D0%BD%D0%B5%D1%80%D0%B3%D0%B5%D1%82%D0%B8%D0%BA%D0%B0_%D0%A3%D0%BA%D1%80%D0%B0%D1%97%D0%BD%D0%B8)
- United States of America
  - Federal: [EIA](https://www.eia.gov/electricity/data.cfm#gencapacity)
  - States: [EIA](https://www.eia.gov/electricity/data/state/)
  - BPA: [BPA](https://transmission.bpa.gov/business/operations/Wind/baltwg.aspx)
  - CAISO: [CAISO](http://www.caiso.com/informed/Pages/CleanGrid/default.aspx)
  - MISO: [MISO](https://www.misoenergy.org/about/media-center/corporate-fact-sheet/)
  - NYISO: [NYISO Gold Book](https://home.nyiso.com/wp-content/uploads/2017/12/2017_Gold-Book.pdf)
  - PJM: [PJM](http://www.pjm.com/-/media/markets-ops/ops-analysis/capacity-by-fuel-type-2017.ashx?la=en)
  - SPP: [SPP](https://www.spp.org/about-us/fast-facts/)
&nbsp;</details>

### Cross-border transmission capacity data sources
Cross-border transmission capacities between the zones are centralized in the [exchanges.json](https://github.com/tmrowco/electricitymap-contrib/blob/master/config/exchanges.json) file.
&nbsp;<details><summary>Click to see the full list of sources</summary>
- Åland ⇄ Sweden: ["Sverigekabeln": 80 MW](http://www.kraftnat.ax/files/rapportdel_2.pdf)
- Åland ⇄ Finland: ["Brändö-Gustafs": 9 MW](http://www.kraftnat.ax/files/rapportdel_2.pdf)
- Australia (Victoria) ⇄ Australia (Tasmania): ["Basslink": 500 MW (regular) or 630 MW (temporarily)](https://en.wikipedia.org/wiki/Basslink)
- Denmark (West) ⇄ Norway: [“Skaggerak”: 1700 MW](https://en.wikipedia.org/wiki/Skagerrak_(power_transmission_system))
- Denmark (East) ⇄ Denmark (West): ["Storebælt HVDC": 600 MW](https://en.wikipedia.org/wiki/Great_Belt_Power_Link)
- Denmark (East) ⇄ Germany: ["Kontek": 600 MW](https://en.wikipedia.org/wiki/Kontek)
- Denmark (West) ⇄ Sweden: ["Konti-Skan": 650 MW](https://en.wikipedia.org/wiki/Konti%E2%80%93Skan)
- Estonia ⇄ Finnland: [“Estlink 1&2”: 1000 MW](https://en.wikipedia.org/wiki/Estlink)
- Germany ⇄ Sweden: [“Baltic Cable”: 600 MW](https://en.wikipedia.org/wiki/Baltic_Cable)
- Great Britain ⇄ North Ireland: [“Moyle”: 500 MW](http://www.wikiwand.com/en/HVDC_Moyle)
- Great Britain ⇄ Ireland: [“East-West Interconnector”: 500 MW](https://en.wikipedia.org/wiki/East%E2%80%93West_Interconnector)
- Great Britain ⇄ France: [“Cross-Channel”: 2000 MW](https://en.wikipedia.org/wiki/NorNed)
- Great Britain ⇄ Netherlands: ["BritNed": 1000 MW](https://en.wikipedia.org/wiki/BritNed)
- Greece ⇄ Italy: ["GRITA": 500 MW](https://en.wikipedia.org/wiki/HVDC_Italy%E2%80%93Greece)
- Lithuania ⇄ Sweden: [“NordBalt”: 700 MW](https://en.wikipedia.org/wiki/NordBalt)
- Lithuania ⇄ Poland: [“LitPol Link”: 500 MW](https://en.wikipedia.org/wiki/LitPol_Link)
- Norway ⇄ Netherlands: [“NorNed”: 700 MW](https://en.wikipedia.org/wiki/NorNed)
- New Zealand (North Island) ⇄ New Zealand (South Island): ["HVDC Inter-Island": 1200 MW](https://en.wikipedia.org/wiki/HVDC_Inter-Island)
- Malta ⇄ Italy: ["Malta–Sicily-Interconnector": 200 MW](https://en.wikipedia.org/wiki/Malta%E2%80%93Sicily_interconnector)
- Russia ⇉ Finland: ["Vyborg HVDC scheme": 1400 MW + 2 AC-connections: 160 MW](https://www.entsoe.eu/Documents/Publications/SOC/Nordic/System_Operation_Agreement_appendices(English_2016_update).pdf)
- Spain ⇄ Spain (Balearic Islands): ["Cometa": 400 MW](https://en.wikipedia.org/wiki/Cometa_(HVDC))
- Sweden ⇄ Poland: [“SwePol”: 600 MW](https://en.wikipedia.org/wiki/SwePol)

A ⇄ B: bidirectional operation, with power flow either "from A to B" or "from B to A"

A ⇉ B: unidirectional operation, only with power flow "from A to B"
&nbsp;</details>

### Electricity prices (day-ahead) data sources
- France: [RTE](http://www.rte-france.com/en/eco2mix/eco2mix-mix-energetique-en)
- Japan: [JEPX](http://www.jepx.org)
- Nicaragua: [CNDC](http://www.cndc.org.ni/)
- Singapore: [EMC](https://www.emcsg.com)
- Turkey: [EPIAS](https://seffaflik.epias.com.tr/transparency/piyasalar/gop/ptf.xhtml)
- Other: [ENTSO-E](https://transparency.entsoe.eu/transmission-domain/r2/dayAheadPrices/show)

### Real-time weather data sources
We use the [US National Weather Service's Global Forecast System (GFS)](http://nomads.ncep.noaa.gov/)'s GFS 0.25 Degree Hourly data.
Forecasts are made every 6 hours, with a 1 hour time step.
The values extracted are wind speed and direction at 10m altitude, and ground solar irradiance (DSWRF - Downward Short-Wave Radiation Flux), which takes into account cloud coverage.
In order to obtain an estimate of those values at current time, an interpolation is made between two forecasts (the one at the beginning of the hour, and the one at the end of the hour).


### Topology data
We use the [Natural Earth Data Cultural Vectors](http://www.naturalearthdata.com/downloads/10m-cultural-vectors/) country subdivisions (map admin subunits).


## Contribute
Want to help? Join us on slack at [http://slack.tmrow.co](http://slack.tmrow.co).

### Logger

We have a public [logger](https://kibana.electricitymap.org/app/kibana#/discover/10af54f0-0c4a-11e9-85c1-1d63df8c862c) which shows warnings and errors for all parsers.

### Running locally

To get started, [clone](https://help.github.com/articles/cloning-a-repository/) or [fork](https://help.github.com/articles/fork-a-repo/) the repository, and install [Docker](https://docs.docker.com/engine/installation/).

The frontend will need compiling. In order to do this, open a terminal in the root directory and run
```
docker-compose run --rm web npm run watch
```
This will watch over source file changes, and recompile if needed.

If you encounter any errors in the build process try the following command first:
```
docker-compose build
```
Now that the frontend is compiled, you can run the application by running the following command in a new terminal:
```
docker-compose up --build
```

Head over to [http://localhost:8000/](http://localhost:8000/) and you should see the map! Note that the backend is responsible for calculation carbon emissions, so the map will be empty.

If you have issues building the map locally check out the [Troubleshooting](###Troubleshooting) section for common problems and fixes.

Once you're done doing your changes, submit a [pull request](https://help.github.com/articles/using-pull-requests/) to get them integrated into the production version.

### Updating country capacities
If you want to update or add production capacities for a country then head over to the [zones file](https://github.com/tmrowco/electricitymap-contrib/blob/master/config/zones.json) and make any changes needed.
The zones use ISO 3166-1 codes as identifiers, a list of which can be found [here](https://en.wikipedia.org/wiki/ISO_3166-1#Current_codes).

### Adding a new country
It is very simple to add a new country. The Electricity Map backend runs a list of so-called *parsers* every 5min. Those parsers are responsible for fetching the generation mix of a given country (check out the existing list in the [parsers](https://github.com/tmrowco/electricitymap-contrib/tree/master/parsers) directory, or look at the [work in progress](https://github.com/tmrowco/electricitymap-contrib/issues?q=is%3Aissue+is%3Aopen+label%3Aparser)).

A parser is a python3 script that is expected to define the method `fetch_production` which returns the production mix at current time, in the format:

```python
def fetch_production(zone_key='FR', session=None, target_datetime=None, logger=None):
    return {
      'countryCode': 'FR',
      'datetime': '2017-01-01T00:00:00Z',
      'production': {
          'biomass': 0.0,
          'coal': 0.0,
          'gas': 0.0,
          'hydro': 0.0,
          'nuclear': None,
          'oil': 0.0,
          'solar': 0.0,
          'wind': 0.0,
          'geothermal': 0.0,
          'unknown': 0.0
      },
      'storage': {
          'hydro': -10.0,
      },
      'source': 'mysource.com'
    }
```

The `session` object is a [python request](http://docs.python-requests.org/en/master/) session that you can re-use to make HTTP requests.

`target_datetime` is used to fetch historical data (when available). `logger` is a `logging.Logger`
whose output is publicly available so that everyone can monitor correct functioning of the parsers.

The production values should never be negative. Use `None`, or omit the key if a specific production mode is not known.
Storage values can be both positive (when storing energy) or negative (when the storage is emptied).

The parser can also return an array of objects if multiple time values can be fetched. The backend will automatically update past values properly.

Once you're done, add your parser to the [zones.json](https://github.com/tmrowco/electricitymap-contrib/tree/master/config/zones.json) and [exchanges.json](https://github.com/tmrowco/electricitymap-contrib/tree/master/config/exchanges.json) configuration files. Finally update the [real-time sources](#real-time-electricity-data-sources).

Run all of the parser tests with the following command from the root directory.
```
python3 -m unittest discover parsers/test/
```

For more info, check out the [example parser](https://github.com/tmrowco/electricitymap-contrib/tree/master/parsers/example.py) or browse existing [parsers](https://github.com/tmrowco/electricitymap-contrib/tree/master/parsers).

### Generating a new map
If your changes involve altering the way countries are displayed on the map a new world.json will need to be generated. Make sure you're in the root directory then run the following command.
```
docker-compose run --rm web ./topogen.sh
```

For a more detailed explanation of how the map is generated see [here](https://github.com/tmrowco/electricitymap-contrib/blob/master/web/README.md).

### Testing parsers locally

In order to test your parser, make sure first that you have installed the required modules as described (consider using a [virtual environment](https://docs.python.org/3/library/venv.html)) in parsers/requirements.txt: for that you can run
```
pip install -r parsers/requirements.txt
```
#### testing a parser
From the root folder, use the `test_parser.py` command line utility:
```python
python test_parser.py FR price  # get latest price parser for France
python test_parser.py FR  # defaults to production if no data type is given
# test a specific datetime (parser needs to be able to fetch past datetimes)
python test_parser.py DE --target_datetime 2018-01-01T08:00
```

#### update the map
We've added a testing server locally.

To add a new country to the map, run
```
PYTHONPATH=. python3 mockserver/update_state.py <zone_name>
```

from the root directory, replacing `<zone_name>` by the zone identifier of the parser you want
to test. This will fetch production and exchanges and assign it a random carbon intensity value.
It should appear on the map as you refresh your local browser.

### Troubleshooting

- `ERROR: for X  Cannot create container for service X: Invalid bind mount spec "<path>": Invalid volume specification: '<volume spec>'`. If you get this error after running `docker-compose up` on Windows, you should tell `docker-compose` to properly understand Windows paths by setting the environment variable `COMPOSE_CONVERT_WINDOWS_PATHS` to `0` by running `setx COMPOSE_CONVERT_WINDOWS_PATHS 0`. You will also need a recent version of `docker-compose`. We have successfully seen this fix work with [v1.13.0-rc4](https://github.com/docker/toolbox/releases/tag/v1.13.0-rc4). More info here: https://github.com/docker/compose/issues/4274.

- No website found at `http://localhost:8000`: This can happen if you're running Docker in a virtual machine. Find out docker's IP using `docker-machine ip default`, and replace `localhost` by your Docker IP when connecting.
