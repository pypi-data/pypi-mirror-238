from __future__ import annotations 

class Page_param:
    def __init__(self) -> None:
        self.pageIndex=1
        self.pageSize=10
        self.orderBy=""
        self.order="asc" #[desc|asc]
        pass
    def get_db_page_index(self):
        return self.pageIndex-1 