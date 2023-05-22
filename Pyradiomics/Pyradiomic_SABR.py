import os, sys
import SimpleITK as sitk
from radiomics import featureextractor
import collections, csv
import pathlib
import argparse, shutil
import six



if __name__ == '__main__':
    
    root = pathlib.Path.cwd()
    
    # Feature dir
    #recon_dir = os.path.join("/Data", "Recon3D", "Test", "Recon")
    Feature_dir = os.path.join(root, "Features_SALM_media")
    if os.path.exists(Feature_dir):
        shutil.rmtree(Feature_dir)
    os.makedirs(Feature_dir)
    
    
    # pyradiomics settings
    pyradiomics_settings = {}
    pyradiomics_settings['binWidth'] = 20# lung window ( lung == tumor = 20)
    #pyradiomics_settings['binWidth'] = 20 # media_window (lung =20, tumor = 5)
    #pyradiomics_settings['binWidth'] = 4
    #pyradiomics_settings['resampledPixelSpacing'] = None  # [3,3,3]
    pyradiomics_settings['resampledPixelSpacing'] = [1,1,1]
    pyradiomics_settings['interpolator'] = sitk.sitkBSpline
    pyradiomics_settings['enableCExtensions'] = True
    pyradiomics_settings['Normalization'] = False
    extractor = featureextractor.RadiomicsFeatureExtractor(**pyradiomics_settings)
    
    
    # traverse images
    # save into csv
    headers = None
  
    input_dir = os.path.join(root, "I-SABR","CT_media")
    mask_dir = os.path.join(root, "I-SABR","SAML_no_tumor")
   # image_names = sorted([ele for ele in os.listdir(input_dir) if ele.endswith(".nii.gz")])
    image_names = sorted([ele for ele in os.listdir(input_dir) if ele.endswith(".nii.gz")])
    image_paths = [os.path.join(input_dir, ele) for ele in image_names]
    for ind, cur_img_path in enumerate(image_paths):
        #file_name = os.path.basename(cur_img_path).split('.', 1)[0][:-2]
        file_name = os.path.basename(cur_img_path).split('_', 1)[1]
        print("Calculating {} {:3d}/{:3d}".format(file_name, ind+1, len(image_paths)))
        radiomics_fea_path = os.path.join(Feature_dir,"SALM_Media_features.csv")

        #ct_path = os.path.join(input_dir,file_name+"_Input_3D.nii.gz")
        ct_path = os.path.join(input_dir,'CT_' + file_name)
        mask_path = os.path.join(mask_dir,'SAML_' + file_name)
        featureVector = collections.OrderedDict({})
        featureVector["PatientID"] = file_name
        featureVector.update(extractor.execute(ct_path, mask_path))
        with open(radiomics_fea_path, "a") as outputFile:
            writer = csv.writer(outputFile, lineterminator='\n')
            if headers is None:
                headers = list(featureVector.keys())
                writer.writerow(headers)
            row = []
            for h in headers:
                row.append(featureVector.get(h, "N/A"))
            writer.writerow(row)

