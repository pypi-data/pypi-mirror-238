
from typing import Tuple

from inspect import getmembers, ismethod

from compiloor.services.parser.legend import ReportLegendUtils
from compiloor.services.typings.config import ProtocolInformationConfigDict
from compiloor.services.typings.finding import Severity
from compiloor.services.typings.utils import MAIN_REPORT_SECTIONS
from compiloor.services.parser.finding import Finding
from compiloor.services.typings.report import INFORMATION_TABLE_VARIABLES, REPORT_SECTION_HEADINGS
from compiloor.services.parser.table import TableUtils
from compiloor.services.environment.utils import FileUtils, FindingUtils
from compiloor.services.utils.config import ConfigUtils


class ReportCustomizer:
    """
        A class that assembles the core report. 
    """
    
    # Report configuration variables:
    config: ProtocolInformationConfigDict
    
    # Report template variables:
    report: str # The report template.
    stylesheet: str # The CSS stylesheet.
    
    # Finding report variables:
    total_findings_amount: int # The total amount of findings.
    finding_amounts_by_severity: dict[Severity, int] # The amount of findings per each severity.
    findings: str # The finding fragments in HTML format.
    serialized_findings: list[Finding] # The serialized findings in Finding object format.
    report_section_headings: list[str] # The report section headings.
    
    def __init__(self) -> str:
        # Gets the report configuration:
        self.config = FileUtils.read_config(json=True)

        # Gets the stylesheet and report template fragment:         
        self.report = FileUtils.read_file(self.config["template_url"], is_url=True)
        self.stylesheet = FileUtils.read_file(self.config["stylesheet_url"], is_url=True, html_tag="style")
        
        # Gets the finding fragments:
        (
            self.total_findings_amount,
            self.finding_amounts_by_severity,
            self.findings,
            self.serialized_findings,
            self.report_section_headings
        ) = FindingReportUtils.get_finding_fragments(6) # 6 is the hardcoded index of the findings section: Will be changed in a future update.
        
        return self.assemble_report() # Assembles the report.
    
    def add_report_config_variables(self) -> None:
        for key in self.config.keys():
            # '{{config.<key>}}' syntax is very confusing when 
            self.report = self.report.replace(f"{{{{config.{key}}}}}", str(self.config[key]))

    def add_information_table_variables_to_report(self, tag: str = "b") -> None:
        """
            Bolds the information table row headings in the report.
        """
        
        for _key in INFORMATION_TABLE_VARIABLES.keys():
            self.report = self.report.replace(
                _key,
                f'<{tag}>{INFORMATION_TABLE_VARIABLES[_key]}</{tag}>'
            )

    def add_dynamic_tables_to_report(self) -> None:
        # Defines the table type -> callable arguments mapping:
        kwargs: dict[str, list[any]] = {
            "severity_classification_table": [],
            "information_table": [self.config],
            "findings_count_table": [self.finding_amounts_by_severity, self.total_findings_amount],
            "findings_summary_table": [self.serialized_findings],
        }
        
        # Maps the table type -> table creation callable:
        table_types = TableUtils.fragment_to_callable()
        
        # Adding the tables to the report:
        for name in table_types.keys():
            callable, args = table_types[name], kwargs[name]
            self.report = self.report.replace(f'{{{{{name}}}}}', callable(*args))
        
        # Adding no-wrap so that the table look doesn't break:
        # TODO: Change with a modular CSS stylesheet.
        self.report = self.report.replace("<td>[", '<td class="no-wrap-column">[')
        
    def add_report_legend(self) -> None:
        # Adding the legend manually:
        self.report = self.report.replace(
            '{{report_legend}}',
            # 6 is the hardcoded index of the findings section: Will be changed in a future update.
            ReportLegendUtils.create_finding_severities_legend(6, self.serialized_findings)
        )
        
    def assemble_report(self) -> str:
        # Adds the main parts of the report to the fragment:
        # I.E. The stylesheet, the findings, the total findings amount.
                
        section_to_attribute: dict[str, any] = {}
        for section in MAIN_REPORT_SECTIONS:
            section_to_attribute[str(section)] = getattr(self, section)
        
        for part in section_to_attribute.keys():
            self.report = self.report.replace(f"{{{{{part}}}}}", str(section_to_attribute[part]))
        
        # Getting all of the class's methods and calling all with the 'get_' prefix:
        for method in getmembers(self, predicate=lambda x: ismethod(x)):

            if not method[0].startswith("add_"): continue
            # Calling the method:
            method[1]()
        
        self.add_report_legend()
    
