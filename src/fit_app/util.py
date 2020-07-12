import csv
import sys


def compare(input_fit, saved_fit):
    extra = {}
    required = {}

    # Finds extra items that are in the input fit but not saved fit
    for item_name in input_fit.keys():
        if item_name in saved_fit.keys():

            # If there are incomplete quantities, computes the difference
            quantity_difference = input_fit[item_name] - saved_fit[item_name]
            if quantity_difference > 0:
                extra[item_name] = quantity_difference
        else:
            extra[item_name] = input_fit[item_name]

    # Finds required items that are in the saved fit but not input fit
    for item_name in saved_fit.keys():
        if item_name in input_fit.keys():

            # If there are incomplete quantities, computes the difference
            quantity_difference = saved_fit[item_name] - input_fit[item_name]
            if quantity_difference > 0:
                required[item_name] = quantity_difference
        else:
            required[item_name] = saved_fit[item_name]

    return(extra, required)


def parse(text):
    item_dict = {}

    for item in text.split('\n'):

        # Retrieve item name from first column
        item_name = item.split('\t')[0].lstrip()
        for attribute in item.split('\t'):

            # Find the first column with a number
            if str.isdigit(attribute.split('\r')[0]):
                item_quantity = int(attribute.split('\r')[0])

                # Add quantities if it already exists
                if item_name in item_dict:
                    item_dict[item_name] += item_quantity

                # Otherwise, create a key with that quantity
                else:
                    item_dict[item_name] = item_quantity

    return(item_dict)


def out(data):
    outstring = ''

    for key, value in data.items():
        outstring = outstring + str(key) + '\t' + str(value) + '\n'

    return(outstring)
