from datetime import datetime
import os, sys
from threading import Thread
from dataclasses import dataclass
from collections import defaultdict
import time
import copy
import AstecManager.omerotools as omerolib
from multiprocessing import cpu_count
from numpy.linalg import norm
import numpy as np
from AstecManager.libs.lineage import AddNodeToXML
from AstecManager.libs.analyze import apply_analysis,plotsignaltonoise,plotsignaltonoise_tofolder,plotmarsinfos
from skimage import exposure
import cv2
from AstecManager.libs.data import imread
from os import listdir
import site
from os.path import isfile, join
import subprocess
from AstecManager.libs.contourlib import compute_contour
import xml.etree.ElementTree as ET
xml_metadata = "metadata.xml"

def compute_user(parameters):
    user = "KB"
    if "user" in parameters:
        user = parameters["user"]
    return user
def brightness(img):
    if len(img.shape) == 3:
        # Colored RGB or BGR (*Do Not* use HSV images with this function)
        # create brightness with euclidean norm
        return np.average(norm(img, axis=2)) / np.sqrt(3)
    else:
        # Grayscale
        return np.average(img)

def save_general_metadata_to_xml(embryo_folder,node_subname,subname_value,node_value,identifier_text='value'):
    xml_file = os.path.join(embryo_folder,xml_metadata)
    dict_val = {}
    dict_val[str(subname_value)] = node_value
    AddNodeToXML(xml_file,dict_val,"metadata",node_subname,identifier_text)



def convertScale(img, alpha):
    """Add bias and gain to an image with saturation arithmetics. Unlike
    cv2.convertScaleAbs, it does not take an absolute value, which would lead to
    nonsensical results (e.g., a pixel at 44 with alpha = 3 and beta = -210
    becomes 78 with OpenCV, when in fact it should become 0).
    """

    new_img = img * alpha
    new_img[new_img < 0] = 0
    new_img[new_img > 255] = 255
    return new_img.astype(np.uint8)


def decrease_brightness(img):

    img[img == img.max()] = 0
    better_contrast = exposure.equalize_adapthist(img, clip_limit=0.03)
    return better_contrast


# Automatic brightness and contrast optimization with optional histogram clipping
def automatic_brightness_and_contrast(image, clip_hist_percent=1):

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Calculate grayscale histogram
    hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
    hist_size = len(hist)

    # Calculate cumulative distribution from the histogram
    accumulator = []
    accumulator.append(float(hist[0]))
    for index in range(1, hist_size):
        accumulator.append(accumulator[index - 1] + float(hist[index]))

    # Locate points to clip
    maximum = accumulator[-1]
    clip_hist_percent *= (maximum / 100.0)
    clip_hist_percent /= 2.0

    # Locate left cut
    minimum_gray = 0
    while accumulator[minimum_gray] < clip_hist_percent:
        minimum_gray += 1

    # Locate right cut
    maximum_gray = hist_size - 1
    while accumulator[maximum_gray] >= (maximum - clip_hist_percent):
        maximum_gray -= 1

    # Calculate alpha and beta values
    alpha = 255 / (maximum_gray - minimum_gray)
    beta = -minimum_gray * alpha

    auto_result = convertScale(image, alpha)
    return auto_result, alpha, beta


def import_credentials(cred_file):
    config = {}
    f = open(cred_file, "r")
    lines = f.readlines()
    f.close()
    for line in lines:
        line_params = line.replace("'", "").replace('"', '').strip().split("=")
        if len(line_params) > 1:
            if line_params[0] == "username":
                config["login"] = line_params[1]
            elif line_params[0] == "password":
                config["password"] = line_params[1]
            elif line_params[0] == "host":
                config["host"] = line_params[1]
            elif line_params[0] == "port":
                config["port"] = int(line_params[1])
            elif line_params[0] == "group":
                config["group"] = line_params[1]
    return config


def compute_astec_command(astec_command):
    final_command_arg0 = ""
    if "fuse" in astec_command.lower():
        final_command_arg0 = "astec_fusion"
    if "mars" in astec_command.lower():
        final_command_arg0 = "astec_mars"
    if "seg" in astec_command.lower() or astec_command.lower() == "astec_astec":
        final_command_arg0 = "astec_astec"
    if "post" in astec_command.lower():
        final_command_arg0 = "astec_postcorrection"
    if "properties" in astec_command.lower():
        final_command_arg0 = "astec_embryoproperties"
    if "intra" in astec_command.lower():
        final_command_arg0 = "astec_intraregistration"
    return final_command_arg0


def compute_source_astec_dir(astec_command, params_dict):
    dir_to_create = ""
    if "mars" in astec_command.lower():
        if "EXP_FUSE" in params_dict:
            dir_to_create = "FUSE/FUSE_" + params_dict["EXP_FUSE"].replace("'", "").replace('"','')
        else:
            dir_to_create = "FUSE/FUSE_RELEASE"
    if "seg" in astec_command.lower() or astec_command.lower() == "astec_astec":
        if "EXP_FUSE" in params_dict:
            dir_to_create = "FUSE/FUSE_" + params_dict["EXP_FUSE"].replace("'", "").replace('"','')
        else:
            dir_to_create = "FUSE/FUSE_RELEASE"
    if "post" in astec_command.lower():
        if "EXP_SEG" in params_dict:
            dir_to_create = "SEG/SEG_" + params_dict["EXP_SEG"].replace("'", "").replace('"','')
        else:
            dir_to_create = "SEG/SEG_RELEASE"
    return dir_to_create


def compute_astec_dir(astec_command, params_dict):
    dir_to_create = []
    if "fuse" in astec_command.lower():
        if "EXP_FUSE" in params_dict:
            splitted_fuse = params_dict["EXP_FUSE"].replace("'", "").replace("[", "").replace("]", "").split(",")
            for fuse in splitted_fuse:
                dir_to_create.append("FUSE/FUSE_" + fuse)
        else:
            dir_to_create.append("FUSE/FUSE_RELEASE")
    if "mars" in astec_command.lower():
        if "EXP_SEG" in params_dict:
            dir_to_create.append("SEG/SEG_" + params_dict["EXP_SEG"].replace("'", "").replace('"',''))
        else:
            dir_to_create.append("SEG/SEG_RELEASE")
    if "seg" in astec_command.lower() or astec_command.lower() == "astec_astec":
        if "EXP_SEG" in params_dict:
            dir_to_create.append("SEG/SEG_" + params_dict["EXP_SEG"].replace("'", "").replace('"',''))
        else:
            dir_to_create.append("SEG/SEG_RELEASE")
    if "post" in astec_command.lower():
        if "EXP_POST" in params_dict:
            dir_to_create.append("POST/POST_" + params_dict["EXP_POST"].replace("'", "").replace('"',''))
        else:
            dir_to_create.append("POST/POST_RELEASE")
    if "properties" in astec_command.lower():
        if "EXP_INTRAREG" in params_dict:
            dir_to_create.append("INTRAREG/INTRAREG_" + params_dict["EXP_INTRAREG"].replace("'", "").replace('"',''))
        else:
            dir_to_create = "INTRAREG/INTRAREG_RELEASE"
    if "intra" in astec_command.lower():
        if "EXP_INTRAREG" in params_dict:
            dir_to_create.append("INTRAREG/INTRAREG_" + params_dict["EXP_INTRAREG"].replace("'", "").replace('"',''))
        else:
            dir_to_create.append("INTRAREG/INTRAREG_RELEASE")
    return dir_to_create


def compute_astec_tag(astec_command):
    tag = ""
    if "fuse" in astec_command.lower():
        tag = "fuse"
    elif "mars" in astec_command.lower() or "seg" in astec_command.lower() or astec_command.lower() == "astec_astec":
        tag = "seg"
    elif "post" in astec_command.lower():
        tag = "post"
    elif "intra" in astec_command.lower():
        tag = "intrareg"
    elif "properties" in astec_command.lower():
        tag = "embryoproperties"
    return tag



def is_file_image(file):
    return file.endswith('.mha') or file.endswith('nii') or file.endswith(".inr")


def is_file_image_or_compressed(file):
    return file.endswith('.mha') or file.endswith('nii') or file.endswith('.mha.gz') or file.endswith(
        'nii.gz') or file.endswith(".inr") or file.endswith(".inr.gz")


@dataclass
class astec_instance:
    astec_command: str
    folder_embryo: str
    embryo_name: str
    mars_path: str = None
    compress_result: bool = True
    params_dict: dict = defaultdict
    begin_time: int = -1
    end_time: int = -1
    omero_result: bool = True
    omero_config_file: str = ""
    tag_list: list = None
    keep_temp: bool = False
    envastec: str = "astec"
    paramsuffix: str = ""
    omero_input: bool = False
    input_project: str = ""
    input_set: str = ""


class download_omero_inputs(Thread):
    def __init__(self, target_folder, project_name, dataset_name):
        Thread.__init__(self)
        self.target_folder = target_folder
        self.project_name = project_name
        self.dataset_name = dataset_name
        self.unzip = dataset_name

    def run(self):
        pyom = omerolib.connect()
        pyom.download_omero_set(self.project_name, self.dataset_name, self.target_folder)


