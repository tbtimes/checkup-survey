from django import forms
from django.contrib.auth.models import User


class SurveyForm(forms.Form):
		
	def __init__(self, *args, **kwargs):
		assignment = kwargs.pop('assignment')
		super(SurveyForm, self).__init__(*args, **kwargs)
		
		questions = assignment.questions.questions.all().order_by('questiongrouporder__order')
		
		for question in questions:
			if question.choices.count():
				choices = []
				for choice in question.choices.all():
					choices.append((choice.id, choice.choice))

				self.fields['question-%s' % question.id] = forms.ChoiceField(
					widget=forms.RadioSelect(), 
					required=False,
					choices=choices, label=question.question,
					help_text=question.explanation)
				
				self.fields['question-%s' % question.id].question_id = question.id

			if question.freetext:
				self.fields['question-%s-freetext' % question.id] = forms.CharField(max_length=30000, required=False,
				label="Explanation" if question.choices.count() else question.question,
				widget=forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}))

				self.fields['question-%s-freetext' % question.id].question_id = question.id
				print(self.fields['question-%s-freetext' % question.id])
		
		# self.fields['comment'] = forms.CharField(max_length=30000, required=False,
				# widget=forms.Textarea(attrs={'rows': 11, 'class': 'form-control'}))
				
		authorized_label = 'I am ' + ' ' + assignment.respondent.title.short if assignment.respondent.title else ""
		authorized_label += ' ' + assignment.respondent.first_name
		authorized_label += ' ' + assignment.respondent.last_name + ' or someone authorized to '
		authorized_label += 'submit this form on their behalf. I understand that my access to '
		authorized_label += 'this form has been logged for security purposes.'
	
		self.fields['authorized'] = forms.BooleanField(label=authorized_label)