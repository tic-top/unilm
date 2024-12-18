#!/usr/bin/env python
# w*- coding: utf-8 -*-

# File: OCR_SROIE_1_0.py
# Version: 1.0
# Date: 2019-04-13
# Description: Evaluation script that computes Text Localization following the Deteval implementation (same as TL2p_deteval_1_0 with 4 points and Python 3 compatibility)

import rrc_evaluation_funcs_1_1 as rrc_evaluation_funcs
import importlib

from shapely.geometry import Polygon
from shapely.ops import unary_union
from Levenshtein import distance

def calculate_ned(str1, str2):

    if len(str1) == 0 and len(str2) == 0:
        d = 0
        ned = 1
        return d, ned

    d = distance(str1, str2)
    ned = 1 - d / max(len(str1), len(str2))
    return ned

def evaluation_imports():
    """
    evaluation_imports: Dictionary ( key = module name , value = alias  )  with python modules used in the evaluation.
    """
    return {}


def default_evaluation_params():
    """
    default_evaluation_params: Default parameters to use for the validation and evaluation.
    """
    return {
        "GT_SAMPLE_NAME_2_ID": "(.+).txt",
        "DET_SAMPLE_NAME_2_ID": "(.+).txt",
        "CRLF": False,
    }


def validate_data(gtFilePath, submFilePath, evaluationParams):
    """
    Method validate_data: validates that all files in the results folder are correct (have the correct name contents).
                            Validates also that there are no missing files in the folder.
                            If some error detected, the method raises the error
    """
    gt = rrc_evaluation_funcs.load_zip_file(
        gtFilePath, evaluationParams["GT_SAMPLE_NAME_2_ID"]
    )

    subm = rrc_evaluation_funcs.load_zip_file(
        submFilePath, evaluationParams["DET_SAMPLE_NAME_2_ID"], True
    )

    if len(subm) != len(gt):
        # print(len(subm), len(gt))
        # raise Exception(
        #     "The Det file is not valid (invalid number of files in ZIP. Expected:"
        #     + str(len(gt))
        #     + " Found:"
        #     + str(len(subm))
        #     + ")"
        # )
        pass

    # Validate format of GroundTruth
    for k in gt:
        rrc_evaluation_funcs.validate_lines_in_file(
            k, gt[k], evaluationParams["CRLF"], False, True
        )

    # Validate format of results
    for k in subm:
        if (k in gt) == False:
            raise Exception("The sample %s not present in GT" % k)


