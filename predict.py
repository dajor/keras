

import os
import glob
import json
import argparse

from invoicenet import FIELDS
from invoicenet.acp.acp import AttendCopyParse
import ocrmypdf
import tensorflow as tf
from tika import parser



def main():
    ap = argparse.ArgumentParser()

    ap.add_argument("--field", type=str, required=True, choices=FIELDS.keys(),
                    help="field to train parser for")
    ap.add_argument("--invoice", type=str, default=None,
                    help="path to directory containing prepared data")
    ap.add_argument("--data_dir", type=str, default='processed_data/',
                    help="path to directory containing prepared data")
    ap.add_argument("--pred_dir", type=str, default='predictions/',
                    help="path to directory containing prepared data")

    args = ap.parse_args()

    paths = []
    if args.invoice:
        if not os.path.exists(args.invoice):
            print("Could not find file '{}'".format(args.invoice))
            return
        paths.append(args.invoice)
    else:
        paths = [os.path.abspath(f) for f in glob.glob(args.data_dir + "**/*.pdf", recursive=True)]

    model = AttendCopyParse(field=args.field, restore=True)

    print("\nExtracting field '{}' from {} invoices...\n".format(args.field, len(paths)))

    predictions = model.predict(paths=paths)

    os.makedirs(args.pred_dir, exist_ok=True)
    for prediction, filename in zip(predictions, paths):
        filename = os.path.basename(filename)[:-3] + 'json'
        labels = {}
        if os.path.exists(os.path.join(args.pred_dir, filename)):
            with open(os.path.join(args.pred_dir, filename), 'r') as fp:
                labels = json.load(fp)
        with open(os.path.join(args.pred_dir, filename), 'w') as fp:
            labels[args.field] = prediction
            fp.write(json.dumps(labels))

        print("\nFilename: {}".format(filename))
        print("{}: {}\n".format(args.field, prediction))

    print("Predictions stored in '{}'".format(args.pred_dir))

def make_predictions(invoice, field, pred_dir):
    paths = []
    paths.append(invoice)
    #ocr_pdf(invoice)


    model = AttendCopyParse(field=field, restore=True)

    print("\nExtracting field '{}' from {} invoices...\n".format(field, len(paths)))

    predictions = model.predict(paths=paths)

    os.makedirs(pred_dir, exist_ok=True)

    for prediction, filename in zip(predictions, paths):
        filename = os.path.basename(filename)[:-3] + 'json'
        labels = {}
        if os.path.exists(os.path.join(pred_dir, filename)):
            with open(os.path.join(pred_dir, filename), 'r') as fp:
                labels = json.load(fp)
        with open(os.path.join(pred_dir, filename), 'w') as fp:
            labels[field] = prediction
            fp.write(json.dumps(labels))
        print("\nFilename: {}".format(filename))
        print("{}: {}\n".format(field, prediction))

    print("Predictions stored in '{}'".format(pred_dir))

def extract_all_data(invoice, pred_dir):
    fields = [
    'invoice_number',
    'vendor_name',
    'invoice_date',
    'tax_amount',
    'total_amount']
 
 
    opdf = ocr_pdf(invoice)
 
    for field in fields:
        make_predictions(invoice, field, pred_dir)


def make_predictions(invoice, field, pred_dir):
    paths = []
    paths.append(invoice)


    model = AttendCopyParse(field=field, restore=True)
    print("\nExtracting field '{}' from {} invoices...\n".format(field, len(paths)))

    predictions = model.predict(paths=paths)
    for prediction, filename in zip(predictions, paths):
        filename = os.path.basename(filename)[:-3] + 'json'
        labels = {}
        if os.path.exists(os.path.join(pred_dir, filename)):
            with open(os.path.join(pred_dir, filename), 'r') as fp:
                labels = json.load(fp)
        with open(os.path.join(pred_dir, filename), 'w') as fp:
            labels[field] = prediction
            fp.write(json.dumps(labels))
        print("\nFilename: {}".format(filename))
        print("{}: {}\n".format(field, prediction))

    print("Predictions stored in '{}'".format(pred_dir))

def ocr_pdf(pdf_document):
    try:
        dir_name = os.path.dirname(pdf_document)
        filename = os.path.basename(pdf_document)[:-4] + '_ocr.pdf'
        new_pdf_doc = os.path.join(dir_name, filename)
        res = ocrmypdf.ocr(pdf_document,new_pdf_doc,use_threads=True )
        return new_pdf_doc
    except Exception as e:
        print(e)




if __name__ == '__main__':
    main()
