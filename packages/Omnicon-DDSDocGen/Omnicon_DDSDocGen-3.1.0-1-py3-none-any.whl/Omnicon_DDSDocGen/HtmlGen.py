import os
import json
from typing import List
from bs4 import BeautifulSoup
import re

from .SharedEnums import ChangeStatusEnum
from . import DocGenInterface

from . import Logger


class HtmlGen(DocGenInterface.DocGenInterface):
    def __init__(self, title: str, new_version: str, time: str, origin_version: str = "",
                 origin_dds_types_files: list = None,
                 new_dds_types_files: list = None,
                 origin_dds_topics_types_mapping: str = "",
                 new_dds_topics_types_mapping: str = "",
                 is_compare_by_name: bool = False,
                 is_ignore_id: bool = False,
                 is_summary_report=False):

        super().__init__(title=title,
                         new_version=new_version,
                         time=time,
                         origin_version=origin_version,
                         origin_dds_types_files=origin_dds_types_files,
                         new_dds_types_files=new_dds_types_files,
                         origin_dds_topics_types_mapping=origin_dds_topics_types_mapping,
                         new_dds_topics_types_mapping=new_dds_topics_types_mapping)
        self.logger = Logger.add_logger(__name__)

        # Create a new '.html' file based on the styling info from the template
        self.html_template_path = HtmlGen.get_html_template_path()
        if not self.html_template_path:
            self.logger.fatal("Template.html wasn't found. Cannot create html file")
            raise Exception("Template.html wasn't found. Cannot create html")
        else:
            self.logger.debug("html template path at " + self.html_template_path)

        with open(self.html_template_path, 'r') as html_file:
            self.soup = BeautifulSoup(html_file, 'html.parser')

        self.add_doc_title_page(title=title,
                                new_version=new_version,
                                time=time,
                                origin_version=origin_version,
                                origin_dds_types_files=origin_dds_types_files,
                                new_dds_types_files=new_dds_types_files,
                                origin_dds_topics_types_mapping=origin_dds_topics_types_mapping,
                                new_dds_topics_types_mapping=new_dds_topics_types_mapping,
                                is_compare_by_name=is_compare_by_name,
                                is_ignore_id=is_ignore_id, is_summary_report=is_summary_report)

        self.json_dict = {}

        self.latest_chapter = False
        self.title = ''

    def add_doc_title_page(self, title: str, new_version: str, time: str, origin_version: str,
                           origin_dds_types_files: list = None,
                           new_dds_types_files: list = None,
                           origin_dds_topics_types_mapping: str = "",
                           new_dds_topics_types_mapping: str = "",
                           is_compare_by_name: bool = False,
                           is_ignore_id: bool = False,
                           is_summary_report=False):
        title_tag = self.soup.find('title')
        title_tag.string = title

        document_title_tag = self.soup.find('h1', {'id': 'document-title'})
        document_title_tag.string = title

        document_version = self.soup.find('h2', {'id': 'document-version'})
        document_version.string = new_version

        document_timestamp = self.soup.find('h2', {'id': 'document-timestamp'})
        document_timestamp.string = time

        if origin_dds_types_files:
            document_source_type_files_list = self.soup.find('ul', {'id': 'source-type-files-list'})
            for filepath in origin_dds_types_files:
                new_li = self.soup.new_tag('li')
                new_li.string = filepath
                document_source_type_files_list.append(new_li)

        if origin_dds_topics_types_mapping:
            document_source_topic_mapping = self.soup.find('ul', {'id': 'source-topic-mapping-list'})
            new_li = self.soup.new_tag('li')
            new_li.string = origin_dds_topics_types_mapping
            document_source_topic_mapping.append(new_li)
        else:
            document_source_topic_mapping_div = self.soup.find('div', {'id': 'source-topic-mapping-div'})
            document_source_topic_mapping_div.clear()

    def add_toc_page(self):
        pass

    def add_chapter(self, section_title, parent_change_status=ChangeStatusEnum.NO_CHANGE, level=1):
        self.latest_chapter = section_title
        self.json_dict[section_title] = {
            'name': section_title
        }

    def add_type_to_chapter(self, dds_type, parent_change_status=ChangeStatusEnum.NO_CHANGE):
        if self.latest_chapter:
            self.json_dict[self.latest_chapter]['type'] = dds_type

    def add_table_header(self, listOfTitles, bLongHeader=True, color="grey"):
        if self.latest_chapter:
            if len(listOfTitles) == 5:
                listOfTitles.insert(4, "Change Type")
            self.json_dict[self.latest_chapter]['table_header'] = listOfTitles
            
            self.json_dict[self.latest_chapter]['table_content'] = [
                ["", self.json_dict[self.latest_chapter].get('type', '').rsplit('::', 1)[-1]] + ["" for i in range(len(listOfTitles) - 2)]
            ]

    def add_table_row(self, theTable, cells_text, align='c',
                      change_status=ChangeStatusEnum.NO_CHANGE):  # align=centered
        if self.latest_chapter:
            if len(cells_text) == 5:
                change_status_cell = change_status.name if change_status else ''
                cells_text.insert(4, change_status_cell)
            cells_text[0] = '[' + cells_text[0]
            self.json_dict[self.latest_chapter]['table_content'].append(cells_text)

    def add_new_page(self):
        pass

    def add_section(self):
        pass

    def add_description(self, descr, parent_change_status=ChangeStatusEnum.NO_CHANGE):
        if self.latest_chapter:
            self.json_dict[self.latest_chapter]['description'] = descr

    def add_message_volumes(self, min_volume, avg_volume, max_volume):
        if self.latest_chapter:
            self.json_dict[self.latest_chapter]['min_volume'] = min_volume
            self.json_dict[self.latest_chapter]['avg_volume'] = avg_volume
            self.json_dict[self.latest_chapter]['max_volume'] = max_volume if int(re.sub(r'[.,]', '', max_volume)) > 0 else "Unbounded"

    def add_new_line(self):
        pass

    @staticmethod
    def get_html_template_path() -> str:
        doc_name = "Template.html"
        local_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), doc_name)
        cwd_path = os.path.join(os.path.join(os.getcwd(), doc_name))
        if os.path.exists(local_path):
            return local_path
        elif os.path.exists(cwd_path):
            return cwd_path
        else:
            # https://importlib-resources.readthedocs.io/en/latest/using.html
            from importlib_resources import files
            whl_path = files('').joinpath(doc_name)
            if whl_path.is_file():
                return str(whl_path)
        return None

    def generate_doc(self, output_file_name: str, temp_folder: str):
        """
        This function invokes the generation of the html file then saves it in the requested folder.
        """
        self.logger.debug(self.generate_doc.__name__)
        output_file_name = f'{output_file_name}.html'
        temp_output_path = os.path.join(temp_folder, output_file_name)
        self.logger.info(f"Generating {output_file_name}")

        document_html_filename = self.soup.find('p', {'id': 'document-filepath'})
        document_html_filename.string = output_file_name

        try:
            with open(temp_output_path, 'w') as final_html_file:
                final_html_file.write(str(self.soup))
            self.logger.debug(f"Initial writing to temporary folder succeeded.")
        except Exception as err:
            self.logger.error(f"The operation of saving into temporary folder has FAILED", exc_info=True)
            return

    def finalize_doc(self):
        """
        This function is invoked after the generation of the html file.
        It is responsible for updating the json file with the new data.
        """
        script_tag = self.soup.find('script', {'id': 'types-data'})
        new_json_string = json.dumps(self.json_dict)
        script_tag.string = new_json_string
