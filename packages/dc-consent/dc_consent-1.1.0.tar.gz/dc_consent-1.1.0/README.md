Cookie Consent
==============

A Django app to add a cookie consent modal to your site.
This can then be used to check if the user has given consent to use cookies.

To clear the cookie preferences; the user can simple navigate to:

    reverse('cookie_consent:revoke')

In templates; it is also possible to check if the user has given consent like so:

    request.cookie_consent.allows('analytics') -> bool

Quick start
-----------

1. Add 'cookie_consent' to your INSTALLED_APPS setting like this:

   ```
   INSTALLED_APPS = [
   ...,
   'cookie_consent',
   ]
   ```
2. Include the cookie_consent URLconf in your project urls.py like this:

   ```
   path('cookies/', include('cookie_consent.urls')),
   ```
3. Add the cookie_consent middleware to your MIDDLEWARE setting like this:

   ```
   MIDDLEWARE = [
   ...,
   'cookie_consent.middleware.CookieConsentMiddleware',
   ]
   ```
4. Use the 'cookie_consent' template tag in your base template like this:

   ```
   {% load cookies_tags %}
   {% cookie_consent %}
   ```
5. Check if the user has given consent to use cookies in your templates like this:

   ```
   {% consents_to 'analytics' %}
   	<script>
   		// Will only get rendered if the user has given consent to use analytics cookies.
   	</script>
   {% endconsents_to %}
   ```
