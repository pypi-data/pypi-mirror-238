import re

from ciohoudini import frames, context

def get_task_template(node, **kwargs):
    """Get the task template from the node."""
    first = kwargs.get("first", 1)
    last = kwargs.get("last", 1)
    step = kwargs.get("step", 1)
    rop_path = kwargs.get("rop_path", None)
    render_script = node.parm("render_script").eval()
    # Use the rop path instead of the driver path.
    # driver_path = node.parm("driver_path").eval()
    render_scene = node.parm("render_scene").eval()
    host_version = node.parm("host_version").eval()

    data = {
        "script": re.sub("^[a-zA-Z]:", "", render_script).replace("\\", "/"),
        "first": first,
        "last": last,
        "step": step,
        # "driver": driver_path,
        "driver": rop_path, # Use the rop path instead of the driver path.
        "hipfile": render_scene,
        "hserver": ""
    }

    try:
        host_version = int(host_version.split()[1].split(".")[0])
    except:
        host_version = 19

    if host_version < 19:
        data["hserver"] = "/opt/sidefx/houdini/19/houdini-19.0.561/bin/hserver --logfile /tmp/hserver.log -C -D; "

    return "{hserver}hython \"{script}\" -f {first} {last} {step} -d {driver} \"{hipfile}\"".format(**data)

def resolve_payload(node, **kwargs):
    """
    Resolve the task_data field for the payload.

    If we are in sim mode, we emit one task.
    """
    task_limit = kwargs.get("task_limit", -1)
    frame_range = kwargs.get("frame_range", None)
    if node.parm("is_sim").eval():
        cmd = node.parm("task_template").eval()
        tasks = [{"command": cmd, "frames": "0"}] 
        return {"tasks_data": tasks}
    #print("resolve_payload: frame_range: ", frame_range)
    tasks = []
    sequence = frames.main_frame_sequence(node, frame_range=frame_range)
    #print("resolve_payload: sequence: ", sequence)
    chunks = sequence.chunks()
    #print("resolve_payload: chunks: ", chunks)
    # Get the scout sequence, if any.
    for i, chunk in enumerate(chunks):
        if task_limit > -1 and i >= task_limit:
            break
        # Get the frame range for this chunk.
        #
        kwargs["first"] = chunk.start
        kwargs["last"] = chunk.end
        kwargs["step"] = chunk.step
        # Get the task template.
        cmd = get_task_template(node, **kwargs)
        # Set the context for this chunk.
        context.set_for_task(first=chunk.start, last=chunk.end, step=chunk.step)
        # cmd = node.parm("task_template").eval()

        tasks.append({"command": cmd, "frames": str(chunk)})


    return {"tasks_data": tasks}
