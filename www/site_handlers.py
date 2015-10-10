from webapp2_extras.routes import RedirectRoute, DomainRoute

import www.index.handlers
import www.error.handlers

www_handlers = [
    RedirectRoute('/', handler=www.index.handlers.IndexHandler, name='Index', strict_slash=True),
    RedirectRoute('/listings', handler=www.index.handlers.ListingsHandler, name='Listings', strict_slash=True),
    RedirectRoute('/populate', handler=www.index.handlers.PopulateHandler, name='Populate', strict_slash=True)
]

error_handlers = {
    404: www.error.handlers.handle404
}
