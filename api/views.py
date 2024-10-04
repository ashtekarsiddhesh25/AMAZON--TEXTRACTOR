from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from textractor import Textractor
from textractor.data.constants import TextractFeatures
import os

class TextractAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        # Handle uploaded file
        uploaded_file = request.FILES.get('file')
        if not uploaded_file:
            return Response({"error": "No file provided."}, status=status.HTTP_400_BAD_REQUEST)

        # Save the uploaded file temporarily
        file_path = f"temp_{uploaded_file.name}"
        with open(file_path, 'wb+') as temp_file:
            for chunk in uploaded_file.chunks():
                temp_file.write(chunk)

        # Initialize Textractor
        extractor = Textractor(profile_name="default")

        try:
            # Detect document text
            document = extractor.detect_document_text(file_source=file_path)

            # Analyze tables with save_image=False to skip image generation
            analyzed_document = extractor.analyze_document(
                file_source=file_path,
                features=[TextractFeatures.TABLES],
                save_image=False  # Disable image generation
            )

            # Analyze expenses
            expense_document = extractor.analyze_expense(file_source=file_path)
            total_amount = expense_document.expense_documents[0].summary_fields.get("TOTAL")[0].text

            # Save the table to Excel
            output_excel_path = "output.xlsx"
            analyzed_document.tables[0].to_excel(output_excel_path)

            # Delete temporary file
            os.remove(file_path)

            # Response data
            return Response({
                "lines": [line.text for line in document.lines],
                "total_amount": total_amount,
                "excel_file_path": output_excel_path
            }, status=status.HTTP_200_OK)

        except Exception as e:
            # Ensure file gets removed in case of an error
            if os.path.exists(file_path):
                os.remove(file_path)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
