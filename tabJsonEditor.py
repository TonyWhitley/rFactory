import sys

sys.path.append('../ScriptedJsonEditor/ScriptedJsonEditor')
from GUI import Tab as _Tab, JobFrames

class Tab(_Tab):
  def __init__(self, parentFrame):
    x = _Tab(parentFrame, cwd='../ScriptedJsonEditor/ScriptedJsonEditor')

    tkLabelframe_jobSettings = x.tkLabelframe_jobSettings

    o_tab = JobFrames(tkLabelframe_jobSettings)

    o_tab.set_checkbutton('G25_jobs', 'Monitor', 1)
    assert o_tab.get_checkbutton('G25_jobs', 'Monitor') == 1
