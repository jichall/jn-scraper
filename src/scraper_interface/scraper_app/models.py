from django.db import models


class ProductItem(models.Model):
    """
    I'm using everything as a char field because I don't need to operate over
    these values.
    """
    name = models.CharField(max_length=150)
    price = models.CharField(max_length=20)

    def __str__(self):
        # Should return a well formatted product.
        return self.name


class Image(models.Model):
    """The images that belong to a product"""
    item = models.ForeignKey(ProductItem, on_delete=models.CASCADE)
    src = models.CharField(max_length=1024)

    def __str__(self):
        return self.src
