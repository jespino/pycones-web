
from django.contrib import admin
from pycones.proposals.models import TalkProposal, TutorialProposal, PosterProposal

admin.site.register(TalkProposal)
admin.site.register(TutorialProposal)
admin.site.register(PosterProposal)
