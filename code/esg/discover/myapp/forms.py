from django import forms


class ExcelUploadForm(forms.Form):
    file = forms.FileField(label="上傳 Excel 檔案")
