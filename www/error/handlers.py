import www.base.handlers
import logging

def render(response, template, **kw):
	t = www.base.handlers.jinja_env.get_template(template)
	page = t.render(**kw)
	response.out.write(page)

def handle404(request, response, exception):
	logging.exception(exception)
	render(response, "error/e404.html")
	response.set_status(404)

class Error404Handler(www.base.handlers.BaseHandler):
	def get(self):
		return self.abort(404)
 