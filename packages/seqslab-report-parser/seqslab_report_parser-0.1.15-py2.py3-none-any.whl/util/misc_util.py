from typing import Dict, List
import json
import os
import re

from parser.const import CHROMOSOME, FUSION_LOCUS, VARIANT_ACCESSION, VARIANT_ALLELE_FRACTION, VARIANT_ALLELE_FREQUENCY, \
    VARIANT_COVERAGE, VARIANT_POSITION, VARIANT_STRAND
from util.entities_util import label_dict


def gen_variables(tab: List[List[List[str]]], headers: List[str]) -> List[Dict[str, List[str]]]:
    results = []
    for row in tab:
        dict = {}
        for i in range(0, len(headers)):
            if isinstance(headers[i], tuple):
                (k1, k2) = headers[i]
                v1 = ''
                v2 = ''
                if k1 != 'AMINO_ACID_CHANGE' and k2 != 'AMINO_ACID_CHANGE':
                    v1 = row[i][0]
                    v2 = ' '.join(row[i][1:])
                elif k1 == 'AMINO_ACID_CHANGE':
                    if is_amino_acid_change(row[i][0]):
                        v1 = row[i][0]
                        v2 = ' '.join(row[i][1:])
                    else:
                        v2 = ' '.join(row[i])
                elif k2 == 'AMINO_ACID_CHANGE':
                    if is_amino_acid_change(row[i][-1]):
                        v1 = ' '.join(row[i][:-1])
                        v2 = row[i][-1]
                    else:
                        v1 = ' '.join(row[i])

                dict[k1] = [v1]
                dict[k2] = [v2]
            else:
                dict[headers[i]] = row[i]
        results.append(dict)

    # filtered_results = []
    # for r in results:
    #     d = {key: value for key, value in r.items() if value != ['ND']}
    #     if d:
    #         filtered_results.append(d)
    filtered_results = [r for r in results if any(value != ['ND'] for value in r.values())]

    return filtered_results


def is_amino_acid_change(w: str) -> bool:
    pattern = r'^[a-zA-Z]\d{3}[a-zA-Z]$'
    match = re.search(pattern, w)
    if match:
        return True
    else:
        return False


def substitute_words(variables: List[Dict[str, List[str]]], words: Dict[str, str]) -> None:
    for var in variables:
        for k, v in var.items():
            updated_v = list(map(lambda i: words.get(i, i), v))
            var[k] = updated_v


# def substitute_variables(template: str, variables: Dict) -> str:
#     for key, values in variables.items():
#         placeholder = "{" + key + "}"
#         if placeholder in template:
#             if len(values) >= 0:
#                 values_str = " ".join(values)
#                 template = template.replace(placeholder, values_str)
#             else:
#                 template = template.replace(placeholder, placeholder)
#
#     pattern = r'\{([A-Z0-9_]+)\}'
#     matches = re.findall(pattern, template)
#     if matches:
#         raise RuntimeError(f"Incomplete substitute: {', '.join(matches)}")
#
#     return template


def substitute_variables(template: str, variables: Dict[str, List[str]]) -> Dict[str, str]:
    template_list = template.split(" ")
    for key, values in variables.items():
        placeholder = "{" + key + "}"
        if placeholder in template:
            if len(values) >= 0:
                values_str = " ".join(values)
                template = template.replace(placeholder, values_str)
            else:
                template = template.replace(placeholder, placeholder)

    pattern = r'\{([A-Z0-9_]+)\}'
    matches = re.findall(pattern, template)
    if matches:
        raise RuntimeError(f"Incomplete substitute: {', '.join(matches)}")

    # Prepare NER Training Data
    result_text = []
    result_tag = []
    result_tag_id = []
    for idx, template_item in enumerate(template_list):
        pairs = list(filter(lambda p: ("{" + p[0] + "}") in template_item, variables.items()))
        if len(pairs) == 1:
            ner_text = []
            ner_tag = []
            ner_tag_id = []
            prefix_suffix = template_item.split("{" + pairs[0][0] + "}")
            if prefix_suffix[0] != "":
                ner_text.append(prefix_suffix[0])
                ner_tag.append("O")
                ner_tag_id.append(label_dict["O"])
            if pairs[0][0].startswith("FUSION_VARIANT"):
                entity = "FUSION_VARIANT"
            else:
                entity = pairs[0][0]
            ner_results = split_entities(' '.join(pairs[0][1]), entity)
            ner_text.extend(ner_results["text"])
            ner_tag.extend(ner_results["tag"])
            ner_tag_id.extend(ner_results["tag_id"])
            if prefix_suffix[1] != "":
                ner_text.append(prefix_suffix[1])
                ner_tag.append("O")
                ner_tag_id.append(label_dict["O"])
            result_text.extend(ner_text)
            result_tag.extend(ner_tag)
            result_tag_id.extend(ner_tag_id)
        else:
            result_text.append(template_item)
            result_tag.append("O")
            result_tag_id.append(label_dict["O"])

    return {"text": template, "tokens": result_text, "tags": result_tag, "tags_ids": result_tag_id,
            "ner": dict(map(lambda p: (p[0], ' '.join(p[1])), variables.items()))}


