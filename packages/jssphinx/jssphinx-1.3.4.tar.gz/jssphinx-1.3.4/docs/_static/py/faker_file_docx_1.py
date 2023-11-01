import os

# Required imports
from faker import Faker
from faker_file.providers.docx_file import DocxFileProvider

FAKER = Faker()  # Initialize Faker
FAKER.add_provider(DocxFileProvider)  # Register DocxFileProvider

# Generate DOCX file
docx_file = FAKER.docx_file()

# Test things out
print(docx_file)
print(docx_file.data["filename"])
assert os.path.exists(docx_file.data["filename"])
