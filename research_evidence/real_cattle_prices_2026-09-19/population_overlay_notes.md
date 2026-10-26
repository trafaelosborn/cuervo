# Cattle prices overlaid with Cuervo population

Created September 19, 2026 from the verified project series.

## Recommended: annual real-price line and population dots

[PNG](../../output/charts/cuervo_cattle_population_real_index_1920_1950.png) · [Editable SVG](../../output/charts/cuervo_cattle_population_real_index_1920_1950.svg)

This version covers **1920–1950**, the first and last census years for which both inflation-adjusted prices and Cuervo precinct population are available in the current data. It uses 31 annual price observations and four population observations: **438, 287, 188, 210**. Both series are divided by their own 1920 value and multiplied by 100. Thus 50 means half the 1920 level, and 200 means twice the 1920 level. Population dots are labeled with the original resident counts.

Dots preserve the distinction between annual prices and decennial population observations. No annual population has been estimated or implied with connecting lines. A shared percentage scale makes proportional changes directly comparable without choosing a separate vertical scale for each series.

## Alternative: actual dollar prices and resident counts

[PNG](../../output/charts/cuervo_cattle_population_real_units_1920_1950.png) · [Editable SVG](../../output/charts/cuervo_cattle_population_real_units_1920_1950.svg)

This uses the same 1920–1950 data. Teal line/left axis: 1950 dollars per 100 lb liveweight. Orange dots/right axis: Cuervo precinct residents. Both axes start at zero. Intersections and vertical distances between two differently scaled series have no numerical meaning; use this version to read actual levels.

## Longest shared record: nominal prices, 1910–1950

[PNG](../../output/charts/cuervo_cattle_population_nominal_index_1910_1950.png) · [Editable SVG](../../output/charts/cuervo_cattle_population_nominal_index_1910_1950.svg)

This adds the 1910 census of **545** people, giving five population points and 41 annual price observations. Both series use 1910=100. Prices are explicitly **nominal**, because the verified BLS CPI-U series begins in 1913. Additional USDA annual prices are $5.70 in 1910, $4.25 in 1911, and $5.60 in 1912, from the visually checked annual column in Bulletin 265, Table 43, printed/PDF page 46. Redistricting limits comparison between the 1910 and 1920 population observations.

## Interpretation and sources

The price upswing is consistent with stronger ranching conditions during Cuervo's modest 1940–1950 rebound. The earlier decline does not follow a simple parallel price trajectory. Price slumps, subsequent recovery, and any delayed population response cannot be dated from four census points alone.

The price series is New Mexico statewide beef-cattle prices excluding calves; population is Cuervo precinct, which includes more than the built-up settlement. Precinct boundaries are not assumed constant. Annual cattle-price averages include months following census enumeration. No correlation statistic or fitted model is presented.

See the [real-price study](../real_cattle_prices_2026-09-19.md) for USDA and BLS sources and calculation methods, and the [population note](../population_series_verified.md) for census source locators. The [chart data](population_overlay_data.json) preserve all plotted values and missing population values. [The script](plot_population_overlay.py) reproduces the PNG and SVG outputs.
