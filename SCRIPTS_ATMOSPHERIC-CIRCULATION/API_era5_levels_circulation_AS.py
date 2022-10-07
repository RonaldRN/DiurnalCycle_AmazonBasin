import cdsapi

c = cdsapi.Client()

c.retrieve(
    'reanalysis-era5-pressure-levels-monthly-means',
    {
        'format': 'netcdf',
        'product_type': 'monthly_averaged_reanalysis',
        'time': '00:00',
        'variable': [
            'u_component_of_wind', 'v_component_of_wind',
        ],
        'pressure_level': [
            '200', '250', '300',
            '500', '850',
        ],
        'year': [
            '2001', '2002', '2003',
            '2004', '2005', '2006',
            '2007', '2008', '2009',
            '2010', '2011', '2012',
            '2013', '2014', '2015',
            '2016', '2017', '2018',
            '2019', '2020',
        ],
        'month': [
            '01', '02', '03',
            '04', '05', '06',
            '07', '08', '09',
            '10', '11', '12',
        ],
        'area': [
            15, -85, -60,
            -30,
        ],
    },
    'circulation_mean_season.nc')
