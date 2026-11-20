# NYC 311 Dataset Schema

Rows: 10000, Columns: 44

| Column | Type | Missing | Missing % | Unique |
|---|---|---|---|---|
| unique_key | int64 | 0 | 0.0 | 10000 |
| created_date | str | 0 | 0.0 | 8145 |
| closed_date | str | 5320 | 53.2 | 3034 |
| agency | str | 0 | 0.0 | 14 |
| agency_name | str | 0 | 0.0 | 14 |
| complaint_type | str | 0 | 0.0 | 133 |
| descriptor | str | 175 | 1.75 | 433 |
| descriptor_2 | str | 5803 | 58.03 | 294 |
| location_type | str | 807 | 8.07 | 69 |
| incident_zip | float64 | 87 | 0.87 | 191 |
| incident_address | str | 264 | 2.64 | 6573 |
| street_name | str | 265 | 2.65 | 2498 |
| cross_street_1 | str | 3562 | 35.62 | 2026 |
| cross_street_2 | str | 3564 | 35.64 | 2127 |
| intersection_street_1 | str | 3512 | 35.12 | 1977 |
| intersection_street_2 | str | 3512 | 35.12 | 2090 |
| address_type | str | 59 | 0.59 | 5 |
| city | str | 574 | 5.74 | 47 |
| landmark | str | 4194 | 41.94 | 1895 |
| facility_type | str | 9991 | 99.91 | 1 |
| status | str | 0 | 0.0 | 4 |
| due_date | str | 9968 | 99.68 | 32 |
| resolution_description | str | 2348 | 23.48 | 130 |
| resolution_action_updated_date | str | 2262 | 22.62 | 3124 |
| community_board | str | 0 | 0.0 | 74 |
| council_district | float64 | 209 | 2.09 | 51 |
| police_precinct | str | 0 | 0.0 | 78 |
| bbl | float64 | 1042 | 10.42 | 5800 |
| borough | str | 0 | 0.0 | 6 |
| x_coordinate_state_plane | float64 | 160 | 1.6 | 6386 |
| y_coordinate_state_plane | float64 | 160 | 1.6 | 6517 |
| open_data_channel_type | str | 0 | 0.0 | 4 |
| park_facility_name | str | 4 | 0.04 | 1 |
| park_borough | str | 0 | 0.0 | 6 |
| vehicle_type | str | 9517 | 95.17 | 6 |
| taxi_company_borough | str | 9984 | 99.84 | 5 |
| taxi_pick_up_location | str | 9914 | 99.14 | 76 |
| bridge_highway_name | str | 9953 | 99.53 | 26 |
| bridge_highway_direction | str | 9973 | 99.73 | 20 |
| road_ramp | str | 9976 | 99.76 | 6 |
| bridge_highway_segment | str | 9953 | 99.53 | 25 |
| latitude | float64 | 160 | 1.6 | 6714 |
| longitude | float64 | 160 | 1.6 | 6714 |
| location | str | 160 | 1.6 | 6714 |
