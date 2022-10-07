import cdsapi

c = cdsapi.Client()

c.retrieve(
    'reanalysis-era5-pressure-levels-monthly-means',
    {
        'product_type': 'monthly_averaged_reanalysis_by_hour_of_day',
        'variable': [
            'specific_humidity', 'u_component_of_wind',
            'v_component_of_wind', 'vertical_velocity',
        ],
        'pressure_level': [
            '200', '225', '250',
            '300', '350', '400',
            '450', '500', '550',
            '600', '650', '700',
            '750', '775', '800',
            '825', '850', '875',
            '900', '925', '950',
            '975', '1000',
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
        'month': '07',
        'time': [
            '00:00', '01:00', '02:00',
            '03:00', '04:00', '05:00',
            '06:00', '07:00', '08:00',
            '09:00', '10:00', '11:00',
            '12:00', '13:00', '14:00',
            '15:00', '16:00', '17:00',
            '18:00', '19:00', '20:00',
            '21:00', '22:00', '23:00',
        ],
        'area': [
            15, -85, -25,
            -45,
        ],
        'format': 'netcdf',
    },
    'local_circulation_july.nc')
