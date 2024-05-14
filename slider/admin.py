from django.contrib import admin

from slider.models import Slider


class SliderAdmin(admin.ModelAdmin):
    model = Slider


admin.site.register(Slider, SliderAdmin)
