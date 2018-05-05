'''
Copyright (C) 2018 SmugTomato

Created by SmugTomato

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
from .gmdc_data import gmdc_header, gmdc_element, gmdc_linkage, gmdc_group, gmdc_model, gmdc_subset
from .gmdc_data.gmdc_header import GMDCHeader
from .data_reader import DataReader
from .data_writer import DataWriter

class GMDC:


    GMDC_IDENTIFIER = 0xAC4F8687


    def __init__(self, file_data, byte_offset):
        self.data_read  = DataReader(file_data, byte_offset)

        self.header     = None
        self.elements   = None
        self.linkages   = None
        self.groups     = None
        self.model      = None
        self.subsets    = None


    @staticmethod
    def from_test_func(file_path):
        print("reading .5gd file...\n")

        file = open(file_path, "rb")
        file_data = file.read()
        byte_offset = 0
        file.close()
        return GMDC(file_data, byte_offset)


    @staticmethod
    def from_file_data(file_path):
        print("reading .5gd file...\n")

        file = open(file_path, "rb")
        file_data = file.read()
        byte_offset = 0
        file.close()
        return GMDC(file_data, byte_offset)


    def write(self, path):
        print("writing .5gd file...\n")

        file_data = open(path, "wb")
        writer = DataWriter()

        # HEADER
        self.header.write(writer)

        # ELEMENTS
        writer.write_int32( len(self.elements) )
        for el in self.elements:
            el.write(writer)

        # LINKAGES
        writer.write_int32( len(self.linkages) )
        for li in self.linkages:
            li.write(writer)

        # GROUPS
        writer.write_int32( len(self.groups) )
        for gr in self.groups:
            gr.write(writer)

        # MODEL
        self.model.write(writer)

        # SUBSETS
        writer.write_int32( len(self.subsets) )
        for su in self.subsets:
            su.write(writer)

        writer.write_out(file_data)
        file_data.close()



    def load_header(self):
        self.header = GMDCHeader.from_data(self.data_read)

        if self.header.version != 4 or self.header.file_type != self.GMDC_IDENTIFIER:
            return False
        return True

    @staticmethod
    def build_data(meshdata, filename):
        gmdc_data = GMDC(None, None)
        header = GMDCHeader.build_data(filename)
        gmdc_data.header = header
        return gmdc_data


    def __build_header(self, filename):
        self.header = GMDCHeader.build_data(filename)


    def load_data(self):
        # ELEMENTS
        count = self.data_read.read_int32()
        self.elements = []
        for i in range(0,count):
            temp_element = gmdc_element.GMDCElement()
            temp_element.read_data(self.data_read)
            self.elements.append(temp_element)

        # LINKAGES
        count = self.data_read.read_int32()
        self.linkages = []
        for i in range(0,count):
            temp_linkage = gmdc_linkage.GMDCLinkage()
            temp_linkage.read_data(self.data_read)
            self.linkages.append(temp_linkage)

        # GROUPS
        count = self.data_read.read_int32()
        self.groups = []
        for i in range(0,count):
            temp_group = gmdc_group.GMDCGroup()
            temp_group.read_data(self.data_read, self.header.version)
            self.groups.append(temp_group)

        # MODEL
        self.model = gmdc_model.GMDCModel()
        self.model.read_data(self.data_read)

        # SUBSETS
        count = self.data_read.read_int32()
        self.subsets = []
        for i in range(0,count):
            temp_subset = gmdc_subset.GMDCSubset()
            temp_subset.read_data(self.data_read)
            self.subsets.append(temp_subset)