def evaluate_method(gtFilePath, submFilePath, evaluationParams):
    """
    Method evaluate_method: evaluate method and returns the results
        Results. Dictionary with the following values:
        - method (required)  Global method metrics. Ex: { 'Precision':0.8,'Recall':0.9 }
        - samples (optional) Per sample metrics. Ex: {'sample1' : { 'Precision':0.8,'Recall':0.9 } , 'sample2' : { 'Precision':0.8,'Recall':0.9 }
    """

    for module, alias in evaluation_imports().items():
        globals()[alias] = importlib.import_module(module)

    def is_latin(s):
        try:
            s.encode(encoding="utf-8").decode("ascii")
        except UnicodeDecodeError:
            return False
        else:
            return True

    perSampleMetrics = {}

    methodRecallSum = 0
    methodIOUSum = 0
    methodPrecisionSum = 0
    methodEditDistanceSum = 0

    gt = rrc_evaluation_funcs.load_zip_file(
        gtFilePath, evaluationParams["GT_SAMPLE_NAME_2_ID"]
    )
    subm = rrc_evaluation_funcs.load_zip_file(
        submFilePath, evaluationParams["DET_SAMPLE_NAME_2_ID"], True
    )

    ioucnt = 0
    numGt = 0
    numDet = 0

    for resFile in gt:
        gtFile = rrc_evaluation_funcs.decode_utf8(gt[resFile])
        # print(resFile)
        gtpointsList, gtconfidencesList, gtWordsLine = (
            rrc_evaluation_funcs.get_tl_line_values_from_file_contents(
                gtFile, evaluationParams["CRLF"], False, True, False
            )
        )
        gtWords = (" ").join(gtWordsLine).split(" ")
        # remove ""
        gtWords = [word for word in gtWords if word != ""]
        cpgtWords = gtWords.copy()
        gtNumWords = len(gtWords)

        detWords = []
        detNumWords = 0

        recall = 0
        precision = 0
        hmean = 0
        recallAccum = 0.0
        precisionAccum = 0.0
        edit_distanceAccum = 0.0

        log = ""

        if resFile in subm:
            detFile = rrc_evaluation_funcs.decode_utf8(subm[resFile])
            # print(detFile)
            detLines = detFile.split("\n")
            for line in detLines:
                line = line.replace("\r", "").replace("\n", "")
                if line != "":
                    detWords.append(line)

            results = []
            detpointsList = []
            for item in detWords:
                # if "<|" in item or "|>" in item:
                #     continue
                texts = item.split(",")
                if len(texts) < 9:
                    # print(resFile)
                    try:
                        points = [int(i) for i in texts[:4]]
                        x0 = points[0]
                        y0 = points[1]
                        x1 = points[2]
                        y1 = points[3]
                        points = [x0, y0, x1, y0, x1, y1, x0, y1]
                        text = ",".join(texts[4:]).strip()
                    except:
                        # print(resFile)
                        points = [0] * 8
                        text = ",".join(texts).strip()
                else:
                    try:
                        points = [int(i) for i in texts[:8]]
                        text = ",".join(texts[8:]).strip()
                    except:
                        continue
                results.extend(text.split())
                detpointsList.append(points)
            detWords = results
            detWords = [word.lower() for word in detWords]
            gtWords = [word.lower() for word in gtWords]
            # calculate the edit distance
            try:
                edit_distanceAccum += calculate_ned("".join(detWords), "".join(gtWords))
            except Exception as e:
                # print(e)
                # print(detWords, gtWords)
                edit_distanceAccum = 0
            detNumWords = len(detWords)

            for word in detWords:
                log += "<br>det word = " + word + " "
                # print(word, gtWords)
                # exit(0)
                if word in gtWords:
                    log += "found"
                    recallAccum += 1
                    precisionAccum += 1
                    gtWords.remove(word)
                else:
                    log += "not found"
            try:
                gt_polygons = [
                    Polygon([(l[0], l[1]), (l[2], l[3]), (l[4], l[5]), (l[6], l[7])])
                    for l in gtpointsList
                ]
                det_polygons = [
                    Polygon([(l[0], l[1]), (l[2], l[3]), (l[4], l[5]), (l[6], l[7])])
                    for l in detpointsList
                ]

                # Calculate the union of all ground truth and detected polygons
                union_gt = unary_union(gt_polygons)
                union_det = unary_union(det_polygons)

                # Calculate the intersection of the unions
                
                intersection = union_gt.intersection(union_det).area
                union = union_gt.union(union_det).area
            except:
                intersection = 0
                union = 0
                # print(resFile)

            # Calculate overall IoU
            methodIOUSum += intersection / union if union != 0 else 0

            if len(detpointsList) == len(gtpointsList) and len(detpointsList) > 0:
                ioucnt += 1

        precision = (
            float(0) if detNumWords == 0 else float(precisionAccum) / detNumWords
        )

        recall = float(1) if gtNumWords == 0 else float(recallAccum) / gtNumWords
        hmean = (
            0
            if (precision + recall) == 0
            else 2.0 * precision * recall / (precision + recall)
        )

        methodEditDistanceSum += edit_distanceAccum
        methodRecallSum += recall
        methodPrecisionSum += precision
        numGt += gtNumWords
        numDet += detNumWords

        perSampleMetrics[resFile] = {
            "precision": precision,
            "recall": recall,
            "hmean": hmean,
            "gtWords": gtNumWords,
            "detWords": detNumWords,
            "correct": recallAccum,
            "log": log,
        }

    methodIOU = methodIOUSum / len(gt) if len(gt) > 0 else 0
    methodRecall = 0 if numGt == 0 else methodRecallSum / len(gt)
    methodPrecision = 0 if numDet == 0 else methodPrecisionSum / len(gt)
    methodHmean = (
        0
        if methodRecall + methodPrecision == 0
        else 2 * methodRecall * methodPrecision / (methodRecall + methodPrecision)
    )
    methodEditDistance = methodEditDistanceSum / len(gt) if len(gt) > 0 else 0

    methodMetrics = {
        "precision": methodPrecision,
        "recall": methodRecall,
        "f1": methodHmean,
        "iou": methodIOU,
        "edit_distance": methodEditDistance,
        "finished_ratio": len(subm) / len(gt),
    }

    resDict = {
        "calculated": True,
        "Message": "",
        "method": methodMetrics,
        "per_sample": perSampleMetrics,
    }

    return resDict


if __name__ == "__main__":

    rrc_evaluation_funcs.main_evaluation(
        None, default_evaluation_params, validate_data, evaluate_method
    )
