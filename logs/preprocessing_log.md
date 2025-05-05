### Extreme Weather Events

- Source: EM-DAT or similar
- Original format & issues
- Cleaning steps taken (duplicates, standardization)
- Imputation method (median)
- Normalization of cost data
- Date handling with fallbacks
- Geospatial structure added
- Output format/schema description

### 🧊 Glacial Lake Evolution & Melt Data (2001)
**Source** ICIMOD
- Removed invalid and empty geometries
- Reprojected shapefile to WGS84 coordinate system (EPSG:4326)
- Normalized and standardized column names (e.g., `Gl_Code`, `Gl_Area`, `Elevation`)
- Handled missing values:
  - Filled `gl_area` and `elevation` using column-wise mean imputation
  - Filled missing `gl_name` with placeholder `'Unknown'`
- Added a `year` column to tag temporal metadata
- Exported cleaned dataset to GeoJSON and CSV formats



### 🧊 Glacial Lake Evolution & Melt Data (2011)

- Removed invalid and empty geometries
- Reprojected to WGS84 (EPSG:4326) for consistency
- Normalized schema to match 2001 dataset
- Handled missing values:
  - Imputed `gl_area` and `elevation` with column means
  - Replaced null `gl_name` with `'Unknown'`
- Added a `year` column for temporal alignment
- Exported as GeoJSON and CSV for analysis and visualization



### 🧊 Glacial Lake Evolution & Melt Data (2015)

- Removed empty and invalid geometries
- Reprojected to WGS84 (EPSG:4326)
- Normalized column names (`gl_id` to `gl_code`, `area` to `gl_area`)
- Filled missing `gl_area` using mean imputation
- Ensured unit consistency with previous datasets
- Added a `year` column for integration
- Exported cleaned data as GeoJSON and CSV



### Land Use / Land Cover (LULC) - Nepal (2000, 2010, 2022)

- Downloaded raster data from ICIMOD for 3 years
- Removed pixels with nodata and value 0
- Sampled every 20th pixel to reduce memory usage
- Converted pixel coordinates to Latitude and Longitude
- Mapped land cover class codes to readable labels
- Added year and source columns for traceability
- Validated latitude, longitude, and class code ranges
- Combined all years into one georeferenced CSV
- Exported final data as `LULC_Sampled.csv`

### River Discharge Data (GRDC)

- Parsed multiple .txt files for different river stations
- Extracted river metadata: River, Station, Latitude, Longitude, NextStation
- Transformed raw monthly discharge data into annual averages
- Normalized discharge values per station for comparison (zero mean, unit variance)
- Aligned data temporally from 1962 to 1993
- Interpolated missing values using linear interpolation for consistent time series
- Validated all entries to ensure numerical integrity and consistent formats
- Compiled everything into a single unified CSV:
- Column Format:
 - Raw_<year>(m³/s): Actual annual discharge
 - Norm_<year>(m³/s): Normalized discharge per station

### Climate Reanalysis data (ERA5)
 **Source:** ERA5 Reanalysis
 **Downloaded:** 2025-04-20
 **Variables:** t2m, tp, smlt, lblt, src
 **Geographic extent:** Lat 31.0 to 26.0, Lon 80.0 to 89.0
 **Date:** 2025-04-09
 Preprocessing:
  - Converted t2m from Kelvin to Celsius
  - Normalized variables using z-score
  - Dropped missing values
  - Restructured to CSV with geo + time fields

### historic_temp_precipitatio.csv

**Source:** OpenData Nepal  
**File Used:** historic_temp_precipitatio.csv  
**Steps Performed:**
- Standardized column names and stripped whitespaces.
- Missing values imputed using linear interpolation and forward/backward fill.
- Normalized all numerical fields using MinMaxScaler.
- Aligned records temporally by converting to datetime.
- Reshaped to long format for better parameter-wise analysis.
- Ensured geolocation structure (station, district).
- Final output saved as: `cleaned_historic_temp_precipitatio.csv` and `processed_historic_temp_precipitation.csv`.

**Validation Summary:**
- No missing values remain.
- No negative values.
- Dates range from earliest to latest available.

### Flood prone infrastructure and vulnerbility:

- **Source**: ICIMOD (flood-prone infrastructure indicators of Nepal)
- **Original Format**: Shapefile (.shp)
- **Steps Applied**:
  - Standardized column names
  - Mean imputation for missing values
  - StandardScaler normalization
  - Saved as `flood_vulnerability.csv` and `.geojson`

### Agricultural Yield Statistics:

- **Source**: ICIMOD (Vegetable production, area, and yield statistics of Nepal)
- **Original Format**: CSV and Metadata (.csv, .pdf/.txt)
- **Steps Applied**:
  - Standardized column names and district names
  - Handled missing values using mean imputation
  - Normalized production, area, and yield values using `StandardScaler`
  - Implemented temporal alignment for annual data from 2003–2014
  - Merged with geospatial district boundaries using district names
  - Saved as `processed_agriculture_data.csv` (without geometry)
  - Saved as `processed_agriculture_data.geojson` (with geometry for spatial analysis)

### Weather Station Data
**Data Source**: DHM Nepal weather station metadata
- Cleaned column names and corrected District names
- Imputed missing elevation with median value
- Converted Lat/Long to decimal degrees
- Parsed establishment dates
- Converted to georeferenced structure using GeoPandas
- Exported to structured CSV
