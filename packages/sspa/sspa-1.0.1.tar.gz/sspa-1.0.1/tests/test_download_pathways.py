# import sspa
# import pandas as pd
# from pandas.testing import assert_frame_equal

# class TestDownloadPathays():

#     def test_reactome_download():
#         pass
#         # reactome_latest = sspa.process_reactome(organism="Homo sapiens", download_latest=True, filepath='.')
#         # actual = reactome_latest
#         # # print(actual.columns[0:3])
#         # # assert 'Pathway_name' in actual.columns

from sspa.process_pathways import *
import pandas as pd
from pandas.testing import assert_frame_equal

class TestPathways():
    def test_reactome_download():
        pass
