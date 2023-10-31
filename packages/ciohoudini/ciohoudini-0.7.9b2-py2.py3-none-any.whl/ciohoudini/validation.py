import os
import sys
from ciocore.validator import Validator
import hou

class ValidateUploadDaemon(Validator):
    def run(self, _):
        node = self._submitter
        use_daemon = node.parm("use_daemon").eval()
        if not use_daemon:
            return

        msg = "This submission expects an uploader daemon to be running.\n"
        msg += 'After you press submit you can open a shell and type:\nconductor uploader'

        location = node.parm("location_tag").eval().strip()
        if location:
            msg = "This submission expects an uploader daemon to be running and set to a specific location tag."
            msg += 'After you press submit you can open a shell and type:\nnconductor uploader --location "{}"\n'.format(
                location
            )
        self.add_notice(msg)

        self.add_warning(
            "Since you are using an uploader daemon, you'll want to make sure that all your assets are "+
            "accessible by the machine on which the daemon is running.\nYou can check the list of upload assets in the Preview tab.\n"+
            "Just hit the Do Asset Scan button and scroll down to the bottom."
            )


"""
class ValidateTaskCount(Validator):
    def run(self, _):
        pass
        #Todo: do we need this?
        
        node = self._submitter
        tasks = node.parm("frame_task_county").eval()
        if tasks > 2000:
            self.add_error(
                "This submission contains over 1000 tasks ({}). You'll need to either increase chunk_size or send several job?".format(
                    tasks
                )
            )
 """

 
class ValidateScoutFrames(Validator):
    def run(self, _):
        """
        Add a validation warning for a potentially costly scout frame configuration.
        """
        node = self._submitter
        use_scout_frames = node.parm("use_scout_frames").eval()


        scout_count = node.parm("scout_frame_task_countx").eval()
        frame_count = node.parm("frame_task_countx").eval()
        chunk_size = node.parm("chunk_size").eval()

        """
        if frame_count < 5:
            return

        if scout_count < 5 and scout_count > 0:
            return

        if scout_count == 0 or scout_count == frame_count:
            msg = "All tasks will start rendering."
            msg += " To avoid unexpected costs, we strongly advise you to configure scout frames so that most tasks are initially put on hold. This allows you to check a subset of frames and estimate costs before you commit a whole sequence."
            self.add_warning(msg)
        """

        if chunk_size > 1 and use_scout_frames:
            msg = "You have chunking set higher than 1."
            msg += " This can cause more scout frames to be rendered than you might expect."
            self.add_warning(msg)


class ValidateGPURendering(Validator):
    def run(self, _):
        """
        Add a validation warning for CPU rendering when using the Redshift plugin.
        """
        node = self._submitter
        instance_type_family = node.parm("instance_type_family").eval().lower()
        driver_software = node.parm("driver_version").eval().lower()

        if "redshift" in driver_software and instance_type_family == "cpu":
            msg = "CPU rendering is selected."
            msg += " We strongly recommend selecting GPU rendering when using the Redshift plugin for Houdini.."
            self.add_warning(msg)



class ValidatePaths(Validator):
    def run(self, _):
        """
        Add a validation warning for using the $HOME path in "loadlayer" USD node.
        """
        stage_node_list = hou.node('/stage').allSubChildren()
        disallowed_list = ["$HOME"]
        for stage_node in stage_node_list:
            if stage_node:
                if stage_node.type().name() == 'loadlayer':
                    filepath_param = stage_node.parm("filepath")
                    if filepath_param:
                        filepath_value = filepath_param.rawValue()
                        for item_sr in disallowed_list:
                            if item_sr in filepath_value:
                                msg = (
                                    "We strongly recommend using an explicit path over using '$HOME' in the filepath of any loadlayer node within the stage as '$HOME' might not be correctly evaluated on the renderfarm."
                                )
                                self.add_warning(msg)

# Implement more validators here
####################################
####################################


def run(*nodes):
    errors, warnings, notices = [], [], []
    for node  in nodes:
        er, wn, nt = _run_validators(node)
        
        errors.extend(er)
        warnings.extend(wn)
        notices.extend(nt)

    return errors, warnings, notices

def _run_validators(node):

    takename =  node.name()
    validators = [plugin(node) for plugin in Validator.plugins()]
    for validator in validators:
        validator.run(takename)

    errors = list(set.union(*[validator.errors for validator in validators]))
    warnings = list(set.union(*[validator.warnings for validator in validators]))
    notices = list(set.union(*[validator.notices for validator in validators]))
    return errors, warnings, notices


