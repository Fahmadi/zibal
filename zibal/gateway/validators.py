from django.core.exceptions import ValidationError

def validate_image(image):
    file_size = image.file.size
    limit_kb = 50
    if file_size > limit_kb :
        raise ValidationError("Max size of file is %s KB" % limit_kb)

def validate_file_extension(value):
    if value.file.content_type != 'application/pdf':
        raise ValidationError(u'Error message about extension of file')
