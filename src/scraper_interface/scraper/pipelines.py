class ProductItemPipeline(object):
    def process_item(self, item, spider):
        item.save()
        return item
