import pandas as pd
from django.shortcuts import render
from .models import UploadedFile
from .forms import UploadFileForm


def file_list(request):
    files = UploadedFile.objects.all()
    return render(request, "files/file_list.html", {"files": files})


def file_detail(request, file_id):
    file_obj = UploadedFile.objects.get(id=file_id)
    file_path = file_obj.file.path

    try:
        if file_path.endswith(".sas7bdat"):
            df = pd.read_sas(file_path, format="sas7bdat")
            df = df.apply(lambda col: col.map(lambda x: x.decode('utf-8') if isinstance(x, bytes) else x) if col.dtype == 'object' else col)
        elif file_path.endswith(".xpt"):
            df = pd.read_sas(file_path, format="xport")
            df = df.apply(lambda col: col.map(lambda x: x.decode() if isinstance(x, bytes) else x) if col.dtype == 'object' else col, axis=0)
        elif file_path.endswith(".csv"):
            df = pd.read_csv(file_path, sep="$")
        elif file_path.endswith(".xlsx"):
            df = pd.read_excel(file_path)
        else:
            return render(request, "files/error.html", {"message": "Unsupported file format"})

        # Перетворюємо таблицю на HTML для перегляду
        data_html = df.head(100).to_html(classes="table table-bordered")

    except Exception as e:
        data_html = f"<p>Error: {e}</p>"

    return render(request, "files/file_detail.html", {"file": file_obj, "table": data_html})


def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'files/upload_success.html')
    else:
        form = UploadFileForm()
    return render(request, 'files/upload_file.html', {'form': form})

