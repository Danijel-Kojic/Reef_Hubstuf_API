from xml.etree import ElementTree as ET


class HtmlGenerator:
    def __init__(self):
        pass


    def dump_work_time_table(self, activities_tuple: tuple):
        activities, users, projects = activities_tuple
        html = ET.Element('html')
        head = ET.SubElement(html, 'head')
        style = ET.SubElement(head, 'style')
        style.text = '''
            table {border: solid; border-width: thin; border-collapse: collapse;}
            td {border: solid; border-width: thin; padding: 4px;}
        '''
        body = ET.SubElement(html, 'body')
        table = ET.SubElement(body, 'table')

        thead = ET.SubElement(table, 'thead')
        tr = ET.SubElement(thead, 'tr')
        td = ET.SubElement(tr, 'td')
        td.text = 'Users'
        for project in projects.values():
            td = ET.SubElement(tr, 'td')
            td.text = project['name']

        tbody = ET.SubElement(table, 'tbody')
        for user_id, activities_per_user in activities.items():
            tr = ET.SubElement(tbody, 'tr')
            td = ET.SubElement(tr, 'td')
            td.text = users[user_id]['name']
            for project_id in projects.keys():
                td = ET.SubElement(tr, 'td')
                if project_id in activities_per_user:
                    td.text = str(activities_per_user[project_id])
                else:
                    td.text = ' '
        
        return ET.tostring(html, encoding='utf-8')
