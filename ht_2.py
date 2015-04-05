import time
import xml.etree.ElementTree as ET
import time
import ht_cpp
import sys

def py_calk(f_input_name, f_output_name):
    start = time.process_time()
    with open(f_input_name) as fr:
        tree = ET.ElementTree()
        tree.parse(fr)
        root = tree.getroot()
        nets_number = len(root.findall('net'))
        table = [[float('inf') for j in range(nets_number)]
                 for i in range(nets_number)]
        for i in range(nets_number):
            table[i][i] = 0
        for resistor in root.findall('resistor'):
            i = int(resistor.attrib['net_from']) - 1
            j = int(resistor.attrib['net_to']) - 1
            res = float(resistor.attrib['resistance'])
            try:
                table[i][j] = 1 / (1 / table[i][j] + 1 / res)
            except ZeroDivisionError:
                if (res == 0) or (table[i][j] == 0):
                    table[i][j] = 0
                else:
                    table[i][j] = float('inf')
            table[j][i] = table[i][j]
        for capactor in root.findall('capactor'):
            i = int(capactor.attrib['net_from']) - 1
            j = int(capactor.attrib['net_to']) - 1
            res = float(capactor.attrib['resistance'])
            try:
                table[i][j] = 1 / (1 / table[i][j] + 1 / res)
            except ZeroDivisionError:
                if (res == 0) or (table[i][j] == 0):
                    table[i][j] = 0
                else:
                    table[i][j] = float('inf')
            table[j][i] = table[i][j]
        for diode in root.findall('diode'):
            i = int(diode.attrib['net_from']) - 1
            j = int(diode.attrib['net_to']) - 1
            res = float(diode.attrib['resistance'])
            try:
                table[i][j] = 1 / (1 / table[i][j] + 1 / res)
            except ZeroDivisionError:
                if (res == 0) or (table[i][j] == 0):
                    table[i][j] = 0
                else:
                    table[i][j] = float('inf')
            rev_res = float(diode.attrib['reverse_resistance'])
            try:
                table[j][i] = 1 / (1 / table[j][i] + 1 / rev_res)
            except ZeroDivisionError:
                if (rev_res == 0) or (table[j][i] == 0):
                    table[j][i] = 0
                else:
                    table[j][i] = float('inf')
        for k in range(nets_number):
            for i in range(nets_number):
                for j in range(nets_number):
                    try:
                        table[i][j] = 1 / (1 / table[i][j] + 1 /
                                           (table[i][k] + table[k][j]))
                    except ZeroDivisionError:
                        if (table[i][j] == 0) or ((table[i][k] +
                                                       table[k][j]) == 0):
                            table[i][j] = 0
                        else:
                            table[i][j] = float('inf')
    with open(f_output_name, "w") as fw:
        for i in range(nets_number):
            for j in range(nets_number):
                print("%.6f" % (table[i][j]), end = ',', file = fw)
            print('\n', end = '', file = fw)
    finish = time.process_time()
    return (finish - start)

def cpp_calk(f_input_name, f_output_name):
    start = time.process_time()
    with open(f_input_name) as fr:
        tree = ET.ElementTree()
        tree.parse(fr)
        root = tree.getroot()
        nets_number = len(root.findall('net'))
        table = [[float('inf') for j in range(nets_number)]
                 for i in range(nets_number)]
        for i in range(nets_number):
            table[i][i] = 0
        for resistor in root.findall('resistor'):
            i = int(resistor.attrib['net_from']) - 1
            j = int(resistor.attrib['net_to']) - 1
            res = float(resistor.attrib['resistance'])
            try:
                table[i][j] = 1 / (1 / table[i][j] + 1 / res)
            except ZeroDivisionError:
                if (res == 0) or (table[i][j] == 0):
                    table[i][j] = 0
                else:
                    table[i][j] = float('inf')
            table[j][i] = table[i][j]
        for capactor in root.findall('capactor'):
            i = int(capactor.attrib['net_from']) - 1
            j = int(capactor.attrib['net_to']) - 1
            res = float(capactor.attrib['resistance'])
            try:
                table[i][j] = 1 / (1 / table[i][j] + 1 / res)
            except ZeroDivisionError:
                if (res == 0) or (table[i][j] == 0):
                    table[i][j] = 0
                else:
                    table[i][j] = float('inf')
            table[j][i] = table[i][j]
        for diode in root.findall('diode'):
            i = int(diode.attrib['net_from']) - 1
            j = int(diode.attrib['net_to']) - 1
            res = float(diode.attrib['resistance'])
            try:
                table[i][j] = 1 / (1 / table[i][j] + 1 / res)
            except ZeroDivisionError:
                if (res == 0) or (table[i][j] == 0):
                    table[i][j] = 0
                else:
                    table[i][j] = float('inf')
            rev_res = float(diode.attrib['reverse_resistance'])
            try:
                table[j][i] = 1 / (1 / table[j][i] + 1 / rev_res)
            except ZeroDivisionError:
                if (rev_res == 0) or (table[j][i] == 0):
                    table[j][i] = 0
                else:
                    table[j][i] = float('inf')
        table = ht_cpp.faster_dot(table)
    with open(f_output_name, "w") as fw:
        for i in range(nets_number):
            for j in range(nets_number):
                print("%.6f" % (table[i][j]), end = ',', file = fw)
            print('\n', end = '', file = fw)
    finish = time.process_time()
    return (finish - start)

def final_answer(f_input_name, f_output_name):
    time_cpp = cpp_calk(f_input_name, f_output_name)
    time_py = py_calk(f_input_name, f_output_name)
    if ((time_py - time_cpp) == 0):
        return 1
    else:
        if time_cpp == 0:
            return float('inf')
    return time_py/time_cpp

if __name__ == "__main__":
    to_print = final_answer(sys.argv[1],sys.argv[2])
    print(to_print)
