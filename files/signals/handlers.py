from django.dispatch import receiver
from django.db.models.signals import pre_save
from files.models import File, Log


@receiver(pre_save, sender=File, weak=False)
def product_handler(**kwargs):
    file:File = kwargs['instance']
    
    old_file = File.objects.filter(id=file.id).first()

    if old_file is not None:
        if file.editor is not None:
            user = file.editor
            action = Log.ACTION_CHECK_IN

        elif old_file.editor is not None:
            user = old_file.editor
            action = Log.ACTION_CHECK_OUT

        else:
            return
        
        Log.objects.create(user=user, file=file, action=action)