class start_astec_cleaner(Thread):
    def __init__(self, astec_command, params_dict, name_embryo, send_to_omero, begin, end, compress_result=True,
                 omero_config_file="", tag_list=None, keep_temp=False):
        Thread.__init__(self)
        self.cleaner_folder = ""
        self.astec_command = astec_command
        self.name_embryo = name_embryo
        self.params_dict = params_dict
        self.stop_signal = False
        self.omero_result = send_to_omero
        self.compress_result = compress_result
        self.omero_file = []
        self.omero_config_file = omero_config_file
        self.omero_project_name = ""
        self.omero_dataset_name = ""
        self.dataset_id = -1
        self.begin = begin
        self.end = end
        self.project_id = -1
        self.tag_list = tag_list
        self.keep_temp = keep_temp

    def stop_cleaning(self):
        self.stop_signal = True

    def list_images(self, folder):
        images = []
        onlyfiles = [f for f in os.listdir(folder) if
                     os.path.isfile(os.path.join(folder, f))]
        for file in onlyfiles:
            if is_file_image(file):
                images.append(file)
        return images

    def get_images_at_t(self, time, folder):
        images = self.list_images(folder)
        result = []
        for image in images:
            if "_t{:03d}".format(time) in image:
                result.append(image)
        return result

    def image_t_exists(self, time, folder):
        images = self.list_images(folder)
        flag = False
        for image in images:
            if "_t{:03d}".format(time) in image:
                flag = True
        return flag

    def compress_and_delete(self, file):
        subprocess.run(["gzip", "-f", file])
        subprocess.run(["rm", file])

    def clean_at_t(self, time, pyom):
        print("Cleaning embryo : " + str(self.name_embryo) + " at t = " + str(time))
        for clean in self.cleaner_folder:
            images = self.get_images_at_t(time, clean)
            for image in images:
                if image is not None and is_file_image(image):
                    imagepath = os.path.join(clean, image)
                    if self.omero_result:
                        if not image in self.omero_file and not "mars" in image:
                            print("Uploading image : " + str(imagepath))
                            pyom.add_image_to_dataset_java(imagepath, self.dataset_id)
                            self.omero_file.append(image)
                            if self.compress_result:
                                print("Compressing image : " + str(imagepath))
                                self.compress_and_delete(str(imagepath))
                    elif self.compress_result:
                        print("Compressing image : " + str(imagepath))
                        self.compress_and_delete(imagepath)

        for recon in self.reconstructions_folder:
            print("Reconstruction : " + str(recon))
            if os.path.isdir(recon):
                images_reconstruction = self.get_images_at_t(time, recon)
                for image_reconstruction in images_reconstruction:
                    if image_reconstruction is not None:
                        if is_file_image(image_reconstruction) and not ".gz" in images_reconstruction:
                            print("Compressing reconstruction : " + str(os.path.join(recon, image_reconstruction)))
                            self.compress_and_delete(os.path.join(recon, image_reconstruction))
        if self.keep_temp:
            print("temp")
            for clean in self.cleaner_folder:
                temp_folder = clean + "/TEMP_{:03d}/".format(time)
                if os.path.isdir(temp_folder):
                    images = []
                    onlyfiles = [f for f in os.listdir(temp_folder) if
                                 os.path.isfile(os.path.join(temp_folder, f))]
                    print("Compressing TEMP : " + "/TEMP_{:03d}/".format(time))
                    for file2 in onlyfiles:
                        self.compress_and_delete("gzip", "-f", os.path.join(temp_folder, file2))

    def compute_recon_dir(self, params_dict):
        reconstruction_dir = []
        for dir in self.cleaner_folder:
            reconstruction_dir.append(dir + "/RECONSTRUCTION/")
        if "EXP_RECONSTRUCTION" in params_dict:
            reconstruction_dir.append("REC-MEMBRANE/REC_" + params_dict["EXP_RECONSTRUCTION"].replace('"', '').replace("'", ""))
            reconstruction_dir.append("REC-SEED/REC_" + params_dict["EXP_RECONSTRUCTION"].replace('"','').replace("'", ""))
            reconstruction_dir.append("REC-MORPHOSNAKE/REC_" + params_dict["EXP_RECONSTRUCTION"].replace('"','').replace("'", ""))
        else:
            if "EXP_SEG" in params_dict:
                reconstruction_dir.append("REC-MEMBRANE/REC_" + params_dict["EXP_SEG"].replace('"','').replace( "'", ""))
                reconstruction_dir.append("REC-SEED/REC_" + params_dict["EXP_SEG"].replace('"', '').replace("'", ""))
                reconstruction_dir.append("REC-MORPHOSNAKE/REC_" + params_dict["EXP_SEG"].replace('"','').replace("'", ""))
        return reconstruction_dir

    def copy_logs_files(self, source_folder, target_folder):
        range_t = len(source_folder)
        for i in range(0, range_t):
            source = source_folder[i]
            target = target_folder[i]
            if os.path.isdir(source):
                if not os.path.isdir(target):
                    os.makedirs(target)
                onlyfiles = [f for f in os.listdir(source) if
                             os.path.isfile(os.path.join(source, f)) and (".py" in f or ".log" in f)]
                for file in onlyfiles:
                    print("copy " + str(file) + " to " + str(target))
                    subprocess.run(["cp", os.path.join(source, file), target])

    def run(self):
        dirs = compute_astec_dir(self.astec_command, self.params_dict)
        self.cleaner_folder = []
        input_folder = []
        target_logs = []
        source_logs = []
        for dir in dirs:
            self.cleaner_folder.append(dir.replace('"', '').replace("'", ""))
            input_folder = dir.replace('"', '').replace("'", "")
        for clean in self.cleaner_folder:
            target_logs = os.path.join(clean, "LOGS")
        for input in input_folder:
            source_logs = os.path.join(input, "LOGS")
        for clean in self.cleaner_folder:
            while not os.path.isdir(clean):
                time.sleep(5)

        self.reconstructions_folder = self.compute_recon_dir(self.params_dict)

        pyom = None
        tag_step = compute_astec_tag(self.astec_command)
        if self.omero_result:
            # Connect to OMERO
            pyom = omerolib.connect()
            # Determine ASTEC folder depending on the step
            astec_dir = compute_astec_dir(self.astec_command, self.params_dict)
            # OMERO Dataset depending of ASTEC parameters
            self.omero_dataset_name = astec_dir.replace("POST/", "").replace("SEG/", "").replace("FUSE/", "").replace(
                '"', '').replace("'", "")
            # Project = embryo name
            self.omero_project_name = self.name_embryo
            # GET or CREATE project
            if pyom.get_project_by_name(self.omero_project_name) is None:
                pyom.create_project(self.omero_project_name)
            self.o_project = pyom.get_project_by_name(self.omero_project_name)
            self.project_id = self.o_project.getId()
            # GET or CREATE dataset
            if pyom.get_dataset_by_name(self.omero_dataset_name, self.project_id) is None:
                pyom.create_dataset(self.omero_dataset_name, self.project_id)
            self.dataset_id = pyom.get_dataset_by_name(self.omero_dataset_name, self.project_id).getId()
        # Manage time points at runtime
        for current_time in range(self.begin, self.end + 1):
            if current_time < self.end:
                for dir in self.cleaner_folder:
                    while not self.image_t_exists(current_time + 1, dir):
                        time.sleep(10)
                    self.clean_at_t(current_time, pyom)
            else:
                for dir in self.cleaner_folder:
                    while not self.image_t_exists(self.end, dir):
                        time.sleep(10)
                    self.clean_at_t(current_time, pyom)

        # upload xml and attachements at the end
        if self.omero_result:
            onlyfiles = []
            for dir in self.cleaner_folder:
               for f in os.listdir(dir):
                   if os.path.isfile(os.path.join(dir, f)):
                       onlyfiles.append(os.path.join(dir, f))
            for file in onlyfiles:
                if not is_file_image_or_compressed(file):
                    if pyom is not None:
                        print("Upload attachment file")
                        pyom.add_file_to_dataset(self.dataset_id, file)
            if self.tag_list is not None and len(self.tag_list) > 0:
                dataset = pyom.get_dataset_by_id(self.dataset_id, project=self.project_id)
                if dataset is not None:
                    for tag in self.tag_list:
                        pyom.add_tag(dataset, tag)
                    if tag_step != "":
                        pyom.add_tag(dataset, tag_step)
                else:
                    print("could not find dataset : " + str(self.dataset_id))
        self.copy_logs_files(source_logs, target_logs)
        if pyom is not None:
            pyom.o_close()
        # omero the non images files and non gz files


def compute_input_folder(astec_command, params_dict):
    dir_to_create = ""
    if "seg" in astec_command.lower() or astec_command.lower() == "astec_astec":
        if "EXP_FUSE" in params_dict:
            dir_to_create = "FUSE/FUSE_" + params_dict["EXP_FUSE"].replace("'", "").replace('"','')
        else:
            dir_to_create = "FUSE/FUSE_RELEASE"
    elif "post" in astec_command.lower():
        if "EXP_SEG" in params_dict:
            dir_to_create = "SEG/SEG_" + params_dict["EXP_SEG"].replace("'", "").replace('"','')
        else:
            dir_to_create = "SEG/SEG_RELEASE"
    else:
        return None
    return dir_to_create