def write_file(output_file: str, lines: List[str]) -> None:
    with open(output_file, 'a') as file:
        for line in lines:
            file.write(line + '\n')


def split_entities(text: str, entity: str) -> Dict[str, List[str]]:
    ret_text = []
    ret_tag = []
    ret_tag_id = []
    begin = True
    space_items = text.split(" ")
    for i, space_item in enumerate(space_items):
        if entity == "REPORT_DATE":
            tag = f"B-{entity}" if begin else f"I-{entity}"
            ret_text.append(space_item)
            ret_tag.append(tag)
            ret_tag_id.append(label_dict[tag])
            begin = False
        else:
            comma_items = space_item.split(",")
            for j, comma_item in enumerate(comma_items):
                if comma_item == "":
                    continue
                elif comma_item == "and":
                    ret_text.append("and")
                    ret_tag.append("O")
                    ret_tag_id.append(label_dict["O"])
                    begin = True
                else:
                    tag = f"B-{entity}" if begin else f"I-{entity}"
                    ret_text.append(comma_item)
                    ret_tag.append(tag)
                    ret_tag_id.append(label_dict[tag])
                    begin = False
                    if j != len(comma_items) - 1:
                        ret_text.append(",")
                        ret_tag.append("O")
                        ret_tag_id.append(label_dict["O"])
                        begin = True
    return {
        "text": ret_text,
        "tag": ret_tag,
        "tag_id": ret_tag_id
    }


def write_json(results: Dict[str, str], output_dir: str, file_name: str) -> None:
    parent = output_dir if output_dir else ''
    with open(os.path.join(parent, file_name + '.json'), "w") as json_file:
        json.dump(results, json_file)


def rm_superscript(ls: List[str]) -> List[str]:
    pattern = r'^\d+(,)?$'
    return [item for item in ls if not re.match(pattern, item)]


def validate(pid: str, vars: List[Dict[str, List[str]]], headers: List[str]):
    supported = [
        CHROMOSOME,
        FUSION_LOCUS,
        VARIANT_ACCESSION,
        VARIANT_ALLELE_FRACTION,
        VARIANT_ALLELE_FREQUENCY,
        VARIANT_POSITION,
        VARIANT_STRAND
    ]
    header_to_check = list(filter(lambda i: i in supported, headers))
    for v in vars:
        for h in header_to_check:
            if h is CHROMOSOME:
                chr = v[CHROMOSOME][0].lower()
                if not chr.startswith('chr')\
                        and not chr.isnumeric()\
                        and chr != 'x' and chr != 'y' and chr != 'm' and chr != 'mt':
                    raise RuntimeError(f'validation failed: {pid} {CHROMOSOME}')

            if h is FUSION_LOCUS:
                locus = ' '.join(v[FUSION_LOCUS])
                if not locus.lower().startswith('chr') or len(locus.split(':')) != 2:
                    raise RuntimeError(f'validation failed: {pid} {FUSION_LOCUS}')

            if h is VARIANT_ACCESSION:
                accession = ' '.join(v[VARIANT_ACCESSION]).upper()
                if not accession.startswith('NM_') and not accession.startswith('NP_') and not accession.startswith('NR_'):
                    raise RuntimeError(f'validation failed: {pid} {VARIANT_ACCESSION}')

            if h is VARIANT_ALLELE_FRACTION:
                frac = v[VARIANT_ALLELE_FRACTION][0]
                if not frac.startswith('0.') and not frac.startswith('1.'):
                    raise RuntimeError(f'validation failed: {pid} {VARIANT_ALLELE_FRACTION}')

            if h is VARIANT_ALLELE_FREQUENCY:
                if not v[VARIANT_ALLELE_FREQUENCY][0].endswith('%'):
                    raise RuntimeError(f'validation failed: {pid} {VARIANT_ALLELE_FREQUENCY}')

            if h is VARIANT_POSITION:
                locus = ' '.join(v[VARIANT_POSITION])
                if not locus.lower().startswith('chr') or len(locus.split(':')) != 2:
                    raise RuntimeError(f'validation failed: {pid} {VARIANT_POSITION}')

            if h is VARIANT_STRAND:
                strand = v[VARIANT_STRAND][0]
                if strand != '+' and strand != '-':
                    raise RuntimeError(f'validation failed: {pid} {VARIANT_STRAND}')
