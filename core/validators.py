from django.core.exceptions import ValidationError

def validate_video_size(value):
    filesize = value.size
    limit_mb = 20
    if filesize > limit_mb * 1024 * 1024:
        raise ValidationError(f"Max video size is {limit_mb}MB")
