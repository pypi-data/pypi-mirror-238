import pstats

try:
    import cProfile as profile
except ImportError:
    import profile
try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO

from django.conf import settings
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class CProfilerMiddleware(MiddlewareMixin):
    """
    Simple profile middleware to profile django views. To run it, add ?prof to
    the URL like this:

        http://localhost:8000/view/?prof

    Optionally pass the following to modify the output:

    ?sort => Sort the output by a given metric. Default is time.
        See
        http://docs.python.org/2/library/profile.html#pstats.Stats.sort_stats
        for all sort options.

    ?count => The number of rows to display. Default is 100.

    ?download => Download profile file suitable for visualization. For example
        in snakeviz or RunSnakeRun
    """

    use_profiler = getattr(settings, "USE_PROFILER", False)
    auth_token = getattr(settings, "PROFILER_AUTH_TOKEN", None)

    def can(self, request):
        if not self.use_profiler:
            return False

        if not 'prof' in request.GET:
            return False
        
        request_auth_token = request.GET.get("token")

        if not request_auth_token:
            return False
        
        if request_auth_token != self.auth_token:
            return False

        return True

    def process_view(self, request, callback, callback_args, callback_kwargs):
        if self.can(request):
            self.profiler = profile.Profile()
            args = (request,) + callback_args
            try:
                return self.profiler.runcall(callback, *args, **callback_kwargs)
            except Exception:
                return

    def process_response(self, request, response):
        if self.can(request):
            self.profiler.create_stats()
            if 'download' in request.GET:
                import marshal
                output = marshal.dumps(self.profiler.stats)
                response = HttpResponse(output, content_type='application/octet-stream')
                response['Content-Disposition'] = 'attachment; filename=view.prof'
                response['Content-Length'] = len(output)
            else:
                sort_by = request.GET.get('sort', 'time')
                rows_count = int(request.GET.get('count', 100))

                io = StringIO()
                stats = pstats.Stats(self.profiler, stream=io)
                stats.strip_dirs().sort_stats(sort_by)
                stats.print_stats(rows_count)
                response = HttpResponse(f'{io.getvalue()}')

        return response
