"""Manual transcription from inspected table images; no OCR column inference."""
from pathlib import Path
import json
OUT=Path(__file__).parent
sources={
 'A35L':{'file':'sources/economic_synthesis_2026-09-23/1935_nm_county_table2.pdf','pdf_page':1,'printed_page':873,'table':'II','column':'Guadalupe, lower panel','rows':'cattle 19-22; sheep 34-37'},
 'A35F':{'file':'sources/economic_synthesis_2026-09-23/1935_nm_county_table1.pdf','pdf_pages':[1,2],'printed_pages':[870,871],'table':'I','column':'Guadalupe','rows':'farms 1-2; mean acres 17-18; land 19-20'},
 'A35W':{'file':'sources/economic_synthesis_2026-09-23/1935_nm_county_table4.pdf','pdf_pages':[1,2],'printed_pages':[864,865],'table':'IV','column':'Guadalupe','rows':'farm population 40/45; labor 62/64; off-farm work 65-66'},
 'A45L':{'file':'sources/03_census/agriculture_rebound_2026-09-19/1945_nm_agriculture_full.pdf','pdf_page':71,'printed_page':54,'table':'III','column':'Guadalupe','rows':'cattle 8-9; sheep 23-24; wool 33; sold alive cattle 35/sheep 39'},
 'A45F':{'file':'sources/03_census/agriculture_rebound_2026-09-19/1945_nm_agriculture_full.pdf','pdf_page':37,'printed_page':20,'table':'I','column':'Guadalupe','rows':'farms 1; land 4; mean acres 7','verification':'Previously verified in rebound_1940_1950_2026-09-19/agriculture_observations.json'},
 'A50L':{'file':'sources/03_census/agriculture_rebound_2026-09-19/1950_nm_agriculture_counties.pdf','pdf_page':15,'printed_page':52,'table':'4 part 1','column':'Guadalupe','rows':'cattle 14/16; sheep 65/67; wool 87-88; enumeration 90'},
 'A50F':{'file':'sources/03_census/agriculture_rebound_2026-09-19/1950_nm_agriculture_counties.pdf','pdf_pages':[3,4],'printed_pages':[40,41],'table':'1','column':'Guadalupe','rows':'farms 1; land 10; mean acres 12','verification':'Previously verified in rebound_1940_1950_2026-09-19/agriculture_observations.json'},
 'A59L':{'file':'sources/economic_synthesis_2026-09-23/1959_nm_county_table8.pdf','pdf_pages':[1,2],'printed_pages':[139,140],'table':'8','column':'Guadalupe','rows':'cattle 1-4; sheep 62-65'},
 'A59F':{'file':'sources/economic_synthesis_2026-09-23/1959_nm_county_table1.pdf','pdf_pages':[1,2],'printed_pages':[116,117],'table':'1','column':'Guadalupe','rows':'farms 1-2; definition change 3; land 6-7; mean 8-9; pasture 40-41/56-57/64-65'},
 'A59W':{'file':'sources/economic_synthesis_2026-09-23/1959_nm_county_table6.pdf','pdf_pages':[1,2],'printed_pages':[133,134],'table':'6','column':'Guadalupe','rows':'sample farms 1-2; trucks 19-22; tractors 23-26; family labor 69-70; hired 79-80; regular hired 83-84; enumeration 66'}
}
years=[1930,1935,1940,1945,1950,1954,1959]
columns=['year','cattle_head','cattle_reporting_farms','sheep_lambs_head','sheep_reporting_farms','all_farms','land_in_farms_acres','mean_farm_acres','livestock_source','land_source']
values=[
 [1930,15509,383,99296,146,596,641088,1075.7,'A35L','A35F'],
 [1935,12027,574,75369,132,851,1150413,1351.8,'A35L','A35F'],
 [1940,19227,370,67765,91,476,963025,2023.2,'A45L','A45F'],
 [1945,27047,481,68772,115,640,1517361,2370.9,'A45L','A45F'],
 [1950,41276,325,56412,62,381,1827287,4796.0,'A50L','A50F'],
 [1954,38598,298,62413,70,333,1776714,5335.5,'A59L','A59F'],
 [1959,31020,258,44426,70,297,1588274,5347.7,'A59L','A59F']
]
rows=[dict(zip(columns,v)) for v in values]
for r in rows:
 r['cattle_per_reporting_farm']=round(r['cattle_head']/r['cattle_reporting_farms'],2)
 r['sheep_per_reporting_farm']=round(r['sheep_lambs_head']/r['sheep_reporting_farms'],2)
