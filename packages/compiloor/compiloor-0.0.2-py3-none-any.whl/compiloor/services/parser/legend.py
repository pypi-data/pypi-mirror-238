from compiloor.services.parser.finding import Finding
from compiloor.services.typings.finding import Severity


class ReportLegendUtils:
    """
        A class that contains utility methods for creating the report legend.
    """
    
    @staticmethod
    def create_finding_severities_legend(findings_section_index: str, findings: list[Finding]) -> str:
        # The bellow code can only work with strings so we are casting the findings_section_index to a string here:
        if not isinstance(findings_section_index, str):
            findings_section_index = str(findings_section_index) 

        fragments = []
        current_severity, current_severity_index, current_severity_finding_index = None, 0, 0

        for finding in findings:
            if finding.severity != current_severity:
                
                current_severity = finding.severity
                current_severity_index += 1
                current_severity_finding_index = 0
                section_index = f'section_{findings_section_index}.{current_severity_index}_page'

                if current_severity_index != 1: fragments.append("</div>")

                fragments.extend([
                    f'''
                    <a href="#section-{findings_section_index}-{current_severity_index}">
                        <div class="section-wrapper">
                            <h3>
                                {findings_section_index}.{current_severity_index}. {current_severity.cast_to_display_case()} Findings
                            </h3>
                            <p>{{{{{section_index}}}}}</p>
                        </div>
                    </a>
                    ''',
                    '<div class="sub-sub-paragraph">'
                ])

            current_severity_finding_index += 1
            section_index = f'section_[{finding.id}]_page'

            fragments.append(
                f'''
                <a href="#section-{findings_section_index}-{current_severity_index}-{current_severity_finding_index}">
                    <div class="section-wrapper">
                        <h3>
                            [{finding.id}] {finding.title}
                        </h3>
                        <p>{{{{{section_index}}}}}</p>
                    </div>
                </a>
                '''
            )

        return "".join(fragments)
    
    # THE OLD FUNCTION:
    # KEEPING IT HERE FOR REFERENCE.
    # @staticmethod
    # def create_finding_severities_legend(findings_section_index: str, findings: list[Finding]) -> str:
    #     """
    #         Creates a legend for the report's findings.
    #     """
    #     if type(findings_section_index) != str: findings_section_index = str(findings_section_index)
        
    #     current_severity: Severity = None
    #     current_severity_index: int = 0
    #     current_severity_finding_index: int = 0
        
    #     fragments: list[str] = []
        
    #     for finding in findings:
            
    #         if finding.severity != current_severity:
            
    #             current_severity = finding.severity
    #             current_severity_index += 1
    #             current_severity_finding_index = 0
    #             section_index = f'section_{findings_section_index}.{current_severity_index}_page'
                
    #             if current_severity_index != 1: fragments.append("</div>")
                
    #             fragments.append(
    #                 f'''
    #                 <a href="#section-{findings_section_index}-{current_severity_index}">
    #                     <div class="section-wrapper">
    #                         <h3>
    #                             {findings_section_index}.{current_severity_index}. {current_severity.cast_to_display_case()} Findings
    #                         </h3>
    #                         <p>{{{{{section_index}}}}}</p>
    #                     </div>
    #                 </a>
    #                 '''
    #             )
                
    #             fragments.append('<div class="sub-sub-paragraph">')
            
    #         current_severity_finding_index += 1
            
    #         section_index = f'section_[{finding.id}]_page'
            
    #         fragments.append(
    #             f'''
    #                 <a href="#section-{findings_section_index}-{current_severity_index}-{current_severity_finding_index}">
    #                     <div class="section-wrapper">
    #                         <h3>
    #                             [{finding.id}] {finding.title}
    #                         </h3>
    #                         <p>{{{{{section_index}}}}}</p>
    #                     </div>
    #                 </a>         
    #             '''
    #         )
            
    #     return "".join(fragments)