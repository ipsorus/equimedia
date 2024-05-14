from django.contrib import admin

from testimonial.models import Testimonial


class TestimonialAdmin(admin.ModelAdmin):
    model = Testimonial


admin.site.register(Testimonial, TestimonialAdmin)
