from django.contrib import admin

from .models import *


admin.site.register(CustomUser)

admin.site.register(PasswordResetCode)

admin.site.register(Customer)


admin.site.register(Product)
admin.site.register(ProductColor)
admin.site.register(ProductImage)
admin.site.register(Review)


admin.site.register(WishList)


admin.site.register(Coupon)


admin.site.register(Category)


admin.site.register(VideoReview)

admin.site.register(PackageContent)

admin.site.register(SelfieCameraDetails)

admin.site.register(MainCameraDetails)

admin.site.register(BatteryDetails)

admin.site.register(CommunicationFeatures)

admin.site.register(SoundFeatures)

admin.site.register(MemoryDetails)

admin.site.register(PlatformDetails)

admin.site.register(DisplayDetails)

admin.site.register(BodyDetails)


admin.site.register(LaunchDetails)


admin.site.register(NetworkFeatures)