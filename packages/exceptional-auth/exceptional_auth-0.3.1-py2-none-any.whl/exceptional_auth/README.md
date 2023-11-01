# exceptional_auth

The purpose of this package is to provide a more flexible/powerful replacement for Django's `login_required` and `permission_required` decorators (and provide some entirely new related functionality).

The idea is to create a standard set of exceptions which any code can raise (even reusable apps distributed on pypi), and leave the handling of these exceptions up to the site developer (via custom middleware). This makes the many per-view decisions easy (ie. just raise PermissionDenied), while letting you centralize/delay the decision of what to do in those situations. Since you have access to the request object in the middleware methods, you can easily tailor the handling of these exceptions base on section of site, request type, etc.

We provide `exceptional_auth.BaseMiddleware`, a Middleware base class which makes it easier to handle our exceptions. Site developers should write a custom middleware extending this class, and add to `MIDDLEWARE` setting. You can also use `exceptional_auth.BaseMiddleware` to start with, and then extend it later.