#************************************************************************
# Copyright 2023 O7 Conseils inc (Philippe Gosselin)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#************************************************************************
"""Module allows to view and access Security Hub resources"""


#--------------------------------
#
#--------------------------------
import logging
import datetime
import pprint
import pandas as pd


from o7util.table import TableParam, ColumnParam, Table
import o7util.menu as o7m
import o7util.terminal as o7t
import o7util.html_report as o7hr


import o7lib.aws.base
import o7cli.sts

logger=logging.getLogger(__name__)



#*************************************************
#
#*************************************************
class SecurityHub(o7lib.aws.base.Base):
    """Class for SecurityHub """

    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html

    #*************************************************
    #
    #*************************************************
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client = self.session.client('securityhub')



        self.df_standards : pd.DataFrame = None
        self.dfs_controls : dict[str, pd.DataFrame] = {}
        self.df_findings : pd.DataFrame = None

        self.standard : pd.Series = None
        self.control : pd.Series = None
        self.finding : pd.Series = None
        self.df_menu_findings : pd.DataFrame = None

        # self.description : dict = None
        # self.enabled_services : list = []
        # self.accounts : list = []
        # self.policies : list = None



    #*************************************************
    #
    #*************************************************
    def load_standards(self):
        """Load all standards"""

        logger.info('load_standards')

        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/client/describe_standards.html
        paginator = self.client.get_paginator('describe_standards')

        standards = []

        for page in paginator.paginate():
            standards.extend(page.get('Standards', []))


        self.df_standards = pd.DataFrame(standards)
        self.df_standards.set_index('StandardsArn', inplace=True)

        logger.info(f'load_standards: Number of standards found {len(standards)}')
        return self

    #*************************************************
    #
    #*************************************************
    def load_enabled_standards(self):
        """Load enabled standards"""

        if self.df_standards is None:
            self.load_standards()

        logger.info('load_enabled_standards')

        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/client/get_enabled_standards.html
        paginator = self.client.get_paginator('get_enabled_standards')
        standards = []

        for page in paginator.paginate():
            standards.extend(page.get('StandardsSubscriptions', []))

        # self.df_standards = pd.DataFrame(standards)
        logger.info(f'load_enabled_standards: Number of standards found {len(standards)}')

        df = pd.DataFrame(standards).set_index('StandardsArn')
        self.df_standards = self.df_standards.join(df, how='left', lsuffix='_left', rsuffix='_right')

        return self

    #*************************************************
    #
    #*************************************************
    def load_standard_controls(self):
        """Load all controles for each standards"""

        if self.df_standards is None:
            self.load_enabled_standards()

        df_ready = self.df_standards[self.df_standards['StandardsStatus'] == 'READY']

        for index, row in df_ready.iterrows():

            # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/client/describe_standards_controls.html
            paginator = self.client.get_paginator('describe_standards_controls')
            controls = []

            for page in paginator.paginate(StandardsSubscriptionArn=row['StandardsSubscriptionArn']):
                controls.extend(page.get('Controls', []))

            df_controls = pd.DataFrame(controls)
            df_controls['ControlStatusUpdatedAt'] = df_controls['ControlStatusUpdatedAt'].dt.tz_localize(None)

            self.dfs_controls[index] = df_controls
            self.dfs_controls[index]['CheckPass'] = None
            self.dfs_controls[index]['CheckFail'] = None

            self.df_standards.loc[index, 'ControlsCount'] = len(df_controls.index)
            self.df_standards.loc[index, 'ControlsDisabled'] = len(df_controls[df_controls['ControlStatus'] == 'DISABLED'].index)

        self.df_standards['ControlsEnabled'] = self.df_standards['ControlsCount'] - self.df_standards['ControlsDisabled']
        self.df_standards['ControlsPassed'] = None
        self.df_standards['ControlsFailed'] = None
        self.df_standards['ControlsNoData'] = None
        self.df_standards['Score'] = None


    #*************************************************
    #
    #*************************************************
    def load_findings(self, standard_arn : str = None):
        """Load findings"""

        logger.info(f'load_findings standard_arn={standard_arn}')


        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub/client/get_findings.html
        paginator = self.client.get_paginator('get_findings')

        findings = []
        filters = {
            'RecordState' : [{
                'Comparison': 'EQUALS',
                'Value': 'ACTIVE'

            }]
        }
        if standard_arn is not None:
            filters['ComplianceStandardsArn'] = [{
                'Comparison': 'EQUALS',
                'Value': standard_arn.split(':')[-1]
            }]

        for page in paginator.paginate(Filters = filters, MaxResults=100):
            print('.', end='', flush=True)
            findings.extend(page.get('Findings', []))
        print(' All finding loaded')


        df = pd.DataFrame(findings)

        df['StandardsArn'] = df['ProductFields'].apply(lambda x: x.get('StandardsArn', x.get('StandardsGuideArn',None)))
        df['ControlId'] = df['ProductFields'].apply(lambda x: x.get('ControlId', x.get('RuleId',None)))
        df['StandardsControlArn'] = df['ProductFields'].apply(lambda x: x.get('StandardsControlArn', None))

        df['Status'] = df['Compliance'].apply(lambda x: x.get('Status', None) if isinstance(x,dict) else x)
        df['SecurityControlId'] = df['Compliance'].apply(lambda x: x.get('SecurityControlId', None) if isinstance(x,dict) else None)
        df['SeverityL'] = df['Severity'].apply(lambda x: x.get('Label', None))
        df['SeverityN'] = df['Severity'].apply(lambda x: x.get('Normalized', None))
        df['SeverityN'] = pd.to_numeric(df['SeverityN'], errors='coerce')


        self.df_findings = df.sort_values(by=['SeverityN', 'Id'], ascending=[False, True])
        logger.info(f'df_findings: Number of standards found {len(self.df_findings.index)}')
        return self


    #*************************************************
    #
    #*************************************************
    def update_findings(self):
        """ Update Findings and Controls statistics"""

        self.load_findings()

        self.df_findings['passed'] = self.df_findings['Status'] == 'PASSED'


        # Update Controls with Findings
        df = self.df_findings[self.df_findings['ProductName'] == 'Security Hub']
        gb_std_ctrl = df.groupby(['StandardsControlArn'])
        df_std_ctrl = pd.DataFrame(index=gb_std_ctrl.groups.keys(),)
        df_std_ctrl['CheckCount'] = gb_std_ctrl['passed'].count()
        df_std_ctrl['CheckPass'] = gb_std_ctrl['passed'].sum()
        df_std_ctrl['CheckFail'] = df_std_ctrl['CheckCount'] - df_std_ctrl['CheckPass']

        for key, df in self.dfs_controls.items():

            # remove columns from df that in df_std_ctrl
            df = df.drop(columns=['CheckCount', 'CheckPass', 'CheckFail', 'ControlPass'], errors='ignore')

            df = df.join(df_std_ctrl, on='StandardsControlArn', how='left', lsuffix='_left', rsuffix='_right')
            df['CheckCount'] = df['CheckCount'].fillna(0)
            df['CheckPass'] = df['CheckPass'].fillna(0)
            df['CheckFail'] = df['CheckFail'].fillna(0)
            df['ControlNoData'] = df['CheckCount'] == 0
            df['ControlPassed'] = (df['CheckPass'] == df['CheckCount']) & (df['CheckCount'] > 0)
            df['ComplianceStatus'] = 'FAILED'
            df.loc[df['ControlPassed'], 'ComplianceStatus'] = 'PASSED'
            df.loc[df['ControlNoData'], 'ComplianceStatus'] = 'NO DATA'

            self.dfs_controls[key] = df

            self.df_standards.loc[key, 'ControlsPassed'] = df['ControlPassed'].sum()
            self.df_standards.loc[key, 'ControlsNoData'] = df['ControlNoData'].sum()

        # Update Standards with Controls
        self.df_standards['ControlsActive'] = self.df_standards['ControlsEnabled'] - self.df_standards['ControlsNoData']
        self.df_standards['ControlsFailed'] = self.df_standards['ControlsActive'] - self.df_standards['ControlsPassed']
        self.df_standards['Score'] = self.df_standards['ControlsPassed'] / self.df_standards['ControlsActive']
        self.df_standards['ScoreTxt'] = self.df_standards['Score'].apply(lambda x: f'{x * 100:.1f}%' if x is not None else '-')


    #*************************************************
    #
    #*************************************************
    def display_standard(self):
        """Display Security Hub"""

        # print(self.standard)
        print('')
        print(f'Name: {self.standard["Name"]}')
        print('')
        print(f'Status: {self.standard["StandardsStatus"]}')

        if self.standard["Score"] :
            print(f'Security Score: {self.standard["Score"] * 100:.1f}% ({self.standard["ControlsPassed"]} of {self.standard["ControlsActive"]} controls passed)')

        print('')

        if self.standard.name in self.dfs_controls.keys() :

            df = self.dfs_controls[self.standard.name]

            params = TableParam(
                columns = [
                    ColumnParam(title = 'id',          type = 'i',    min_width = 4  ),
                    ColumnParam(title = 'ControlId',  type = 'str',  data_col = 'ControlId'),
                    #ColumnParam(title = 'Title',     type = 'str',  data_col = 'Title'),
                    ColumnParam(title = 'Status',     type = 'str',  data_col = 'ComplianceStatus', format= 'aws-status'),
                    ColumnParam(title = 'Severity',     type = 'str',  data_col = 'SeverityRating'),
                    ColumnParam(title = 'Check Count',     type = 'int',  data_col = 'CheckCount'),
                    ColumnParam(title = 'Pass',     type = 'int',  data_col = 'CheckPass')

                ]
            )
            Table(params, df.to_dict(orient='records')).print()

        print()

    #*************************************************
    #
    #*************************************************
    def display_control(self):
        """Display Security Hub"""

        # print(self.control)
        print(f'Standard: {self.standard["Name"]}')
        print(f'Id: {self.control["ControlId"]}')
        print('')
        print(f'Title: {self.control["Title"]}')
        print(f'Severity: {self.control["SeverityRating"]}')
        print(f'Compliance Status: {self.control["ComplianceStatus"]}')
        print('')
        print('Description:')
        print(self.control["Description"])
        print('')
        print(f'RemediationUrl: {self.control["RemediationUrl"]}')
        print('')

        self.df_menu_findings = self.df_findings[self.df_findings['StandardsControlArn'] == self.control['StandardsControlArn']]

        params = TableParam(
            columns = [
                ColumnParam(title = 'id',          type = 'i',    min_width = 4  ),
                ColumnParam(title = 'Status',     type = 'str',  data_col = 'Status', format= 'aws-status'),
                ColumnParam(title = 'Account',  type = 'str',  data_col = 'AwsAccountId'),
                ColumnParam(title = 'Region',  type = 'str',  data_col = 'Region')
            ]
        )
        Table(params, self.df_menu_findings.to_dict(orient='records')).print()

        print()


    #*************************************************
    #
    #*************************************************
    def display_all_findings(self):
        """Display Security Hub"""

        print('')
        if self.df_findings is None:
            print('Findings are not loaded')
            print('Use "l" to load')
            print()
            return

        print('Top 100 Findings')
        params = TableParam(
            columns = [
                ColumnParam(title = 'id',          type = 'i',    min_width = 4  ),
                ColumnParam(title = 'Source',     type = 'str',  data_col = 'ProductName'),
                ColumnParam(title = 'Account',     type = 'str',  data_col = 'AwsAccountId'),
                ColumnParam(title = 'Severity',     type = 'str',  data_col = 'SeverityL'),
                ColumnParam(title = 'Title',     type = 'str',  data_col = 'Title'),
            ]
        )
        Table(params, self.df_findings[0:100].to_dict(orient='records')).print()

        print()

    #*************************************************
    #
    #*************************************************
    def display_finding(self):
        """Display A Finding"""

        print('')
        print(f'Source: {self.finding["ProductName"]}')
        print(f'Account / Region: {self.finding["AwsAccountId"]} / {self.finding["Region"]}')
        print(f'Type: {self.finding["Types"]}')
        print()
        print(f'Title: {self.finding["Title"]}')
        print()
        print(f'Description: {self.finding["Description"]}')
        print()
        print('Severity')
        pprint.pprint(self.finding['Severity'])
        print()
        print('Remediation')
        pprint.pprint(self.finding['Remediation'])
        print()
        print('Resources')
        pprint.pprint(self.finding['Resources'])
        print()
        print('Compliance')
        pprint.pprint(self.finding['Compliance'])


    #*************************************************
    #
    #*************************************************
    def display_overview(self):
        """Display Security Hub"""

        if len(self.dfs_controls.keys()) == 0:
            self.load_standard_controls()

        print('')
        print('Available Standards')
        params = TableParam(
            columns = [
                ColumnParam(title = 'id',          type = 'i',    min_width = 4  ),
                ColumnParam(title = 'Name',     type = 'str',  data_col = 'Name'),
                ColumnParam(title = 'Status',     type = 'str',  data_col = 'StandardsStatus'),
                ColumnParam(title = 'Controls',     type = 'int',  data_col = 'ControlsCount'),
                ColumnParam(title = 'Enabled',     type = 'int',  data_col = 'ControlsEnabled'),
                ColumnParam(title = 'Passed',     type = 'int',  data_col = 'ControlsPassed'),
                ColumnParam(title = 'Failed',     type = 'int',  data_col = 'ControlsFailed'),
                ColumnParam(title = 'No Data',     type = 'int',  data_col = 'ControlsNoData'),
                ColumnParam(title = 'Score',     type = 'str',  data_col = 'ScoreTxt')
            ]
        )
        Table(params, self.df_standards.to_dict(orient='records')).print()

        print('')
        print('Top 10 Findings')
        if self.df_findings is not None:
            params = TableParam(
                columns = [
                    ColumnParam(title = 'Source',    type = 'str',  data_col = 'ProductName'),
                    ColumnParam(title = 'Account',   type = 'str',  data_col = 'AwsAccountId'),
                    ColumnParam(title = 'Severity',  type = 'int',  data_col = 'SeverityN', alarm_hi = 70.0, warning_hi=40.0),
                    ColumnParam(title = 'Title',     type = 'str',  data_col = 'Title'),
                ]
            )
            Table(params, self.df_findings[0:10].to_dict(orient='records')).print()
        else:
            print('Findings not loaded. Use "l" to load')
        print()




    #*************************************************
    #
    #*************************************************
    def to_excel(self):
        """Save to Excel"""

        filename= f"aws-securityhub-{datetime.datetime.now().isoformat()[0:19].replace(':','-')}.xlsx"
        with pd.ExcelWriter(filename) as writer: # pylint: disable=abstract-class-instantiated

            df_parameters = pd.DataFrame([
                {'Parameter' : 'Date', 'Value' : datetime.datetime.now().isoformat()},
                {'Parameter' : 'Account', 'Value' : o7cli.sts.Sts(session=self.session).get_account_id()}
            ])
            df_parameters.to_excel(writer, sheet_name="Parameters")

            self.df_standards.to_excel(writer, sheet_name="Standards")

            for count, df in enumerate(self.dfs_controls.values()):
                df.to_excel(writer, sheet_name=f"Standard-{count}")

            if self.df_findings is not None:
                self.df_findings.to_excel(writer, sheet_name="Findings")



        print(f"Security Hub saved in file: {filename}")


    #*************************************************
    #
    #*************************************************
    def from_excel(self, filename):
        """Save to Excel"""

        print(f"Loading file: {filename}")
        self.df_standards = pd.read_excel(filename, sheet_name='Standards')
        self.df_findings = pd.read_excel(filename, sheet_name='Findings')


    #*************************************************
    #
    #*************************************************
    def generate_html_report(self):
        """Generate HTML Report"""

        print("Generating Security Hub HTML Report")

        if len(self.dfs_controls.keys()) == 0:
            self.load_standard_controls()

        self.update_findings()

        standards = self.df_standards[self.df_standards['StandardsStatus'] == 'READY']
        params = TableParam(
            columns = [
                ColumnParam(title = 'Name',     type = 'str',  data_col = 'Name'),
                ColumnParam(title = 'Controls',     type = 'int',  data_col = 'ControlsCount'),
                ColumnParam(title = 'Enabled',     type = 'int',  data_col = 'ControlsEnabled'),
                ColumnParam(title = 'Passed',     type = 'int',  data_col = 'ControlsPassed'),
                ColumnParam(title = 'Failed',     type = 'int',  data_col = 'ControlsFailed'),
                ColumnParam(title = 'No Data',     type = 'int',  data_col = 'ControlsNoData'),
                ColumnParam(title = 'Score',     type = 'str',  data_col = 'ScoreTxt')
            ]
        )
        compliance_html = Table(params, standards.to_dict(orient='records')).generate_html()

        params = TableParam(
            columns = [
                ColumnParam(title = 'Source',     type = 'str',  data_col = 'ProductName'),
                ColumnParam(title = 'Account',     type = 'str',  data_col = 'AwsAccountId'),
                ColumnParam(title = 'Severity',  type = 'int',  data_col = 'SeverityN', critical_hi=90, alarm_hi = 70.0, warning_hi=50.0),
                ColumnParam(title = 'Title',     type = 'str',  data_col = 'Title'),
            ]
        )
        findigs_html = Table(params, self.df_findings[0:25].to_dict(orient='records')).generate_html()
        Table(params, self.df_findings[0:10].to_dict(orient='records')).print()


        report = o7hr.HtmlReport(name='Security Hub')
        report.greeting = 'Bonjour la police'
        report.add_section(title=f'Account Id # {o7cli.sts.Sts(session=self.session).get_account_id()}', html="")
        report.add_section(title='Standards Compliance', html=compliance_html)
        report.add_section(title='Top 25 Findings', html=findigs_html)

        return report.generate()

    #*************************************************
    #
    #*************************************************
    def menu_finding(self, index):
        """Organization menu"""


        if  not 0 < index <= len(self.df_menu_findings.index):
            return self

        self.finding = self.df_menu_findings.iloc[index-1]

        obj = o7m.Menu(exit_option = 'b', title='Secutity Hub - Finding Details', title_extra=self.session_info(), compact=False)

        obj.add_option(o7m.Option(
            key='r',
            name='Raw',
            short='Raw',
            callback=lambda : print(self.finding)
        ))

        obj.display_callback = self.display_finding
        obj.loop()

        return self

    #*************************************************
    #
    #*************************************************
    def menu_all_finding(self):
        """Organization menu"""


        self.df_menu_findings = self.df_findings

        obj = o7m.Menu(exit_option = 'b', title='Secutity Hub - All Findings', title_extra=self.session_info(), compact=False)
        obj.add_option(o7m.Option(
            key='int',
            name='Details for a Finding',
            short='Details',
            callback=self.menu_finding
        ))

        obj.display_callback = self.display_all_findings
        obj.loop()

        return self

    #*************************************************
    #
    #*************************************************
    def menu_control(self, index):
        """Organization menu"""

        if self.standard.name not in self.dfs_controls.keys() :
            return self

        df_controls = self.dfs_controls[self.standard.name]

        if  not 0 < index <= len(df_controls.index):
            return self

        self.control = df_controls.iloc[index-1]

        obj = o7m.Menu(exit_option = 'b', title='Secutity Hub - Control Details', title_extra=self.session_info(), compact=False)

        obj.add_option(o7m.Option(
            key='int',
            name='Details for a Finding',
            short='Details',
            callback=self.menu_finding
        ))

        obj.display_callback = self.display_control
        obj.loop()

        return self

    #*************************************************
    #
    #*************************************************
    def menu_standard(self, index):
        """Organization menu"""

        if  not 0 < index <= len(self.df_standards.index):
            return self

        self.standard = self.df_standards.iloc[index-1]

        obj = o7m.Menu(exit_option = 'b', title='Secutity Hub - Standard Details', title_extra=self.session_info(), compact=False)

        obj.add_option(o7m.Option(
            key='int',
            name='Details for a Control',
            short='Details',
            callback=self.menu_control
        ))


        obj.display_callback = self.display_standard
        obj.loop()

        return self

    #*************************************************
    #
    #*************************************************
    def menu_overview(self):
        """Organization menu"""


        obj = o7m.Menu(exit_option = 'b', title='Secutity Hub Overview', title_extra=self.session_info(), compact=False)

        obj.add_option(o7m.Option(
            key='l',
            name='Load Findings',
            short='Load',
            callback=self.update_findings
        ))
        obj.add_option(o7m.Option(
            key='f',
            name='View All Findings',
            short='Findings',
            callback=self.menu_all_finding
        ))
        obj.add_option(o7m.Option(
            key='x',
            name='Save To Excel',
            short='To Excel',
            callback=self.to_excel
        ))
        obj.add_option(o7m.Option(
            key='int',
            name='Details for a Standard',
            short='Details',
            callback=self.menu_standard
        ))


        obj.display_callback = self.display_overview
        obj.loop()

        return self

#*************************************************
#
#*************************************************
def menu(**kwargs):
    """Run Main Menu"""
    SecurityHub(**kwargs).menu_overview()


#*************************************************
#
#*************************************************
if __name__ == "__main__":

    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', o7t.get_width())
    pd.set_option('display.max_colwidth',  20)

    logging.basicConfig(
        level=logging.INFO,
        format="[%(levelname)-5.5s] [%(name)s] %(message)s"
    )

    the_obj = SecurityHub()

    # the_obj.menu_overview()
    # the_obj.from_excel(filename='aws-securityhub-2023-10-28T13-23-28.xlsx')
    the_report = the_obj.generate_html_report()

    # print('*'*80)
    # print(the_report)
    # print('*'*80)

    # the_obj.to_excel()

    #--------------------------------
    # Save to File
    #--------------------------------
    filname = 'security_hub.cache.html'
    try:
        with open(filname, 'w', newline='', encoding='utf-8') as htmlfile:
            htmlfile.write(the_report)

    except IOError:
        print(f"Count not write to: {filname}")