class start_astec_command(Thread):
    def __init__(self, astec_instance):
        Thread.__init__(self)
        self.astec_command = astec_instance.astec_command
        self.embryo_folder = astec_instance.folder_embryo
        self.name_embryo = astec_instance.embryo_name
        self.begin = astec_instance.begin_time
        self.end = astec_instance.end_time
        self.mars_path = astec_instance.mars_path
        self.params_dict = astec_instance.params_dict
        self.keep_temp = astec_instance.keep_temp
        self.use_omero_input = astec_instance.omero_input
        self.omero_config_file = astec_instance.omero_config_file
        self.omero_project_name = astec_instance.input_project
        self.omero_dataset_name = astec_instance.input_set
        self.astecenv = astec_instance.envastec
        self.paramsuffix = astec_instance.paramsuffix
        self.running_dir = ""
    def copy_logs_files(self, source_folder, target_folder):
        range_t = len(source_folder)
        for i in range(0, range_t):
            source = source_folder[i]
            target = target_folder[i]
            if os.path.isdir(source):
                if not os.path.isdir(target):
                    os.makedirs(target)
                onlyfiles = [f for f in os.listdir(source) if
                             os.path.isfile(os.path.join(source, f)) and (".py" in f or ".log" in f)]
                for file in onlyfiles:
                    print("copy " + str(file) + " to " + str(target))
                    subprocess.run(["cp", os.path.join(source, file), target])

    def run(self):
        print("Managining data for " + self.astec_command + " on embryo " + self.embryo_folder)
        final_command_arg0 = compute_astec_command(self.astec_command)
        dir_to_create = []
        dirs = compute_astec_dir(self.astec_command, self.params_dict)
        for dir in dirs:
            dir_to_create.append(dir)
        self.running_dir = dir_to_create
        if self.use_omero_input:
            folder_target = compute_input_folder(self.astec_command, self.params_dict)
            if folder_target is None:
                print("Unable to comput input files folders , exiting")
                return
            os.makedirs(folder_target)
            pyom = omerolib.connect()
            pyom.download_omero_set(self.omero_project_name, self.omero_project_name, folder_target)
        if final_command_arg0 != "astec_embryoproperties":
            for dir in dir_to_create:
                if dir != "":
                    final_dir = dir.replace('"', '').replace("'", "").replace("[", "").replace("]", "")
                    if not os.path.isdir(final_dir):
                        os.makedirs(final_dir, mode=0o777)
            if self.mars_path is not None and final_command_arg0 == "astec_astec":
                if not os.path.isdir(self.running_dir[0].replace("'", "").replace('"', '')):
                    os.makedirs(self.running_dir[0].replace("'", "").replace('"', ''), mode=0o777)
                print("Copying mars for " + self.astec_command + " on embryo " + self.embryo_folder)
                os.system("cp " + str(self.mars_path).replace("'", "").replace('"', '') + " " + str(
                    self.running_dir[0]).replace("'", "").replace('"', '') + "/")
        print("Generating parameters for " + self.astec_command + " on embryo " + self.embryo_folder)
        parameters_name = self.astec_command + "_" + self.running_dir[0].replace("/", "_").replace("\\",
                                                                                                   "_").replace(
            '"', '') + "_" + self.paramsuffix + ".py"
        parameter_content = ""
        parameter_content += 'PATH_EMBRYO = "."\n'
        parameter_content += 'EN = "' + str(self.name_embryo).replace("'","").replace('"','') + '"\n'
        parameter_content += 'begin = ' + str(self.begin) + '\n'
        if self.end != -1:
            parameter_content += 'end = ' + str(self.end) + '\n'
        for dict_key in self.params_dict:
            if not dict_key == "mars_path":
                parameter_content += str(dict_key) + ' = ' + str(self.params_dict[dict_key]) + '\n'
        print("Writing parameters file for " + self.astec_command)
        f = open(parameters_name, "w+")
        f.write(parameter_content)
        f.close()
        commandrun = ""
        if self.keep_temp:
            commandrun = " conda run -n " + self.astecenv + " " + final_command_arg0 + " -k -p " + parameters_name
        else:
            commandrun = " conda run -n " + self.astecenv + " " + final_command_arg0 + " -p " + parameters_name
        os.system(commandrun)
        print("Command finished for " + self.astec_command)
        source_logs = []
        target_logs = []
        source_logs.append(
            os.path.join(compute_input_folder(self.astec_command,self.params_dict), "LOGS"))
        for inputfold in self.running_dir:
            target_logs.append(os.path.join(inputfold, "LOGS"))
        self.copy_logs_files(source_logs, target_logs)
        os.system("rm " + parameters_name)


