from textractor import Textractor

extractor = Textractor(profile_name="default")
# file_source can be an image, list of images, bytes or S3 path
document = extractor.detect_document_text(file_source=r"C:\Users\Siddhesh Ashtekar\Downloads\image,pdf\educational.jpg")
print(document.lines)
from textractor.data.constants import TextractFeatures

document = extractor.analyze_document(
	file_source=r"C:\Users\Siddhesh Ashtekar\Downloads\image,pdf\educational.jpg",
	features=[TextractFeatures.TABLES]
)
# Saves the table in an excel document for further processing
document.tables[0].to_excel("output.xlsx")
document = extractor.analyze_expense(file_source=r"C:\Users\Siddhesh Ashtekar\Downloads\image,pdf\educational.jpg")
print(document.expense_documents[0].summary_fields.get("TOTAL")[0].text)
