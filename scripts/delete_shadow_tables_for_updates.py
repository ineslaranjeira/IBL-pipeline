import datajoint as dj
from ibl_pipeline.ingest import alyxraw, data
from ibl_pipeline.ingest import action, acquisition


dj.config['safemode'] = False

# delete alyxraw except for datasets and file records
#(alyxraw.AlyxRaw & 'model not in ("data.dataset", "data.filerecord")').delete()

# delete alyxraw for data.filerecord if exists = 0
print('Deleting alyxraw entries corresponding to file records...')
file_record_fields = alyxraw.AlyxRaw.Field & \
    'fname = "exists"' & 'fvalue = "False"'

for key in file_record_fields:
    (alyxraw.AlyxRaw.Field & key).delete_quick()

# delete water tables and related alyxraw entries
print('Deleting alyxraw entries of shadow weighing and water tables...')
(alyxraw.AlyxRaw & 'model in ("actions.weighing", "actions.waterrestriction", \
     "actions.wateradministration")').delete()

# delete some shadow membership tables
print('Deleting shadow membership tables...')
action.WaterRestrictionProcedure.delete()
action.WaterRestrictionUser.delete()
acquisition.WaterAdministrationSession.delete()