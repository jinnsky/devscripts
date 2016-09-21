#!/usr/bin/python
#coding=utf-8

import os

TARGET_DIRECTORY = './Planetoid/Assets.xcassets'
TARGET_POSTFIX = '.imageset'
TARGET_SWIFT_FILE = './Planetoid/Resources/GlobalImage.swift'

def scan_target_files(directory, postfix):
    files_list = []
    for root, sub_dirs, files in os.walk(directory):
        for special_file in sub_dirs:
            if special_file.endswith(postfix):
                files_list.append(special_file)
    return files_list

def generate_variable_name(original_name):
    captialized_items = map(lambda item: item.capitalize(), original_name.split('_'))
    return reduce(lambda x,y: x + y, captialized_items)

def generate_swift_file(file_name, imageset_names):
    variable_lines = map(lambda imageset: '    case {0} = "{1}"\n'.format(generate_variable_name(imageset), imageset), imageset_names)

    with open(file_name, 'w+') as file:
        file.writelines(['//\n',
                         '//  GlobalImage.swift\n',
                         '//  Planetoid\n',
                         '//\n',
                         '//  Created by script automatically.\n',
                         '//\n',
                         '\n',
                         'import Foundation\n\n',
                         'enum ImageName: String {\n'])
        file.writelines(variable_lines)
        file.write('}\n')
    print '{0} is created success.'.format(TARGET_SWIFT_FILE)

def main():
    imageset_names = map(lambda item: item[:-len(TARGET_POSTFIX)], scan_target_files(TARGET_DIRECTORY, TARGET_POSTFIX))
    generate_swift_file(TARGET_SWIFT_FILE, imageset_names)

if __name__ == '__main__':
    main()
