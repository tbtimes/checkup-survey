from django.contrib import admin
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.utils.html import mark_safe
from django.template import Template, Context
from django.utils.encoding import smart_text

from checkup.models import Reporter, Survey, Group, Title, Respondent
from checkup.models import Question, Choice, QuestionGroup, QuestionGroupOrder
from checkup.models import Assignment, Answer, Contribution, Comment, FormRequest
from checkup.models import ContributionType


class QuestionGroupOrderInline(admin.TabularInline):
	model = QuestionGroupOrder
	verbose_name = 'Question group'
	verbose_name_plural = 'Questions'
	sortable_field_name = 'order'
	extra = 1
	
class QuestionGroupAdmin(admin.ModelAdmin):
	inlines = (QuestionGroupOrderInline,)
	
class QuestionAdmin(admin.ModelAdmin):
	filter_horizontal = ('choices',)
	list_display = ('question', 'explanation')

class AssignmentAdmin(admin.ModelAdmin):
	# change_list_template = 'admin/change_list_filter_sidebar.html'

	change_list_filter_template = 'admin/filter_listing.html'
	list_display = ('respondent', 'download_answers', 'respondent_link', 'phone', 'email', 'contacted', 'visits',
		'receipt_confirmed', 'survey_complete', 'confirmation_sent', 'reporter', 'form_url', )
	list_filter = ('survey', 'reporter', 'contacted', 'receipt_confirmed', 
		'survey_complete', 'confirmation_sent')
	readonly_fields = ('form_url', 'respondent_link', 'display_url', 'survey_complete', 
		'visits', 'phone', 'email',)
	list_editable = ('contacted', 'receipt_confirmed', 
		'confirmation_sent', 'reporter')
	templateString = u"{% for a in answers %}\n{{ forloop.counter }}. {{a.question.question.question}}\n{% if a.choice %} {{a.choice}} &mdash; {% endif %}{{ a.freetext }}\n{% endfor %}"
	answersTemplate = Template(templateString)

	class Media:
		js = ('checkup/js/download_answers.js',)

	def download_answers(self, instance):
		context = { "answers": [] }
		for answer in instance.answers.all():
			obj = { "freetext": answer.freetext }
			if answer.answer_id:
				obj["choice"] = Choice.objects.get(id=answer.answer_id).choice
			context["answers"].append(obj)
		return mark_safe(u'<a href="#">Download</a><div class="answerset" style="display: none;">{}</div>'.format(self.answersTemplate.render(Context(context))))

	def form_url(self, instance):
		form_url = None
		if instance.form_slug:
			form_url = 'http://' + Site.objects.get_current().domain
			form_url += '/checkup/forms/' + instance.form_slug + '/'
		return form_url

	def display_url(self, instance):
		display_url = None
		if instance.display_slug:
			display_url = 'http://' + Site.objects.get_current().domain
			display_url += '/checkup/' + instance.survey.home_slug + '/' + instance.display_slug + '/'
		return display_url
	
	def visits(self, instance):
		visits = 0
		if FormRequest.objects.filter(assignment=instance).exists():
			visits = FormRequest.objects.filter(assignment=instance).count()
		return visits
	
	def phone(self, instance):
		phone = ''
		if instance.respondent.contact_phone:
			phone = instance.respondent.contact_phone
		else:
			phone = instance.respondent.office_phone
		return phone
			
	def email(self, instance):
		email = ''
		if instance.respondent.contact_email:
			email = instance.respondent.contact_email
		else:
			email = instance.respondent.email
		return email
	
	def respondent_link(self, instance):
		return '<a href="%s" target="_blank">Modify respondent</a>' % (
			reverse('admin:checkup_respondent_change', args=(instance.respondent.id,)))
	
	respondent_link.allow_tags = True
	respondent_link.short_description = 'Respondent'
	form_url.short_description = 'Web address of this assignment\'s form'

	
class RespondentAdmin(admin.ModelAdmin):
	fieldsets = (
		(None, {
			'fields': ('group', 'headshot')
		}),
		('How to print their name...', {
			'fields': ('title', 'party', 'district', 'gender', 'first_name', 'last_name')
		}),
		('How to contact them for this survey...', {
			'fields': ('contact_name', 'contact_phone', 'contact_email')
		}),
		('How the public should contact them...', {
			'fields': ('website', 'office_phone', 'email', 'twitter', 'address', 'address2', 
						'city', 'state', 'zip')
		}),
	)
	
	list_display = ('first_name', 'last_name', 'office_phone', 'email', 
		'contact_name', 'contact_phone', 'contact_email',)


class SurveyAdmin(admin.ModelAdmin):
	list_display = ('name', 'home_url', 'form_chatter', 'display_chatter',)
	prepopulated_fields = {'home_slug': ('name',)}
	readonly_fields = ('home_url',)
	
	def home_url(self, instance):
		home_url = None
		if instance.home_slug:
			home_url = 'http://' + Site.objects.get_current().domain
			home_url += '/checkup/' + instance.home_slug + '/'
		return home_url
        
class ContributionAdmin(admin.ModelAdmin):
	list_display = ('assignment', 'contrib_count', 'years', 'amount',)
	
	
admin.site.register(Reporter)
admin.site.register(Survey, SurveyAdmin)
admin.site.register(Respondent, RespondentAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionGroup, QuestionGroupAdmin)
admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(Contribution, ContributionAdmin)

admin.site.register(Group)
admin.site.register(FormRequest)
admin.site.register(Title)
admin.site.register(Choice)
admin.site.register(Answer)
admin.site.register(Comment)
admin.site.register(ContributionType)
