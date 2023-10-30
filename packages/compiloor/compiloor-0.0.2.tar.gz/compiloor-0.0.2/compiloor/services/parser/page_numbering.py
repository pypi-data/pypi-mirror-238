from fitz import (
    Document, Page, Rect, TEXT_ALIGN_CENTER,
    TEXT_ALIGN_RIGHT, PDF_REDACT_IMAGE_NONE, PDF_ENCRYPT_KEEP
)

from compiloor.services.typings.utils import PAGE_NUMBER_FONT_SIZE, PRIMARY_COLOR_IN_PERCENTAGES


class PageNumberingUtils:
    """
        A class containing methods for adding page numbers and finding legend to a report.
    """

    # TODO: Rewrite this method with more elegant code.    
    @staticmethod
    def create_report_with_page_numbers_and_legend(report_path: str, report_section_headings: list[str]) -> None:
        """
            Creates a new report with page numbers and a legend for the findings.
        """
    
        new_pdf = Document(report_path) # Using fitz to edit the PDF.
            
        pages_to_delete: list[int] = []
        
        page: Page    
        
        page_to_section_index: dict[str, int] = {}
        page_to_section_index_occurences: dict[str, int] = {}
        
        for page in new_pdf.pages():
            if page.get_textpage().extractText() == "": 
                pages_to_delete.append(page.number) 
                continue
            page.clean_contents()
            
        if len(pages_to_delete): new_pdf.delete_pages(pages_to_delete) # Deleting empty pages.
            
        # Normalizing the page orientations:    
        for page in new_pdf.pages():
            if page.number == 0: continue         
            x1, y1 = page.cropbox.x1, page.cropbox.y1

            page.clean_contents()
            
            # Insert page numbers on each page:
            page.insert_textbox(
                # The whole width of the page for the last 18th of the page vertically:
                Rect(0, y1 - y1 / 18, x1, y1),
                str(page.number),
                align = TEXT_ALIGN_CENTER,
                fontsize = PAGE_NUMBER_FONT_SIZE,
                color = PRIMARY_COLOR_IN_PERCENTAGES
            )
            
            for section_index in range(len(report_section_headings)):
                heading = report_section_headings[section_index]
                
                if not heading in page.get_textpage().extractText(): continue
                
                if heading in page_to_section_index: continue
                
                if not heading in page_to_section_index_occurences: page_to_section_index_occurences[heading] = 0
                
                page_to_section_index_occurences[heading] += 1
                
                if page_to_section_index_occurences[heading] != 2: continue
                page_to_section_index[heading] = page.number

        for section in page_to_section_index.keys():

            for page in new_pdf.pages():

                section_index = section.split(" ")[0]

                section_index = section_index if not "." in section_index else section_index[:-1]

                fragment = page.search_for('{{section_' + section_index + '_page}}')
                
                if not fragment: continue

                page.add_redact_annot(
                    fragment[0],
                    str(page_to_section_index[section]),
                    cross_out=False,
                    align=TEXT_ALIGN_RIGHT,
                    fontsize = PAGE_NUMBER_FONT_SIZE,
                    text_color = PRIMARY_COLOR_IN_PERCENTAGES
                )
                page.apply_redactions(images=PDF_REDACT_IMAGE_NONE)
                break
            
        new_pdf.save(report_path, incremental=True, encryption=PDF_ENCRYPT_KEEP)