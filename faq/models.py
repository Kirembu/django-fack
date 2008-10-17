from django.db import models
from datetime import datetime
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from managers import QuestionManager
import enums

class FaqBase(models.Model):
    '''
    Base class for models.
    
    '''
    created_by = models.ForeignKey(User, null=True, editable=False, related_name="%(class)s_created_by" )    
    created_on = models.DateTimeField( _('created on'), default=datetime.now, editable=False,  )
    updated_on = models.DateTimeField( _('updated on'), editable=False )
    updated_by = models.ForeignKey(User, null=True, editable=False )  
    
    class Meta:
        abstract = True

class Question(FaqBase):
    """
    Represents a frequently asked question.

    """

    slug = models.SlugField( max_length=100, help_text="This is a unique identifier that allows your questions to display its detail view, ex 'how-can-i-contribute'", )
    text = models.TextField(_('question'), help_text='The actual question itself.')
    answer = models.TextField( _('answer'), help_text='The answer text.' )    
    status = models.IntegerField( choices=enums.QUESTION_STATUS_CHOICES, default=enums.STATUS_INACTIVE, help_text="Only questions with their status set to 'Active' will be displayed. " )
    order = models.IntegerField(_('order'), help_text='The order you would like the question to be displayed.')
    
    objects = QuestionManager()
    
    class Meta:
        ordering = ['order',]

    def __unicode__(self):
        return self.text

    def save(self):
        self.updated_on = datetime.now()
        super(Question, self).save()
    