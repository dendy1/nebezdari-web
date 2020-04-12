from django.core.paginator import Paginator


class CustomPaginator(Paginator):
    def __init__(self, object_list, per_page, pagination_pages_range, orphans=0,
                 allow_empty_first_page=True):
        super().__init__(object_list, per_page, orphans, allow_empty_first_page)
        self.pagination_pages_range = pagination_pages_range  #count of pages right and left to the current page
        self.pagination_pages_totally = pagination_pages_range * 2 + 1  #count of pages in pagination bar totally

    def pagination_list(self):
        pagination_list = []
        if self.num_pages <= self.pagination_pages_totally:
            for n in range(1, self.num_pages + 1):
                pagination_list.append(n)
        elif (self.page_num - self.pagination_pages_range > 0 and
              self.page_num + self.pagination_pages_range <= self.num_pages):
            for n in range(-self.pagination_pages_range, self.pagination_pages_range + 1):
                pagination_list.append(self.page_num + n)
        else:
            if self.page_num - self.pagination_pages_range <= 0:
                for n in range(1, self.pagination_pages_totally + 1):
                    pagination_list.append(n)
            else:
                for n in reversed(range(0, self.pagination_pages_totally)):
                    pagination_list.append(self.paginator.num_pages - n)
        return pagination_list
