"""
use Mako to apply patch to all scripts in a directory.
Patch in-place - write out the same filename as we started with.
"""


from mako.template import Template as MakoTemplate
import os
import shutil


def consolidate_params(parameter_list):
        """
        receive a list of dicts [{"name":"xxx","value":"yyy"},{ ...}]
        output one dict {"xxx":"yyy", ... }
        """
        output_dict = {}
        for param in parameter_list:
            output_dict[param["name"]] = param["value"]
            pass
        return output_dict

def patch_all_scripts(scripts, parameters, job_dir):
        """
        Method to apply a patch based on a supplied template file.
        Loop through all files in a given directory.
        Create (if not already there) a subdirectory of the supplied
        dir called "patched", where the patched scripts will go.
        """
        # these directories have already been made by preprocessor
        raw_dir = os.path.join(job_dir, 'raw')
        patched_basedir = os.path.join(job_dir, 'patched')

        ### need parameters in the form of one dictionary {"param" : "value", ... }
        param_dict = consolidate_params(parameters)

        ### loop through all files in the input directory
        for script in scripts:

            raw_path = os.path.join(raw_dir, script["source"])

            patched_path = os.path.join(patched_basedir, script["destination"])
            # "destination" may contain subdirectories - need to create dir structure
            # if it's not already there..
            patched_dir = os.path.dirname(patched_path)
            os.makedirs(patched_dir,exist_ok=True)

            # patch or copy
            if script["patch"]:
                patch_one_script(raw_path, patched_path, param_dict)
            else:
                shutil.copy(raw_path, patched_path)
        return True, 'All scripts patched.'


def patch_one_script(raw_path, patched_path, parameters):
        """
        Apply mako dict to one script.
        """
        template = MakoTemplate(filename=raw_path,
                                input_encoding='utf-8')
        try:
            with open(patched_path, "w") as f:
                f.write(template.render(parameters=parameters))
        except(KeyError):
        # nothing to patch, copy the file anyway.
            shutil.copy(raw_path, patched_path)
        return True
