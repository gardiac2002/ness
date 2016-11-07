
from collections import UserDict
from xml.etree import ElementTree


class NessusReport(UserDict):

    def __init__(self, hosts):
        super().__init__()
        self['hosts'] = hosts

    @classmethod
    def from_string(cls, content):
        tree = ElementTree.fromstring(content)

        for report in tree.findall('Report'):

            hosts = list()
            for host_element in report.findall('ReportHost'):
                report_host = NessusReportHost.from_etree(host_element)
                hosts.append(report_host)

        return NessusReport(hosts)


class NessusReportHost(UserDict):

    def __init__(self, host_data, report_items):
        super().__init__()
        self['host_properties'] = host_data
        self['report_items'] = list(report_items)

    @classmethod
    def from_etree(cls, host_element):

        host_properties = host_element.find('HostProperties')
        host_name = host_element.attrib.get('name')
        host_data = {prop.attrib.get('name'): prop.text for prop in host_properties}
        host_data.update(dict(name=host_name))

        report_items = list()
        for item in host_element.findall('ReportItem'):
            item_obj = NessusReportItem.from_etree(item)
            report_items.append(item_obj)

        return NessusReportHost(host_data, report_items)


class NessusReportItem(UserDict):

    def __init__(self, report_item_info):
        super().__init__()
        self.data = dict(report_item_info)

    @classmethod
    def from_etree(cls, item_element):

        data = dict()
        data.update(item_element.attrib)

        tags = ['bid', 'cve', 'iava', 'iavb', 'osvdb', 'xref']

        for element in item_element:
            if element.tag in tags:
                data.setdefault(element.tag, []).append(element.text)

        return NessusReportItem(data)
