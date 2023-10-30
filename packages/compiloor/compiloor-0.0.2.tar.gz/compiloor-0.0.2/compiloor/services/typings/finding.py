from enum import Enum

FINDING_LIST_TABLE_COLUMNS = ["ID", "Title", "Severity"]

class Severity(Enum):
    """
        Enum class for severity levels.
    """
    
    GAS = 1
    QA = 2
    LOW = 3
    MEDIUM = 4
    HIGH = 5
    CRITICAL = 6
    
    def __str__(self) -> str:
        return str(self.value)
    
    def __repr__(self) -> str:
        return str(self)
    
    def cast_to_folder_sig(self: "Severity") -> "SeverityFolderIndex":
        mapping = {
            Severity.GAS: SeverityFolderIndex.GAS,
            Severity.QA: SeverityFolderIndex.QA,
            Severity.LOW: SeverityFolderIndex.LOW,
            Severity.MEDIUM: SeverityFolderIndex.MEDIUM,
            Severity.HIGH: SeverityFolderIndex.HIGH,
            Severity.CRITICAL: SeverityFolderIndex.CRITICAL,
        }
        return mapping[self]
    
    def cast_to_display_case(self: "Severity") -> str:
        mapping = {
            Severity.GAS: "GAS",
            Severity.QA: "QA",
            Severity.LOW: "Low",
            Severity.MEDIUM: "Medium",
            Severity.HIGH: "High",
            Severity.CRITICAL: "Critical",
        }
        return mapping[self]
    
class SeverityAnnotation(Enum):
    """Annotation class for severity levels."""
    GAS = "gas"
    QA = "QA"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    
    def cast_to_severity(self: "SeverityAnnotation") -> Severity:
        mapping = {
            SeverityAnnotation.GAS: Severity.GAS,
            SeverityAnnotation.QA: Severity.QA,
            SeverityAnnotation.LOW: Severity.LOW,
            SeverityAnnotation.MEDIUM: Severity.MEDIUM,
            SeverityAnnotation.HIGH: Severity.HIGH,
            SeverityAnnotation.CRITICAL: Severity.CRITICAL,
        }
        return mapping[self]
    
class SeverityFolderIndex(Enum):
    """Enum class for severity levels."""
    GAS = "GAS"
    QA = "QA"
    LOW = "L"
    MEDIUM = "M"
    HIGH = "H"
    CRITICAL = "C"
    
    def cast_to_severity(self: "SeverityFolderIndex") -> Severity:
        mapping = {
            SeverityFolderIndex.GAS: Severity.GAS,
            SeverityFolderIndex.QA: Severity.QA,
            SeverityFolderIndex.LOW: Severity.LOW,
            SeverityFolderIndex.MEDIUM: Severity.MEDIUM,
            SeverityFolderIndex.HIGH: Severity.HIGH,
            SeverityFolderIndex.CRITICAL: Severity.CRITICAL,
        }
        return mapping[self]