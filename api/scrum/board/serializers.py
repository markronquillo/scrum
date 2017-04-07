from rest_framework import serializers
from rest_framework.reverse import reverse

from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from .models import Sprint, Task

from datetime import date


User = get_user_model()


class SprintSerializer(serializers.ModelSerializer):

	links = serializers.SerializerMethodField()

	class Meta:
		model = Sprint
		fields = ('id', 'name', 'description', 'end', 'links', )

	def get_links(self, obj):
		request = self.context['request']
		return {
			'self': reverse('sprint-detail',
				kwargs={'pk': obj.pk}, request=request),
			'tasks': reverse('task-list',
				request=request) + '?sprint={}'.format(obj.pk)
		}

	def validate_end(self, end_date):
		obj = self.instance
		new = not obj

		# if the end date didn't change
		# no need to validate
		changed = obj and obj.end != end_date
		if (new or changed) and (end_date < date.today()):
			msg = _('End date cannot be in the past')
			raise serializers.ValidationError(msg)
		return end_date


class TaskSerializer(serializers.ModelSerializer):
	status_display = serializers.SerializerMethodField()
	links = serializers.SerializerMethodField()
	assigned = serializers.SlugRelatedField(slug_field=User.USERNAME_FIELD, 
		required=False, queryset=User.objects.all())

	class Meta:
		model = Task
		fields = (
			'id', 'name', 'description', 'sprint', 'status',
			'order', 'assigned', 'started', 'due', 'completed',
			'links', 'status_display'
		)

	def get_status_display(self, obj):
		return obj.get_status_display()


	def get_links(self, obj):
		request = self.context['request']

		links = {
			'self': reverse('task-detail',
				kwargs={'pk': obj.pk}, request=request),
			'sprint': None,
			'assigned': None
		}

		if obj.sprint_id:
			links['sprint'] = reverse('sprint-detail', 
				kwargs={'pk': obj.sprint_id}, request=request)

		if obj.assigned:
			links['assigned'] = reverse('user-detail', 
				kwargs={User.USERNAME_FIELD: obj.assigned}, request=request)


		return links

	def validate_sprint(self, sprint):
		obj = self.instance
		if obj and obj.pk:
			if sprint != obj.sprint:
				if obj.status == Task.STATUS_DONE:
					msg = _('Cannot change the sprint of a completed task.')
					raise serializers.ValidationError(msg)
				if sprint and sprint.end < date.today():
					msg = _('Cannot assign tasks to past sprints.')
					raise serializers.ValidationError(msg)
		else:
			if sprint and sprint.end < date.today():
				msg = _('Cannot add tasks to past sprints.')
				raise serializers.ValidationError(msg)
		return sprints

	def validate(self, data):
		sprint = data['sprint']
		status = int(data['status'])
		started = data['started']
		completed = data['completed']

		if not sprint and status != Task.STATUS_TODO:
			msg = _('Backlog tasks must have "Not Started" status.')
			raise serializers.ValidationError(msg)
		if started and status == Task.STATUS_TODO:
			msg = _('Started date cannot be set for not started tasks.')
			raise serializers.ValidationError(msg)
		if completed and status != Task.STATUS_DONE:
			msg = _('Completed date cannot be set for uncompleted tasks.')
			raise serializers.ValidationError(msg)
		return data



class UserSerializer(serializers.ModelSerializer):
	full_name = serializers.CharField(source='get_full_name', read_only=True)
	links = serializers.SerializerMethodField()


	class Meta:
		model = User
		fields = (
			'id', User.USERNAME_FIELD, 
			'full_name', 'is_active', 
			'links'
		)

	def get_links(self, obj):
		request = self.context['request']
		username = obj.get_username()

		return {
			'self': reverse('user-detail',
				kwargs={User.USERNAME_FIELD : username}, request=request),
			'tasks': "{}?assigned={}".format(
				reverse('task-list', request=request), username)
		}

