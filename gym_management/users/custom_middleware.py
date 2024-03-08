# from django.shortcuts import redirect
# from django.contrib import messages
# from django.utils.deprecation import MiddlewareMixin

# class CustomCsrfViewMiddleware(MiddlewareMixin):
#     def process_response(self, request, response):
#         # Check if it's a CSRF failure response
#         if response.status_code == 403 and request.user.is_authenticated:
#             # Add your message
#             messages.error(request, "You are already logged in. Please log out before trying to log in again.")
#             # Redirect to a safe page, e.g., user's profile or home
#             return redirect('user_login')  # Change 'home' to your appropriate URL name
#         return response