class FindingReportUtils:
    """
        A class containing utilities for creating the finding report.
    """
    # OLD VERSION OF THE FUNCTION:
    
    # @staticmethod
    # def get_finding_fragments(
    #     findings_section_index: str,
    #     paragraph_subheading_tag: str = "h2"
    # ) -> Tuple[int, dict[Severity, int], str, list[Finding]]:
    #     """
    #         Gets the finding fragments from the findings directory and serializes them into different formats intended for different use.
            
    #         Returns a tuple of:
    #         - The total amount of findings.
    #         - The amount of findings per severity.
    #         - The finding fragments.
    #         - The finding summary table.
    #         - The serialized findings.
    #     """
        
    #     if type(findings_section_index) != str: findings_section_index = str(findings_section_index)
        
    #     (
    #         total_findings_amount, finding_amounts_by_severity, findings
    #     ) = FindingUtils.get_finding_fragments()
    
    #     finding_markdowns: list[str] = []
    #     _finding_fragments: list[str] = []
        
    #     __finding_fragments = findings.copy()
        
    #     for severity in __finding_fragments:
    #         if not __finding_fragments[severity]: del findings[severity]
            
    #     report_section_headings = REPORT_SECTION_HEADINGS.copy()
            
    #     for severity in findings:
            
    #         __finding_fragments = findings[severity]
    #         __finding_fragments.reverse()
    #         _finding_fragments += __finding_fragments
        
    #     _finding_fragments.reverse()
        
    #     serialized_findings: list[Finding] = [Finding(finding) for finding in _finding_fragments]
        
    #     severity_index: int = 0
    #     current_severity: Severity = None

    #     serialized_full_findings_by_severity: dict[Severity, list[Finding]] = {}
        
    #     for severity in Severity:
    #         if not severity in findings: continue
    #         serialized_full_findings_by_severity[severity] = [
    #             Finding(finding).full_fragment for finding in findings[severity]
    #         ]

    #     for finding in serialized_findings:
            
    #         severity_display = finding.severity.cast_to_display_case()
            
    #         report_section_headings.append(f"[{finding.id}] {finding.title}")
    #         if finding.severity == current_severity: continue
            
    #         current_severity = finding.severity
    #         severity_index += 1
            
    #         report_section_headings.append(f"{findings_section_index}.{severity_index}. {severity_display} Findings")

    #         serialized_full_findings_by_severity[finding.severity].reverse()
    #         finding_html_fragments = "\n".join(serialized_full_findings_by_severity[finding.severity])
    #         finding_markdowns.append(
    #             f'''<div id="section-{findings_section_index}-{severity_index}" class="page-break-after">
    #                     <{paragraph_subheading_tag} class="paragraph-subheading">
    #                         {findings_section_index}.{severity_index}. {severity_display} Findings
    #                     </{paragraph_subheading_tag}>
    #                     <div class="findings">
    #                         {finding_html_fragments}
    #                     </div>
    #                 </div>
    #             '''
    #         )        
            
    #         finding_markdowns_len = len(finding_markdowns) - 1
            
    #         finding_markdowns[finding_markdowns_len] = finding_markdowns[finding_markdowns_len].replace(
    #             f'[[{finding.severity.value}_severity_index]]',
    #             str(severity_index)
    #         )

    #     _finding_fragments.reverse()
                
    #     return (
    #         total_findings_amount, finding_amounts_by_severity, "\n".join(finding_markdowns),
    #         serialized_findings, report_section_headings
    #     )


    # NEW VERSION OF THE FUNCTION:
    @staticmethod
    def get_finding_fragments(findings_section_index: str, paragraph_subheading_tag: str = "h2") -> Tuple[int, dict[Severity, int], str, list[Finding]]:
        total_amount, amounts_by_severity, findings = FindingUtils.get_finding_fragments()

        # Remove empty severity levels
        _findings = {}

        for severity, fragments in findings.items():
            if fragments:
                _findings[severity] = fragments

        # Copy the non-empty severity levels
        findings = _findings

        markdowns, _finding_fragments = [], []

        # Copying the static headings present in the report template:
        section_headings = REPORT_SECTION_HEADINGS.copy()

        # Sort severity levels from high to low
        for severity in reversed(list(findings.keys())):
            _finding_fragments.extend(findings[severity])

        serialized = [Finding(finding) for finding in _finding_fragments]

        full_by_severity = {}
        current_severity, severity_index = None, 0

        # Iterate through severity levels from high to low
        for severity in reversed(list(Severity)):
            if not severity in findings: continue # Skip empty severity levels
            
            full_by_severity[severity] = [Finding(finding).full_fragment for finding in findings[severity]]

        for finding in serialized:
            severity_display = finding.severity.cast_to_display_case()
            section_headings.append(f"[{finding.id}] {finding.title}")

            if finding.severity == current_severity: continue # Skip if the severity level is the same as the previous one

            severity_index += 1
            current_severity = finding.severity

            # Adding the severity level heading to the section headings:
            section_headings.append(f"{findings_section_index}.{severity_index}. {severity_display} Findings")

            # Get the HTML fragments in the correct order for the current severity:
            html_fragments = "\n".join(full_by_severity[finding.severity])

            # TODO: Can this be done in a more elegant way?
            markdowns.append(
                f'''
                    <div id="section-{findings_section_index}-{severity_index}" class="page-break-after">
                        <{paragraph_subheading_tag} class="paragraph-subheading">
                            {findings_section_index}.{severity_index}. {severity_display} Findings
                        </{paragraph_subheading_tag}>
                        <div class="findings">
                            {html_fragments}
                        </div>
                    </div>
                '''
            )

            # Adding the link to the heading:
            markdowns[-1] = markdowns[-1].replace(f'[[{finding.severity.value}_severity_index]]', str(severity_index))

        return total_amount, amounts_by_severity, "\n".join(markdowns), serialized, section_headings