class Manager:
    def __init__(self,astec_env="astec"):
        self.running_sessions = []
        self.running_cleaners = []
        self.to_run_list = []
        self.stop_run = False
        self.astec_instance = astec_env

    def add_to_run(self, astec_command, folder_embryo, embryo_name, begin_time, params_dict=None, end_time=-1,
                   mars_path=None, compress_result=True, omero_result=False, omero_config_file="", tag_list=None,
                   keep_temp=False, paramsuffix="", omeroinput=False, inputproject=None,
                   inputset=None):
        ai = astec_instance(astec_command, folder_embryo, embryo_name, mars_path, compress_result,
                            copy.deepcopy(params_dict),
                            begin_time, end_time, omero_result, omero_config_file, tag_list, keep_temp, self.astec_instance,
                            paramsuffix, omeroinput, inputproject, inputset)
        self.to_run_list.append(ai)


    def start_running(self, thread_number=-1):
        cpuCount = cpu_count()
        thread_count = cpuCount * 2 / 6
        if thread_number != -1:
            thread_count = thread_number
        for param in self.to_run_list:
            if len(self.running_sessions) >= thread_count:
                tc = self.running_sessions.pop(0)
                tc.join()
            tc = start_astec_command(param)
            tc.start()
            if param.compress_result or param.omero_result:
                tc2 = start_astec_cleaner(param.astec_command, param.params_dict, param.embryo_name, param.omero_result,
                                          param.begin_time, param.end_time,
                                          param.compress_result, param.omero_config_file, param.tag_list,
                                          param.keep_temp)
                tc2.start()
            self.running_sessions.append(tc)
            if param.compress_result or param.omero_result:
                self.running_cleaners.append(tc2)
        while len(self.running_sessions) > 0:
            tc = self.running_sessions.pop(0)
            if param.compress_result or param.omero_result:
                tc2 = self.running_cleaners.pop(0)
            if tc is not None:
                tc.join()
            if (param.compress_result or param.omero_result) and tc2 is not None:
                tc2.stop_cleaning()
                tc2.join()
        self.running_sessions = []
        self.running_cleaners = []
        self.to_run_list = []

    def compute_graphs_test_segmentation(self, embryo_name, begin, end):
        #atlas_path = self.compute_atlas()
        #ref_lineage = atlas_path[0]
        mincells_test = 64
        maxcells_test = 500

        folder_out = os.path.join("analysis/", "test_segmentation")
        lineages = [
            "POST/POST_test_maximum_gace/" + embryo_name + "_post_lineage.xml",
            "POST/POST_test_maximum_glace/" + embryo_name + "_post_lineage.xml",
            "POST/POST_test_addition_gace/" + embryo_name + "_post_lineage.xml",
            "POST/POST_test_addition_glace/" + embryo_name + "_post_lineage.xml"]
        names = ["SEG_test_maximum_gace", "SEG_test_maximum_glace", "SEG_test_addition_gace", "SEG_test_addition_glace"]

        apply_analysis(lineages, names, folder_out, embryo_name, mincells_test, maxcells_test, begin, end,
                       path=embryo_name + "_output_comparison.png", ref_lineage=None, data_path=folder_out)
        if os.path.isfile("histogram_branch_data.csv"):
            os.system("rm histogram_branch_data.csv")

    def compute_graphs_post(self, embryo_name, begin, end,post_list):
        #atlas_path = self.compute_atlas()
        #ref_lineage = atlas_path[0]
        mincells_test = 64
        maxcells_test = 500
        folder_out = os.path.join("analysis/", "post_segmentation")
        lineages = []
        names = []
        for exp_post in post_list:
            lineages.append( "."+ "/POST/POST_" + str(exp_post) + "/" + embryo_name + "_post_lineage.xml")
            names.append("POST_"+str(exp_post))

        apply_analysis(lineages, names, folder_out, embryo_name, mincells_test, maxcells_test, begin, end,
                       path=embryo_name + "_output_comparison.png", is_post=True, ref_lineage=None,
                       data_path=folder_out)
        if os.path.isfile("histogram_branch_data.csv"):
            os.system("rm histogram_branch_data.csv")


    def compute_folder_graphs_post(self, embryo_folder,embryo_name, begin, end,post_list):
        #atlas_path = self.compute_atlas()
        #ref_lineage = atlas_path[0]
        mincells_test = 64
        maxcells_test = 500
        folder_out = os.path.join(".", os.path.join("analysis/", "post_segmentation"))
        lineages = []
        names = []
        for exp_post in post_list:
            lineages.append( "."+ "/POST/POST_" + str(exp_post) + "/" + embryo_name + "_post_lineage.xml")
            names.append("POST_"+str(exp_post))

        apply_analysis(lineages, names, folder_out, embryo_name, mincells_test, maxcells_test, begin, end,
                       path=embryo_name + "_output_comparison.png", is_post=True, ref_lineage=None,
                       data_path=folder_out)
        if os.path.isfile("histogram_branch_data.csv"):
            os.system("rm histogram_branch_data.csv")
    def compute_images_from_movie(self, image, embryo_name):

        print("-> Reading image")
        image_movie = imread(image)
        shape = image_movie.shape
        z_stack_count = shape[2]
        img_array = []
        for i in range(0, z_stack_count):
            img_array.append(image_movie[:, :, i])
        shape = image_movie[:, :, i].shape
        image_list = []
        print("-> Writing video file")
        for i in range(len(img_array)):
            print("Frame : " + str(i))
            # opencv_image = cv2.cvtColor(decrease_brightness(img_array[i]), cv2.COLOR_GRAY2BGR)
            opencv_image = cv2.cvtColor(img_array[i], cv2.COLOR_GRAY2BGR)
            image_link = join(embryo_name, 'frame' + str(i) + '.jpg')
            image_list.append(image_link)
            cv2.imwrite(image_link, opencv_image)
            height, width = img_array[i].shape
        return image_list, height, width

    def compute_video_from_movie(self, embryo_name, intrareg_folder, fuse_folder):

        print("Creating video")
        path = "."
        path_intrareg = join(join(path, "INTRAREG"), "INTRAREG_" + str(intrareg_folder) + "/MOVIES/")
        path_fuse = join(path_intrareg, join("FUSE", "FUSE_" + str(fuse_folder))).replace('"', '').replace("'", "")
        final_path = join(join(path, "analysis").replace("'", "").replace('"', ''), "fuse")
        if not os.path.exists(final_path):
            os.makedirs(final_path)
        image_files = [f for f in listdir(path_fuse) if isfile(join(path_fuse, f)) and (".nii" in f or ".mha" in f)]
        image_list, height, width = self.compute_images_from_movie(os.path.join(path_fuse, image_files[0]), embryo_name)
        ouputname = join(final_path, 'fusion_movie.avi')
        framerate = int(len(image_list) / 15)
        fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        video = cv2.VideoWriter(ouputname, fourcc, framerate, (width, height))
        if not video.isOpened():
            print('Error cannot create ' + 'fusion_movie.avi')
            quit()

        for image in image_list:
            img = cv2.imread(image)
            video.write(img)
            os.system("rm " + str(image))
        cv2.destroyAllWindows()
        video.release()
        os.system('ffmpeg -i ' + ouputname + '  ' + ouputname.replace('.avi', '.mp4'))
        os.system('rm -f ' + ouputname)

    def plot_signal_to_noise(self, embryo_name, parameters):
        plotsignaltonoise(embryo_name, parameters)

    def plot_signal_to_noise_tofolder(self, folder,embryo_name):
        plotsignaltonoise_tofolder(folder,embryo_name)

    def plot_mars_info(self, embryo_name, exp_seg, begin_time, working_resolution=0.3):
        plotmarsinfos(embryo_name, exp_seg, begin_time, resolution=working_resolution)

    def generate_init_naming_parameters(self, cell_count, xml_folder, xml_file, embryo_name):
        atlas_path = self.compute_atlas()
        now = datetime.now()
        parameters_name = "init_naming" + str(now.timestamp()).replace('.', '') + ".py"
        final_file = os.path.join(xml_folder.replace(str(embryo_name) + "/", ""), xml_file)
        txt = ""
        txt += "inputFile = '" + str(final_file) + "'" + "\n"
        txt += "outputFile = '" + str(final_file) + "'" + "\n"
        txt += "cell_number = " + str(cell_count) + "\n"
        txt += 'atlasFiles = '+atlas_path + "\n"
        txt += "check_volume=False" + "\n"
        f = open(parameters_name, "w+")
        f.write(txt)
        f.close()
        return parameters_name

    def generate_surface(self, exp_fuse, exp_post, begin, end, xmloutput, embryo_name, exp_intrareg):
        fuse_path =  "INTRAREG/INTRAREG_" + str(exp_intrareg) + "/FUSE/FUSE_" + str(exp_fuse)
        fuse_template = os.path.join(fuse_path, embryo_name + "_fuse_t%03d.nii").replace("'", "").replace('"', '')
        post_path = "INTRAREG/INTRAREG_" + str(exp_intrareg) + "/POST/POST_" + str(exp_post)
        post_template = os.path.join(post_path, embryo_name + "_post_t%03d.nii").replace("'", "").replace('"', '')
        os.system("conda run -n astec mc-cellProperties -fusion-format " + str(
                fuse_template) + " -segmentation-format " + str(post_template) + " -first " + str(
                begin) + " -last " + str(end) + " -o " + str(
                xmloutput) + " -feature contact-surface -feature barycenter")


    def compute_atlas(self):
        from importlib_resources import files
        path = []
        path.append(files("AstecManager.atlas").joinpath("pm1.xml"))
        path.append(files("AstecManager.atlas").joinpath("pm3.xml"))
        path.append(files("AstecManager.atlas").joinpath("pm4.xml"))
        path.append(files("AstecManager.atlas").joinpath("pm5.xml"))
        path.append(files("AstecManager.atlas").joinpath("pm7.xml"))
        path.append(files("AstecManager.atlas").joinpath("pm8.xml"))
        path.append(files("AstecManager.atlas").joinpath("pm9.xml"))
        return path

    def generate_prop_naming_parameters(self, xml_folder, xml_file, embryo_name):
        atlas_path = self.compute_atlas()
        atlases_files = []
        now = datetime.now()
        parameters_name = "prop_naming" + str(now.timestamp()).replace('.', '') + ".py"
        txt = ""
        final_file = os.path.join(xml_folder.replace(str(embryo_name) + "/", ""), xml_file)
        txt += "inputFile = '" + str(final_file) + "'" + "\n"
        txt += "outputFile = '" + str(final_file) + "'" + "\n"
        txt += "confidence_atlases_nmin = 2" + "\n"
        txt += "confidence_atlases_percentage = 0" + "\n"
        txt += 'atlasFiles = '+str(atlas_path) + "\n"
        atlases_files.append("pm9.xml")
        f = open(parameters_name, "w+")
        f.write(txt)
        f.close()
        return parameters_name,atlas_path

    def backup_xml(self, xml_file):
        split_name = xml_file[1:len(xml_file)].split(".")
        backup_name = split_name[0] + "_backup." + split_name[1]
        os.system("cp " + str(xml_file) + " ." + str(backup_name))

    def compute_cell_count(self, mars_path):
        count = -1
        image_first = imread(mars_path)
        if mars_path is not None:
            count = len(np.unique(image_first)) - 1
        return count

    def generate_init_naming(self, xml_folder, xml_file, begin_time_name, embryo_name, exp_fuse, exp_post, begin, end,
                             exp_intrareg):

        print(" -> Generate init naming")
        xml_path = os.path.join(xml_folder, xml_file)
        mars_path = os.path.join(xml_folder, begin_time_name)
        source = open(xml_path)
        tree = ET.parse(source)
        tree = tree.getroot()
        lineage_elem = tree.find("cell_contact_surface")
        print("     - backup xml")
        self.backup_xml(xml_path)
        surface_xml = xml_path.replace("lineage", "lineage_surfaces")
        if lineage_elem is None:
            print("     - generate surfaces in side xml")
            self.generate_surface(exp_fuse, exp_post, begin, end, surface_xml, embryo_name, exp_intrareg)
            print("     - merging 2 xml")
            os.system(
                "conda run -n astec astec_embryoproperties -i " + xml_path + " " + surface_xml + " -o " + xml_path)
            print("     - cleaning temp xml")
            os.system("rm " + str(surface_xml))
        print("     - compute cell count from mars")
        cell_count = self.compute_cell_count(mars_path)
        print("     - generate naming parameter file")
        parameter_file = self.generate_init_naming_parameters(cell_count, xml_folder, xml_file, embryo_name)
        print("     - running naming")
        os.system("conda run -n astec-dev astec_atlas_init_naming -v -v -v -p " + str(
            parameter_file))
        os.system("rm " + str(parameter_file))

    def propagate_naming(self, xml_folder, xml_file, embryo_name):
        print(" -> Propagate naming")
        print("     - generate parameters")
        parameter_file,atlases_files = self.generate_prop_naming_parameters(xml_folder, xml_file, embryo_name)
        print("     - propagation of naming")
        os.system("conda run -n astec-dev astec_atlas_naming -v -v -v -p " + str(
            parameter_file))
        print("     - cleaning")
        os.system("rm " + str(parameter_file))
        return atlases_files

    def downscale_folder_parameters(self, parameters):
        user = compute_user(parameters)
        embryo_folder = "."
        voxel_size = parameters["resolution"]
        save_general_metadata_to_xml(embryo_folder, "downscale_date", "FUSE_" + str(parameters["EXP_FUSE"]) + "_down0"+str(voxel_size).split(".")[1],
                                      datetime.now().strftime("%m/%d/%Y %H:%M:%S"), identifier_text="downscale_target")
        save_general_metadata_to_xml(embryo_folder, "downscale_user", "FUSE_" + str(parameters["EXP_FUSE"]) + "_down0"+str(voxel_size).split(".")[1],
                                      user, identifier_text="downscale_target")
        save_general_metadata_to_xml(embryo_folder, "downscale_source", "FUSE_" + str(parameters["EXP_FUSE"]) + "_down0"+str(voxel_size).split(".")[1],
                                      "FUSE_"+str(parameters["EXP_FUSE"]), identifier_text="downscale_target")
        save_general_metadata_to_xml(embryo_folder, "downscale_resolution", "FUSE_" + str(parameters["EXP_FUSE"]) + "_down0"+str(voxel_size).split(".")[1],
                                      str(voxel_size), identifier_text="downscale_target")
    def downscale_folder(self, parameters):
        embryo_name = parameters["embryo_name"].replace('"','').replace("'","")
        omero_config_file = None
        if "omero_config_file" in parameters:
            omero_config_file = parameters["omero_config_file"]
        voxel_size = parameters["resolution"]
        embryo_folder = "."
        input_folder = os.path.join(embryo_folder, "FUSE/FUSE_" + str(parameters["EXP_FUSE"]))
        output_folder = os.path.join(embryo_folder, "FUSE/FUSE_" + str(parameters["EXP_FUSE"]) + "_down0"+str(voxel_size).split(".")[1])
        files = os.listdir(input_folder)
        files.sort()
        if not os.path.isdir(output_folder):
            os.makedirs(output_folder)
        for file in files:
            # make sure file is an image
            if file.endswith(('.mha', '.nii', '.mha.gz', '.nii.gz', '.inr', '.inr.gz')):
                img_path = os.path.join(input_folder, file)
                print("     -> " + str(img_path))
                img_t = os.path.join(output_folder, file)
                os.system("conda run -n astec applyTrsf -iso " + str(voxel_size) + " " + img_path + " " + img_t)

        if omero_config_file is not None:
            self.upload_on_omero(omero_config_file, embryo_name, "FUSE_" + str(parameters["EXP_FUSE"]) + "_down0"+str(voxel_size).split(".")[1],
                                 output_folder)

    def save_upload_parameters(self, omero_project_name, omero_dataset_name, embryo_folder,user=None):
        save_general_metadata_to_xml(embryo_folder, "upload_user",
                                     omero_project_name+"/"+omero_dataset_name,
                                     user, identifier_text="upload_instance")
        save_general_metadata_to_xml(embryo_folder, "upload_date",
                                     omero_dataset_name,
                                     datetime.now().strftime("%m/%d/%Y %H:%M:%S"),
                                     identifier_text="upload_instance")
    def upload_on_omero(self, config_file, omero_project_name, omero_dataset_name, input_folder, include_logs=False,embryo_name=None,user=None):
        config_array = omerolib.parse_parameters_file(config_file)
        om_login = config_array['login']
        om_pw = config_array['password']
        om_host = config_array['host']
        om_port = int(config_array['port'])
        om_group = config_array['group']
        om_secure = config_array['secure']
        embryo_folder = "."

        pyom = omerolib.connect(login=om_login, passwd=om_pw, server=om_host, port=om_port, group=om_group,
                                secure=om_secure)
        pyom.upload_omero_set(omero_project_name.replace("'", "").replace('"', ''),
                              omero_dataset_name.replace("'", "").replace('"', ''),
                              input_folder.replace("'", "").replace('"', ''), include_logs=include_logs)
        self.save_upload_parameters(omero_project_name, omero_dataset_name,embryo_folder,user)


    def download_from_omero(self, parameters):
        config_file = None
        if "omero_config_file" in parameters:
            config_file = parameters["omero_config_file"]
        omero_project_name = parameters["embryo_name"].replace('"','').replace("'","")
        omero_dataset_name = parameters["dataset_name"]
        output_folder = parameters["output_folder"]
        if config_file is None:
            print("OMERO config file is not bound, unable to upload")
            exit()
        if not os.path.isfile(config_file):
            print("Unable to find OMERO config file , unable to upload")
            exit()
        config_array = omerolib.parse_parameters_file(config_file)
        om_login = config_array['login']
        om_pw = config_array['password']
        om_host = config_array['host']
        om_port = int(config_array['port'])
        om_group = ""
        if 'group' in config_array:
            om_group = config_array['group']
        om_secure = config_array['secure']
        if not os.path.isdir(output_folder):
            os.makedirs(output_folder)

        pyom = omerolib.connect(login=om_login, passwd=om_pw, server=om_host, port=om_port, group=om_group,
                                secure=om_secure)
        pyom.download_omero_set(omero_project_name.replace("'", "").replace('"', ''),
                                omero_dataset_name.replace("'", "").replace('"', ''),
                                output_folder.replace("'", "").replace('"', ''))

    def compute_contours(self, parameters):

        omero_config_file = None
        if "omero_config_file" in parameters:
            omero_config_file = parameters["omero_config_file"]
        normalisation = parameters["normalisation"]
        background_folder_name = parameters["EXP_BACKGROUND"]
        voxel_size = parameters["resolution"]
        parameters = self.format_embryo_name(parameters)
        embryo_name = parameters["embryo_name"].replace('"','').replace("'","")
        user = compute_user(parameters)
        embryo_folder = os.path.join("./", embryo_name)
        compute_contour(embryo_folder, background_folder_name, reducvoxelsize=float(voxel_size),
                        target_normalization_max=normalisation, correction_vsize=True,user=user)
        if omero_config_file is not None:
            contour_folder = "CONTOUR/CONTOUR_RELEASE_" + str(voxel_size).split(".")[1]
            self.upload_on_omero(omero_config_file, embryo_name, "CONTOUR_RELEASE_" + str(voxel_size).split(".")[1],
                                 contour_folder)

    def name_embryo_parameters(self,parameters,atlases_files):
        user = compute_user(parameters)
        embryo_folder = os.path.join(".")
        embryo_name = parameters["embryo_name"].replace('"','').replace("'","")
        begin = parameters["begin"]
        lineage_name = embryo_name + "_intrareg_post_lineage.xml"
        save_general_metadata_to_xml(embryo_folder, "naming_date", lineage_name,
                                     datetime.now().strftime("%m/%d/%Y %H:%M:%S"), identifier_text="naming_target")
        save_general_metadata_to_xml(embryo_folder, "naming_atlas", lineage_name,
                                     str(atlases_files), identifier_text="naming_target")
        save_general_metadata_to_xml(embryo_folder, "naming_user", lineage_name,
                                     str(user), identifier_text="naming_target")
        save_general_metadata_to_xml(embryo_folder, "naming_init_time", lineage_name,
                                     str(begin), identifier_text="naming_target")
    def format_embryo_name(self,parameters):
        if "embryo_name" in parameters:
            if not parameters["embryo_name"].startswith("'"):
                parameters["embryo_name"] = "'"+parameters["embryo_name"]
            if not parameters["embryo_name"].endswith("'"):
                parameters["embryo_name"] = parameters["embryo_name"]+"'"
        return parameters
    def name_embryo(self, parameters):
        parameters = self.format_embryo_name(parameters)
        embryo_name = parameters["embryo_name"].replace('"','').replace("'","")
        begin = parameters["begin"]
        end = parameters["end"]
        lineage_path = "INTRAREG/INTRAREG_" + str(parameters["EXP_INTRAREG"])+"/POST/POST_" + parameters["EXP_POST"] + "/"
        lineage_name = embryo_name + "_intrareg_post_lineage.xml"
        mars_filename = embryo_name + "_intrareg_post_t{:03d}.nii".format(begin)
        self.generate_init_naming(lineage_path.replace('"', '').replace("'", ""),
                                  lineage_name.replace('"', '').replace("'", ""),
                                  mars_filename.replace('"', '').replace("'", ""),
                                  embryo_name.replace('"', '').replace("'", ""),
                                  str(parameters["EXP_FUSE"]).replace('"', '').replace("'", ""),
                                  str(parameters["EXP_POST"]).replace('"', '').replace("'", ""), begin, end,
                                  str(parameters["EXP_INTRAREG"]).replace('"', '').replace("'", ""))
        atlases_files = self.propagate_naming(lineage_path.replace('"', '').replace("'", ""),
                              lineage_name.replace('"', '').replace("'", ""),
                              embryo_name.replace('"', '').replace("'", ""))
        self.name_embryo_parameters(parameters,atlases_files)


    def copy_raw_data(self, parameters):

        searcher = compute_user(parameters)

        if not "embryo_name" in parameters:
            print("Embryo name is not provided in parameters ")
            exit()
        if not "input_folder" in parameters:
            print("Distant raw data folder path is not provided in parameters")
            exit()
        input_folder = parameters["input_folder"]
        embryo_dir = "."
        if not os.path.isdir(embryo_dir):
            os.makedirs(embryo_dir)
        raw_data_output = os.path.join(embryo_dir, "RAWDATA")
        if not os.path.isdir(raw_data_output):
            os.makedirs(raw_data_output)
        try:
            subprocess.run(['rsync', '-avzr', str(input_folder), raw_data_output + "/"], check=True)
            save_general_metadata_to_xml(embryo_dir, "raw_copy_date", "", datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            save_general_metadata_to_xml(embryo_dir, "raw_copy_source", "", input_folder)
            save_general_metadata_to_xml(embryo_dir, "raw_copy_user", "", searcher)
        except subprocess.CalledProcessError:
            print('Error during the copy of the data , please verify the parameters and try again')

    def save_mars_downscale_parameters(self,parameters):
        embryo_folder = os.path.join(".")
        voxel_size = parameters["resolution"]
        mars = parameters["mars_file"]
        fusion = parameters["template_file"]
        marsname = mars.replace("\\", "/").split("/")[-1]
        output_folder = parameters["output_folder"]
        output_file = os.path.join(output_folder, marsname)
        user = compute_user(parameters)
        save_general_metadata_to_xml(embryo_folder, "mars_downscale_date", output_file,
                                      datetime.now().strftime("%m/%d/%Y %H:%M:%S"), identifier_text="mars_downscale_target")
        save_general_metadata_to_xml(embryo_folder, "mars_downscale_user", output_file,
                                      user, identifier_text="mars_downscale_target")
        save_general_metadata_to_xml(embryo_folder, "mars_downscale_template", output_file,
                                      fusion, identifier_text="mars_downscale_target")
        save_general_metadata_to_xml(embryo_folder, "mars_downscale_source",output_file,
                                      mars, identifier_text="mars_downscale_target")
        save_general_metadata_to_xml(embryo_folder, "mars_downscale_resolution", output_file,
                                      str(voxel_size), identifier_text="mars_downscale_target")
    def downscale_mars(self, parameters):
        voxel_size = parameters["resolution"]
        if not "mars_file" in parameters:
            print("Please specify a MARS file path")
            exit()
        if not "output_folder" in parameters:
            print("Please specify the folder for the downscaled file")
            exit()
        if not "template_file" in parameters:
            print("Please specify the corresponding fusion image (downscaled version)")
            exit()
        mars = parameters["mars_file"]
        if not os.path.isfile(mars):
            print("MARS file does not exist")
            exit()
        fusion = parameters["template_file"]
        output_folder = parameters["output_folder"]
        if not os.path.isdir(output_folder):
            os.makedirs(output_folder)
        marsname = mars.replace("\\", "/").split("/")[-1]
        output_file = os.path.join(output_folder, marsname)
        os.system("conda run -n astec applyTrsf -ref " + str(fusion) + " -interpolation nearest -iso " + str(
            voxel_size) + " " + str(mars) + " " + str(output_file))
        self.save_mars_downscale_parameters(parameters)

    def test_fusion(self,parameters,rerun=False):

        # TESTS DEPENDENT PARAMETERS, DO NOT CHANGE
        #
        #
        #
        if not rerun:
            parameters["fusion_strategy"] = "'hierarchical-fusion'"
            parameters["EXP_FUSE"] = '"01_right_hierarchical"'
            parameters["acquisition_orientation"] = "'right'"
            self.start_fusion(parameters,run_now=False, keep_temp=True)

            parameters["fusion_strategy"] = "'direct-fusion'"
            parameters["EXP_FUSE"] = '"01_right_direct"'
            parameters["acquisition_orientation"] = "'right'"
            self.start_fusion(parameters,run_now=False, keep_temp=True)

            parameters["fusion_strategy"] = "'hierarchical-fusion'"
            parameters["EXP_FUSE"] = '"01_left_hierarchical"'
            parameters["acquisition_orientation"] = "'left'"

            self.start_fusion(parameters,run_now=False, keep_temp=True)

            parameters["fusion_strategy"] = "'direct-fusion'"
            parameters["EXP_FUSE"] = '"01_left_direct"'
            parameters["acquisition_orientation"] = "'left'"

            self.start_fusion(parameters,run_now=False, keep_temp=True)
            self.start_running(thread_number=4)
            self.write_fusions_parameters(parameters, keep_temp=True)
        else :
            parameters["fusion_strategy"] = "'direct-fusion'"
            parameters["EXP_FUSE"] = '"01_test"'
            parameters["acquisition_orientation"] = "'right'"
            self.start_fusion(parameters, keep_temp=True)


    def write_fusions_parameters(self,parameters,keep_temp=False):
        searcher = compute_user(parameters)
        omero_config_file = None
        if "omero_config_file" in parameters:
            omero_config_file = parameters["omero_config_file"]
        embryo_dir = "./"
        save_general_metadata_to_xml(embryo_dir, "fusion_user", "FUSE_"+parameters["EXP_FUSE"].replace('"','').replace("'",""), searcher,identifier_text="fusion_instance")
        save_general_metadata_to_xml(embryo_dir, "fusion_is_test", "FUSE_"+parameters["EXP_FUSE"].replace('"','').replace("'",""), str(keep_temp),identifier_text="fusion_instance")
        save_general_metadata_to_xml(embryo_dir, "fusion_date", "FUSE_"+parameters["EXP_FUSE"].replace('"','').replace("'",""), datetime.now().strftime("%m/%d/%Y %H:%M:%S"),identifier_text="fusion_instance")
        if omero_config_file is not None:
            save_general_metadata_to_xml(embryo_dir, "fusion_upload_user",
                                         "FUSE_" + parameters["EXP_FUSE"].replace('"', '').replace("'", ""),
                                         searcher, identifier_text="fusion_instance")
            save_general_metadata_to_xml(embryo_dir, "fusion_upload_date", "FUSE_"+parameters["EXP_FUSE"].replace('"','').replace("'",""), datetime.now().strftime("%m/%d/%Y %H:%M:%S"),identifier_text="fusion_instance")
    def start_fusion(self,parameters,run_now=True,keep_temp=False):
        omero_config_file = None
        if "omero_config_file" in parameters:
            omero_config_file = parameters["omero_config_file"]
        embryo_name = parameters["embryo_name"].replace('"','').replace("'","")

        begin = parameters["begin"]
        end = parameters["end"]
        real_parameters = {}
        real_parameters["acquisition_resolution"] = "(.195, .195, 1.)"
        real_parameters["target_resolution"] = ".3"
        real_parameters["result_image_suffix"] = "'nii'"
        real_parameters["acquisition_slit_line_correction"] = "True"
        real_parameters["acquisition_cropping_opening"] = "2"
        real_parameters["acquisition_cropping"] = "False"
        real_parameters["raw_crop"] = "True"
        real_parameters["fusion_crop"] = "True"

        real_parameters["fusion_preregistration_compute_registration"] = "True"
        real_parameters["fusion_preregistration_normalization"] = "False"
        real_parameters["fusion_registration_normalization"] = "False"
        real_parameters["fusion_stack_preregistration_normalization"] = "False"
        real_parameters["fusion_stack_registration_normalization"] = "False"
        real_parameters["fusion_xzsection_extraction"] = "False"

        # DATA DEPENDENT PARAMETERS , SHOUD NOT CHANGE IF UPDATED ONCE
        #
        #
        #

        real_parameters["DIR_RAWDATA"] = '"RAWDATA"'
        real_parameters["DIR_LEFTCAM_STACKZERO"] = '"stack_0_channel_0_obj_left"'
        real_parameters["DIR_RIGHTCAM_STACKZERO"] = '"stack_0_channel_0_obj_right"'
        real_parameters["DIR_LEFTCAM_STACKONE"] = '"stack_1_channel_0_obj_left"'
        real_parameters["DIR_RIGHTCAM_STACKONE"] = '"stack_1_channel_0_obj_right"'
        real_parameters["acquisition_leftcam_image_prefix"] = '"Cam_Left_000"'
        real_parameters["acquisition_rightcam_image_prefix"] = '"Cam_Right_000"'
        real_parameters["fusion_weighting"] = "'guignard'"
        real_parameters["fusion_strategy"] = '"hierarchical-fusion"'

        real_parameters["EXP_FUSE"] = '"01"'
        real_parameters["acquisition_orientation"] = '"right"'
        real_parameters["acquisition_mirrors"] = "False"
        real_parameters["acquisition_leftcamera_z_stacking"] = '"direct"'
        for key_param in parameters:
            real_parameters[key_param] = parameters[key_param]

        self.add_to_run("FUSE", ".", embryo_name, begin, real_parameters, end_time=end, compress_result=False,omero_result=(omero_config_file is not None),omero_config_file=omero_config_file,keep_temp=keep_temp)
        if run_now:
            self.start_running(thread_number=1)
            self.write_fusions_parameters(parameters, keep_temp=keep_temp)

    def compute_fusion_movie(self,parameters):
        real_parameters = {}
        real_parameters["EXP_INTRAREG"] = '"01_TEST"'
        real_parameters["intra_registration_movie_fusion_images"] = "True"
        embryo_name = parameters["embryo_name"].replace('"','').replace("'","")

        begin = parameters["begin"]
        end = parameters["end"]
        for key in parameters:
            real_parameters[key] = parameters[key]

        try:
            self.add_to_run("INTRAREG", ".", embryo_name, begin, real_parameters, end_time=end, compress_result=True)

            self.start_running(thread_number=1)

            self.compute_video_from_movie(embryo_name, real_parameters["EXP_INTRAREG"], real_parameters["EXP_FUSE"])
        except:
            print("Error during video computation: ", sys.exc_info()[0])
    def final_fusion(self, parameters):
        embryo_name = parameters["embryo_name"].replace('"','').replace("'","")
        if not "EXP_FUSE" in parameters:
            parameters["EXP_FUSE"] = '"01"'
        real_parameters = self.start_fusion(parameters)

        self.compute_fusion_movie(real_parameters)

        try:
            self.plot_signal_to_noise(embryo_name, real_parameters)
        except:
            print("Error during signal plot: ", sys.exc_info()[0])


    def start_mars(self,parameters):
        use_contour = parameters["use_contour"]
        omero_config_file = None
        if "omero_config_file" in parameters:
            omero_config_file = parameters["omero_config_file"]
        embryo_name = parameters["embryo_name"].replace('"','').replace("'","")
        embryo_dir ="."
        begin = parameters["begin"]
        end = parameters["end"]
        normalisation = 1000
        if "normalisation" in parameters:
            normalisation = parameters["normalisation"]
        voxel_size = parameters["resolution"]
        real_parameters = {}

        real_parameters["sigma_TV"] = "4.5"
        real_parameters["result_image_suffix"] = "'nii'"
        real_parameters["intensity_enhancement"] = "'gace'"

        if use_contour:
            real_parameters["EXP_CONTOUR"] = "'RELEASE_" + str(voxel_size).split(".")[1] + "'"
            real_parameters["outer_contour_enhancement"] = "'from_contour_image'"
            real_parameters["enhancement_normalization_max_value"] = str(normalisation)
            real_parameters["enhancement_transformation"] = "'normalization_to_u16'"
            real_parameters["normalization_max_value"] = str(normalisation)
            real_parameters["intensity_transformation"] = "'normalization_to_u16'"
        user = None
        if "user" in parameters:
            user = parameters["user"]
        for key_param in parameters:
            real_parameters[key_param] = parameters[key_param]
        self.add_to_run("MARS", ".", embryo_name, begin, real_parameters, end_time=end, compress_result=False,omero_result=(omero_config_file is not None),omero_config_file=omero_config_file)
        self.start_running(thread_number=1)

        if omero_config_file is not None:
            save_general_metadata_to_xml(embryo_dir, "mars_upload_user",
                                         "MARS_" + real_parameters["EXP_SEG"].replace('"', '').replace("'", ""),
                                         user, identifier_text="mars_instance")
            save_general_metadata_to_xml(embryo_dir, "mars_upload_date", "MARS_"+real_parameters["EXP_SEG"].replace('"','').replace("'",""), datetime.now().strftime("%m/%d/%Y %H:%M:%S"),identifier_text="mars_instance")


        try:
            self.plot_mars_info(embryo_name, "mars_add", begin, working_resolution=voxel_size)
        except:
            print("Error  mars plot for add : ", sys.exc_info()[0])

    def test_mars(self,parameters):
        parameters["EXP_SEG"] = '"mars_add"'
        parameters["reconstruction_images_combination"] = "'addition'"
        real_parameters = self.start_mars(parameters)

        real_parameters["EXP_SEG"] = '"mars_max"'
        real_parameters["reconstruction_images_combination"] = "'maximum'"
        self.start_mars(real_parameters)

    def test_segmentation(self,parameters):
        # TESTS DEPENDENT PARAMETERS, DO NOT CHANGE
        #
        #
        #
        parameters["EXP_SEG"] = '"test_addition_glace"'
        parameters["reconstruction_images_combination"] = "'addition'"
        parameters["intensity_enhancement"] = "'glace'"
        self.start_segmentation(parameters,run_now=False)

        parameters["EXP_SEG"] = '"test_addition_gace"'
        parameters["reconstruction_images_combination"] = "'addition'"
        parameters["intensity_enhancement"] = "'gace'"
        self.start_segmentation(parameters,run_now=False)

        parameters["EXP_SEG"] = '"test_maximum_glace"'
        parameters["reconstruction_images_combination"] = "'maximum'"
        parameters["intensity_enhancement"] = "'glace'"
        self.start_segmentation(parameters,run_now=False)

        parameters["EXP_SEG"] = '"test_maximum_gace"'
        parameters["reconstruction_images_combination"] = "'maximum'"
        parameters["intensity_enhancement"] = "'gace'"

        self.start_segmentation(parameters,run_now=False)

        self.start_running(thread_number=4)

        self.segmentation_parameters(parameters)

        # Embryo dependant parameters

        parameters["EXP_SEG"] = '"test_maximum_gace"'
        parameters["EXP_POST"] = '"test_maximum_gace"'

        self.start_post_correction(parameters,run_now=False)

        parameters["EXP_SEG"] = '"test_addition_glace"'
        parameters["EXP_POST"] = '"test_addition_glace"'

        self.start_post_correction(parameters,run_now=False)

        parameters["EXP_SEG"] = '"test_addition_gace"'
        parameters["EXP_POST"] = '"test_addition_gace"'

        self.start_post_correction(parameters,run_now=False)

        parameters["EXP_SEG"] = '"test_maximum_glace"'
        parameters["EXP_POST"] = '"test_maximum_glace"'

        self.start_post_correction(parameters,run_now=False)

        self.post_correction_parameters(parameters)

        self.start_running(thread_number=4)

    def segmentation_parameters(self,parameters):
        embryo_folder = "."
        user = compute_user(parameters)
        MARS_PATH = parameters["mars_path"]
        begin = parameters["begin"]
        end = parameters["end"]
        omero_config_file = None
        if "omero_config_file" in parameters:
            omero_config_file = parameters["omero_config_file"]
        save_general_metadata_to_xml(embryo_folder, "segmentation_date", "SEG_" + str(parameters["EXP_SEG"]),
                                     datetime.now().strftime("%m/%d/%Y %H:%M:%S"),
                                     identifier_text="segmentation_instance")
        save_general_metadata_to_xml(embryo_folder, "segmentation_mars_path", "SEG_" + str(parameters["EXP_SEG"]),
                                     MARS_PATH, identifier_text="segmentation_instance")
        save_general_metadata_to_xml(embryo_folder, "segmentation_begin_time", "SEG_" + str(parameters["EXP_SEG"]),
                                     str(begin), identifier_text="segmentation_instance")
        save_general_metadata_to_xml(embryo_folder, "segmentation_end_time", "SEG_" + str(parameters["EXP_SEG"]),
                                     str(end), identifier_text="segmentation_instance")
        save_general_metadata_to_xml(embryo_folder, "segmentation_user", "SEG_" + str(parameters["EXP_SEG"]),
                                     str(user), identifier_text="segmentation_instance")
        save_general_metadata_to_xml(embryo_folder, "segmentation_is_uploaded", "SEG_" + str(parameters["EXP_SEG"]),
                                     str((omero_config_file is not None)), identifier_text="segmentation_instance")

        if omero_config_file is not None:
            save_general_metadata_to_xml(embryo_folder, "seg_upload_user",
                                         "SEG_" + parameters["EXP_SEG"].replace('"', '').replace("'", ""),
                                         user, identifier_text="segmentation_instance")
            save_general_metadata_to_xml(embryo_folder, "seg_upload_date",
                                         "SEG_" + parameters["EXP_SEG"].replace('"', '').replace("'", ""),
                                         datetime.now().strftime("%m/%d/%Y %H:%M:%S"),
                                         identifier_text="segmentation_instance")

    def start_segmentation(self,parameters,run_now=True):
        use_contour = parameters["use_contour"]
        omero_config_file = None
        if "omero_config_file" in parameters:
            omero_config_file = parameters["omero_config_file"]
        normalisation = 1000
        if "normalisation" in parameters:
            normalisation = parameters["normalisation"]
        voxel_size = parameters["resolution"]

        MARS_PATH = parameters["mars_path"]
        parameters = self.format_embryo_name(parameters)
        embryo_name = parameters["embryo_name"].replace("'","").replace('"','')
        begin = parameters["begin"]
        end = parameters["end"]

        real_parameters = {}

        real_parameters["sigma_TV"] = "4.5"
        real_parameters["result_image_suffix"] = "'nii'"
        real_parameters["intensity_enhancement"] = "'gace'"
        real_parameters["EXP_FUSE"] = "'01'"
        if use_contour:
            real_parameters["EXP_CONTOUR"] = "'RELEASE_" + str(voxel_size).split(".")[1] + "'"
            real_parameters["outer_contour_enhancement"] = "'from_contour_image'"
            real_parameters["enhancement_normalization_max_value"] = str(normalisation)
            real_parameters["enhancement_transformation"] = "'normalization_to_u16'"
            real_parameters["normalization_max_value"] = str(normalisation)
            real_parameters["intensity_transformation"] = "'normalization_to_u16'"

        for key_param in parameters:
            real_parameters[key_param] = parameters[key_param]
        self.add_to_run("SEG", ".", embryo_name, begin, parameters, end_time=end, compress_result=False,
                           mars_path=MARS_PATH,omero_result=(omero_config_file is not None),omero_config_file=omero_config_file)
        if run_now:
            self.start_running(thread_number=1)
            self.segmentation_parameters(real_parameters)
        return real_parameters

    def post_correction_parameters(self,parameters):
        user = compute_user(parameters)
        embryo_folder ="."
        omero_config_file = None
        if "omero_config_file" in parameters:
            omero_config_file = parameters["omero_config_file"]
        begin = parameters["begin"]
        end = parameters["end"]
        save_general_metadata_to_xml(embryo_folder, "post_correction_date", "POST_"+str(parameters["EXP_POST"]),
                                      datetime.now().strftime("%m/%d/%Y %H:%M:%S"), identifier_text="post_correction_instance")
        save_general_metadata_to_xml(embryo_folder, "post_correction_begin_time", "POST_"+str(parameters["EXP_POST"]),
                                      str(begin), identifier_text="post_correction_instance")
        save_general_metadata_to_xml(embryo_folder, "post_correction_end_time", "POST_"+str(parameters["EXP_POST"]),
                                      str(end), identifier_text="post_correction_instance")
        save_general_metadata_to_xml(embryo_folder, "post_correction_user", "POST_"+str(parameters["EXP_POST"]),
                                      str(user), identifier_text="post_correction_instance")
        if omero_config_file is not None:
            save_general_metadata_to_xml(embryo_folder, "post_correction_upload_user",
                                         "POST_" + parameters["EXP_POST"].replace('"', '').replace("'", ""),
                                         user, identifier_text="post_correction_instance")
            save_general_metadata_to_xml(embryo_folder, "post_correction_upload_date", "POST_"+parameters["EXP_POST"].replace('"','').replace("'",""), datetime.now().strftime("%m/%d/%Y %H:%M:%S"),identifier_text="post_correction_instance")

    def start_post_correction(self,parameters,run_now=True):
        parameters = self.format_embryo_name(parameters)
        embryo_name = parameters["embryo_name"].replace('"','').replace("'","")
        omero_config_file = None
        if "omero_config_file" in parameters:
            omero_config_file = parameters["omero_config_file"]
        begin = parameters["begin"]
        end = parameters["end"]
        voxel_size = parameters["resolution"]
        real_parameters = {}
        real_parameters["EXP_POST"] = '"01"'
        real_parameters["intra_registration_resolution"] = str(voxel_size)
        real_parameters["test_branch_length"] = "True"
        real_parameters["test_early_division"] = "True"
        real_parameters["test_volume_correlation"] = "True"
        real_parameters["test_postponing_division"] = "True"
        real_parameters["result_image_suffix"] = "'nii'"
        for key_param in parameters:
            real_parameters[key_param] = parameters[key_param]
        self.add_to_run("POST", ".", embryo_name, begin, parameters, end_time=end, compress_result=False,omero_result=(omero_config_file is not None),omero_config_file=omero_config_file)
        if run_now:
            self.start_running(thread_number=1)
            self.post_correction_parameters(parameters)
        try :
            self.compute_graphs_post(embryo_name, begin, end)
        except :
            print("Error during computation of the Post correction graphs")

        return real_parameters

    def apply_intrareg_parameters(self,parameters):
        user = compute_user(parameters)
        embryo_folder = "."
        begin = parameters["begin"]
        end = parameters["end"]
        save_general_metadata_to_xml(embryo_folder, "intraregistration_date",
                                     "INTRAREG_" + str(parameters["EXP_INTRAREG"]),
                                     datetime.now().strftime("%m/%d/%Y %H:%M:%S"),
                                     identifier_text="intraregistration_instance")
        save_general_metadata_to_xml(embryo_folder, "intraregistration_begin_time",
                                     "POST_" + str(parameters["EXP_INTRAREG"]),
                                     str(begin), identifier_text="intraregistration_instance")
        save_general_metadata_to_xml(embryo_folder, "intraregistration_end_time",
                                     "POST_" + str(parameters["EXP_INTRAREG"]),
                                     str(end), identifier_text="intraregistration_instance")
        save_general_metadata_to_xml(embryo_folder, "intraregistration_user",
                                     "POST_" + str(parameters["EXP_INTRAREG"]),
                                     str(user), identifier_text="intraregistration_instance")
    def apply_intrareg(self,parameters):
        omero_config_file = None
        if "omero_config_file" in parameters:
            omero_config_file = parameters["omero_config_file"]
        parameters = self.format_embryo_name(parameters)
        embryo_name = parameters["embryo_name"].replace("'","").replace('','"')
        begin = parameters["begin"]
        end = parameters["end"]
        real_parameters = {}
        real_parameters["EXP_INTRAREG"] = '"01"'
        real_parameters["delta"] = "1"
        real_parameters["raw_delay"] = "0"
        real_parameters["intra_registration_template_type"] = '"POST-SEGMENTATION"'
        real_parameters["intra_registration_template_threshold"] = "2"
        real_parameters["intra_registration_margin"] = "20"
        real_parameters["intra_registration_resample_post_segmentation_images"] = "True"
        real_parameters["intra_registration_resample_segmentation_images"] = "False"
        real_parameters["intra_registration_movie_post_segmentation_images"] = "True"
        real_parameters["intra_registration_movie_segmentation_images"] = "False"
        real_parameters["intra_registration_rebuild_template"] = "True"
        for key_param in parameters:
            real_parameters[key_param] = parameters[key_param]

        # PRODUCTION PARAMETERS, UPDATE WITH THE TEST CHOSEN PREVIOUSLY
        #
        #
        #

        try:
            self.add_to_run("INTRAREG", ".", embryo_name, begin, real_parameters, end_time=end, compress_result=False)

            self.start_running(thread_number=1)
            self.apply_intrareg_parameters(parameters)
        except:
            print("Error  during seg intrareg : ", sys.exc_info()[0])

        try:
            intra_folder = "INTRAREG/INTRAREG_" + str(parameters["EXP_INTRAREG"]) + "/POST/POST_" + str(
                                            parameters["EXP_POST"])
            self.upload_on_omero(omero_config_file, embryo_name, "INT_POST_" + str(parameters["EXP_POST"]),
                                    intra_folder, include_logs=True)
        except:
            print("Error  during intrareg upload : ", sys.exc_info()[0])
        try:
            intra_fuse_folder = "INTRAREG/INTRAREG_" + str(
                parameters["EXP_INTRAREG"]) + "/FUSE/FUSE_" + str(parameters["EXP_FUSE"])
            self.upload_on_omero(omero_config_file, embryo_name, "INT_FUSE_" + str(parameters["EXP_FUSE"]),
                                    intra_fuse_folder, include_logs=True)
        except:
            print("Error  during intrareg fuse upload : ", sys.exc_info()[0])
        return real_parameters

    def compute_properties_parameters(self,parameters):
        embryo_folder = os.path.join(".")
        user = compute_user(parameters)
        begin = parameters["begin"]
        end = parameters["end"]
        save_general_metadata_to_xml(embryo_folder, "properties_date",
                                     "INTRAREG_" + str(parameters["EXP_INTRAREG"]),
                                     datetime.now().strftime("%m/%d/%Y %H:%M:%S"),
                                     identifier_text="intraregistration_instance")
        save_general_metadata_to_xml(embryo_folder, "properties_begin_time",
                                     "POST_" + str(parameters["EXP_INTRAREG"]),
                                     str(begin), identifier_text="intraregistration_instance")
        save_general_metadata_to_xml(embryo_folder, "properties_end_time",
                                     "POST_" + str(parameters["EXP_INTRAREG"]),
                                     str(end), identifier_text="intraregistration_instance")
        save_general_metadata_to_xml(embryo_folder, "properties_user", "POST_" + str(parameters["EXP_INTRAREG"]),
                                     str(user), identifier_text="intraregistration_instance")
    def compute_properties(self,parameters):
        embryo_name = parameters["embryo_name"]
        begin = parameters["begin"]
        end = parameters["end"]
        try:
            self.add_to_run("PROPERTIES", ".", embryo_name, begin, parameters, end_time=end, compress_result=False)
            self.start_running(thread_number=1)
            self.compute_properties_parameters(parameters)
        except:
            print("Error  during seg properties : ", sys.exc_info()[0])

    def prod_segmentation(self,parameters):
        parameters["embryo_name"] = parameters["embryo_name"].replace('"','').replace("'","")
        real_parameters = self.start_segmentation(parameters)

        # Embryo dependant parameters

        real_parameters = self.start_post_correction(real_parameters)

        real_parameters = self.apply_intrareg(real_parameters)

        self.compute_properties(real_parameters)






    def upload_data(self,parameters):
        omero_config_file = None
        if "omero_config_file" in parameters:
            omero_config_file = parameters["omero_config_file"]
        project_name = parameters["project_name"]
        dataset_name = parameters["dataset_name"]
        input_folder = parameters["input_folder"]
        if omero_config_file is None:
            print("OMERO config file is not bound, unable to upload")
            exit()
        if not os.path.isfile(omero_config_file):
            print("Unable to find OMERO config file , unable to upload")
            exit()
        self.upload_on_omero(omero_config_file, project_name, dataset_name, input_folder,
                                include_logs=True)