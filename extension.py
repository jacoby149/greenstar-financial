import pandas as pd
from zipline.data.bundles import register
from zipline.data.bundles.csvdir import csvdir_equities    

print("Registering",flush=True)
start_session = pd.Timestamp('2005-1-3', tz='utc')
end_session = pd.Timestamp('2014-12-31', tz='utc')
register(
    'provins_bundle',
    csvdir_equities(
        ['daily'],
        '/app/csvs',
    ),
    calendar_name='NYSE', # US equities
    start_session=start_session,
    end_session=end_session
)