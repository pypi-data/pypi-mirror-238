from __future__ import unicode_literals


"""
Handle the UI for CustomFrames:

when the useCustomFrames checkbox is unchecked,
the field is hidden. 
"""

import pymel.core as pm
from ciomaya.lib import const as k
from ciomaya.lib.ae import AEcommon
import math

MAX_TASKS = 1000


def create_ui(node_attr):
    """Build static UI."""

    with AEcommon.ae_template():
        pm.intFieldGrp("chunkSizeField", label="Chunk Size", value1=1)
        pm.checkBoxGrp("frameSpecCheckbox", label="Use Custom Range")

        pm.frameLayout("frameSpecFrame", visible=False, lv=False, cl=False, cll=False)

        pm.textFieldGrp("frameSpecField", label="Custom Range")

        pm.setParent("..")  # out of frameLayout
        populate_ui(node_attr)


def populate_ui(node_attr):
    """Reconfigure action buttons when node changes."""

    attr = pm.Attribute(node_attr)

    widgets = _get_widgets()

    chunk_size_attr = attr.node().attr("chunkSize")
    pm.intFieldGrp(
        widgets["chunkSizeField"],
        edit=True,
        value1=chunk_size_attr.get(),
        changeCommand=pm.Callback(_on_chunk_size_changed, chunk_size_attr, **widgets),
    )

    bool_attr = attr.node().attr("useCustomRange")
    bool_val = bool_attr.get()
    val = attr.get()

    pm.checkBoxGrp(
        widgets["checkbox"],
        edit=True,
        value1=bool_val,
        changeCommand=pm.Callback(_on_bool_changed, bool_attr, **widgets),
    )

    pm.textFieldGrp(
        widgets["field"],
        edit=True,
        text=val,
        changeCommand=pm.Callback(_on_text_changed, attr, **widgets),
    )

    _on_bool_changed(bool_attr, **widgets)
    _setup_script_jobs(attr.node(), **widgets)


def _get_widgets(parent=None):
    if not parent:
        parent = pm.setParent(q=True)
    return {
        "chunkSizeField": AEcommon.find_ui("chunkSizeField", parent),
        "checkbox": AEcommon.find_ui("frameSpecCheckbox", parent),
        "frame": AEcommon.find_ui("frameSpecFrame", parent),
        "field": AEcommon.find_ui("frameSpecField", parent),
    }


def _setup_script_jobs(node, **widgets):
    """
    Update the chunk size based on changes to startFrame, endFrame, byFrame, animation)
    """
    pm.scriptJob(
        attributeChange=(
            node.attr("frameCount"),
            pm.Callback(_reconcile_chunk_size, node, **widgets),
        ),
        parent=widgets["chunkSizeField"],
        replacePrevious=True,
    )


def _on_bool_changed(attr, **widgets):
    checkbox = widgets["checkbox"]
    frame = widgets["frame"]
    val = pm.checkBoxGrp(checkbox, q=True, value1=True)
    attr.set(val)
    pm.frameLayout(frame, edit=True, enable=True, visible=val)
    AEcommon.print_setAttr_cmd(attr)


def _on_text_changed(attr, **widgets):
    attr.set(pm.textFieldGrp(widgets["field"], q=True, text=True))
    AEcommon.print_setAttr_cmd(attr)


def _on_chunk_size_changed(attr, **widgets):
    try:
        attr.set(pm.intFieldGrp(widgets["chunkSizeField"], q=True, value1=True))
        node = attr.node()
        _reconcile_chunk_size(node, **widgets)
        AEcommon.print_setAttr_cmd(attr)
    except RuntimeError:
        value = attr.get()
        pm.intFieldGrp(widgets["chunkSizeField"], edit=True, value1=value)


def _reconcile_chunk_size(node, **widgets):
    """
    Count the tasks, and if there are too many, increase the chunk size.
    """

    chunk_size = node.attr("chunkSize").get()
    current_frames = node.attr("frameCount").get()
    current_tasks = node.attr("taskCount").get()
    if current_tasks > MAX_TASKS:
        chunk_size = math.ceil(current_frames / MAX_TASKS)
        try:
            node.attr("chunkSize").set(chunk_size)
            pm.intFieldGrp(widgets["chunkSizeField"], edit=True, value1=chunk_size)
            pm.displayWarning(
                "{}: Chunk size was adjusted to {} to keep the number of tasks below {}.".format(
                    node.name(),
                    chunk_size,
                    MAX_TASKS
                )
            )
        except RuntimeError:
            pass
