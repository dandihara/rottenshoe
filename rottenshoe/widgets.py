from django import forms

class PreviewFileWidget(forms.ClearableFileInput):
    tmeplate_name = 'board.html'

    class Media:
        js = [
            "//code.jquery.com/jquery-3.4.1.min.js",
        ]