data={'geography':'Guadalupe County, New Mexico; NOT Cuervo or its trade catchment','method':'Manual image transcription, aligned with column headers and row labels. Earlier farm/land figures reuse a separately verified project transcription.','sources':sources,'inventory_reference_dates':{'1930':'April 1; cattle exclude animals under 3 months','1935':'January 1','1940':'April 1','1945':'January 1','1950':'Enumeration in April; reported county mean interval April 15-28','1954':'Fall enumeration; not the September labor reference week','1959':'Fall enumeration; county average interval November 15-21'},'series':rows,
 'land_use':[{'year':1954,'other_pasture_acres':1740663,'woodland_pastured_acres':15319,'cropland_only_pasture_acres':2852,'source':'A59F'},{'year':1959,'other_pasture_acres':1562499,'woodland_pastured_acres':12409,'cropland_only_pasture_acres':1337,'source':'A59F'}],
 'labor_and_equipment':[{'year':1935,'family_workers':1434,'hired_workers':261,'reference_period':'First week of January 1935','source':'A35W','sample_based':False},{'year':1954,'family_workers':593,'hired_workers':292,'regular_hired_workers':91,'estimated_farms':328,'farms_reporting_motortrucks':285,'motortrucks':394,'farms_reporting_tractors':103,'tractors':121,'reference_period':'Labor: September 26-October 2, 1954','source':'A59W','sample_based':True},{'year':1959,'family_workers':413,'hired_workers':121,'regular_hired_workers':66,'estimated_farms':299,'farms_reporting_motortrucks':250,'motortrucks':349,'farms_reporting_tractors':97,'tractors':116,'reference_period':'Labor: week preceding enumeration; county average enumeration November 15-21','source':'A59W','sample_based':True}],
 'additional_observations':[{'metric':'1959 decrease in farm count attributed by census to definition change','value':10,'source':'A59F'},{'metric':'farm population April 1 1930','value':2562,'source':'A35W'},{'metric':'farm population January 1 1935','value':3888,'source':'A35W'},{'metric':'farm operators reporting off-farm work for pay/income in 1934','value':390,'percent':45.8,'source':'A35W'},{'metric':'wool shorn 1939','value':560362,'unit':'pounds','source':'A45L'},{'metric':'wool shorn 1944','value':642919,'unit':'pounds','source':'A45L','note':'Source image reads 642,919; supersedes an OCR-like misreading of 612,919.'},{'metric':'wool shorn 1949','value':544477,'unit':'pounds','source':'A50L'}],
 'limits':['Inventory dates and cattle age coverage vary; do not treat this as a harmonized annual series.','Farm definitions, coverage and location rules change. A farm can be a ranch; a reporting farm is neither a household nor a full-time job.','Land assigned to farm headquarters can include acreage in adjoining counties. Land in farms is not identical to grazing land or all land physically inside the county.','1954 and 1959 labor and equipment are sample estimates. Labor measures different seasonal weeks, not annual employment, unique people, or full-time equivalents. The 1935 measure has a further definition/reference-period break.','Heads of sheep and cattle are not equivalent units of output, labor, income, or grazing pressure. No animal-unit conversion is made.','Fewer farms with larger mean size is consistent with concentration but cannot identify parcel mergers, individual ranch survival, or mechanization causally.','No direct Cuervo-vs-Santa Rosa spending, freight-origin, land-use, or farm-labor allocation is available here.']}
(OUT/'agriculture_transcription.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
print('Saved',len(rows),'census snapshots and source metadata.')
