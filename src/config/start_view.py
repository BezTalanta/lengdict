from django.views import View
from django.shortcuts import render


class StartView(View):

    def get(self, request):
        return render(request, 'start_page.html', {
            'msg': request.session.get('msg', ''),
        })
