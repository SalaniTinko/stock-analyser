from .models import Freebie
from django.core.exceptions import ObjectDoesNotExist

def allowed(request):
	if request.user.is_authenticated:
		print("Auth")
		if request.user.has_active_subscription:
			print("Subscribed")
			return True
	value = checkfreebies(request)
	return value

def checkfreebies(request):
	print("Anon userr")
	ip = request.META.get('X-Forwarded-For')
	print(ip)
	try:
		free = Freebie.objects.get(ip=ip)
		print(free.counter)
		if free.counter < 3:
			print("added")
			free.counter = free.counter + 1
			free.save()
			return True
		elif free.counter >= 3:
			print("too many")
			return False
	except ObjectDoesNotExist:
		print("doesnt exist")
		freebie = Freebie.objects.create(ip=ip,counter=0)
		freebie.save()
		return True